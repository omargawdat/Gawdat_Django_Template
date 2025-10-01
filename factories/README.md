# Factories

This directory contains Factory Boy factories for generating test data and seeding databases.

## Purpose

Factories can be used in multiple contexts:
- **Tests**: Automatically registered as pytest fixtures
- **Development**: Seed local databases with realistic data
- **Management Commands**: Create sample data for demos
- **Data Migrations**: Generate data during migrations

## Usage

### 1. Management Command (Easiest for Development)

Seed your local database with realistic test data:

```bash
# Docker Compose
docker compose -f docker-compose.local.yml run --rm django python manage.py seed_db

# With custom counts
docker compose -f docker-compose.local.yml run --rm django python manage.py seed_db --customers 100 --countries 20

# Flush existing data first, then seed
docker compose -f docker-compose.local.yml run --rm django python manage.py seed_db --flush

# See all options
docker compose -f docker-compose.local.yml run --rm django python manage.py seed_db --help
```

See [common/management/commands/seed_db.py](../common/management/commands/seed_db.py) for implementation.

### 2. Django Shell (Interactive)

```bash
# Start Django shell
docker compose -f docker-compose.local.yml run --rm django python manage.py shell
```

```python
# In the shell
from factories import CustomerFactory, CountryFactory, BannerFactory

# Create a single customer
customer = CustomerFactory()
print(f"{customer.full_name} - {customer.email}")

# Create 10 customers
customers = CustomerFactory.create_batch(10)
print(f"Created {len(customers)} customers")

# Create with custom attributes
customer = CustomerFactory(
    full_name="John Doe",
    email="john@example.com"
)

# Build without saving to database
customer = CustomerFactory.build()  # Not saved to DB
```

### 3. In Tests (Automatic)

Factories are automatically registered as pytest fixtures in `tests/conftest.py`:

```python
# tests/test_something.py
import pytest

@pytest.mark.django_db
def test_customer_creation(customer_factory):
    """Factories are available as fixtures"""
    customer = customer_factory()
    assert customer.full_name
```

### 4. In Python Scripts

```python
# scripts/populate_demo_data.py
from factories import CustomerFactory, CountryFactory

def populate():
    # Create data programmatically
    countries = CountryFactory.create_batch(10)
    customers = CustomerFactory.create_batch(50)

    print(f"Created {len(countries)} countries")
    print(f"Created {len(customers)} customers")

if __name__ == "__main__":
    import django
    django.setup()
    populate()
```

Run with:
```bash
docker compose -f docker-compose.local.yml run --rm django python scripts/populate_demo_data.py
```


## Available Factories

### Location
- `CountryFactory`: Creates countries with flags, currencies, and reward amounts

### Users
- `CustomerFactory`: Creates customers with profiles, images, and countries

### App Info
- `BannerGroupFactory`: Creates banner groups
- `BannerFactory`: Creates banners with images

## Adding New Factories

1. **Create the factory** in `factories/factories.py`:

```python
import factory
from apps.myapp.models import MyModel

class MyModelFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    description = factory.Faker("text", max_nb_chars=200)

    class Meta:
        model = MyModel
```

2. **Export it** in `factories/__init__.py`:

```python
from factories.factories import MyModelFactory

__all__ = [
    # ... existing factories
    "MyModelFactory",
]
```

3. **Use it** anywhere in your code or tests!

## Factory Features

### Faker Integration
Use [Faker](https://faker.readthedocs.io/) for realistic data:

```python
name = factory.Faker("name")
email = factory.Faker("email")
phone = factory.Faker("phone_number")
date = factory.Faker("date_of_birth", minimum_age=18)
```

### Relationships
Handle foreign keys and relationships:

```python
# SubFactory for ForeignKey
country = factory.SubFactory(CountryFactory)

# RelatedFactory for reverse relationships
@factory.post_generation
def addresses(self, create, extracted, **kwargs):
    if create:
        AddressFactory.create_batch(2, customer=self)
```

### Sequences
Generate unique sequential data:

```python
email = factory.Sequence(lambda n: f"user{n}@example.com")
order = factory.Sequence(lambda n: n)
```

### LazyAttribute
Compute values based on other attributes:

```python
slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
currency = factory.LazyAttribute(lambda obj: Money(10, obj.country.currency))
```

## Best Practices

1. **Keep factories simple**: One factory per model
2. **Use sensible defaults**: Factories should work with no parameters
3. **Use Faker**: Generate realistic data instead of static strings
4. **Handle relationships**: Use SubFactory for foreign keys
5. **Document complex logic**: Add comments for non-obvious configurations
6. **Export in __init__.py**: Make factories easily importable

## Testing

Factories are automatically tested when you run the test suite. The `test_admin_data_coverage.py` test will fail if models don't have corresponding factories.

Run tests:
```bash
docker compose -f docker-compose.local.yml run --rm django pytest
```
