class NotificationFields:
    NOTIFICATION_TYPE = "notification_type"
    TITLE = "title"
    TITLE_AR = "title_ar"
    TITLE_EN = "title_en"
    MESSAGE_BODY = "message_body"
    MESSAGE_BODY_AR = "message_body_ar"
    MESSAGE_BODY_EN = "message_body_en"
    CREATED_AT = "created_at"
    USERS = "users"
    SEND_SMS = "send_sms"
    SEND_FCM = "send_fcm"
    IS_READ = "is_read"

    @classmethod
    def get_field_name(cls, model, field):
        return model._meta.get_field(field).name
