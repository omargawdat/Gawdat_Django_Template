"""
Pytest fixtures for automatic test data setup

Auto-discovers all factories and creates test data before each test.
Data is automatically cleaned up via Django's transaction rollback.
"""

import inspect

import pytest
from pytest_factoryboy import register

import factories as factories_module
from factories.loader import load_all_factories

# Auto-register all factories as pytest fixtures
for name, obj in inspect.getmembers(factories_module):
    if (
        inspect.isclass(obj)
        and name.endswith("Factory")
        and hasattr(obj, "_meta")
        and hasattr(obj._meta, "model")
    ):
        register(obj)


@pytest.fixture(autouse=True)
def setup_test_data(db, django_db_reset_sequences):
    """Create test data for all factories before each test"""
    load_all_factories(count=2, use_transaction=False)
