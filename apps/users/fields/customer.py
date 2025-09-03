class CustomerFields:
    PASSWORD = "password"  #  pragma: allowlist secret # noqa: S105
    LAST_LOGIN = "last_login"
    IS_SUPERUSER = "is_superuser"
    POLYMORPHIC_CTYPE = "polymorphic_ctype"
    USERNAME = "username"
    IS_ACTIVE = "is_active"
    IS_STAFF = "is_staff"
    DATE_JOINED = "date_joined"
    GROUPS = "groups"
    USER_PERMISSIONS = "user_permissions"
    PHONE_NUMBER = "phone_number"
    EMAIL = "email"
    IMAGE = "image"
    FULL_NAME = "full_name"
    GENDER = "gender"
    BIRTH_DATE = "birth_date"
    COUNTRY = "country"
    PRIMARY_ADDRESS = "primary_address"
    REFERRAL_CUSTOMER_ID = "referral_customer_id"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
