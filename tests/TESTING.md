# Testing Guide

## Overview

Tests are automatically configured to:
- ✅ **Auto-flush** all factory data before each test
- ✅ **Auto-create** test data for all models (2 instances per model)
- ✅ **Reset sequences** to ensure clean state
- ✅ **Preserve UN country** (required by WalletService)

## Running Tests

```bash
# Run all tests
docker compose -f docker-compose.local.yml run --rm django pytest

# Run specific test file
docker compose -f docker-compose.local.yml run --rm django pytest tests/admin/test_admin_pages.py

# Run specific test
docker compose -f docker-compose.local.yml run --rm django pytest tests/admin/test_admin_pages.py::test_admin_index

# Run with extra verbose output
docker compose -f docker-compose.local.yml run --rm django pytest -vv
```

## Automatic Test Setup (conftest.py)

### What Happens Before Each Test

1. **Flush Phase** - All factory-created data is deleted
   - Deletes in reverse order (handles dependencies)
   - Preserves UN country (code="UN")
   - Silently skips protected foreign keys

2. **Creation Phase** - Fresh data is created
   - Creates 2 instances of each model
   - Handles singletons (only creates if doesn't exist)
   - Skips WalletFactory (created by WalletTransactionFactory)

### Test Data Available

Every test automatically has access to:
- 2 Addresses
- 2 AdminUsers
- 1 AppInfo (singleton)
- 2 Banners
- 2 BannerGroups
- 2 ContactUs
- 2 Countries (+ UN country)
- 2 Customers
- 2 FAQs
- 2 Notifications
- 2 Onboardings
- 2 PopUpBanners
- 2 Regions
- 1 SocialAccount (singleton)
- 2 WalletTransactions (with wallets)

## Test Organization

```
tests/
├── conftest.py              # Global fixtures & auto-setup
├── admin/
│   ├── conftest.py          # Admin-specific fixtures
│   ├── test_admin_pages.py  # Page loading tests
│   ├── test_admin_operations.py  # CRUD tests
│   └── test_admin_data_coverage.py  # Data validation
```

## Writing New Tests

### Basic Test
```python
import pytest

@pytest.mark.django_db
def test_something():
    """Test description"""
    from apps.users.models.customer import Customer

    # Data is already created by conftest
    customers = Customer.objects.all()
    assert customers.count() >= 2
```

### Using Factory Fixtures
```python
@pytest.mark.django_db
def test_with_factory(customer_factory):
    """Test using factory fixture"""
    # Create additional customer
    customer = customer_factory(full_name="John Doe")
    assert customer.full_name == "John Doe"
```

### Admin Tests
```python
@pytest.mark.django_db
def test_admin_page(admin_client):
    """Test admin interface"""
    from django.urls import reverse

    response = admin_client.get(reverse("admin:index"))
    assert response.status_code == 200
```

## Configuration (pyproject.toml)

Default pytest settings:
- `-v` - Verbose output
- `--tb=short` - Short tracebacks
- `--strict-markers` - Strict marker checking
- `--showlocals` - Show local variables on failure
- `--reuse-db` - Reuse database between runs

## Tips

### Speed Up Tests
The `--reuse-db` flag reuses the test database between runs (already configured).

### Debug Failed Tests
```bash
# Show captured output (print statements)
pytest -s

# Show very verbose output
pytest -vv

# Show slowest tests
pytest --durations=10
```

### Clean Database
The auto-flush happens before each test, so you always start with a clean slate.

### Skip Auto-Flush (if needed)
If you need to skip auto-flush for a specific test:
```python
@pytest.mark.django_db
def test_without_flush(db):
    """This test won't auto-flush"""
    # Don't use setup_test_data fixture
    pass
```

## Troubleshooting

### "Models without test data" Error
Add a factory for the missing model in `factories/factories.py`:
```python
class MyModelFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = MyModel
```

### Unique Constraint Violations
Use `factory.Sequence()` for unique fields:
```python
username = factory.Sequence(lambda n: f"user_{n}")
email = factory.Sequence(lambda n: f"user{n}@example.com")
```

### Slow Tests
Check if you're creating too many instances in `conftest.py`. The default is 2 per model, which should be sufficient for most tests.
