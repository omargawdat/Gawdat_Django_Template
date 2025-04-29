class AppInfoFields:
    ABOUT_US = "about_us"
    TERMS = "terms"
    POLICY = "policy"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
