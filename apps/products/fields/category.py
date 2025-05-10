class CategoryFields:
    NAME = "name"
    NAME_AR = "name_ar"
    NAME_EN = "name_en"
    IMAGE = "image"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
