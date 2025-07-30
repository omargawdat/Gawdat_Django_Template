class ContactUsFields:
    CUSTOMER = "customer"
    CONTACT_TYPE = "contact_type"
    DESCRIPTION = "description"
    HAS_CHECKED = "has_checked"
    CREATED_AT = "created_at"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
