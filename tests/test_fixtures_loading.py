"""Test fixture loading to ensure loadfixtures command works without errors."""

import pytest
from django.core.management import call_command


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class TestFixtureLoading:
    """Test that loadfixtures command runs successfully in isolation."""

    def test_loadfixtures_default_behavior(self):
        """Test that loadfixtures command runs without errors (default behavior)."""
        # Flush database to ensure clean state (removes seed_db data)
        call_command("flush", "--noinput", verbosity=0)

        # Default behavior - should complete successfully if all fixtures are valid
        # If this raises an exception, the test will fail
        call_command("loadfixtures", verbosity=0)

    def test_loadfixtures_with_continue_on_error_flag(self):
        """Test that loadfixtures command completes with --continue-on-error flag."""
        # Flush database to ensure clean state
        call_command("flush", "--noinput", verbosity=0)

        # With --continue-on-error flag - should complete even if individual fixtures fail
        # SystemExit with code 0 or 1 is acceptable (0=success, 1=had failures but continued)
        exit_code = None
        try:
            call_command("loadfixtures", continue_on_error=True, verbosity=0)
        except SystemExit as e:
            exit_code = e.code

        # Verify acceptable exit codes
        assert exit_code in [0, 1, None], f"Unexpected exit code: {exit_code}"
