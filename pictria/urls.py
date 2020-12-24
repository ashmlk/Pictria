from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
import admin_honeypot
from allauth.account import views as allauth_views
from allauth.socialaccount import views as allauth_socialviews
from allauth.socialaccount import providers
from importlib import import_module
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

urlpatterns = (
    [
        path("taggit/", include("taggit_selectize.urls")),
        path("accounts/", include("allauth.urls")),
        path("user/", include("django.contrib.auth.urls")),
        path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
        path("qrhprbvwtb-3589hgwe-qrviwnhr-wirWERVH9RE989-weih/", admin.site.urls),
        path("", include("pictures.urls"), name="pictures"),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
