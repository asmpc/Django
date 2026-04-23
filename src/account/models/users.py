from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from account.managers import UserManager
from config.models import BaseModel


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(max_length=64, null=True, blank=True, unique=True)
    phone = models.CharField(max_length=255, unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(max_length=64, unique=True)
    USERNAME_FIELD = 'email'


    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)



    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    class Meta:
        ordering = ["id","-created_at"]
        db_table = "users"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Owners(User):
    class Meta:
        db_table = "owners"
        verbose_name = "Owner"
        verbose_name_plural = "Owners"


class Employees(User):
    work_time_hours = models.PositiveSmallIntegerField
    worktime_timezone = models.SmallIntegerField()

    class Meta:
        db_table = "employees"
        verbose_name = "Employee"
        verbose_name_plural = "Employees"