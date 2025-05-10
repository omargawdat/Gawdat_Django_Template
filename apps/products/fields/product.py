class ProductFields:
    NAME = "name"
    NAME_AR = "name_ar"
    NAME_EN = "name_en"
    DESCRIPTION = "description"
    PRICE_CURRENCY = "price_currency"
    PRICE = "price"
    IMAGE = "image"
    CATEGORY = "category"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
