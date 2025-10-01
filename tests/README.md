# Tests Directory Structure

This directory contains all project tests, organized by functionality.

## Directory Structure

```
tests/
├── __init__.py
├── conftest.py                    # Global test fixtures (registers factories/)
├── README.md                      # This file
└── admin/                         # Admin interface tests
    ├── __init__.py
    ├── conftest.py                # Admin-specific fixtures
    ├── test_admin_pages.py        # Page loading & navigation tests
    ├── test_admin_operations.py   # CRUD operations tests
    └── test_admin_data_coverage.py # Data coverage validation

Note: Model factories are in the root `factories/` directory (not in tests/)
```

## Running Tests

### Run all tests
```bash
docker compose -f docker-compose.local.yml run --rm django pytest
```

### Run specific test modules
```bash
# Run all admin tests
docker compose -f docker-compose.local.yml run --rm django pytest tests/admin/

# Run specific test file
docker compose -f docker-compose.local.yml run --rm django pytest tests/admin/test_admin_pages.py

# Run specific test function
docker compose -f docker-compose.local.yml run --rm django pytest tests/admin/test_admin_pages.py::test_admin_index
```

### Run with verbose output
```bash
docker compose -f docker-compose.local.yml run --rm django pytest -v
```

### Run with coverage
```bash
docker compose -f docker-compose.local.yml run --rm django pytest --cov=apps
```

## Test Categories

### Admin Tests (`tests/admin/`)

#### test_admin_pages.py
Tests basic admin page functionality:
- Index page loading
- List/changelist pages
- Search functionality
- Add pages
- Change/edit pages
- History pages

#### test_admin_operations.py
Tests admin CRUD operations:
- Save/update operations
- Delete confirmation pages

#### test_admin_data_coverage.py
Validates test data coverage:
- Ensures all custom models have test data
- Ignores third-party models (django-allauth, FCM, etc.)
- Fails if models are missing test data

## Adding New Tests

### 1. Create a new test file
```python
# tests/admin/test_admin_custom.py
import pytest

@pytest.mark.django_db
def test_something(admin_client):
    """Test description"""
    # Your test code
    pass
```

### 2. Add model factories
```python
# factories/factories.py
import factory
from apps.myapp.models import MyModel

class MyModelFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")

    class Meta:
        model = MyModel
```

Then export in `factories/__init__.py`. Factories are automatically registered as pytest fixtures in `tests/conftest.py`. See `factories/README.md` for more details.

### 3. Use fixtures
Available fixtures:
- `admin_user`: Superuser instance
- `admin_client`: Authenticated Django test client
- `mock_request`: Mock request with admin user
- `{model}_factory`: Auto-generated from factories.py (e.g., `country_factory`)

## Best Practices

1. **Organize by functionality**: Group related tests in the same file
2. **Use descriptive names**: `test_admin_list_pages` is better than `test_lists`
3. **One assertion per concept**: Split complex tests into multiple functions
4. **Use fixtures**: Don't create test data manually when fixtures exist
5. **Mark database tests**: Always use `@pytest.mark.django_db` for tests that touch the database
6. **Document tests**: Add docstrings explaining what each test validates

## Fixtures

### Global Fixtures (tests/conftest.py)
- Auto-registers all Factory classes as pytest fixtures
- Creates test data automatically before each test
- Creates UN country (required by WalletService)

### Admin Fixtures (tests/admin/conftest.py)
- `admin_user`: Creates superuser
- `admin_client`: Logged-in test client
- `mock_request`: Request object with admin user

## Ignored Models

The data coverage test ignores these third-party models:
- `fcm_django.fcmdevice`
- `authtoken.tokenproxy`
- `token_blacklist.*`
- `django_tasks_database.*`
- `account.emailaddress`
- `socialaccount.*`
- `auth.group`
