class BannerGroupFields:
    NAME = "name"
    NAME_AR = "name_ar"
    NAME_EN = "name_en"
    ORDER = "order"
    IS_ACTIVE = "is_active"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
