# User Profile Architecture

## Overview
This document explains the multi-profile architecture where User (account) is separate from Customer (profile).

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         User (Account)                       │
│  - email, username, password                                 │
│  - language, is_active, date_joined                          │
│  - Authentication & Authorization                            │
└──────────┬──────────────────────────────┬───────────────────┘
           │                              │
           │ OneToOne                     │ OneToOne
           │                              │
┌──────────▼──────────┐        ┌─────────▼─────────┐
│     Customer        │        │   Wallet          │
│  - phone_number     │        │  - balance        │
│  - full_name        │        │  - is_use_wallet  │
│  - image            │        └───────────────────┘
│  - gender           │
│  - birth_date       │
│  - country          │        ┌───────────────────┐
│  - is_verified      │        │ Future: Provider  │
│  - inviter          │        │  - company_name   │
└─────────────────────┘        │  - business_type  │
                               └───────────────────┘
```

## Key Design Decisions

### 1. User as Account Layer
**User** represents the authentication account:
- Handles login, password, email
- Common fields across all profile types
- Used by Django authentication system

### 2. Customer as Profile Layer
**Customer** is a profile that extends User:
- Contains business-specific data
- Can access User fields via proxy properties
- Multiple users can be Customers

### 3. Wallet at Account Level (User)
**Why Wallet → User instead of Wallet → Customer?**

#### ✅ Benefits:
1. **Multi-Profile Support**: When you add Provider, they share the same wallet
   ```python
   user = User.objects.get(email="john@example.com")
   customer = user.customer  # Customer profile
   provider = user.provider  # Future: Provider profile
   wallet = user.wallet      # Same wallet for both!
   ```

2. **Single Source of Truth**: One user = one wallet = one balance
   ```python
   # User has $100 in wallet
   user.wallet.balance  # $100
   user.customer.user.wallet.balance  # Same $100
   user.provider.user.wallet.balance  # Same $100 (future)
   ```

3. **Simplified Transactions**: No need to sync between multiple wallets
   ```python
   # Customer buys something
   customer.user.wallet.balance -= 50

   # Provider gets paid (future)
   provider.user.wallet.balance += 50  # Same user? Can't happen!
   ```

4. **Cleaner Business Logic**: Wallet operations are user-level, not profile-level

#### ❌ Alternative (Wallet → Customer) Problems:
- Need separate wallet for each profile type
- Complex synchronization between profiles
- User with multiple profiles has multiple wallets (confusing)
- Duplication of wallet logic for Provider, Vendor, etc.

## Access Patterns

### From Customer to Wallet
```python
customer = Customer.objects.get(phone_number="+966123456789")
wallet = customer.user.wallet
balance = wallet.balance
```

### From User to Customer
```python
user = request.user
if hasattr(user, 'customer'):
    customer = user.customer
    phone = customer.phone_number
```

### From User to Wallet
```python
user = request.user
wallet = user.wallet
wallet.balance += Money(100, 'USD')
wallet.save()
```

### Creating Customer with Wallet
```python
# 1. Create User
user = User.objects.create(
    email="john@example.com",
    username="john123"
)

# 2. Create Customer
customer = Customer.objects.create(
    user=user,
    phone_number="+966123456789",
    country=country
)

# 3. Create Wallet (for the User, not Customer!)
wallet = Wallet.objects.create(
    user=user,  # ← User, not Customer!
    balance=Money(0, 'USD')
)

# Access
customer.user.wallet  # Works!
user.wallet           # Works!
```

## Query Optimization

Always use `select_related` for related objects:

```python
# Good: Efficient query
customer = Customer.objects.select_related('user', 'country').get(pk=1)
wallet = customer.user.wallet  # No extra query!

# Bad: N+1 queries
customer = Customer.objects.get(pk=1)
wallet = customer.user.wallet  # Extra query!

# Best: Prefetch wallet too
customer = (
    Customer.objects
    .select_related('user', 'user__wallet', 'country')
    .get(pk=1)
)
```

## Future Extensibility

### Adding Provider Profile

```python
# models/provider.py
class Provider(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="provider"
    )
    company_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=100)
    # ... provider-specific fields
```

### User with Multiple Profiles
```python
user = User.objects.get(email="john@example.com")

# John is both a customer and provider
customer = user.customer  # Buys products
provider = user.provider  # Sells products
wallet = user.wallet      # Shared wallet!

# Business rules can prevent conflicts
if hasattr(user, 'customer') and hasattr(user, 'provider'):
    # User can't buy from their own store, etc.
    pass
```

## Proxy Properties in Customer

Customer has proxy properties for convenient access to User fields:

```python
customer.email  # → customer.user.email
customer.username  # → customer.user.username
customer.language  # → customer.user.language
customer.is_active  # → customer.user.is_active
customer.date_joined  # → customer.user.date_joined

# Authentication methods
customer.set_password("new_password")  # → customer.user.set_password()
customer.check_password("password")    # → customer.user.check_password()
```

This makes the code cleaner while maintaining separation of concerns.

## Best Practices

### DO ✅
- Access wallet via `customer.user.wallet`
- Create wallet for User, not Customer
- Use `select_related('user', 'user__wallet')` for queries
- Check `hasattr(user, 'customer')` to detect customer users
- Keep account-level data in User
- Keep business-level data in Customer

### DON'T ❌
- Create Wallet → Customer relationship
- Access User fields directly without going through Customer
- Create multiple wallets per user
- Put business logic in User model
- Put authentication logic in Customer model

## Testing

### Factory Usage
```python
# Create customer with user and wallet
customer = CustomerFactory()
customer.user.email  # Has email
customer.user.wallet  # Has wallet

# Create just a user with wallet
user = UserFactory()
wallet = WalletFactory(user=user)

# Create provider with wallet (future)
provider = ProviderFactory()
provider.user.wallet  # Same wallet system!
```

## Migration Path

See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for detailed migration instructions from the old inheritance-based model to this architecture.

## Summary

This architecture provides:
- ✅ **Flexibility**: Easy to add new profile types
- ✅ **Scalability**: One wallet system for all profiles
- ✅ **Maintainability**: Clear separation of concerns
- ✅ **Performance**: Optimizable with select_related
- ✅ **Extensibility**: Future-proof for new features

The key insight: **Wallet is an account-level feature, not a profile-level feature**.
