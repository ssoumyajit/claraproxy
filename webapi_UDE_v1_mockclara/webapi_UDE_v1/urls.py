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
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.decorators import parser_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
        instance.img=validated_data.get('img', instance.img1)
        instance.save()
        return instance


@csrf_exempt
@api_view(['GET', 'POST'])
def UDEFile_list(request):
    """
    Django request class extends HttpRequest class & provides more flexible 
    request parsing.

    List all upload files, or create a new file.
    """
    renderer_classes = [TemplateHTMLRenderer]

    if request.method == 'GET':
        files = UDEUpload.objects.all()
        serializer = UDEUploadSerilaizer(files, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # data = MultiPartParser().parse(request)
        serializer = UDEUploadSerilaizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# ------------------------------------------------------------------------------


class ModelConfigUpload(models.Model):
    model = models.FileField(upload_to="model_files/")
    config = models.FileField(upload_to="config_files/")


class ModelConfigSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    model = serializers.FileField()
    config = serializers.FileField()

    def create(self, validated_data):
        """
        create and return a new ModelConfig instance, given the validated data
        """
        return ModelConfig.objects.create(**validated_data)

@csrf_exempt
@parser_classes([MultiPartParser])
def ModelConfigList(request):
    #parser_classes = [MultiPartParser]

    if request.method == 'GET':
        modelconfigs = ModelConfigUpload.objects.all()
        serializer = ModelConfigSerializer(modelconfigs, many = True, context={'request': request})
        return JsonResponse(serializer.data, safe = False)
    
    elif request.method == 'POST':
        data = MultiPartParser().parse(request)
        serilaizer = ModelConfigSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/udeuploads/', UDEFile_list),
    path('api/v1/model_config_uploads/', ModelConfigList)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
