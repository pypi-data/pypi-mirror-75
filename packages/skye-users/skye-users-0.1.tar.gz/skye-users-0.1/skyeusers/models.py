from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserAccountManager(UserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        return super().create_user(email, email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        return super().create_superuser(email, email, password, **extra_fields)


class UserAccount(AbstractUser):
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='users/photos', null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    USERNAME_FIELD = 'email'

    objects = UserAccountManager()

    def __str__(self):
        return self.get_full_name()
