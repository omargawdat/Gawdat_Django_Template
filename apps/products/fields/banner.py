class BannerFields:
    IMAGE = "image"
    BANNER_TYPE = "banner_type"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
