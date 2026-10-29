from django.conf import settings
from django.contrib import admin
from django.urls import path, include

# The admin site is only for local development, so the live site doesn't have it. (I don't want random people seeing the admin interface)
admin_urls = [path('admin/', admin.site.urls)] if settings.DEBUG else []

urlpatterns = admin_urls + [
    path("", include("pokedata.urls")),
]
