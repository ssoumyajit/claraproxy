"""webapi_UDE_v1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.db import models
from rest_framework import serializers
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.renderers import TemplateHTMLRenderer

class UDEUpload(models.Model):
    img = models.FileField(upload_to="dicom_files/")


class UDEUploadSerilaizer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    img = serializers.FileField()

    def create(self, validated_data):
        """
        Create ans return a new UDEUpload instance, given the validated_data.
        """
        return UDEUpload.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        """
        Update and returns an existing "UDEUpload" instance, given the validated_data.
        """
        instance.img =validated_data.get('img', instance.img1)
        instance.save()
        return instance


@csrf_exempt
def UDEFile_list(request):
    """
    List all upload files, or create a new file.
    """
    renderer_classes = [TemplateHTMLRenderer]

    if request.method == 'GET':
        files = UDEUpload.objects.all()
        serializer = UDEUploadSerilaizer(files, many = True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UDEUploadSerilaizer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status = 400)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/udeuploads/', UDEFile_list)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)