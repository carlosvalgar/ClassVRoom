from django.urls import path

from . import views

urlpatterns = [
    path('ejercicio/<int:courseid>/<int:taskid>/<int:userid>', views.indvidualQualification, name='indvidualQualification'),
    path('', views.landingPage, name='landingPage'),
]