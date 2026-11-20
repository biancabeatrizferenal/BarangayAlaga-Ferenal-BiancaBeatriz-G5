
from django.urls import path
from . import views

app_name = "appointments"

urlpatterns = [
    # RESIDENT ROUTES
    path("", views.appointment_list, name="list"),
    path("book/", views.appointment_create, name="create"),
    path("<int:pk>/", views.appointment_detail, name="detail"),
    path("<int:pk>/edit/", views.appointment_update, name="update"),
    path("<int:pk>/cancel/", views.appointment_cancel, name="cancel"),

    # STAFF ROUTES
    path("staff/", views.staff_appointment_list, name="staff_list"),
    path("staff/<int:pk>/", views.staff_appointment_detail, name="staff_detail"),
    path(
        "staff/<int:pk>/status/",
        views.staff_appointment_update_status,
        name="staff_update_status",
    ),

    # ADMIN ROUTES
    path("admin/", views.admin_appointment_list, name="admin_list"),
    path("admin/<int:pk>/", views.admin_appointment_detail, name="admin_detail"),
]
