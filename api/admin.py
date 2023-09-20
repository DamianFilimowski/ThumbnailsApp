from django.contrib import admin

from api.models import Image, ThumbnailSize

# Register your models here.

admin.site.register(Image)
admin.site.register(ThumbnailSize)
