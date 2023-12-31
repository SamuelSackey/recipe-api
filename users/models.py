from django.db import models

from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # check if email is present
        if not email:
            raise ValueError("User must have an email address")

        # we normalize email during user creation using in-built function
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # define fields
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # link the model to the manager
    objects = CustomUserManager()

    # set to use the email for authentication
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.email

    # in case you use "is_admin", you can overwrite to link it to "is_staff"
    # @property
    # def is_staff(self):
    #     # "Is the user a member of staff?"
    #     Simplest possible answer: All admins are staff
    #     return self.is_admin
