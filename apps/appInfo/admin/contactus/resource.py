from import_export import resources

from apps.appInfo.models.contact_us import ContactUs


class ContactUsResource(resources.ModelResource):
    class Meta:
        model = ContactUs
        fields = []
