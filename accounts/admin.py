from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import AdminCustomUserCreationForm, AdminCustomUserChangeForm
from .models import CustomUser

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = AdminCustomUserCreationForm
    form = AdminCustomUserChangeForm
    model = CustomUser
    list_display = ["email", "username", "is_superuser"]
    list_editable = ["is_superuser"]


admin.site.register(CustomUser, CustomUserAdmin)