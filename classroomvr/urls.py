from django.urls import path

from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('exercise/<int:taskid>/<int:userid>', views.indvidualQualification, name='index'),
    path('update/<int:deliveryid>/<int:score>/<str:comprof>', views.update, name='update'),
    path('', views.landingPage, name='landingPage'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='login.html'), name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('taskAllAlumns', views.taskAllAlumns, name='taskAllAlumns'),
    path('files/<str:filename>', views.downloadFile, name='download_file'),
]