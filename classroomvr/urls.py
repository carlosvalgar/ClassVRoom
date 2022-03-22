from django.urls import path

from . import views

urlpatterns = [
    path('ejercicio/<int:courseid>/<int:taskid>/<int:userid>', views.indvidualQualification, name='index'),
    path('files/<str:filename>', views.downloadFile, name='download_file'),
]