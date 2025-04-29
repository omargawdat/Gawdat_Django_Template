class NotificationFields:
    NOTIFICATION_TYPE = "notification_type"
    TITLE = "title"
    MESSAGE_BODY = "message_body"
    CREATED_AT = "created_at"
    USERS = "users"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
