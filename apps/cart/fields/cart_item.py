class CartItemFields:
    CART = "cart"
    PRODUCT = "product"
    QUANTITY = "quantity"
    CREATED_AT = "created_at"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
