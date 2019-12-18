from django.db import models

from app01.models import UserInfo


# Create your models here.
class User(UserInfo):
    roles = models.ManyToManyField("Role")

    def __str__(self):
        return self.username


class Role(models.Model):
    role_name = models.CharField(max_length=18)
    permissions = models.ManyToManyField("Permission")

    def __str__(self):
        return self.role_name


class Permission(models.Model):
    url = models.CharField(max_length=1000)
    title = models.CharField(max_length=16)
    left_menu = models.BooleanField(default=False)
    icon = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.title
