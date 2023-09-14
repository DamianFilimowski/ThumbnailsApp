from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class AdminCustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")


class AdminCustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")