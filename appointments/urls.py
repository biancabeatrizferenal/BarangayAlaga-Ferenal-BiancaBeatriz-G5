
from django.urls import path

from . import views


app_name = "appointments"

urlpatterns = [
    path(
        "",
        views.appointment_list,
        name="list",
    ),
    path(
        "book/",
        views.appointment_create,
        name="create",
    ),
    path(
        "<int:pk>/",
        views.appointment_detail,
        name="detail",
    ),
    path(
        "<int:pk>/edit/",
        views.appointment_update,
        name="update",
    ),
    path(
        "<int:pk>/cancel/",
        views.appointment_cancel,
        name="cancel",
    ),
]
