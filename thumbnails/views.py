from django.shortcuts import render, get_object_or_404
from django.views import View

from api.models import Image


# Create your views here.


class ImageView(View):
    def get(self, request, pk):
        image = get_object_or_404(Image, pk=pk)
        return render(request, 'thumbnails/image_original.html', {'image': image})