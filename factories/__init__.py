"""
Model Factories

This package contains Factory Boy factories for creating test data and seeding databases.
Factories can be used in:
- Tests (pytest fixtures)
- Development database seeding
- Management commands
- Data migration scripts

Usage:
    from factories.factories import CustomerFactory, CountryFactory

    # Create a single instance
    customer = CustomerFactory()

    # Create multiple instances
    customers = CustomerFactory.create_batch(10)

    # Create with custom attributes
    customer = CustomerFactory(full_name="John Doe")
"""

from factories.factories import BannerFactory
from factories.factories import BannerGroupFactory
from factories.factories import CountryFactory
from factories.factories import CustomerFactory

__all__ = [
    "BannerFactory",
    "BannerGroupFactory",
    "CountryFactory",
    "CustomerFactory",
]
