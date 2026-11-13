
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from .forms import ResidentRegistrationForm
from .models import User


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = ResidentRegistrationForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                form.save()

            messages.success(
                request,
                "Your account has been created successfully! "
                "You can now log in."
            )

            return redirect("login")

        messages.error(
            request,
            "Registration failed. Please correct the errors below."
        )

    else:
        form = ResidentRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


@login_required
def dashboard_view(request):
    user = request.user

    if user.role == User.Role.RESIDENT:
        return render(
            request,
            "accounts/resident_dashboard.html"
        )

    elif user.role == User.Role.STAFF:
        return render(
            request,
            "accounts/staff_dashboard.html"
        )

    elif user.role == User.Role.ADMIN:
        return render(
            request,
            "accounts/admin_dashboard.html"
        )

    return HttpResponseForbidden(
        "Unauthorized account role."
    )
