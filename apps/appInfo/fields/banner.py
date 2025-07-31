class BannerFields:
    IMAGE = "image"
    GROUP = "group"
    IS_ACTIVE = "is_active"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
