"""
Tests for FieldPermissions and AdminContext in common/base/admin.py

This test file covers the field-level permissions system in the admin base classes.
"""

import pytest
from django.contrib.auth import get_user_model
from django.test import RequestFactory

from common.base.admin import AdminContext
from common.base.admin import FieldPermissions

User = get_user_model()


class TestFieldPermissions:
    """Test FieldPermissions dataclass functionality."""

    def test_default_permissions_are_false(self):
        """Test that default FieldPermissions have visible and editable as False."""
        perms = FieldPermissions()
        assert perms.visible is False
        assert perms.editable is False

    def test_is_visible_with_bool_true(self):
        """Test is_visible() returns True when visible is True."""
        perms = FieldPermissions(visible=True)
        assert perms.is_visible() is True

    def test_is_visible_with_bool_false(self):
        """Test is_visible() returns False when visible is False."""
        perms = FieldPermissions(visible=False)
        assert perms.is_visible() is False

    def test_is_visible_with_tuple_all_true(self):
        """Test is_visible() returns True when tuple contains True values."""
        perms = FieldPermissions(visible=(True, True))
        assert perms.is_visible() is True

    def test_is_visible_with_tuple_some_true(self):
        """Test is_visible() returns True when tuple contains at least one True."""
        perms = FieldPermissions(visible=(False, True, False))
        assert perms.is_visible() is True

    def test_is_visible_with_tuple_all_false(self):
        """Test is_visible() returns False when tuple contains all False."""
        perms = FieldPermissions(visible=(False, False))
        assert perms.is_visible() is False

    def test_is_visible_with_empty_tuple(self):
        """Test is_visible() returns False with empty tuple."""
        perms = FieldPermissions(visible=())
        assert perms.is_visible() is False

    def test_is_editable_with_bool_true(self):
        """Test is_editable() returns True when editable is True."""
        perms = FieldPermissions(editable=True)
        assert perms.is_editable() is True

    def test_is_editable_with_bool_false(self):
        """Test is_editable() returns False when editable is False."""
        perms = FieldPermissions(editable=False)
        assert perms.is_editable() is False

    def test_is_editable_with_tuple_all_true(self):
        """Test is_editable() returns True when tuple contains True values."""
        perms = FieldPermissions(editable=(True, True))
        assert perms.is_editable() is True

    def test_is_editable_with_tuple_some_true(self):
        """Test is_editable() returns True when tuple contains at least one True."""
        perms = FieldPermissions(editable=(False, True))
        assert perms.is_editable() is True

    def test_is_editable_with_tuple_all_false(self):
        """Test is_editable() returns False when tuple contains all False."""
        perms = FieldPermissions(editable=(False, False))
        assert perms.is_editable() is False

    def test_readonly_field_permissions(self):
        """Test common pattern: visible but not editable (readonly)."""
        perms = FieldPermissions(visible=True, editable=False)
        assert perms.is_visible() is True
        assert perms.is_editable() is False


@pytest.mark.django_db
class TestAdminContext:
    """Test AdminContext dataclass functionality."""

    @pytest.fixture
    def regular_user(self):
        """Create a regular user (not staff, not superuser)."""
        return User.objects.create_user(
            email="regular@test.com",
            password="testpass123",  # noqa: S106 # pragma: allowlist secret
        )

    @pytest.fixture
    def staff_user(self):
        """Create a staff user."""
        return User.objects.create_user(
            email="staff@test.com",
            password="testpass123",  # noqa: S106 # pragma: allowlist secret
            is_staff=True,
        )

    @pytest.fixture
    def super_user(self):
        """Create a superuser."""
        return User.objects.create_user(
            email="super@test.com",
            password="testpass123",  # noqa: S106 # pragma: allowlist secret
            is_staff=True,
            is_superuser=True,
        )

    @pytest.fixture
    def request_factory(self):
        """Request factory for creating mock requests."""
        return RequestFactory()

    def test_is_super_admin_with_superuser(self, super_user, request_factory):
        """Test is_super_admin returns True for superuser."""
        request = request_factory.get("/admin/")
        request.user = super_user
        context = AdminContext(request)
        assert context.is_super_admin is True

    def test_is_super_admin_with_staff(self, staff_user, request_factory):
        """Test is_super_admin returns False for staff user."""
        request = request_factory.get("/admin/")
        request.user = staff_user
        context = AdminContext(request)
        assert context.is_super_admin is False

    def test_is_staff_with_staff_user(self, staff_user, request_factory):
        """Test is_staff returns True for staff user."""
        request = request_factory.get("/admin/")
        request.user = staff_user
        context = AdminContext(request)
        assert context.is_staff is True

    def test_is_staff_with_regular_user(self, regular_user, request_factory):
        """Test is_staff returns False for regular user."""
        request = request_factory.get("/admin/")
        request.user = regular_user
        context = AdminContext(request)
        assert context.is_staff is False

    def test_is_created_with_object(self, staff_user, request_factory):
        """Test is_created returns True when obj is provided."""
        request = request_factory.get("/admin/")
        request.user = staff_user
        context = AdminContext(request, obj=staff_user)
        assert context.is_created is True

    def test_is_created_without_object(self, staff_user, request_factory):
        """Test is_created returns False when obj is None."""
        request = request_factory.get("/admin/")
        request.user = staff_user
        context = AdminContext(request, obj=None)
        assert context.is_created is False

    def test_is_creating_with_object(self, staff_user, request_factory):
        """Test is_creating returns False when obj is provided."""
        request = request_factory.get("/admin/")
        request.user = staff_user
        context = AdminContext(request, obj=staff_user)
        assert context.is_creating is False

    def test_is_creating_without_object(self, staff_user, request_factory):
        """Test is_creating returns True when obj is None."""
        request = request_factory.get("/admin/")
        request.user = staff_user
        context = AdminContext(request, obj=None)
        assert context.is_creating is True

    def test_backward_compatibility_is_normal_admin(self, staff_user, request_factory):
        """Test backward compatibility static method is_normal_admin."""
        request = request_factory.get("/admin/")
        request.user = staff_user
        assert AdminContext.is_normal_admin(request) is True

    def test_backward_compatibility_is_object_created(self, staff_user):
        """Test backward compatibility static method is_object_created."""
        assert AdminContext.is_object_created(staff_user) is True
        assert AdminContext.is_object_created(None) is False
