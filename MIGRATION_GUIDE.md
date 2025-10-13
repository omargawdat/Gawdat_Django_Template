# Customer Model Migration Guide: Inheritance → OneToOne Relationship

## Overview
This guide documents the migration from Customer inheriting from User (Multi-Table Inheritance) to a OneToOne relationship between Customer and User.

## ⚠️ IMPORTANT: Backup Your Database First!
```bash
# Create a database backup before proceeding
docker compose -f docker-compose.local.yml exec postgres pg_dump -U postgres projectname > backup_$(date +%Y%m%d_%H%M%S).sql
```

## Changes Made

### 1. Model Changes
- **[apps/users/models/customer.py](apps/users/models/customer.py)**
  - Changed `class Customer(User)` to `class Customer(models.Model)`
  - Added `user = OneToOneField(User, unique=True)` (NOT primary_key to allow Customer to have its own id)
  - Added proxy properties for User fields (email, username, language, is_active, date_joined)
  - Added proxy methods for authentication (set_password, check_password)
  - Updated `related_name` on country ForeignKey from "users" to "customers"

- **[apps/payment/models/wallet.py](apps/payment/models/wallet.py)**
  - ⚠️ **Kept as `user = OneToOneField(User)`** - This is intentional for multi-profile support
  - Rationale: Wallet belongs to User (account level), not Customer (profile level)
  - This allows future Provider/Vendor profiles to share the same wallet system
  - Access pattern: `customer.user.wallet` or `user.wallet`

### 2. Service Layer Updates
- **[apps/users/domain/services/customer.py](apps/users/domain/services/customer.py)**
  - Removed `update_or_create_customer` method (unused)
  - Updated `create_customer` to create User first, then Customer
  - Updated `change_password` to work with `customer.user`
  - Updated `get_or_create_active_customer` to validate user via `customer.user`

- **[apps/payment/domain/services/wallet.py](apps/payment/domain/services/wallet.py)**
  - Updated to use `customer.user` when creating/accessing wallets
  - Renamed `create_wallet_for_customer` to `create_wallet_for_user` (takes User parameter directly)
  - `add_referral_points` accesses wallets via `customer.user`

### 3. API Updates
- **[apps/users/api/permissions.py](apps/users/api/permissions.py)**
  - Changed `isinstance(request.user, Customer)` to `hasattr(request.user, 'customer')`

- **[apps/users/api/customer/views.py](apps/users/api/customer/views.py)**
  - Updated all views to use `request.user.customer` instead of `request.user`

- **[apps/users/api/customer/serializers.py](apps/users/api/customer/serializers.py)**
  - Added custom `update()` method to handle User fields separately

### 4. Admin Updates
- **[apps/users/admin/customer/list_view.py](apps/users/admin/customer/list_view.py)**
  - Updated `list_filter` to use `user__date_joined` and `user__is_active`
  - Updated `date_hierarchy` to `user__date_joined`
  - Updated `ordering` to `("-user__date_joined",)`

### 5. Domain Layer Updates
- **[apps/users/domain/selectors/user.py](apps/users/domain/selectors/user.py)**
  - Updated `group_users_by_type` to use `hasattr(user, 'customer')`

### 6. Adapter Updates
- **[apps/users/adapters/account.py](apps/users/adapters/account.py)**
  - Updated to create Customer profile after User creation in allauth signup

### 7. Test Factory Updates
- **[factories/factories.py](factories/factories.py)**
  - Updated `CustomerFactory` to use `SubFactory` for User
  - Updated `CustomerFactory.create_wallet` to pass `user=self.user` to WalletFactory
  - Updated `WalletFactory` to use `user = SubFactory(UserFactory)` (kept as User for multi-profile support)
  - `WalletFactory.balance` now safely handles users with or without customer profiles

## Migration Steps

### Step 1: Create Database Backup (CRITICAL)
```bash
docker compose -f docker-compose.local.yml exec postgres pg_dump -U postgres projectname > backup_before_migration.sql
```

### Step 2: Stop the Application
```bash
docker compose -f docker-compose.local.yml down
```

### Step 3: Create Migration Files

This migration is complex and requires a multi-step approach. The recommended approach is:

#### Option A: Fresh Database (Development Only)
If you're working on a development environment with no critical data:

```bash
# Delete database
docker compose -f docker-compose.local.yml down -v

# Recreate and run migrations
docker compose -f docker-compose.local.yml up -d postgres
docker compose -f docker-compose.local.yml run --rm django python manage.py migrate

# Create superuser
docker compose -f docker-compose.local.yml run --rm django python manage.py createsuperuser
```

#### Option B: Data Preservation (Production)
For production or when you need to preserve data:

1. **Create custom migration file** at `apps/users/migrations/0005_customer_to_onetoone.py`:

```python
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


def migrate_customer_to_onetoone(apps, schema_editor):
    """
    Migrate Customer data from MTI to OneToOne.

    Steps:
    1. Create temporary table for new Customer structure
    2. Copy data from old Customer (includes User fields via MTI)
    3. Drop old Customer table
    4. Rename temp table to Customer
    """
    # This needs to be implemented carefully based on your database
    # It's recommended to do this manually with SQL commands
    pass


def reverse_migration(apps, schema_editor):
    """Reverse the migration"""
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0004_alter_historicalcustomer_email_alter_user_email'),
        ('location', '0003_alter_address_options'),
    ]

    operations = [
        migrations.RunPython(
            migrate_customer_to_onetoone,
            reverse_migration,
        ),
    ]
```

2. **Run SQL commands manually** (safer for production):

```sql
-- Step 1: Backup current data
CREATE TABLE customer_backup AS SELECT * FROM users_customer;

-- Step 2: Create new customer table
CREATE TABLE users_customer_new (
    user_id bigint PRIMARY KEY REFERENCES users_user(id) ON DELETE CASCADE,
    phone_number varchar(128) UNIQUE,
    image varchar(100),
    full_name varchar(255) DEFAULT '',
    gender varchar(20) DEFAULT 'NS',
    birth_date date,
    country_id varchar(10) NOT NULL REFERENCES location_country(code) ON DELETE PROTECT,
    primary_address_id bigint UNIQUE REFERENCES location_address(id) ON DELETE SET NULL,
    is_verified boolean DEFAULT false,
    inviter integer
);

-- Step 3: Copy data from old customer table to new
INSERT INTO users_customer_new (
    user_id, phone_number, image, full_name, gender, birth_date,
    country_id, primary_address_id, is_verified, inviter
)
SELECT
    user_ptr_id, phone_number, image, full_name, gender, birth_date,
    country_id, primary_address_id, is_verified, inviter
FROM users_customer;

-- Step 4: Update wallet references
ALTER TABLE payment_wallet RENAME COLUMN user_id TO customer_id;

-- Step 5: Drop old customer table
DROP TABLE users_customer CASCADE;

-- Step 6: Rename new table
ALTER TABLE users_customer_new RENAME TO users_customer;

-- Step 7: Recreate indexes and constraints
CREATE INDEX users_customer_country_id_idx ON users_customer(country_id);
CREATE INDEX users_customer_inviter_idx ON users_customer(inviter);
```

### Step 4: Update Dependencies

Update all ForeignKey references to Customer in other migrations:

```bash
# Check for any pending migrations
docker compose -f docker-compose.local.yml run --rm django python manage.py showmigrations
```

### Step 5: Test the Migration

```bash
# Run migrations
docker compose -f docker-compose.local.yml run --rm django python manage.py migrate

# Check for issues
docker compose -f docker-compose.local.yml run --rm django python manage.py check

# Test authentication
docker compose -f docker-compose.local.yml run --rm django python manage.py shell
```

Test in Django shell:
```python
from apps.users.models.customer import Customer
from apps.users.models import User

# Test customer access
customer = Customer.objects.first()
print(customer.user.email)  # Should work
print(customer.email)  # Should work (proxy property)
print(customer.is_active)  # Should work (proxy property)

# Test user to customer access
user = User.objects.first()
print(hasattr(user, 'customer'))  # Should be True
print(user.customer.phone_number)  # Should work
```

### Step 6: Update Wallet References

After migrating Customer, you need to migrate Payment app:

```bash
docker compose -f docker-compose.local.yml run --rm django python manage.py makemigrations payment
docker compose -f docker-compose.local.yml run --rm django python manage.py migrate payment
```

### Step 7: Restart Application

```bash
docker compose -f docker-compose.local.yml up -d
```

### Step 8: Verify Everything Works

1. **Test Authentication**
   - Login with existing users
   - Create new user via API
   - Update user profile

2. **Test Customer Operations**
   - View customer list in admin
   - Create/update customers
   - Test wallet operations

3. **Test Related Models**
   - Addresses still work
   - Payments still work
   - Wallet transactions still work

## Rollback Plan

If something goes wrong:

```bash
# Stop the application
docker compose -f docker-compose.local.yml down

# Restore from backup
docker compose -f docker-compose.local.yml up -d postgres
docker compose -f docker-compose.local.yml exec postgres psql -U postgres projectname < backup_before_migration.sql

# Revert code changes
git revert <commit-hash>

# Restart
docker compose -f docker-compose.local.yml up -d
```

## Testing Checklist

- [ ] Database backup created
- [ ] All tests pass
- [ ] User login works
- [ ] Customer profile CRUD works
- [ ] Admin panel customer list works
- [ ] Wallet operations work
- [ ] Address management works
- [ ] Payment creation works
- [ ] Allauth signup creates Customer
- [ ] API endpoints respond correctly
- [ ] Serializers work correctly
- [ ] Permissions work correctly

## Known Issues & Considerations

1. **Historical Records**: If using django-simple-history, the HistoricalCustomer table will need similar migration
2. **Third-party Packages**: Any packages expecting Customer to be a User subclass may break
3. **Custom Queries**: Review all queries that use `Customer.objects.filter()` with User fields
4. **Performance**: Add `select_related('user')` to queries fetching Customer data
5. **Admin Display Methods**: Update any display methods that access User fields directly

## Performance Optimization

After migration, add these optimizations:

```python
# In CustomerSelector
@staticmethod
def get_customer_with_user(customer_id):
    return Customer.objects.select_related('user').get(pk=customer_id)

# In views
def get_queryset(self):
    return Customer.objects.select_related('user', 'country', 'wallet')
```

## Support

If you encounter issues during migration:
1. Check the error logs: `docker compose -f docker-compose.local.yml logs django`
2. Review database state: `docker compose -f docker-compose.local.yml exec postgres psql -U postgres projectname`
3. Consult Django documentation on changing model inheritance patterns
