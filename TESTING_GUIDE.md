# Testing Guide - Minimal Maintenance Setup

## Overview

This project uses a **zero-maintenance testing approach** for admin panel tests:
- Test data is **automatically loaded** once per test session
- New models are **automatically discovered** when factories are added
- Admin tests **automatically test** all registered admin pages

## Quick Start

```bash
# Run all tests
docker compose -f docker-compose.local.yml run --rm django pytest tests/

# Run with database reuse (much faster on subsequent runs)
docker compose -f docker-compose.local.yml run --rm django pytest tests/ --reuse-db

# Run specific test file
docker compose -f docker-compose.local.yml run --rm django pytest tests/admin/test_admin_pages.py -v

# Run with coverage
docker compose -f docker-compose.local.yml run --rm django pytest tests/ --cov=apps --cov=config --cov-report=html
```

## How It Works

### 1. Auto-Discovery & Auto-Loading

**conftest.py** automatically:
1. Discovers all factories from `factories/` module
2. Registers them with pytest-factoryboy
3. Loads test data once per session (before any test runs)

```python
# Session-scoped, autouse=True means:
# - Runs automatically (no need to inject)
# - Data loaded once and shared across all tests
# - Compatible with --reuse-db for even faster runs

@pytest.fixture(scope="session", autouse=True)
def django_db_setup(...):
    load_all_factories(count=2)  # Creates 2 instances per model
```

### 2. Zero-Maintenance Admin Tests

Admin tests iterate through `admin.site._registry` to automatically test:
- List pages (changelist)
- Add pages
- Change/edit pages
- History pages
- Delete pages
- Search functionality

**When you add a new model:**
1. ✅ Create the model
2. ✅ Register in admin
3. ✅ Create factory
4. ✅ **DONE!** Tests automatically pick it up

No test file changes needed!

### 3. Data Coverage Validation

`test_admin_data_coverage.py` ensures all admin models have test data.

**Fails if:**
- New model added to admin but factory is missing
- Factory exists but failed to create data

## Adding New Models (Zero Test Maintenance)

### Example: Adding a Product Model

```python
# 1. Create model (apps/products/models/product.py)
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

# 2. Register in admin (apps/products/admin.py)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active']
    search_fields = ['name']

# 3. Create factory (factories/factories.py)
class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("word")
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    is_active = True

    class Meta:
        model = Product

# 4. Export factory (factories/__init__.py)
from factories.factories import ProductFactory
__all__ = [..., "ProductFactory"]
```

**That's it!** Next test run will:
- ✅ Auto-discover `ProductFactory`
- ✅ Auto-load Product test data
- ✅ Auto-test Product admin pages (list, add, change, delete, history, search)
- ✅ Verify Product has data in coverage test

## Using pytest-factoryboy Fixtures (Optional)

While admin tests use bulk-loaded data, individual tests can use pytest-factoryboy fixtures:

```python
# Auto-generated fixtures available:
# - customer          → Creates a Customer instance
# - customer_factory  → Access to CustomerFactory
# - customer__email   → Override email field

def test_customer_profile(customer):
    """Customer auto-created by pytest-factoryboy"""
    assert customer.username.startswith("user_")
    assert customer.wallet.balance.amount >= 0

def test_verified_customer(customer_factory):
    """Create custom customer using factory"""
    verified = customer_factory(is_verified=True)
    assert verified.is_verified is True

def test_multiple_addresses(customer, address_factory):
    """Create multiple related instances"""
    addresses = address_factory.create_batch(5, customer=customer)
    assert len(addresses) == 5
```

## Test Structure

```
tests/
├── conftest.py                      # Auto-discovery and auto-loading
├── admin/
│   ├── test_admin_pages.py          # Admin page smoke tests
│   ├── test_admin_operations.py     # CRUD operation tests
│   └── test_admin_data_coverage.py  # Data validation
└── [future test modules]            # Add more as needed
```

## Benefits

| Feature | Benefit |
|---------|---------|
| **Auto-discovery** | New factories automatically registered |
| **Auto-loading** | Test data loaded once per session |
| **Auto-testing** | Admin tests discover new models automatically |
| **Data coverage** | Automated validation ensures no missing factories |
| **Fast execution** | Session scope + `--reuse-db` = minimal overhead |
| **pytest-factoryboy** | Individual test fixtures available when needed |

## Best Practices

### ✅ Do:
- Create factories for all models registered in admin
- Use `Model.objects.first()` in admin tests
- Use pytest-factoryboy fixtures for specific test customization
- Run with `--reuse-db` for faster development

### ❌ Don't:
- Add test data loading to individual test files
- Manually create test data in admin tests
- Modify conftest.py when adding new models

## Troubleshooting

### Test fails: "Model has no data"
**Cause:** Factory doesn't exist or failed to create data
**Solution:** Check `test_admin_data_coverage.py` output for missing factories

### Tests are slow
**Cause:** Not using `--reuse-db`
**Solution:** Add `--reuse-db` flag to pytest command

### New factory not discovered
**Cause:** Factory not exported in `factories/__init__.py`
**Solution:** Add factory to `__all__` list in `factories/__init__.py`

## Configuration

### pytest.ini (in pyproject.toml)
```toml
[tool.pytest.ini_options]
addopts = """
    --ds=config.settings.test
    --reuse-db
    --import-mode=importlib
    -v
    --tb=short
    --strict-markers
    --showlocals
"""
```

### Coverage
```bash
# Generate HTML coverage report
docker compose -f docker-compose.local.yml run --rm django \
    pytest tests/ --cov=apps --cov=config --cov-report=html

# View report
open htmlcov/index.html
```

## Summary

This testing setup provides **minimal maintenance overhead**:
1. Add factory when creating model
2. Everything else is automatic
3. Zero test file changes
4. Fast execution with session-scoped data
5. pytest-factoryboy fixtures available for customization

**Result:** Focus on building features, not maintaining tests!
