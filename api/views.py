from pathlib import Path

from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, BasePermission
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
        file_serializer = ImageSerializer(data=request.data)

        valid_extensions = ['.jpg', '.jpeg', '.png']
        file_extension = Path(request.FILES['image'].name).suffix.lower()
        if file_extension not in valid_extensions:
            raise ValidationError('Invalid file type. Only .jpg and .png files are allowed.')

        if file_serializer.is_valid():
            file_serializer.save(user=request.user)
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserImageListView(request):
    user = request.user
    user_plan = UserPlan.objects.get(user=user)
    plans = user_plan.plan.sizes.all()
    images = Image.objects.filter(user=user)
    image_data = []

    for image in images:
        image_info = {}
        if user_plan.plan.original:
            image_info['original'] = request.build_absolute_uri(
                reverse('thumbnails:image', args=[image.pk]))

        for size in plans:
            thumbnail_url = request.build_absolute_uri(reverse('thumbnails:thumbnail', args=[image.pk, size.height]))
            image_info[f'thumbnail_height_{size.height}px'] = thumbnail_url

        image_data.append(image_info)

    data = {'images': image_data}
    return Response(data, status=status.HTTP_200_OK)


class HasExpLinkPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        image_id = request.data.get('image')
        image_object = get_object_or_404(Image, id=image_id)
        if image_object.user != user:
            return False
        user_plan = get_object_or_404(UserPlan, user=user)
        return user_plan.plan.exp_link



@api_view(['POST'])
@permission_classes([IsAuthenticated, HasExpLinkPermission])
def GetExpLink(request):
    user = request.user
    if request.data.get('image', None) is None or request.data.get('expiration_time', None) is None:
        return Response("Missing parameter", status=status.HTTP_400_BAD_REQUEST)
    if int(request.data['expiration_time']) > 30000 or int(request.data['expiration_time']) < 300:
        return Response("Expiration time must be between 300 and 30000", status=status.HTTP_400_BAD_REQUEST)
    image = request.data['image']
    image_object = get_object_or_404(Image, id=image)
    if image_object.user != user:
        return Response("That image doesn't belong to You!", status=status.HTTP_401_UNAUTHORIZED)
    current_time = timezone.now()
    expiration_time = int(request.data['expiration_time'])
    expiration_time = current_time + timezone.timedelta(seconds=expiration_time)
    expiration_time = expiration_time.isoformat()
    signed_link = signing.dumps({'image': image, 'expiration_time': expiration_time})
    url = request.build_absolute_uri(reverse('thumbnails:verify-signed-link', args=[signed_link]))

    return Response(url, status=status.HTTP_200_OK)
