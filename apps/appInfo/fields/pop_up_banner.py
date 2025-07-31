class PopUpBannerFields:
    IMAGE = "image"
    COUNT_PER_USER = "count_per_user"
    IS_ACTIVE = "is_active"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
