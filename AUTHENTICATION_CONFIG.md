# Cross-Origin Authentication Configuration Guide

## Table of Contents
1. [Introduction](#1-introduction)
2. [Quick Reference Table](#2-quick-reference-table)
3. [Configuration Options (Detailed)](#3-configuration-options-detailed)
4. [Environment Examples](#4-environment-examples)
5. [Deployment Scenarios](#5-deployment-scenarios)
6. [Troubleshooting](#6-troubleshooting)
7. [Security Best Practices](#7-security-best-practices)

---

## 1. Introduction

### Architecture Overview
This project uses **Django Allauth Headless** for backend authentication with a **React** frontend. The backend provides JSON APIs for authentication, and the frontend handles all UI rendering.

```
┌─────────────┐         ┌──────────────┐
│   React     │  HTTP   │   Django     │
│  Frontend   │ ──────► │   Backend    │
│ (port 3000) │  CORS   │  (port 8000) │
└─────────────┘         └──────────────┘
```

### Why Cross-Origin Configuration?
When the frontend and backend run on **different origins** (different domains, ports, or protocols), browsers enforce **CORS** (Cross-Origin Resource Sharing) and **CSRF** (Cross-Site Request Forgery) protections. We must explicitly configure which origins are trusted.

### Different Origins Examples
- `http://localhost:3000` vs `http://localhost:8000` ❌ (different ports)
- `https://app.example.com` vs `https://api.example.com` ❌ (different subdomains)
- `http://example.com` vs `https://example.com` ❌ (different protocols)

---

## 2. Quick Reference Table

| Option | Env Variable | Local Dev | Dev/Staging | Production | Purpose |
|--------|--------------|-----------|-------------|------------|---------|
| **Frontend Base URL** | `FRONTEND_DEFAULT_URL` | `http://localhost:3000` | `https://dev-app.example.com` | `https://app.example.com` | Email links & OAuth redirects |
| **Allowed Origins** | `FRONTEND_ALLOWED_ORIGINS` | `localhost:3000,localhost:8000` | `dev-app.example.com,localhost:3000` ⚠️ | `app.example.com` | CORS & CSRF allowed origins |
| **Cookie Domain** | `COOKIE_DOMAIN` | *(empty)* | *(empty)* ⚠️ | `.example.com` | Cross-subdomain cookies |
| **CSRF SameSite** | *(code)* | `Lax` | `Lax` | `Lax` | OAuth compatibility |
| **CSRF HttpOnly** | *(code)* | `False` | `False` | `False` | JS needs to read token |
| **CSRF Secure** | *(code)* | `False` | `False` | `True` | HTTPS-only in prod |
| **Session HttpOnly** | *(code)* | `True` | `True` | `True` | Prevent XSS attacks |
| **Session SameSite** | *(code)* | `Lax` | `Lax` | `Lax` | OAuth compatibility |
| **Session Secure** | *(code)* | `False` | `False` | `True` | HTTPS-only in prod |

⚠️ **Dev/Staging Note**: Include `localhost` origins to allow frontend developers to test locally against deployed backend!

---

## 3. Configuration Options (Detailed)

### 3.1 FRONTEND_DEFAULT_URL

**Environment Variable**: `FRONTEND_DEFAULT_URL`
**Type**: String (URL)
**Required**: ✅ Yes
**Configured in**: `config/helpers/env.py`

#### What it does
The base URL of your frontend application. Django uses this to construct URLs in:
- Email verification links
- Password reset links
- OAuth callback redirects
- Account confirmation links

#### Example Values
```bash
# Local Development
FRONTEND_DEFAULT_URL=http://localhost:3000

# Dev/Staging Server
FRONTEND_DEFAULT_URL=https://dev-app.example.com

# Production
FRONTEND_DEFAULT_URL=https://app.example.com

# Mobile App (deep links)
FRONTEND_DEFAULT_URL=myapp://auth
```

#### How it works
Django builds URLs like:
```
{FRONTEND_DEFAULT_URL}/account/verify-email/{key}
{FRONTEND_DEFAULT_URL}/account/password/reset
{FRONTEND_DEFAULT_URL}/account/provider/callback
```

#### Common Mistakes
- ❌ Including trailing slash: `http://localhost:3000/` (wrong)
- ✅ No trailing slash: `http://localhost:3000` (correct)
- ❌ Using backend URL instead of frontend URL
- ❌ Forgetting to update in production

---

### 3.2 FRONTEND_ALLOWED_ORIGINS

**Environment Variable**: `FRONTEND_ALLOWED_ORIGINS`
**Type**: Comma-separated string (URLs)
**Required**: ✅ Yes
**Configured in**: `config/helpers/env.py`
**Used by**: `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`

#### What it does
Defines which frontend origins can:
- Make cross-origin API requests (CORS)
- Submit forms and POST data (CSRF)
- Access authenticated endpoints

#### Example Values
```bash
# Local Development (both services local)
FRONTEND_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000

# Dev/Staging (CRITICAL: Include localhost for developers!)
FRONTEND_ALLOWED_ORIGINS=https://dev-app.example.com,https://dev-api.example.com,http://localhost:3000,http://127.0.0.1:3000

# Production (strict - only production URLs)
FRONTEND_ALLOWED_ORIGINS=https://app.example.com,https://example.com
```

#### How it works
1. Browser makes request from `http://localhost:3000` to `http://localhost:8000/api/...`
2. Backend checks if `localhost:3000` is in `CORS_ALLOWED_ORIGINS`
3. If yes, returns `Access-Control-Allow-Origin: http://localhost:3000` header
4. Browser allows the request ✅
5. If no, browser blocks the request ❌

#### Why Dev/Staging Should Include Localhost
Frontend developers need to:
1. Run React locally (`localhost:3000`)
2. Point to deployed dev backend (`dev-api.example.com`)
3. Test authentication without deploying frontend

**Configuration**:
```bash
# Dev Backend .env
FRONTEND_ALLOWED_ORIGINS=https://dev-app.example.com,http://localhost:3000

# Frontend Developer .env.local
REACT_APP_API_URL=https://dev-api.example.com
```

#### Common Mistakes
- ❌ Forgetting `http://` or `https://` prefix
- ❌ Including trailing slashes: `http://localhost:3000/`
- ❌ Forgetting to add commas between URLs
- ❌ Not including localhost in dev/staging (breaks local development)
- ❌ Including localhost in production (security risk)

---

### 3.3 COOKIE_DOMAIN

**Environment Variable**: `COOKIE_DOMAIN`
**Type**: String (domain name)
**Required**: ⚠️ Optional (empty for most cases)
**Configured in**: `config/helpers/env.py`
**Default**: `""` (empty string)

#### What it does
Controls which domain(s) can access session and CSRF cookies. Used for **cross-subdomain** authentication.

#### When to Use
✅ **Use** when frontend and backend are on different subdomains of the same domain:
- Backend: `api.example.com`
- Frontend: `app.example.com`
- Set: `COOKIE_DOMAIN=.example.com` (note the leading dot!)

❌ **Don't use** when:
- Frontend and backend are on the same origin
- Using localhost (will break cookies!)
- Frontend developers test from localhost against deployed backend

#### Example Values
```bash
# Local Development - LEAVE EMPTY
COOKIE_DOMAIN=

# Dev/Staging - LEAVE EMPTY (allows localhost testing)
COOKIE_DOMAIN=

# Production (same domain)
# Backend: example.com/api, Frontend: example.com
COOKIE_DOMAIN=example.com

# Production (subdomains)
# Backend: api.example.com, Frontend: app.example.com
COOKIE_DOMAIN=.example.com
```

#### How it works
**Without COOKIE_DOMAIN** (empty):
- Cookie set by `api.example.com` → only accessible on `api.example.com`
- Cookie set by `localhost:8000` → only accessible on `localhost:8000`

**With COOKIE_DOMAIN=.example.com**:
- Cookie set by `api.example.com` → accessible on all `*.example.com` subdomains
- Cookie accessible on: `api.example.com`, `app.example.com`, `www.example.com`
- Cookie NOT accessible on: `localhost` ❌

#### Common Mistakes
- ❌ Setting `.example.com` in development (breaks localhost)
- ❌ Forgetting the leading dot: `example.com` vs `.example.com`
- ❌ Using `COOKIE_DOMAIN` when not needed (same origin doesn't need it)
- ❌ Setting `COOKIE_DOMAIN` in dev/staging (prevents developers from testing locally)

---

### 3.4 CSRF_COOKIE_SAMESITE

**Django Setting**: `CSRF_COOKIE_SAMESITE`
**Type**: String
**Configured in**: `config/settings/local.py`, `config/settings/base.py`
**Value**: `"Lax"`

#### What it does
Controls when browsers send CSRF cookies with cross-site requests.

#### Options
- `Strict`: Cookie ONLY sent for same-site requests (breaks OAuth!)
- `Lax`: Cookie sent for top-level navigation (allows OAuth ✅)
- `None`: Cookie sent for all requests (requires `Secure=True`)

#### Why We Use "Lax"
OAuth flow involves:
1. User clicks "Login with Google" on `localhost:3000`
2. Redirects to `accounts.google.com`
3. Google redirects back to `localhost:3000/account/provider/callback`
4. Frontend calls `localhost:8000/api/_allauth/provider/token`

With `Strict`, step 3 would fail (no cookie sent). `Lax` allows this! ✅

---

### 3.5 CSRF_COOKIE_HTTPONLY

**Django Setting**: `CSRF_COOKIE_HTTPONLY`
**Type**: Boolean
**Configured in**: `config/settings/local.py`
**Value**: `False`

#### What it does
Controls whether JavaScript can read the CSRF cookie.

#### Why False?
Frontend JavaScript needs to read the CSRF token cookie and send it in the `X-CSRFToken` header with each POST request.

```javascript
// frontend/src/lib/django.js
export function getCSRFToken() {
  return getCookie('csrftoken')  // Needs HttpOnly=False
}

// frontend/src/lib/allauth.js
options.headers['X-CSRFToken'] = getCSRFToken()  // Send in header
```

#### Security Trade-off
- `HttpOnly=True`: More secure (XSS can't steal), but JS can't read
- `HttpOnly=False`: Less secure, but required for SPA architecture

**Mitigation**: Session cookies remain `HttpOnly=True` for security.

---

### 3.6 SESSION_COOKIE_HTTPONLY

**Django Setting**: `SESSION_COOKIE_HTTPONLY`
**Type**: Boolean
**Configured in**: `config/settings/base.py`
**Value**: `True`

#### What it does
Prevents JavaScript from accessing the session cookie.

#### Why True?
Session cookies contain authentication state. `HttpOnly=True` prevents XSS attacks from stealing session tokens.

```javascript
// This would fail (and that's good!):
document.cookie  // Cannot read sessionid cookie ✅
```

---

### 3.7 CSRF_COOKIE_SECURE & SESSION_COOKIE_SECURE

**Django Setting**: `CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`
**Type**: Boolean
**Configured in**: `config/settings/prod.py`
**Local/Dev**: `False`
**Production**: `True`

#### What it does
Ensures cookies are ONLY sent over HTTPS connections.

#### Environment-Specific
```python
# Local Development (HTTP)
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Production (HTTPS)
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
```

#### Why False in Development?
Local development uses `http://localhost` (not HTTPS). Setting `Secure=True` would prevent cookies from being set!

---

### 3.8 CSRF_EXEMPT_URLS (Local Development Only)

**Django Setting**: `CSRF_EXEMPT_URLS`
**Type**: List of regex patterns
**Configured in**: `config/settings/local.py`
**Value**: `[r'^/api/_allauth/']`

#### What it does
Exempts specific URL patterns from CSRF validation in **local development only**.

#### Why Needed?
In local development:
1. Frontend runs on `localhost:3000`
2. Backend runs on `localhost:8000`
3. Different ports = different origins
4. JavaScript can't read cookies from different port
5. Can't send CSRF token → requests fail ❌

**Solution**: Exempt allauth endpoints from CSRF in local development.

#### Security
⚠️ **This is ONLY for local development!** Production must use proper CSRF protection.

**Implementation**: Custom middleware in `config/middleware/csrf_exempt.py`

---

### 3.9 OAuth Provider Settings

**Environment Variables**:
- `GOOGLE_OAUTH2_CLIENT_ID`
- `GOOGLE_OAUTH2_CLIENT_SECRET`

**Type**: Strings
**Required**: ✅ Yes (if using Google OAuth)
**Configured in**: `config/helpers/env.py`

#### What it does
Credentials for Google OAuth integration.

#### Where to Get
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project
3. Enable OAuth 2.0
4. Add authorized redirect URIs:
   ```
   http://localhost:8000/accounts/google/login/callback/
   https://dev-api.example.com/accounts/google/login/callback/
   https://api.example.com/accounts/google/login/callback/
   ```
5. Copy Client ID and Client Secret

#### Environment-Specific
```bash
# Local Development
GOOGLE_OAUTH2_CLIENT_ID=123-local.apps.googleusercontent.com
GOOGLE_OAUTH2_CLIENT_SECRET=GOCSPX-local-secret

# Production (different credentials!)
GOOGLE_OAUTH2_CLIENT_ID=456-prod.apps.googleusercontent.com
GOOGLE_OAUTH2_CLIENT_SECRET=GOCSPX-prod-secret
```

---

## 4. Environment Examples

### 4.1 Local Development (Both Services Local)

**Scenario**: Frontend and backend both run locally on developer machine.

```bash
# .env
FRONTEND_DEFAULT_URL=http://localhost:3000
FRONTEND_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000,http://127.0.0.1:8000
COOKIE_DOMAIN=

GOOGLE_OAUTH2_CLIENT_ID=your-dev-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-dev-secret
```

**Frontend** (`frontend/.env.local`):
```bash
REACT_APP_API_URL=http://localhost:8000
```

**URLs**:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

**Cookies**: Work without domain restriction
**CSRF**: Exempted for allauth endpoints

---

### 4.2 Dev/Staging (Deployed Backend + Local Frontend)

**Scenario**: Backend deployed to dev server, frontend developers test locally.

```bash
# .env (on dev server)
FRONTEND_DEFAULT_URL=https://dev-app.example.com
FRONTEND_ALLOWED_ORIGINS=https://dev-app.example.com,https://dev-api.example.com,http://localhost:3000,http://127.0.0.1:3000
COOKIE_DOMAIN=

GOOGLE_OAUTH2_CLIENT_ID=your-dev-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-dev-secret
```

**Frontend Developer** (`frontend/.env.local`):
```bash
REACT_APP_API_URL=https://dev-api.example.com
```

**URLs**:
- Frontend (deployed): https://dev-app.example.com
- Frontend (local dev): http://localhost:3000
- Backend: https://dev-api.example.com

**Why This Works**:
- `localhost:3000` is in `FRONTEND_ALLOWED_ORIGINS` ✅
- `COOKIE_DOMAIN` is empty (allows localhost cookies) ✅
- CORS allows requests from localhost ✅

---

### 4.3 Production (Same Domain)

**Scenario**: Frontend and backend on same domain.

```bash
# .env (production)
FRONTEND_DEFAULT_URL=https://example.com
FRONTEND_ALLOWED_ORIGINS=https://example.com
COOKIE_DOMAIN=example.com

GOOGLE_OAUTH2_CLIENT_ID=your-prod-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-prod-secret
```

**URLs**:
- Frontend: https://example.com
- Backend: https://example.com/api

**Cookies**: Domain set to `example.com`
**CSRF**: Fully protected (no exemptions)

---

### 4.4 Production (Subdomains)

**Scenario**: Frontend and backend on different subdomains.

```bash
# .env (production)
FRONTEND_DEFAULT_URL=https://app.example.com
FRONTEND_ALLOWED_ORIGINS=https://app.example.com,https://api.example.com
COOKIE_DOMAIN=.example.com

GOOGLE_OAUTH2_CLIENT_ID=your-prod-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-prod-secret
```

**URLs**:
- Frontend: https://app.example.com
- Backend: https://api.example.com

**Cookies**: Domain set to `.example.com` (works across subdomains)
**CSRF**: Fully protected

---

### 4.5 Mobile App (Deep Links)

**Scenario**: Mobile app using deep links for OAuth callbacks.

```bash
# .env (production)
FRONTEND_DEFAULT_URL=myapp://auth
FRONTEND_ALLOWED_ORIGINS=myapp://auth,https://app.example.com
COOKIE_DOMAIN=

GOOGLE_OAUTH2_CLIENT_ID=your-mobile-client-id
GOOGLE_OAUTH2_CLIENT_SECRET=your-mobile-secret
```

**URLs**:
- Frontend: myapp://auth
- Backend: https://api.example.com

**Email Links**: `myapp://auth/password/reset/key/{key}`
**OAuth Redirect**: `myapp://auth/account/provider/callback`

---

## 5. Deployment Scenarios

### Scenario 1: Local Development

**Setup**:
```
Developer Machine
├── Frontend: http://localhost:3000
└── Backend: http://localhost:8000
```

**Configuration**:
```bash
FRONTEND_DEFAULT_URL=http://localhost:3000
FRONTEND_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
COOKIE_DOMAIN=
```

**Workflow**:
1. Start backend: `docker compose up django postgres`
2. Start frontend: `cd frontend && npm start`
3. Access: http://localhost:3000
4. Login, signup, OAuth all work ✅

---

### Scenario 2: Remote Backend + Local Frontend

**Setup**:
```
Dev Server
└── Backend: https://dev-api.example.com

Developer Machine
└── Frontend: http://localhost:3000
```

**Backend Configuration** (on server):
```bash
FRONTEND_DEFAULT_URL=https://dev-app.example.com
FRONTEND_ALLOWED_ORIGINS=https://dev-app.example.com,http://localhost:3000
COOKIE_DOMAIN=
```

**Frontend Configuration** (developer's machine):
```javascript
// frontend/.env.local
REACT_APP_API_URL=https://dev-api.example.com
```

**Workflow**:
1. Backend already deployed at `dev-api.example.com`
2. Developer starts local frontend: `npm start`
3. Frontend makes requests to remote backend
4. CORS allows it because `localhost:3000` is in allowed origins ✅

---

### Scenario 3: Production (CDN + API Subdomain)

**Setup**:
```
Production
├── Frontend: https://app.example.com (CloudFlare CDN)
└── Backend: https://api.example.com (AWS)
```

**Configuration**:
```bash
FRONTEND_DEFAULT_URL=https://app.example.com
FRONTEND_ALLOWED_ORIGINS=https://app.example.com,https://api.example.com
COOKIE_DOMAIN=.example.com
```

**Features**:
- Cross-subdomain cookies work ✅
- HTTPS enforced ✅
- Strict origin validation ✅
- No localhost access ✅

---

## 6. Troubleshooting

### Issue: CORS Error "No 'Access-Control-Allow-Origin' header"

**Error in Browser**:
```
Access to fetch at 'http://localhost:8000/api/_allauth/...' from origin 'http://localhost:3000'
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present.
```

**Cause**: Frontend origin not in `FRONTEND_ALLOWED_ORIGINS`

**Solution**:
```bash
# Add your frontend origin
FRONTEND_ALLOWED_ORIGINS=http://localhost:3000,...
```

**Verify**:
```bash
curl -H "Origin: http://localhost:3000" http://localhost:8000/api/_allauth/browser/v1/config -I
# Should see: Access-Control-Allow-Origin: http://localhost:3000
```

---

### Issue: CSRF Error "CSRF verification failed"

**Error**: `403 Forbidden - CSRF cookie not set`

**Cause**:
- JavaScript can't read CSRF cookie (different port)
- CSRF exemption not configured in local development

**Solution (Local Development)**:
Already handled by `CSRF_EXEMPT_URLS` in `local.py` ✅

**Solution (Production)**:
Use same domain or configure proper CSRF handling.

---

### Issue: Cookies Not Being Sent

**Symptom**: Session cookie not included in API requests

**Cause 1**: `withCredentials` not set in frontend
```javascript
// frontend/src/lib/allauth.js
// Should be:
withCredentials: true  ✅
```

**Cause 2**: Cookie domain mismatch
```bash
# Wrong: COOKIE_DOMAIN=.example.com when accessing from localhost
# Fix: COOKIE_DOMAIN= (empty for localhost)
```

**Verify**:
1. Open DevTools → Application → Cookies
2. Check if cookies are set
3. Check Network tab → Request Headers → Cookie

---

### Issue: OAuth Callback Returns 404

**Symptom**: After Google login, redirected to 404 page

**Cause**: `FRONTEND_DEFAULT_URL` doesn't match actual frontend URL

**Solution**:
```bash
# Wrong:
FRONTEND_DEFAULT_URL=http://localhost:8000  ❌ (backend URL)

# Correct:
FRONTEND_DEFAULT_URL=http://localhost:3000  ✅ (frontend URL)
```

---

### Issue: "Set-Cookie domain attribute is invalid"

**Error in Console**: Browser rejects cookie due to invalid domain

**Cause**: Cookie domain doesn't match current domain

**Example**:
```bash
# Accessing from localhost with:
COOKIE_DOMAIN=.example.com  ❌

# Fix:
COOKIE_DOMAIN=  ✅
```

---

## 7. Security Best Practices

### Development vs Production

| Setting | Development | Production | Why Different |
|---------|-------------|------------|---------------|
| `FRONTEND_ALLOWED_ORIGINS` | Includes `localhost` | Only production URLs | Security |
| `COOKIE_DOMAIN` | Empty | Set to domain | Localhost compatibility |
| `CSRF_COOKIE_SECURE` | `False` | `True` | HTTP vs HTTPS |
| `SESSION_COOKIE_SECURE` | `False` | `True` | HTTP vs HTTPS |
| `CSRF_EXEMPT_URLS` | `['/api/_allauth/']` | Not set | Cross-port compatibility |

### Security Checklist

#### Local Development ✅
- [ ] `FRONTEND_ALLOWED_ORIGINS` includes localhost
- [ ] `COOKIE_DOMAIN` is empty
- [ ] `CSRF_EXEMPT_URLS` configured for allauth
- [ ] Using test OAuth credentials

#### Dev/Staging ⚠️
- [ ] `FRONTEND_ALLOWED_ORIGINS` includes both deployed URL AND localhost
- [ ] `COOKIE_DOMAIN` is empty (to allow localhost testing)
- [ ] Using dev OAuth credentials
- [ ] `DEBUG=False` to test production behavior

#### Production 🔒
- [ ] `FRONTEND_ALLOWED_ORIGINS` only includes production URLs (NO localhost!)
- [ ] `COOKIE_DOMAIN` set if using subdomains
- [ ] `CSRF_COOKIE_SECURE=True`
- [ ] `SESSION_COOKIE_SECURE=True`
- [ ] Using production OAuth credentials
- [ ] `DEBUG=False`
- [ ] HTTPS enforced

### Common Security Mistakes

❌ **NEVER DO**:
```bash
# Production with localhost (SECURITY RISK!)
FRONTEND_ALLOWED_ORIGINS=https://app.example.com,http://localhost:3000

# Using wildcard (SECURITY RISK!)
FRONTEND_ALLOWED_ORIGINS=*

# Wrong cookie domain in production
COOKIE_DOMAIN=  # Should be .example.com for subdomains
```

✅ **ALWAYS DO**:
```bash
# Production (strict)
FRONTEND_ALLOWED_ORIGINS=https://app.example.com
COOKIE_DOMAIN=.example.com
# ... all Secure flags True
```

### Defense in Depth

1. **CORS**: Prevents unauthorized API access
2. **CSRF**: Prevents forged requests
3. **SameSite Cookies**: Limits cross-site cookie usage
4. **HttpOnly**: Prevents XSS cookie theft (for session)
5. **Secure Flag**: Prevents MITM cookie theft (HTTPS only)
6. **Cookie Domain**: Limits cookie scope

---

## Additional Resources

- [Django CORS Headers Documentation](https://github.com/adamchainz/django-cors-headers)
- [Django CSRF Protection](https://docs.djangoproject.com/en/stable/ref/csrf/)
- [Django Allauth Headless](https://docs.allauth.org/en/latest/headless/index.html)
- [MDN: HTTP Cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies)
- [MDN: CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

---

**Last Updated**: 2025-10-21
**Maintained by**: DevOps Team
