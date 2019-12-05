from django.db import models

# Create your models here.

class UserInfo(models.Model):

    username = models.CharField(max_length=18)
    password = models.CharField(max_length=32)
    telephone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)