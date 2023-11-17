from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from user.models import CustomUser
from user.forms import CustomUserCreationForm, CustomUserChangeForm


class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    ordering = ["id"]
    list_display = ["email", "name", "is_staff"]
    list_filter = ["is_active", "is_staff"]

    fieldsets = [
        (None, {"fields": ["email", "name", "password"]}),
        ("Logged Data", {"fields": ["last_login"]}),
        (
            "Permissions",
            {
                "fields": [
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ]
            },
        ),
    ]
    readonly_fields = ["last_login"]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ],
            },
        ),
    ]

    search_fields = ["email"]


admin.site.register(CustomUser, UserAdmin)
