from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


handler404 = "django.views.defaults.page_not_found"
handler500 = "django.views.defaults.server_error"


urlpatterns = [
    path(
        "",
        RedirectView.as_view(
            pattern_name="login",
            permanent=False,
        ),
    ),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("appointments/", include("appointments.urls")),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )