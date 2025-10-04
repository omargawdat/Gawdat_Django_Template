"""
Shared factory loading utilities

Used by both tests/conftest.py and management commands to avoid duplication.
"""

import inspect

from django.db import transaction

import factories as factories_module


def discover_factories():
    """
    Auto-discover all factories from factories module

    Returns:
        List of tuples: [(factory_name, factory_class), ...]
    """
    discovered_factories = []

    for name, obj in inspect.getmembers(factories_module):
        if (
            inspect.isclass(obj)
            and name.endswith("Factory")
            and hasattr(obj, "_meta")
            and hasattr(obj._meta, "model")
        ):
            discovered_factories.append((name, obj))

    return discovered_factories


def create_factory_data(factory_class, count=2, skip_if_exists=False):
    """
    Create instances using a factory

    Args:
        factory_class: The factory class to use
        count: Number of instances to create (default: 2)
        skip_if_exists: For singleton models, skip if instance already exists

    Returns:
        bool: True if successful, False if skipped/failed
    """
    model = factory_class._meta.model

    # Handle singleton models
    if hasattr(model, "singleton_instance_id"):
        if skip_if_exists and model.objects.exists():
            return False

        if not model.objects.exists():
            factory_class.create()
        return True

    # Create batch for regular models
    factory_class.create_batch(count)
    return True


def load_all_factories(count=2, skip_factories=None, use_transaction=False):
    """
    Load data for all discovered factories

    Args:
        count: Number of instances per factory (default: 2)
        skip_factories: Set of factory names to skip (default: None)
        use_transaction: Whether to wrap each factory in a transaction (default: False)

    Returns:
        dict: Results with 'created', 'skipped', and 'failed' lists
    """
    if skip_factories is None:
        skip_factories = set()

    results = {
        "created": [],
        "skipped": [],
        "failed": [],
    }

    factories = discover_factories()

    # Sort factories by dependency order: independent factories first
    # Priority 0: No dependencies (countries, groups, etc.)
    # Priority 1: User models
    # Priority 2: Models dependent on users
    priority_order = {
        "CountryFactory": 0,
        "AppInfoFactory": 0,
        "SocialAccountFactory": 0,
        "BannerGroupFactory": 0,
        "FAQFactory": 0,
        "OnboardingFactory": 0,
        "PopUpBannerFactory": 0,
        "AdminUserFactory": 1,
        "CustomerFactory": 1,
        # Everything else gets priority 2 (dependent on users/countries)
    }

    factories_sorted = sorted(factories, key=lambda x: priority_order.get(x[0], 2))

    for factory_name, factory_class in factories_sorted:
        if factory_name in skip_factories:
            results["skipped"].append(factory_name)
            continue

        try:
            if use_transaction:
                with transaction.atomic():
                    success = create_factory_data(
                        factory_class, count, skip_if_exists=True
                    )
            else:
                success = create_factory_data(factory_class, count, skip_if_exists=True)

            if success:
                results["created"].append(factory_name)
            else:
                results["skipped"].append(factory_name)

        except Exception:
            results["failed"].append(factory_name)
            import logging

            logging.exception(f"Failed to create {factory_name}")

    return results
