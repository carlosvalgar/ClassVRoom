from django.urls import path,include
from rest_framework import routers

from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('exercise/<int:taskid>/<int:userid>', views.indvidualQualification, name='index'),
    path('update/<int:deliveryid>/<int:score>/<str:comprof>', views.update, name='update'),
    path('vrupdate/<int:qualificationid>/<int:score>/<str:comprof>', views.vrupdate, name='vrupdate'),
    path('', views.landingPage, name='landingPage'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='login.html'), name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('task-deliveries/<int:taskid>', views.taskAllAlumns, name='taskAllAlumns'),
    path('vr-task/<int:vrtaskid>/<int:userid>', views.taskVrIndividualQualification, name='VrIndividualQualification'),
    path('vr-task-deliveries/<int:vrtaskid>', views.vrTaskAllAlumns, name='vrTaskAllAlumns'),
    path('files/<str:filename>', views.downloadFile, name='download_file'),
    path('course/<int:courseID>',views.courses,name='courses'),
    path('course/<int:course_id>/tasks', views.allTasksPerCoursePerStudent, name='all_tasks_per_course_per_student'),
]