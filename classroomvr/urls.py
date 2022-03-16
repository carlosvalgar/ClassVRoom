from django.urls import path

from . import views

urlpatterns = [
    path('ejercicio/<int:taskid>/<int:userid>', views.indvidualQualification, name='index'),
]