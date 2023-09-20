from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core import signing
from django.utils import timezone

from .models import Image, UserPlan
from .serializers import ImageSerializer


class ImageUploadView(APIView):
    queryset = Image.objects.all()
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, filename):
        request.data['user'] = request.user.id
        file_serializer = ImageSerializer(data=request.data)
        print(file_serializer.initial_data)

        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserImageListView(request):
    user = request.user
    user_plan = UserPlan.objects.get(user=user)
    plans = user_plan.Plan.sizes.all()
    images = Image.objects.filter(user=user)
    image_data = []

    for image in images:
        image_info = {}
        if user_plan.Plan.original:
            image_info['original'] = request.build_absolute_uri(
                reverse('thumbnails:image', args=[image.pk]))

        for size in plans:
            thumbnail_url = request.build_absolute_uri(reverse('thumbnails:thumbnail', args=[image.pk, size.height]))
            image_info[f'thumbnail_height_{size.height}px'] = thumbnail_url

        image_data.append(image_info)

    data = {'images': image_data}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetExpLink(request):
    user = request.user
    current_time = timezone.now()
    expiration_time = int(request.data['expiration_time'])
    expiration_time = current_time + timezone.timedelta(seconds=expiration_time)
    expiration_time = expiration_time.isoformat()
    image = request.data['image']
    signed_link = signing.dumps({'image': image, 'expiration_time': expiration_time})
    url = request.build_absolute_uri(reverse('thumbnails:verify-signed-link', args=[signed_link]))

    return Response(url, status=status.HTTP_200_OK)