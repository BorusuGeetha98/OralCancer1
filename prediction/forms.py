from django import forms
from .models import CustomUser, PredictionHistory

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password and Confirm Password do not match."
            )
        return cleaned_data

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'role']

class PredictionForm(forms.ModelForm):
    class Meta:
        model = PredictionHistory
        fields = ['image']
