import inspect

import factories as factories_module


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
        count: Number of instances to create for each factory
        use_transaction: Wrap each factory in atomic transaction
        verbose: Print creation progress (for seed_db command)

    Returns:
        dict: Statistics {"success": 10, "failed": 1, "skipped": 2}
    """
    import logging

    logger = logging.getLogger(__name__)
    factories = discover_factories()

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
                if verbose:
                    logger.info(f"  Creating {count} {model_name}(s)...")

                factory_class.create_batch(count)
                stats["success"] += 1

                if verbose:
                    logger.info(f"    ✓ Created {count} {model_name}(s)")

        except Exception:
            stats["failed"] += 1
            logger.exception(f"Failed to create {factory_name}")

    return stats
