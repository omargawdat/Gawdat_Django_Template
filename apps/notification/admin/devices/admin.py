from django.contrib import admin
from fcm_django.models import FCMDevice

admin.site.unregister(FCMDevice)

# @admin.register(FCMDevice)
# class FCMDeviceAdmin(ModelAdmin):
#     pass
