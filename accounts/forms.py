
from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, ResidentProfile


class ResidentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label="First Name"
    )

    last_name = forms.CharField(
        max_length=150,
        required=True,
        label="Last Name"
    )

    email = forms.EmailField(
        required=True,
        label="Email Address"
    )

    phone = forms.CharField(
        max_length=20,
        required=True,
        label="Phone Number"
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 3}),
        required=True,
        label="Home Address"
    )

    birth_date = forms.DateField(
        required=True,
        label="Date of Birth",
        widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean_birth_date(self):
        birth_date = self.cleaned_data["birth_date"]

        if birth_date > date.today():
            raise forms.ValidationError(
                "Date of birth cannot be in the future."
            )

        return birth_date

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data["email"]
        user.role = User.Role.RESIDENT
        user.phone = self.cleaned_data["phone"]

        if commit:
            user.save()

            ResidentProfile.objects.create(
                user=user,
                phone=self.cleaned_data["phone"],
                address=self.cleaned_data["address"],
                birth_date=self.cleaned_data["birth_date"],
            )

        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User

        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "profile_photo",
        )

        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email Address",
            "phone": "Contact Number",
            "profile_photo": "Profile Photo",
        }

        widgets = {
            "profile_photo": forms.ClearableFileInput(
                attrs={"accept": "image/jpeg,image/png,image/webp"}
            ),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(
            email__iexact=email
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean_profile_photo(self):
        photo = self.cleaned_data.get("profile_photo")

        if photo and hasattr(photo, "size"):
            if photo.size > 2 * 1024 * 1024:
                raise forms.ValidationError(
                    "Profile photo must be 2 MB or smaller."
                )

            allowed_formats = {"JPEG", "PNG", "WEBP"}

            if getattr(photo, "image", None):
                if photo.image.format not in allowed_formats:
                    raise forms.ValidationError(
                        "Please upload a JPG, PNG, or WebP image."
                    )

        return photo


class ResidentProfileForm(forms.ModelForm):
    class Meta:
        model = ResidentProfile

        fields = (
            "address",
            "birth_date",
        )

        labels = {
            "address": "Home Address",
            "birth_date": "Date of Birth",
        }

        widgets = {
            "address": forms.Textarea(
                attrs={"rows": 3}
            ),
            "birth_date": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

    def clean_birth_date(self):
        birth_date = self.cleaned_data["birth_date"]

        if birth_date and birth_date > date.today():
            raise forms.ValidationError(
                "Date of birth cannot be in the future."
            )

        return birth_date
