
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from .forms import (
    ResidentRegistrationForm,
    UserProfileForm,
    ResidentProfileForm,
)
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


@login_required
def profile_view(request):
    user = request.user

    resident_profile = None

    if user.role == User.Role.RESIDENT:
        resident_profile = getattr(
            user,
            "resident_profile",
            None
        )

    if request.method == "POST":
        user_form = UserProfileForm(
            request.POST,
            request.FILES,
            instance=user
        )

        resident_form = (
            ResidentProfileForm(
                request.POST,
                instance=resident_profile
            )
            if resident_profile is not None
            else None
        )

        user_valid = user_form.is_valid()

        resident_valid = (
            resident_form.is_valid()
            if resident_form is not None
            else True
        )

        if user_valid and resident_valid:
            with transaction.atomic():
                updated_user = user_form.save()

                if resident_form is not None:
                    updated_resident_profile = resident_form.save(
                        commit=False
                    )

                    updated_resident_profile.phone = (
                        updated_user.phone
                    )

                    updated_resident_profile.save()

            messages.success(
                request,
                "Your profile has been updated successfully!"
            )

            return redirect("profile")

        messages.error(
            request,
            "Profile update failed. Please correct the errors below."
        )

    else:
        user_form = UserProfileForm(
            instance=user
        )

        resident_form = (
            ResidentProfileForm(
                instance=resident_profile
            )
            if resident_profile is not None
            else None
        )

    return render(
        request,
        "accounts/profile.html",
        {
            "user_form": user_form,
            "resident_form": resident_form,
        }
    )
