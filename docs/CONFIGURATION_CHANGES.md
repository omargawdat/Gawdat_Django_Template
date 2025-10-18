# Configuration Refactoring Summary

## ✅ What Changed

Successfully refactored CORS/CSRF configuration to be **environment-agnostic** and controlled entirely by environment variables.

### Before (Problems)
- ❌ Duplicate configuration in `local.py` and `prod.py`
- ❌ Hardcoded values in multiple places
- ❌ CSRF_COOKIE_HTTPONLY = True in production (broke allauth headless)
- ❌ No CORS configuration in production
- ❌ Difficult to maintain and prone to inconsistencies

### After (Benefits)
- ✅ Single source of truth in `base.py`
- ✅ All configuration from environment variables
- ✅ Same code works in all environments (local, staging, prod)
- ✅ CSRF_COOKIE_HTTPONLY = False (correct for headless)
- ✅ Full CORS support in all environments
- ✅ Easy to maintain and extend

---

## 📝 Files Modified

### 1. [config/helpers/env.py](../config/helpers/env.py)
**Added:**
```python
# Frontend Configuration
frontend_default_url: str           # Default frontend for email links
frontend_allowed_origins: str       # Comma-separated allowed origins
cookie_domain: str | None = None    # Cookie domain for subdomains
```

### 2. [dummy.env](../dummy.env)
**Added:**
```bash
# Frontend Configuration
FRONTEND_DEFAULT_URL=http://localhost:3000
FRONTEND_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,...
COOKIE_DOMAIN=
```

### 3. [config/settings/base.py](../config/settings/base.py)
**Changed:**
- Made `HEADLESS_FRONTEND_URLS` dynamic using `env.frontend_default_url`
- Added parsing of `FRONTEND_ALLOWED_ORIGINS` from env var
- **Moved all CORS/CSRF configuration here** (was in local.py and prod.py)
- Added `CSRF_USE_SESSIONS = False`
- Set `CSRF_COOKIE_HTTPONLY = False` (required for headless)
- Set `CSRF_COOKIE_DOMAIN` and `SESSION_COOKIE_DOMAIN` from env
- Set `CSRF_TRUSTED_ORIGINS` from env
- Configured `CORS_ALLOWED_ORIGINS` and `CORS_ALLOW_CREDENTIALS`

**New unified configuration:**
```python
# Parse allowed origins from environment
FRONTEND_ALLOWED_ORIGINS = [
    origin.strip() for origin in env.frontend_allowed_origins.split(",") if origin.strip()
]

# CSRF Configuration
CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False  # Required for headless!
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_DOMAIN = env.cookie_domain if env.cookie_domain else None
CSRF_TRUSTED_ORIGINS = FRONTEND_ALLOWED_ORIGINS

# Session Configuration
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_DOMAIN = env.cookie_domain if env.cookie_domain else None

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = FRONTEND_ALLOWED_ORIGINS
CORS_ALLOW_CREDENTIALS = True
CORS_URLS_REGEX = r"^/api/.*$"
```

### 4. [config/settings/local.py](../config/settings/local.py)
**Removed:**
- All CORS configuration (moved to base.py)
- All CSRF configuration (moved to base.py)
- All Session configuration (moved to base.py)

**Added:**
- Comment explaining configuration is now in base.py

### 5. [config/settings/prod.py](../config/settings/prod.py)
**Removed:**
- CORS configuration (moved to base.py)
- CSRF domain configuration (moved to base.py)
- Session domain configuration (moved to base.py)
- CSRF_TRUSTED_ORIGINS (moved to base.py)

**Kept:**
- Production-specific overrides: `SESSION_COOKIE_SECURE = True`
- Production-specific overrides: `CSRF_COOKIE_SECURE = True`
- Production-specific cookie names: `__Secure-sessionid`, `__Secure-csrftoken`
- SSL/HTTPS settings

**Added:**
- Comment explaining base configuration
- Auto-add cookie_domain to ALLOWED_HOSTS for subdomain support

### 6. [docs/AUTHENTICATION_CONFIG.md](../docs/AUTHENTICATION_CONFIG.md)
**Created:** Comprehensive 400+ line documentation covering:
- Environment variable explanations
- Configuration scenarios (4 examples)
- Frontend integration guide
- Troubleshooting guide
- Security explanations

---

## 🎯 How It Works Now

### Configuration Flow

```
1. Set 3 environment variables in .env:
   - FRONTEND_DEFAULT_URL
   - FRONTEND_ALLOWED_ORIGINS
   - COOKIE_DOMAIN (optional)

2. base.py reads these and configures:
   - HEADLESS_FRONTEND_URLS (email links)
   - CSRF settings (cookie domain, trusted origins)
   - Session settings (cookie domain)
   - CORS settings (allowed origins, credentials)

3. local.py: No CORS/CSRF config (uses base.py)
4. prod.py: Only adds secure flags (HTTPS, Secure cookies)
```

### Environment Variables Control Everything

| Setting | Local Dev | Production |
|---------|-----------|------------|
| `FRONTEND_DEFAULT_URL` | `http://localhost:3000` | `https://app.example.com` |
| `FRONTEND_ALLOWED_ORIGINS` | `localhost:3000,localhost:8000` | `app.example.com,example.com` |
| `COOKIE_DOMAIN` | _(empty)_ | `.example.com` |
| `CSRF_COOKIE_HTTPONLY` | `False` (base.py) | `False` (base.py) |
| `CSRF_COOKIE_SECURE` | `False` (default) | `True` (prod.py) |
| `SESSION_COOKIE_SECURE` | `False` (default) | `True` (prod.py) |

---

## 🔧 Migration Guide for Existing Deployments

### Step 1: Update .env file

**Add these three variables:**
```bash
# Local Development
FRONTEND_DEFAULT_URL=http://localhost:3000
FRONTEND_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
COOKIE_DOMAIN=

# Production
FRONTEND_DEFAULT_URL=https://app.example.com
FRONTEND_ALLOWED_ORIGINS=https://app.example.com,https://example.com
COOKIE_DOMAIN=.example.com
```

### Step 2: Remove old configurations

**If you customized local.py or prod.py:**
- Remove any manual CORS_ALLOWED_ORIGINS overrides
- Remove any manual CSRF_TRUSTED_ORIGINS overrides
- Remove any manual COOKIE_DOMAIN overrides
- Production: Keep only the Secure flags (CSRF_COOKIE_SECURE, SESSION_COOKIE_SECURE)

### Step 3: Restart application

```bash
# Docker
docker compose -f docker-compose.local.yml down
docker compose -f docker-compose.local.yml up -d

# Production
# Restart your application server
```

### Step 4: Verify configuration

**Test checklist:**
- [ ] Frontend can access API endpoints
- [ ] CORS headers present in responses
- [ ] CSRF token cookie is set and readable
- [ ] Session persists after login
- [ ] Email links point to correct frontend URL
- [ ] Cookies work across subdomains (if applicable)

---

## 🚀 Benefits

### 1. **Simplicity**
- Only 3 environment variables to configure
- Same code in all environments
- No per-environment overrides needed

### 2. **Correctness**
- CSRF_COOKIE_HTTPONLY = False (required for allauth headless)
- CORS_ALLOW_CREDENTIALS = True (required for cookies)
- Proper cookie domain handling for subdomains

### 3. **Flexibility**
- Support multiple frontend environments
- Easy to add new frontend URLs
- Works with any domain/subdomain configuration

### 4. **Maintainability**
- Single source of truth in base.py
- No duplicate configuration
- Changes apply to all environments automatically

### 5. **Security**
- Production still has secure flags
- CSRF protection active
- Cookies marked as Secure in production
- HSTS enabled in production

---

## 📚 Additional Resources

- **Full documentation:** [AUTHENTICATION_CONFIG.md](./AUTHENTICATION_CONFIG.md)
- **Environment examples:** [../dummy.env](../dummy.env)
- **Base configuration:** [../config/settings/base.py](../config/settings/base.py)

---

## ⚠️ Breaking Changes

### For existing deployments:

**Required action:** Add three new environment variables to `.env`

**Why?** Previously hardcoded values are now from environment variables.

**Timeline:**
- Without these variables, application will fail to start
- Add variables before deploying this change

### For custom configurations:

If you have custom CORS/CSRF overrides in `local.py` or `prod.py`:
- They will be overridden by base.py
- Move customizations to environment variables instead
- Or remove if no longer needed

---

**Migration Date:** 2025-01-15
**Breaking Change:** Yes (requires new env vars)
**Rollback:** Revert commits and restore old .env file
