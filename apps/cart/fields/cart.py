class CartFields:
    CUSTOMER = "customer"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
