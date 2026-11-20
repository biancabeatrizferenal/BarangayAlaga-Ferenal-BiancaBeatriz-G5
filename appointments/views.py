from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.models import User
from .forms import AppointmentForm
from .models import Appointment


def resident_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != User.Role.RESIDENT:
            raise PermissionDenied(
                "Only residents can manage appointment requests."
            )

        return view_func(request, *args, **kwargs)

    return wrapper


def staff_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != User.Role.STAFF:
            raise PermissionDenied(
                "Only staff members can manage appointments."
            )

        return view_func(request, *args, **kwargs)

    return wrapper


# RESIDENT APPOINTMENT MANAGEMENT

@resident_required
def appointment_list(request):
    appointments = Appointment.objects.filter(
        resident=request.user
    ).order_by("-created_at")

    return render(
        request,
        "appointments/appointment_list.html",
        {
            "appointments": appointments,
        },
    )


@resident_required
def appointment_create(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    appointment = form.save(commit=False)
                    appointment.resident = request.user
                    appointment.status = Appointment.Status.PENDING
                    appointment.save()

            except IntegrityError:
                form.add_error(
                    "appointment_time",
                    (
                        "This appointment slot was just booked "
                        "by another resident. Please select "
                        "another available time."
                    ),
                )

                messages.error(
                    request,
                    "The selected appointment slot is unavailable.",
                )

            else:
                messages.success(
                    request,
                    "Your appointment request has been submitted successfully.",
                )

                return redirect(
                    "appointments:detail",
                    pk=appointment.pk,
                )

        else:
            messages.error(
                request,
                "Please correct the errors in your appointment request.",
            )

    else:
        form = AppointmentForm()

    return render(
        request,
        "appointments/appointment_form.html",
        {
            "form": form,
            "page_title": "Book Healthcare Appointment",
            "submit_label": "Submit Appointment",
        },
    )


@resident_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(
        Appointment,
        pk=pk,
        resident=request.user,
    )

    return render(
        request,
        "appointments/appointment_detail.html",
        {
            "appointment": appointment,
        },
    )


@resident_required
def appointment_update(request, pk):
    appointment = get_object_or_404(
        Appointment,
        pk=pk,
        resident=request.user,
    )

    if appointment.status != Appointment.Status.PENDING:
        messages.error(
            request,
            "Only pending appointments can be edited.",
        )

        return redirect(
            "appointments:detail",
            pk=appointment.pk,
        )

    if request.method == "POST":
        form = AppointmentForm(
            request.POST,
            instance=appointment,
        )

        if form.is_valid():
            try:
                with transaction.atomic():
                    locked_appointment = get_object_or_404(
                        Appointment.objects.select_for_update(),
                        pk=pk,
                        resident=request.user,
                    )

                    if locked_appointment.status != Appointment.Status.PENDING:
                        messages.error(
                            request,
                            "This appointment can no longer be edited.",
                        )

                        return redirect(
                            "appointments:detail",
                            pk=pk,
                        )

                    updated = form.save(commit=False)

                    locked_appointment.service_type = updated.service_type
                    locked_appointment.appointment_date = updated.appointment_date
                    locked_appointment.appointment_time = updated.appointment_time
                    locked_appointment.reason = updated.reason

                    locked_appointment.save()

            except IntegrityError:
                form.add_error(
                    "appointment_time",
                    (
                        "This appointment time is already booked. "
                        "Please select another available time."
                    ),
                )

                messages.error(
                    request,
                    "The selected appointment slot is unavailable.",
                )

            else:
                messages.success(
                    request,
                    "Your appointment has been updated successfully.",
                )

                return redirect(
                    "appointments:detail",
                    pk=pk,
                )

        else:
            messages.error(
                request,
                "Please correct the errors below.",
            )

    else:
        form = AppointmentForm(instance=appointment)

    return render(
        request,
        "appointments/appointment_form.html",
        {
            "form": form,
            "appointment": appointment,
            "page_title": "Edit Healthcare Appointment",
            "submit_label": "Save Changes",
        },
    )


@resident_required
@require_POST
def appointment_cancel(request, pk):
    with transaction.atomic():
        appointment = get_object_or_404(
            Appointment.objects.select_for_update(),
            pk=pk,
            resident=request.user,
        )

        if appointment.status != Appointment.Status.PENDING:
            messages.error(
                request,
                "Only pending appointments can be cancelled.",
            )

            return redirect(
                "appointments:detail",
                pk=appointment.pk,
            )

        appointment.status = Appointment.Status.CANCELLED

        appointment.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

    messages.success(
        request,
        "Your appointment has been cancelled successfully.",
    )

    return redirect(
        "appointments:detail",
        pk=appointment.pk,
    )


# STAFF APPOINTMENT MANAGEMENT

@staff_required
def staff_appointment_list(request):
    appointments = (
        Appointment.objects
        .select_related("resident")
        .order_by("appointment_date", "appointment_time")
    )

    return render(
        request,
        "appointments/staff_appointment_list.html",
        {
            "appointments": appointments,
        },
    )


@staff_required
def staff_appointment_detail(request, pk):
    appointment = get_object_or_404(
        Appointment.objects.select_related("resident"),
        pk=pk,
    )

    return render(
        request,
        "appointments/staff_appointment_detail.html",
        {
            "appointment": appointment,
        },
    )


@staff_required
@require_POST
def staff_appointment_update_status(request, pk):
    new_status = request.POST.get("status")

    with transaction.atomic():
        appointment = get_object_or_404(
            Appointment.objects.select_for_update(),
            pk=pk,
        )

        allowed_transitions = {
            Appointment.Status.PENDING: {
                Appointment.Status.CONFIRMED,
                Appointment.Status.REJECTED,
            },
            Appointment.Status.CONFIRMED: {
                Appointment.Status.COMPLETED,
            },
        }

        allowed_statuses = allowed_transitions.get(
            appointment.status,
            set(),
        )

        if new_status not in allowed_statuses:
            messages.error(
                request,
                "Invalid appointment status change.",
            )

            return redirect(
                "appointments:staff_detail",
                pk=appointment.pk,
            )

        appointment.status = new_status

        appointment.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

    messages.success(
        request,
        "Appointment status updated successfully.",
    )

    return redirect(
        "appointments:staff_detail",
        pk=appointment.pk,
    )
