from datetime import datetime

from django.core import signing
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.utils import timezone
from api.models import Image


# Create your views here.


class ImageView(View):
    def get(self, request, pk):
        image = get_object_or_404(Image, pk=pk)
        return render(request, 'thumbnails/image_original.html', {'image': image})


class ImageThumbnailView(View):
    def get(self, request, pk, size):
        image = get_object_or_404(Image, pk=pk)
        size = f'{size}'
        return render(request, 'thumbnails/image_thumbnail.html', {'image': image, 'size': size})


class VerifySignedLinkView(View):
    def get(self, request, signed_link):
        try:
            data = signing.loads(signed_link)
            image = data['image']
            current_time = timezone.now()
            expiration_time = data['expiration_time']
            expiration_time = datetime.fromisoformat(expiration_time)

            if current_time > expiration_time:
                return HttpResponseNotFound('Link has expired')
            return redirect('thumbnails:image', image)
        except signing.BadSignature:
            return HttpResponseNotFound('Invalid link')
