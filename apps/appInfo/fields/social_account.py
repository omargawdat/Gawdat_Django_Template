class SocialAccountFields:
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    WEBSITE = "website"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
