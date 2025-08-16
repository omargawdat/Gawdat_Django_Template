from django.shortcuts import render

from apps.appInfo.models.app_info import AppInfo


def terms_and_policy(request):
    info = AppInfo.get_solo()
    context = {"info": info}
    return render(request, "terms/terms_and_policy.html", context)
