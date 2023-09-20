from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api'

urlpatterns = [
    path('obtain-auth-token/', obtain_auth_token, name='obtain-auth-token'),
    path('upload-image/<str:filename>/', ImageUploadView.as_view(), name='upload-image'),
    path('image-list/', UserImageListView, name='image-list'),
]
