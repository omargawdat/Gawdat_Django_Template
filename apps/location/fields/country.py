class CountryFields:
    CODE = "code"
    CURRENCY = "currency"
    NAME = "name"
    NAME_AR = "name_ar"
    NAME_EN = "name_en"
    PHONE_CODE = "phone_code"
    FLAG = "flag"
    IS_ACTIVE = "is_active"
    REFERRAL_POINTS = "referral_points"
    REFERRAL_POINTS_CURRENCY = "referral_points_currency"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
