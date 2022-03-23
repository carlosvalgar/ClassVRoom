from django.urls import path

from . import views

urlpatterns = [
    path('exercise/<int:taskid>/<int:userid>', views.indvidualQualification, name='index'),
    path('update/<int:deliveryid>/<int:score>/<str:comprof>', views.update, name='update'),
    path('', views.landingPage, name='landingPage'),
    path('login', views.login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('files/<str:filename>', views.downloadFile, name='download_file'),
]