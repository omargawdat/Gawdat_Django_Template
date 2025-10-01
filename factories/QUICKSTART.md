# Factory Quickstart Guide

Quick reference for loading factory data in development.

## 🚀 Fastest Method: Management Command

The `seed_db` command **auto-discovers all factories** and creates random amounts of data.

```bash
# Seed database with random amounts (5-20 instances per model)
docker compose -f docker-compose.local.yml run --rm django python manage.py seed_db

# Create exactly 50 instances of each model
docker compose -f docker-compose.local.yml run --rm django python manage.py seed_db --count 50

# Create random amounts between 10-100 per model
docker compose -f docker-compose.local.yml run --rm django python manage.py seed_db --min 10 --max 100
```

**✨ Auto-Discovery**: The command automatically discovers all factories in `factories/factories.py`, so when you add new factories, they'll be automatically included!

## 💻 Django Shell (Interactive)

```bash
# Start shell
docker compose -f docker-compose.local.yml run --rm django python manage.py shell
```

```python
from factories import CustomerFactory, CountryFactory

# Create single instance
customer = CustomerFactory()

# Create batch
customers = CustomerFactory.create_batch(10)

# Custom attributes
customer = CustomerFactory(full_name="John Doe")
```

## 📝 Available Factories

```python
from factories import (
    CountryFactory,      # Location app
    CustomerFactory,     # Users app
    BannerGroupFactory,  # AppInfo app
    BannerFactory,       # AppInfo app
)
```

## 🔧 Common Patterns

### Create with relationships
```python
from factories import CustomerFactory, CountryFactory

# Country is auto-created for customer
customer = CustomerFactory()
print(customer.country.name)

# Or specify a country
country = CountryFactory(name="Egypt")
customer = CustomerFactory(country=country)
```

### Create realistic data
```python
# Factories use Faker for realistic data
customers = CustomerFactory.create_batch(20)
for c in customers:
    print(f"{c.full_name} - {c.email} - {c.country.name}")
```

### Build without saving
```python
# Build instance without saving to DB
customer = CustomerFactory.build()
# Modify before saving
customer.email = "custom@example.com"
customer.save()
```

## 📚 Full Documentation

See [README.md](README.md) for complete documentation including:
- Adding new factories
- Factory features (Faker, sequences, lazy attributes)
- Advanced usage patterns
- Best practices
