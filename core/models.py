from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # check if email is present
        if not email:
            raise ValueError("User must have an email address")

        # we normalize email during user creation using in-built function
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_super_user = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # define fields
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # set to use the email for authentication
    USERNAME_FIELD = "email"
