from django.db import models


# Create your models here.
class FirstLevelMenu(models.Model):
    title = models.CharField(max_length=18)
    icon = models.CharField(max_length=32, null=True, blank=True)
    weight = models.IntegerField(default=100)  # 权重，用于排序

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    username = models.CharField(max_length=18)
    password = models.CharField(max_length=32)

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
    title = models.CharField(max_length=18)
    menu = models.ForeignKey("FirstLevelMenu", null=True, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True)
    icon = models.CharField(max_length=32, null=True, blank=True)
    url_name = models.CharField(max_length=32, null=True, blank=True)
    def __str__(self):
        return self.title
