from django.contrib import admin

from api.models import Image, ThumbnailSize, Plan, UserPlan

# Register your models here.

admin.site.register(Image)
admin.site.register(ThumbnailSize)
admin.site.register(Plan)
admin.site.register(UserPlan)
