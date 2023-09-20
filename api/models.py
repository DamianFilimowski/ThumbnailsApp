from django.db import models
from sorl.thumbnail import ImageField

from accounts.models import CustomUser


# Create your models here.


class ThumbnailSize(models.Model):
    size = models.PositiveIntegerField()


class Plan(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    sizes = models.ManyToManyField(ThumbnailSize)


class Image(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = ImageField(upload_to='post_images')

