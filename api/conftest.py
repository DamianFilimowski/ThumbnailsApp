import pytest
from rest_framework.authtoken.models import Token

from accounts.models import CustomUser
from api.models import Image, Plan, ThumbnailSize


@pytest.fixture
def user():
    u = CustomUser.objects.create(username='test_user')
    token, created = Token.objects.get_or_create(user=u)
    token = f'Token {token}'
    return u, token


@pytest.fixture
def image(user):
    user, token = user
    image = Image.objects.create(user=user, image='image.jpg')
    return image


@pytest.fixture
def thumbnail_size():
    thumbnail = ThumbnailSize.objects.create(height=200)
    return thumbnail


@pytest.fixture
def plan_basic(thumbnail_size):
    plan = Plan.objects.create(name='x')
    plan.sizes.add(thumbnail_size)
    return plan


@pytest.fixture
def plan_premium(thumbnail_size):
    plan = Plan.objects.create(name='x')
    plan.sizes.add(thumbnail_size)
    plan.original = True
    plan.save()
    return plan


@pytest.fixture
def plan_enterprise(thumbnail_size):
    plan = Plan.objects.create(name='x')
    plan.sizes.add(thumbnail_size)
    plan.original = True
    plan.exp_link = True
    plan.save()
    return plan
