class AddressFields:
    CUSTOMER = "customer"
    POINT = "point"
    DESCRIPTION = "description"
    LOCATION_TYPE = "location_type"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
