# Developer Testing Guide: Local Machine → Deployed Backend

## 🎯 Scenario

You want developers to test authentication endpoints from their **local machines** against a **deployed development/staging backend**.

**Example:**
- **Backend (deployed):** `https://dev-api.example.com`
- **Developer's machine:** `http://localhost:3000`

---

## ⚠️ The Cookie Problem

### Why This Is Tricky

Django-allauth headless uses **session-based authentication** with cookies. This creates a challenge:

```
Developer's Browser:
├─ Frontend: http://localhost:3000 (local)
└─ Backend: https://dev-api.example.com (deployed)
   └─ Issue: Cookies from dev-api.example.com won't work with localhost!
```

### The Root Cause

**Cookies are domain-specific:**
- Cookie set by `dev-api.example.com` with `domain=.example.com`
- Browser won't send this cookie to `localhost`
- Result: Authentication fails!

---

## ✅ Solution: Configure for Cross-Domain Testing

### Step 1: Update Backend Environment Variables

On your **development/staging server**, configure `.env` to allow localhost:

```bash
# ==============================================================================
# DEVELOPMENT/STAGING SERVER CONFIGURATION
# ==============================================================================

# Default frontend URL (for email links)
# Use your deployed frontend URL
FRONTEND_DEFAULT_URL=https://dev-app.example.com

# Allowed origins (CRITICAL: Include localhost for developers!)
# Include BOTH deployed frontend AND localhost origins
FRONTEND_ALLOWED_ORIGINS=https://dev-app.example.com,http://localhost:3000,http://127.0.0.1:3000,http://localhost:8080

# Cookie domain (CRITICAL: Leave EMPTY for cross-domain testing!)
# If set to .example.com, localhost won't receive cookies
COOKIE_DOMAIN=

# Other settings
DOMAIN_NAME=dev-api.example.com
ENVIRONMENT=development
```

### Step 2: Why Each Setting Matters

#### `FRONTEND_ALLOWED_ORIGINS` - Include localhost
```bash
# ✅ Correct - Includes developer localhost
FRONTEND_ALLOWED_ORIGINS=https://dev-app.example.com,http://localhost:3000,http://127.0.0.1:3000

# ❌ Wrong - Developers can't access from localhost
FRONTEND_ALLOWED_ORIGINS=https://dev-app.example.com
```

**What this does:**
- Allows CORS requests from localhost
- Adds localhost to `CSRF_TRUSTED_ORIGINS`
- Browsers allow API calls from `localhost:3000` → `dev-api.example.com`

#### `COOKIE_DOMAIN` - Keep Empty
```bash
# ✅ Correct - Works with localhost
COOKIE_DOMAIN=

# ❌ Wrong - localhost won't receive cookies
COOKIE_DOMAIN=.example.com
```

**What this does:**
- Empty = cookies use the exact domain (`dev-api.example.com`)
- Browser sends cookies based on request origin, not cookie domain
- Works with `CORS_ALLOW_CREDENTIALS = True`

---

## 🔧 How It Works

### Configuration Flow

```
1. Developer's browser at localhost:3000 makes request to dev-api.example.com

2. Backend checks CORS:
   ✓ Is http://localhost:3000 in CORS_ALLOWED_ORIGINS? YES
   ✓ Is CORS_ALLOW_CREDENTIALS = True? YES
   → Allow request, set Access-Control-Allow-Origin: http://localhost:3000

3. Backend sets cookies:
   - Cookie domain: dev-api.example.com (not .example.com)
   - SameSite: None (for cross-origin) or Lax with proper setup

4. Browser receives cookies:
   ✓ Backend allowed credentials in CORS
   ✓ Developer used credentials: 'include' in fetch
   → Cookies stored

5. Subsequent requests:
   ✓ Browser sends cookies to dev-api.example.com
   ✓ CSRF token validated
   ✓ Session authenticated
   → Success!
```

---

## 🚨 Common Issues & Solutions

### Issue 1: "Cookies not being set"

**Symptom:**
```javascript
// Request succeeds but no cookies in DevTools
fetch('https://dev-api.example.com/api/_allauth/browser/v1/auth/session', {
  credentials: 'include'
})
```

**Solution:**
```bash
# Check backend .env
COOKIE_DOMAIN=  # ← Must be EMPTY for localhost testing
FRONTEND_ALLOWED_ORIGINS=...,http://localhost:3000  # ← Must include localhost
```

---

### Issue 2: "CORS policy error"

**Symptom:**
```
Access to fetch at 'https://dev-api.example.com' from origin 'http://localhost:3000'
has been blocked by CORS policy: The value of the 'Access-Control-Allow-Origin'
header must not be the wildcard '*' when credentials flag is 'true'.
```

**Solution:**
```bash
# Backend .env must explicitly allow localhost
FRONTEND_ALLOWED_ORIGINS=https://dev-app.example.com,http://localhost:3000
```

---

### Issue 3: "CSRF token missing"

**Symptom:**
```
403 Forbidden
CSRF verification failed. CSRF token missing or incorrect.
```

**Solutions:**

1. **Get CSRF token first:**
   ```javascript
   // Step 1: Get CSRF token
   await fetch('https://dev-api.example.com/api/_allauth/browser/v1/auth/session', {
     credentials: 'include'
   });

   // Step 2: Read token from cookie
   const csrfToken = document.cookie
     .split('; ')
     .find(row => row.startsWith('csrftoken='))
     ?.split('=')[1];

   // Step 3: Use in POST requests
   fetch('https://dev-api.example.com/api/_allauth/browser/v1/auth/login', {
     method: 'POST',
     credentials: 'include',
     headers: {
       'X-CSRFToken': csrfToken
     },
     body: JSON.stringify({...})
   });
   ```

2. **Check CSRF_TRUSTED_ORIGINS:**
   ```bash
   # Backend automatically sets this from FRONTEND_ALLOWED_ORIGINS
   # Ensure localhost is included
   FRONTEND_ALLOWED_ORIGINS=...,http://localhost:3000
   ```

---

### Issue 4: "SameSite cookie warning"

**Symptom:**
```
Browser console warning:
Cookie "csrftoken" has been rejected because it is in a cross-site context
and its "SameSite" is "Lax".
```

**Solution:**

**Option A: Use Chrome flags (Development only)**
```bash
# Launch Chrome with these flags:
chrome --disable-features=SameSiteByDefaultCookies,CookiesWithoutSameSiteMustBeSecure
```

**Option B: Add custom middleware (for dev/staging only)**

Create `config/middleware/samesite_dev.py`:
```python
class SameSiteNoneMiddleware:
    """Set SameSite=None for cookies in development (cross-origin testing)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only in development environment
        if settings.ENVIRONMENT in ['local', 'development']:
            # Check if request is cross-origin
            origin = request.headers.get('Origin', '')
            if 'localhost' in origin or '127.0.0.1' in origin:
                # Modify Set-Cookie headers to use SameSite=None
                if 'Set-Cookie' in response:
                    # Process each cookie
                    for cookie in response.cookies.values():
                        cookie['samesite'] = 'None'
                        cookie['secure'] = True  # Required with SameSite=None

        return response
```

Add to `settings/base.py`:
```python
# Only for development/staging environments
if env.environment in ['local', 'development']:
    MIDDLEWARE.append('config.middleware.samesite_dev.SameSiteNoneMiddleware')
```

**Option C: Use HTTPS for local development**

Use a tool like `mkcert` to set up local HTTPS:
```bash
# Install mkcert
brew install mkcert  # macOS
# or
choco install mkcert  # Windows

# Generate certificate
mkcert -install
mkcert localhost 127.0.0.1

# Use with your frontend dev server
npm run dev -- --https --cert localhost+1.pem --key localhost+1-key.pem
```

---

## 📋 Deployment Checklist

### For Development/Staging Servers

Before deploying, ensure your `.env` has:

- [ ] `FRONTEND_ALLOWED_ORIGINS` includes localhost URLs
- [ ] `COOKIE_DOMAIN` is empty (not set to `.example.com`)
- [ ] `FRONTEND_DEFAULT_URL` points to deployed frontend (for emails)
- [ ] `ENVIRONMENT=development` or `ENVIRONMENT=staging`

**Example `.env` for dev server:**
```bash
FRONTEND_DEFAULT_URL=https://dev-app.example.com
FRONTEND_ALLOWED_ORIGINS=https://dev-app.example.com,http://localhost:3000,http://127.0.0.1:3000,http://localhost:8080
COOKIE_DOMAIN=
DOMAIN_NAME=dev-api.example.com
ENVIRONMENT=development
```

### For Production Servers

For production, restrict to production URLs only:

- [ ] `FRONTEND_ALLOWED_ORIGINS` has ONLY production URLs
- [ ] `COOKIE_DOMAIN` set to `.example.com` (if using subdomains)
- [ ] `FRONTEND_DEFAULT_URL` points to production frontend
- [ ] `ENVIRONMENT=production`

**Example `.env` for production:**
```bash
FRONTEND_DEFAULT_URL=https://app.example.com
FRONTEND_ALLOWED_ORIGINS=https://app.example.com,https://example.com
COOKIE_DOMAIN=.example.com
DOMAIN_NAME=api.example.com
ENVIRONMENT=production
```

---

## 🧪 Testing from Developer's Local Machine

### Complete Example: React Frontend

```javascript
// config.js
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://dev-api.example.com';

// auth.js
class AuthService {
  async getSession() {
    const response = await fetch(`${API_BASE_URL}/api/_allauth/browser/v1/auth/session`, {
      method: 'GET',
      credentials: 'include',  // CRITICAL!
    });
    return response.json();
  }

  getCsrfToken() {
    // Read from cookie
    const csrfToken = document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      ?.split('=')[1];
    return csrfToken;
  }

  async login(email, password) {
    // Ensure CSRF token is available
    await this.getSession();

    const csrfToken = this.getCsrfToken();

    const response = await fetch(`${API_BASE_URL}/api/_allauth/browser/v1/auth/login`, {
      method: 'POST',
      credentials: 'include',  // CRITICAL!
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,  // CRITICAL!
      },
      body: JSON.stringify({ email, password }),
    });

    return response.json();
  }

  async logout() {
    const csrfToken = this.getCsrfToken();

    const response = await fetch(`${API_BASE_URL}/api/_allauth/browser/v1/auth/logout`, {
      method: 'DELETE',
      credentials: 'include',
      headers: {
        'X-CSRFToken': csrfToken,
      },
    });

    return response.ok;
  }
}

export default new AuthService();
```

### Developer Workflow

1. **Start local frontend:**
   ```bash
   cd frontend
   REACT_APP_API_URL=https://dev-api.example.com npm start
   # Opens at http://localhost:3000
   ```

2. **Test authentication:**
   - Open `http://localhost:3000`
   - Try to login
   - Check browser DevTools → Application → Cookies
   - Should see `csrftoken` and `sessionid` cookies

3. **Verify CORS:**
   - Open DevTools → Network tab
   - Check API request headers
   - Should see: `Access-Control-Allow-Origin: http://localhost:3000`
   - Should see: `Access-Control-Allow-Credentials: true`

---

## 🔒 Security Considerations

### Why This Is Safe for Dev/Staging

1. **CORS is still restricted:**
   - Only explicitly listed origins allowed
   - Not using `CORS_ALLOW_ALL_ORIGINS = True`

2. **CSRF protection active:**
   - CSRF tokens still required
   - Origin validation still happens

3. **Environment-specific:**
   - Only dev/staging allow localhost
   - Production restricts to production URLs only

### What NOT To Do

❌ **Never in production:**
```bash
# DON'T: Allow all origins
CORS_ALLOW_ALL_ORIGINS=True

# DON'T: Include localhost in production
FRONTEND_ALLOWED_ORIGINS=https://app.example.com,http://localhost:3000

# DON'T: Disable CSRF
CSRF_COOKIE_HTTPONLY=True  # (This breaks headless, but also don't disable CSRF entirely)
```

---

## 📚 Quick Reference

### Environment Variable Patterns

| Environment | Frontend Origins | Cookie Domain | Notes |
|------------|------------------|---------------|-------|
| **Local Dev** | `localhost:3000,localhost:8000` | _(empty)_ | Both backend and frontend local |
| **Dev Server** | `dev-app.example.com,localhost:3000` | _(empty)_ | Deployed backend, developers test from localhost |
| **Staging** | `staging-app.example.com,localhost:3000` | _(empty)_ | Same as dev server |
| **Production** | `app.example.com,example.com` | `.example.com` | Only production URLs, no localhost |

### Frontend Checklist

When calling deployed backend from localhost:

- ✅ Use `credentials: 'include'` in all fetch requests
- ✅ Get CSRF token before POST/PUT/PATCH/DELETE requests
- ✅ Include `X-CSRFToken` header in mutating requests
- ✅ Use correct backend URL (not localhost)
- ✅ Handle HTTPS → HTTP errors (backend must be HTTPS)

---

## 🆘 Still Not Working?

### Debug Steps

1. **Check backend logs:**
   ```bash
   docker-compose logs -f django
   # or
   tail -f /var/log/django/debug.log
   ```

2. **Test with curl:**
   ```bash
   # Get CSRF token
   curl -i -c cookies.txt https://dev-api.example.com/api/_allauth/browser/v1/auth/session

   # Check cookies file
   cat cookies.txt

   # Test login
   curl -b cookies.txt -c cookies.txt \
     -X POST https://dev-api.example.com/api/_allauth/browser/v1/auth/login \
     -H "Content-Type: application/json" \
     -H "Origin: http://localhost:3000" \
     -H "X-CSRFToken: YOUR_TOKEN" \
     -d '{"email":"test@example.com","password":"pass123"}'
   ```

3. **Verify environment variables:**
   ```bash
   # SSH into server
   ssh user@dev-api.example.com

   # Check .env file
   cat .env | grep FRONTEND

   # Verify Django settings
   docker-compose exec django python manage.py shell
   >>> from django.conf import settings
   >>> print(settings.FRONTEND_ALLOWED_ORIGINS)
   >>> print(settings.CORS_ALLOW_CREDENTIALS)
   >>> print(settings.CSRF_COOKIE_DOMAIN)
   ```

4. **Check browser console:**
   - Open DevTools (F12)
   - Network tab → Check request/response headers
   - Console tab → Check for CORS errors
   - Application tab → Check cookies

---

**Last Updated:** 2025-01-15

**Related Docs:**
- [AUTHENTICATION_CONFIG.md](./AUTHENTICATION_CONFIG.md) - Complete authentication guide
- [CONFIGURATION_CHANGES.md](./CONFIGURATION_CHANGES.md) - Recent configuration updates
