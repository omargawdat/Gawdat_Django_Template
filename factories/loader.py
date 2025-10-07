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


def load_all_factories(count=2, use_transaction=False, verbose=False):
    """
    Load test data for all factories.

    Used by:
    - tests/conftest.py (count=2, verbose=False)
    - seed_db command (count=20+, verbose=True)

    Args:
        count: Base count for creating instances
        use_transaction: Wrap each factory in atomic transaction
        verbose: Print creation progress (for seed_db command)

    Returns:
        dict: Statistics {"success": 10, "failed": 1, "skipped": 2}
    """
    import logging

    logger = logging.getLogger(__name__)
    factories = sorted(discover_factories(), key=lambda x: get_factory_priority(x[1]))

    stats = {"success": 0, "failed": 0, "skipped": 0}

    for factory_name, factory_class in factories:
        try:
            model = factory_class._meta.model
            model_name = model.__name__

            # Handle singletons (AppInfo, SocialAccount)
            if hasattr(model, "singleton_instance_id"):
                if model.objects.exists():
                    stats["skipped"] += 1
                    if verbose:
                        logger.info(
                            f"  ⊘ Skipped {model_name} (singleton already exists)"
                        )
                    continue
                factory_class.create()
                stats["success"] += 1
                if verbose:
                    logger.info(f"  ✓ Created singleton {model_name}")
            else:
                # Get count from factory config or use default
                count_spec = get_factory_seed_count(factory_class, count)
                create_count = _calculate_count(count_spec, count)

                if verbose:
                    logger.info(f"  Creating {create_count} {model_name}(s)...")

                factory_class.create_batch(create_count)
                stats["success"] += 1

                if verbose:
                    logger.info(f"    ✓ Created {create_count} {model_name}(s)")

        except Exception:
            stats["failed"] += 1
            logger.exception(f"Failed to create {factory_name}")

    return stats


def _calculate_count(count_spec, base_count):
    """
    Calculate actual count from specification.

    Args:
        count_spec: Can be:
            - int: exact count (e.g., 10)
            - "count": use base_count
            - "1.5x", "0.8x": multiply base_count
        base_count: Base count from caller

    Returns:
        int: Calculated count

    Examples:
        _calculate_count(10, 20) -> 10
        _calculate_count("count", 20) -> 20
        _calculate_count("1.5x", 20) -> 30
    """
    if isinstance(count_spec, int):
        return count_spec

    if count_spec == "count":
        return base_count

    if isinstance(count_spec, str) and count_spec.endswith("x"):
        multiplier = float(count_spec[:-1])
        return int(base_count * multiplier)

    return base_count
