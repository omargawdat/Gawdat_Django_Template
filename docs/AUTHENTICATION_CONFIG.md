# Django-Allauth Headless: Authentication Configuration Guide

This guide explains how to configure CSRF, CORS, and authentication for django-allauth headless in different environments.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Environment Variables](#environment-variables)
3. [Configuration Scenarios](#configuration-scenarios)
4. [Frontend Integration](#frontend-integration)
5. [Troubleshooting](#troubleshooting)
6. [Security Notes](#security-notes)

---

## Overview

This project uses **django-allauth headless mode** for API-based authentication. The authentication flow uses:

- **Django Sessions** - Server-side session management
- **CSRF Tokens** - Cross-Site Request Forgery protection
- **HTTP-Only Session Cookies** - Secure session storage
- **JavaScript-Readable CSRF Cookies** - CSRF token for API requests

### Key Architecture Decisions

1. **Session-based authentication** (not JWT for allauth endpoints)
2. **CSRF protection** via cookies (CSRF_COOKIE_HTTPONLY = False)
3. **Same-domain/subdomain requirement** for cookie sharing
4. **Multiple frontend support** via CORS configuration

---

## Environment Variables

Configure these three variables in your `.env` file:

### 1. FRONTEND_DEFAULT_URL

**Purpose:** Primary frontend URL for email links (password reset, email verification)

**Examples:**
```bash
# Local development
FRONTEND_DEFAULT_URL=http://localhost:3000

# Production
FRONTEND_DEFAULT_URL=https://app.example.com
```

### 2. FRONTEND_ALLOWED_ORIGINS

**Purpose:** Comma-separated list of frontend origins allowed to access the API

**Why separate from default URL?** You might have:
- Multiple environment frontends (dev, staging, prod)
- Mobile app webviews
- Admin dashboards
- Different domains/subdomains

**Examples:**
```bash
# Local development
FRONTEND_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000

# Production with multiple environments
FRONTEND_ALLOWED_ORIGINS=https://app.example.com,https://app-staging.example.com,https://example.com

# Production with multiple apps
FRONTEND_ALLOWED_ORIGINS=https://app.example.com,https://admin.example.com,https://mobile.example.com
```

### 3. COOKIE_DOMAIN

**Purpose:** Cookie domain for cross-subdomain authentication

**How it works:**
- `None` or empty = localhost only
- `example.com` = exact domain match only
- `.example.com` = domain + all subdomains (note the leading dot!)

**Examples:**
```bash
# Local development
COOKIE_DOMAIN=

# Production - same domain (backend: example.com/api, frontend: example.com)
COOKIE_DOMAIN=example.com

# Production - subdomains (backend: api.example.com, frontend: app.example.com)
COOKIE_DOMAIN=.example.com
```

**Important:** The leading dot (`.example.com`) is critical for subdomain support!

---

## Configuration Scenarios

### Scenario 1: Local Development

**Setup:** Backend on localhost:8000, Frontend on localhost:3000

**Environment variables:**
```bash
FRONTEND_DEFAULT_URL=http://localhost:3000
FRONTEND_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000
COOKIE_DOMAIN=
```

**What happens:**
- ✅ Cookies work across localhost ports
- ✅ CSRF protection active
- ✅ CORS allows specified origins
- ✅ Email links point to localhost:3000

---

### Scenario 2: Production - Same Domain

**Setup:** Backend at example.com/api, Frontend at example.com

**Environment variables:**
```bash
FRONTEND_DEFAULT_URL=https://example.com
FRONTEND_ALLOWED_ORIGINS=https://example.com,https://www.example.com
COOKIE_DOMAIN=example.com
DOMAIN_NAME=example.com
```

**What happens:**
- ✅ Cookies shared within example.com
- ✅ HTTPS-only cookies (secure)
- ✅ CSRF protection active
- ✅ Email links point to example.com

---

### Scenario 3: Production - Backend on Subdomain

**Setup:** Backend at api.example.com, Frontend at app.example.com

**Environment variables:**
```bash
FRONTEND_DEFAULT_URL=https://app.example.com
FRONTEND_ALLOWED_ORIGINS=https://app.example.com,https://example.com
COOKIE_DOMAIN=.example.com
DOMAIN_NAME=api.example.com
```

**What happens:**
- ✅ Cookies shared across *.example.com
- ✅ Backend accessible at api.example.com
- ✅ Frontend accessible at app.example.com or example.com
- ✅ CSRF protection across subdomains
- ✅ Email links point to app.example.com

---

### Scenario 4: Multiple Frontend Environments

**Setup:** Production + Staging + Development frontends

**Environment variables:**
```bash
FRONTEND_DEFAULT_URL=https://app.example.com
FRONTEND_ALLOWED_ORIGINS=https://app.example.com,https://app-staging.example.com,https://app-dev.example.com,https://example.com
COOKIE_DOMAIN=.example.com
DOMAIN_NAME=api.example.com
```

**What happens:**
- ✅ All frontend environments can access API
- ✅ Email links always use production URL
- ✅ Cookies work across all subdomains
- ✅ Each environment isolated but sharing auth

---

## Frontend Integration

### JavaScript Fetch with Credentials

**Critical:** You MUST include `credentials: 'include'` in all API requests!

```javascript
// ✅ Correct - includes cookies (session + CSRF)
fetch('http://localhost:8000/api/_allauth/browser/v1/auth/session', {
  method: 'GET',
  credentials: 'include',  // REQUIRED!
  headers: {
    'Content-Type': 'application/json',
  },
})

// ❌ Wrong - no cookies sent
fetch('http://localhost:8000/api/_allauth/browser/v1/auth/session', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
  },
})
```

### Reading CSRF Token

The CSRF token is stored in a cookie named `csrftoken` (or `__Secure-csrftoken` in production).

**Option 1: Read from Cookie**
```javascript
function getCsrfToken() {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [key, value] = cookie.trim().split('=');
    if (key === name) {
      return decodeURIComponent(value);
    }
  }
  return null;
}

// Use in requests
const csrfToken = getCsrfToken();
fetch('http://localhost:8000/api/_allauth/browser/v1/auth/login', {
  method: 'POST',
  credentials: 'include',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrfToken,  // Add CSRF token
  },
  body: JSON.stringify({ email, password }),
})
```

**Option 2: Use a Library**
```javascript
// Using js-cookie library
import Cookies from 'js-cookie';

const csrfToken = Cookies.get('csrftoken');
```

### React Example

```javascript
import { useState, useEffect } from 'react';

const API_BASE_URL = 'http://localhost:8000';

function LoginForm() {
  const [csrfToken, setCsrfToken] = useState('');

  useEffect(() => {
    // Get CSRF token on mount
    fetch(`${API_BASE_URL}/api/_allauth/browser/v1/auth/session`, {
      method: 'GET',
      credentials: 'include',
    })
      .then(() => {
        // CSRF token is now in cookies
        const token = document.cookie
          .split('; ')
          .find(row => row.startsWith('csrftoken='))
          ?.split('=')[1];
        setCsrfToken(token || '');
      });
  }, []);

  const handleLogin = async (email, password) => {
    const response = await fetch(`${API_BASE_URL}/api/_allauth/browser/v1/auth/login`, {
      method: 'POST',
      credentials: 'include',  // Send cookies
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,  // CSRF protection
      },
      body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
      const data = await response.json();
      console.log('Logged in:', data);
    }
  };

  return (
    // ... form UI
  );
}
```

### Next.js Example

```javascript
// app/api/auth/route.js
import { cookies } from 'next/headers';

export async function POST(request) {
  const cookieStore = cookies();
  const csrfToken = cookieStore.get('csrftoken')?.value;

  const response = await fetch('http://localhost:8000/api/_allauth/browser/v1/auth/login', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
      'Cookie': request.headers.get('cookie') || '',
    },
    body: await request.text(),
  });

  return response;
}
```

---

## Troubleshooting

### Issue 1: CSRF Token Not Found

**Symptoms:**
- 403 Forbidden errors
- "CSRF token not set" error messages

**Solutions:**

1. **Check if CSRF cookie is set:**
   - Open browser DevTools → Application → Cookies
   - Look for `csrftoken` cookie
   - If missing, you need to call a GET endpoint first (e.g., `/api/_allauth/browser/v1/auth/session`)

2. **Verify credentials are included:**
   ```javascript
   // Must include this!
   credentials: 'include'
   ```

3. **Check CORS configuration:**
   - Verify `FRONTEND_ALLOWED_ORIGINS` includes your frontend URL
   - Ensure URL matches exactly (http vs https, port numbers)

---

### Issue 2: Cookies Not Being Sent

**Symptoms:**
- Session not persisting
- User logged out after refresh
- CSRF token empty

**Solutions:**

1. **Check SameSite attribute:**
   - Local dev: `SameSite=Lax` (set by default)
   - Ensure frontend and backend on compatible origins

2. **Verify CORS_ALLOW_CREDENTIALS:**
   ```python
   # Must be True in settings
   CORS_ALLOW_CREDENTIALS = True
   ```

3. **Check browser console for CORS errors:**
   - "Access to fetch has been blocked by CORS policy"
   - Add your frontend URL to `FRONTEND_ALLOWED_ORIGINS`

4. **Verify cookie domain:**
   ```bash
   # For subdomains, use leading dot
   COOKIE_DOMAIN=.example.com

   # For localhost, leave empty
   COOKIE_DOMAIN=
   ```

---

### Issue 3: CORS Errors

**Symptoms:**
- "No 'Access-Control-Allow-Origin' header"
- "CORS policy: Credentials flag is 'true'"

**Solutions:**

1. **Add frontend URL to allowed origins:**
   ```bash
   FRONTEND_ALLOWED_ORIGINS=http://localhost:3000,...
   ```

2. **Ensure exact URL match:**
   ```bash
   # ❌ Wrong - missing port
   http://localhost

   # ✅ Correct - with port
   http://localhost:3000
   ```

3. **Check protocol match:**
   ```bash
   # ❌ Wrong - protocol mismatch
   http://example.com  # (but using https)

   # ✅ Correct
   https://example.com
   ```

---

### Issue 4: Production Subdomain Issues

**Symptoms:**
- Works on same domain but not on subdomain
- Cookies not shared between api.example.com and app.example.com

**Solutions:**

1. **Use leading dot in COOKIE_DOMAIN:**
   ```bash
   # ❌ Wrong - no leading dot
   COOKIE_DOMAIN=example.com

   # ✅ Correct - with leading dot
   COOKIE_DOMAIN=.example.com
   ```

2. **Update ALLOWED_HOSTS:**
   ```python
   # Should automatically include .example.com
   # Check prod.py configuration
   ALLOWED_HOSTS = [env.domain_name]
   if env.cookie_domain and env.cookie_domain.startswith("."):
       ALLOWED_HOSTS.append(env.cookie_domain)
   ```

3. **Verify DNS configuration:**
   - Ensure both api.example.com and app.example.com resolve correctly
   - Check SSL certificates cover both domains

---

## Security Notes

### Why CSRF_COOKIE_HTTPONLY = False is Safe

**Concern:** "Isn't making CSRF cookie JavaScript-readable insecure?"

**Answer:** No, this is the correct configuration for django-allauth headless:

1. **CSRF Token Purpose:**
   - CSRF tokens prevent unauthorized actions, not unauthorized access
   - The token itself doesn't grant access - the session cookie does

2. **Session Cookie Remains Secure:**
   - Session cookie is HTTPONLY = True (cannot be read by JavaScript)
   - Session cookie contains actual authentication data
   - Stealing CSRF token alone is useless without the session

3. **How CSRF Protection Works:**
   - Django validates that CSRF token matches the session
   - Even if attacker gets CSRF token, they need the session cookie
   - Session cookie is HTTP-only, so attacker can't get it via JavaScript

4. **This is Django's Recommended Approach:**
   - Django docs: "If you are using AJAX requests, you need to pass the CSRF token in the request header"
   - To do this, JavaScript must be able to read the CSRF cookie

### Cookie Security Summary

| Cookie | HttpOnly | Secure | SameSite | Readable by JS? | Purpose |
|--------|----------|--------|----------|-----------------|---------|
| `sessionid` | ✅ True | ✅ True (prod) | Lax | ❌ No | Authentication |
| `csrftoken` | ❌ False | ✅ True (prod) | Lax | ✅ Yes | CSRF Protection |

### Production Security Checklist

- ✅ **HTTPS only** - `SECURE_SSL_REDIRECT = True`
- ✅ **Secure cookies** - `*_COOKIE_SECURE = True`
- ✅ **HSTS enabled** - `SECURE_HSTS_SECONDS = 518400`
- ✅ **Session cookie HTTP-only** - `SESSION_COOKIE_HTTPONLY = True`
- ✅ **CSRF validation** - `CSRF_USE_SESSIONS = False`
- ✅ **CORS restricted** - `CORS_ALLOWED_ORIGINS` (no wildcard)
- ✅ **Credentials required** - `CORS_ALLOW_CREDENTIALS = True`
- ✅ **Trusted origins** - `CSRF_TRUSTED_ORIGINS` matches frontend URLs

---

## Quick Reference

### Local Development (.env)
```bash
FRONTEND_DEFAULT_URL=http://localhost:3000
FRONTEND_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
COOKIE_DOMAIN=
```

### Production - Same Domain (.env)
```bash
FRONTEND_DEFAULT_URL=https://example.com
FRONTEND_ALLOWED_ORIGINS=https://example.com,https://www.example.com
COOKIE_DOMAIN=example.com
DOMAIN_NAME=example.com
```

### Production - Subdomains (.env)
```bash
FRONTEND_DEFAULT_URL=https://app.example.com
FRONTEND_ALLOWED_ORIGINS=https://app.example.com,https://example.com
COOKIE_DOMAIN=.example.com
DOMAIN_NAME=api.example.com
```

### Frontend API Call Template
```javascript
const csrfToken = document.cookie
  .split('; ')
  .find(row => row.startsWith('csrftoken='))
  ?.split('=')[1];

fetch(`${API_URL}/api/_allauth/browser/v1/auth/login`, {
  method: 'POST',
  credentials: 'include',  // REQUIRED
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrfToken,  // REQUIRED for POST/PUT/PATCH/DELETE
  },
  body: JSON.stringify({ email, password }),
});
```

---

## Need Help?

If you encounter issues not covered in this guide:

1. Check Django logs for detailed error messages
2. Verify all three environment variables are set correctly
3. Test with `curl` to isolate frontend vs backend issues:
   ```bash
   # Get CSRF token
   curl -c cookies.txt http://localhost:8000/api/_allauth/browser/v1/auth/session

   # View cookies
   cat cookies.txt

   # Login with CSRF token
   curl -b cookies.txt -c cookies.txt \
     -X POST http://localhost:8000/api/_allauth/browser/v1/auth/login \
     -H "Content-Type: application/json" \
     -H "X-CSRFToken: YOUR_TOKEN_HERE" \
     -d '{"email":"test@example.com","password":"testpass123"}'
   ```

4. Review browser DevTools Network tab for request/response headers
5. Check that middleware order is correct in settings (see [config/settings/base.py](../config/settings/base.py#L131))

---

**Last Updated:** 2025-01-15
