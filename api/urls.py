from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    path('upload-image/<str:filename>/', ImageUploadView.as_view(), name='upload-image'),
]
