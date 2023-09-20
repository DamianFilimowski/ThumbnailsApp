import pytest
from django.test import Client
from django.urls import reverse

browser = Client()

@pytest.mark.django_db
def test_image_view(user, image):
    url = reverse('thumbnails:image', kwargs={'pk':image.id})
    response = browser.get(url)
    assert response.status_code == 200
