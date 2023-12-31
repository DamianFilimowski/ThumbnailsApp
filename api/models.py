from django.db import models
from sorl.thumbnail import ImageField

from accounts.models import CustomUser


# Create your models here.


class ThumbnailSize(models.Model):
    height = models.PositiveIntegerField()

    def __str__(self):
        return f'Thumbnail {self.height} height'


class Plan(models.Model):
    name = models.CharField(max_length=100)
    sizes = models.ManyToManyField(ThumbnailSize)
    original = models.BooleanField(default=False)
    exp_link = models.BooleanField(default=False)

    def __str__(self):
        return f'"{self.name}" Plan'


class Image(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    image = ImageField(upload_to='post_images')


class UserPlan(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    plan = models.OneToOneField(Plan, on_delete=models.CASCADE)
