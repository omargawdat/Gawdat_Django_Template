class AdminUserFields:
    PASSWORD = "password"  # pragma: allowlist secret # noqa: S105
    LAST_LOGIN = "last_login"
    IS_SUPERUSER = "is_superuser"
    POLYMORPHIC_CTYPE = "polymorphic_ctype"
    USERNAME = "username"
    IS_ACTIVE = "is_active"
    IS_STAFF = "is_staff"
    DATE_JOINED = "date_joined"
    GROUPS = "groups"
    USER_PERMISSIONS = "user_permissions"
    LANGUAGE = "language"
    IMAGE = "image"
    CAN_ACCESS_MONEY = "can_access_money"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
