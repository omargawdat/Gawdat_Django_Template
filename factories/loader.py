"""
Auto-discovery system for FactoryBoy factories

Usage:
    # Optionally add metadata to override defaults:
    class AddressFactory(factory.DjangoModelFactory):
        _priority = 2        # Load order: 0=first, 1=users, 2=dependent (default)
        _seed_count = "1.5x" # For seed_db: int, "count", "1.5x", etc. (default: "count")
"""

import inspect

import factories as factories_module


def get_factory_priority(factory_class):
    """Get factory load priority (0=first, default=2)"""
    if hasattr(factory_class, "_priority"):
        return factory_class._priority

    name = factory_class.__name__
    # Priority 0: Independent models
    if name in {
        "CountryFactory",
        "AppInfoFactory",
        "SocialAccountFactory",
        "BannerGroupFactory",
        "FAQFactory",
        "OnboardingFactory",
        "PopUpBannerFactory",
    }:
        return 0
    # Priority 1: User models
    if name in {"AdminUserFactory", "CustomerFactory"}:
        return 1
    # Default: Dependent models
    return 2


def get_factory_seed_count(factory_class, default_count):
    """Get seed count (int, 'count', '1.5x', etc.). Default: 'count'"""
    if hasattr(factory_class, "_seed_count"):
        return factory_class._seed_count
    return "count"  # All factories use base count by default


def discover_factories():
    """Auto-discover all factories. Returns [(name, class), ...]"""
    return [
        (name, obj)
        for name, obj in inspect.getmembers(factories_module)
        if inspect.isclass(obj)
        and name.endswith("Factory")
        and hasattr(obj, "_meta")
        and hasattr(obj._meta, "model")
    ]


def load_all_factories(count=2, use_transaction=False):
    """Load test data for all factories (used by tests/conftest.py)"""
    import logging

    factories = sorted(discover_factories(), key=lambda x: get_factory_priority(x[1]))

    for factory_name, factory_class in factories:
        try:
            model = factory_class._meta.model

            # Handle singletons (AppInfo, SocialAccount)
            if hasattr(model, "singleton_instance_id"):
                if not model.objects.exists():
                    factory_class.create()
            else:
                factory_class.create_batch(count)

        except Exception:
            logging.exception(f"Failed to create {factory_name}")
