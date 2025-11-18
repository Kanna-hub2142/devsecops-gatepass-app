from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Hostel, StudentProfile, GatePass


# ---------------------------------------------------
# STUDENT SIGNUP FORM
# ---------------------------------------------------
class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    hostel = forms.ModelChoiceField(
        queryset=Hostel.objects.all(),
        required=True,
        empty_label="Select Hostel",
    )

    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
            "hostel",
            "phone",
        )

    def save(self, commit=True):
        """Create user + student profile (no auto-login)."""
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()  # Save User first

            # Create StudentProfile
            StudentProfile.objects.create(
                user=user,
                hostel=self.cleaned_data["hostel"],
                phone=self.cleaned_data.get("phone", ""),
            )

        return user


# ---------------------------------------------------
# GATEPASS FORM
# ---------------------------------------------------
class GatePassForm(forms.ModelForm):
    from_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )
    to_datetime = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    class Meta:
        model = GatePass
        fields = ["reason", "from_datetime", "to_datetime"]


# ---------------------------------------------------
# STUDENT PROFILE UPDATE FORM
# ---------------------------------------------------
class StudentProfileUpdateForm(forms.ModelForm):
    """Allows updating user first/last name + phone."""

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = StudentProfile
        fields = ["phone"]  # Phone belongs to StudentProfile

    def save(self, user, commit=True):
        """Update both User and StudentProfile."""
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            super().save(commit=True)
        return user
