from django.db import models

from accounts.models import CustomUser


# Create your models here.


class Plan(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

