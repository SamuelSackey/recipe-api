from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from user.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    # make name field optional
    name = forms.CharField(label="name", max_length=255, required=False)

    class Meta:
        model = CustomUser
        fields = "__all__"


class CustomUserChangeForm(UserChangeForm):
    # make name field optional
    name = forms.CharField(label="name", max_length=255, required=False)

    class Meta:
        model = CustomUser
        fields = "__all__"
