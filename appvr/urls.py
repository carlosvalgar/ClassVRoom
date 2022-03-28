"""appvr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from classroomvr.models import *
from classroomvr.views import *
from rest_framework import routers, serializers, viewsets
from django.http import JsonResponse
from rest_framework.authtoken import views as apiviews

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff',]

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SchoolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = School
        fields = ['url', 'name',]

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    school = SchoolSerializer()
    class Meta:
        model = Course
        fields = ['url', 'name', 'school',]

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'get_courses', CourseViewSet)
router.register(r'schools', SchoolViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('classroomvr.urls')),
    path('api/', include(router.urls)),
    path('api/', include('classroomvr.api')),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', apiviews.obtain_auth_token),
]
