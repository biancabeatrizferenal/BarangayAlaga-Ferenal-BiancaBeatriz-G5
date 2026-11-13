
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

        if commit:
            user.save()

            ResidentProfile.objects.create(
                user=user,
                phone=self.cleaned_data["phone"],
                address=self.cleaned_data["address"],
                birth_date=self.cleaned_data["birth_date"],
            )

        return user
