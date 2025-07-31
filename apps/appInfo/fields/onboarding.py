class OnboardingFields:
    TITLE = "title"
    TITLE_AR = "title_ar"
    TITLE_EN = "title_en"
    IMAGE = "image"
    TEXT = "text"
    TEXT_AR = "text_ar"
    TEXT_EN = "text_en"
    SUB_TEXT = "sub_text"
    SUB_TEXT_AR = "sub_text_ar"
    SUB_TEXT_EN = "sub_text_en"
    ORDER = "order"
    IS_ACTIVE = "is_active"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
