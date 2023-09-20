import pytest
from rest_framework.authtoken.models import Token

from accounts.models import CustomUser
from api.models import Image


@pytest.fixture
def user():
    u = CustomUser.objects.create(username='test_user')
    token, created = Token.objects.get_or_create(user=u)
    return u, token


@pytest.fixture
def image(user):
    user, token = user
    image = Image.objects.create(user=user, image='image.jpg')
    return image
