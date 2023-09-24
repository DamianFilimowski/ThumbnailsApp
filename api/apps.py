from django.apps import AppConfig
from django.db.utils import IntegrityError


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        try:
            from api.models import ThumbnailSize, Plan
            thumbnail_200, created_200 = ThumbnailSize.objects.get_or_create(height=400)
            thumbnail_400, created_400 = ThumbnailSize.objects.get_or_create(height=200)
            basic, created_basic = Plan.objects.get_or_create(name='Basic')
            basic.sizes.add(thumbnail_200)
            premium, created_premium = Plan.objects.get_or_create(name='Premium', original=True)
            premium.sizes.add(thumbnail_200, thumbnail_400)
            enterprise, created_enterprise = Plan.objects.get_or_create(name='Enterprise', original=True, exp_link=True)
            enterprise.sizes.add(thumbnail_200, thumbnail_400)
        except IntegrityError:
            pass
