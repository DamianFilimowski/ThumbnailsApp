import pytest
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client
from django.urls import reverse
from django.core.files.uploadedfile import  SimpleUploadedFile

from api.models import Image, UserPlan

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


# @pytest.mark.django_db
# def test_image_thumbnail(image):
#     url = reverse('thumbnails:thumbnail', kwargs={'pk': image.id, 'size': 400})
#     response = browser.get(url)
#     assert response.status_code == 200
#     assert response.context['image'] == image
#
#
# @pytest.mark.django_db
# def test_image_thumbnail_does_not_exists():
#     url = reverse('thumbnails:thumbnail', kwargs={'pk': 1, 'size': 400})
#     response = browser.get(url)
#     assert response.status_code == 404


@pytest.mark.django_db
def test_image_upload(user):
    user, token = user
    url = reverse('api:upload-image', kwargs={'filename': "abc"})
    with open('./tests/test.jpg', 'rb') as image_file:
        data = {'image': image_file}
        response = browser.post(url, data=data, HTTP_AUTHORIZATION=token)
    image_id = response.data.get('id')
    assert response.status_code == 201
    assert Image.objects.filter(id=image_id, user=user)


@pytest.mark.django_db
def test_image_upload_wrong_format(user):
    user, token = user
    url = reverse('api:upload-image', kwargs={'filename': "abc"})
    with open('./tests/test.txt', 'rb') as image_file:
        data = {'image': image_file}
        response = browser.post(url, data=data, HTTP_AUTHORIZATION=token)
    assert response.status_code == 400


@pytest.mark.django_db
def test_image_upload_not_auth():
    url = reverse('api:upload-image', kwargs={'filename': "abc"})
    with open('./tests/test.jpg', 'rb') as image_file:
        data = {'image': image_file}
        response = browser.post(url, data=data)
    image_id = response.data.get('id')
    assert response.status_code == 401
    with pytest.raises(ObjectDoesNotExist):
        Image.objects.get(id=image_id)


@pytest.mark.django_db
def test_user_image_list_basic_plan(user, image, plan_basic):
    url = reverse('api:image-list')
    user, token = user
    UserPlan.objects.create(user=user, plan=plan_basic)
    response = browser.get(url, HTTP_AUTHORIZATION=token)
    assert response.status_code == 200
    assert response.data['images'][0]['thumbnail_height_200px']
    assert 'original' not in response.data['images'][0]


@pytest.mark.django_db
def test_user_image_list_premium_plan(user, image, plan_premium):
    url = reverse('api:image-list')
    user, token = user
    UserPlan.objects.create(user=user, plan=plan_premium)
    response = browser.get(url, HTTP_AUTHORIZATION=token)
    assert response.status_code == 200
    assert response.data['images'][0]['thumbnail_height_200px']
    assert response.data['images'][0]['original']


@pytest.mark.django_db
def test_user_image_list_enterprise_plan(user, image, plan_enterprise):
    url = reverse('api:image-list')
    user, token = user
    UserPlan.objects.create(user=user, plan=plan_enterprise)
    response = browser.get(url, HTTP_AUTHORIZATION=token)
    assert response.status_code == 200
    assert response.data['images'][0]['thumbnail_height_200px']
    assert response.data['images'][0]['original']


@pytest.mark.django_db
def test_user_image_list_not_auth():
    url = reverse('api:image-list')
    response = browser.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_get_exp_link(user, image, plan_enterprise):
    url = reverse('api:get-exp-link')
    user, token = user
    data = {'image': '1',
            'expiration_time': '50'}
    UserPlan.objects.create(user=user, plan=plan_enterprise)
    response = browser.post(url, data, HTTP_AUTHORIZATION=token)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_exp_link_missing_parameter(user, image, plan_enterprise):
    url = reverse('api:get-exp-link')
    user, token = user
    data = {'image': '1'}
    UserPlan.objects.create(user=user, plan=plan_enterprise)
    response = browser.post(url, data, HTTP_AUTHORIZATION=token)
    assert response.status_code == 400


@pytest.mark.django_db
def test_get_exp_link_not_auth(user, image, plan_enterprise):
    url = reverse('api:get-exp-link')
    user, token = user
    data = {'image': '1',
            'expiration_time': '50'}
    UserPlan.objects.create(user=user, plan=plan_enterprise)
    response = browser.post(url, data)
    assert response.status_code == 401

@pytest.mark.django_db
def test_get_exp_link_not_users_image(user, image, plan_enterprise):
    url = reverse('api:get-exp-link')
    user, token = user
    image.user = None
    image.save()
    data = {'image': '1',
            'expiration_time': '50'}
    UserPlan.objects.create(user=user, plan=plan_enterprise)
    response = browser.post(url, data)
    assert response.status_code == 401
