from django.urls import path
from .views import *

app_name = 'thumbnails'

urlpatterns = [
    path('original/<int:pk>/', ImageView.as_view(), name='image'),
]
