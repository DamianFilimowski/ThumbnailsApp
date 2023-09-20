import pytest
from django.test import Client
from django.urls import reverse

browser = Client()


@pytest.mark.django_db
def test_image(image):
    url = reverse('thumbnails:image', kwargs={'pk':image.id})
    response = browser.get(url)
    assert response.status_code == 200
    assert response.context['image'] == image


@pytest.mark.django_db
def test_image_does_not_exists():
    url = reverse('thumbnails:image', kwargs={'pk': 1})
    response = browser.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_image_thumbnail(image):
    url = reverse('thumbnails:thumbnail', kwargs={'pk': image.id, 'size': 400})
    response = browser.get(url)
    assert response.status_code == 200
    assert response.context['image'] == image


@pytest.mark.django_db
def test_image_thumbnail_does_not_exists():
    url = reverse('thumbnails:thumbnail', kwargs={'pk': 1, 'size': 400})
    response = browser.get(url)
    assert response.status_code == 404
