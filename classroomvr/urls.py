from django.urls import path

from . import views

urlpatterns = [
    path('exercise/<int:taskid>/<int:userid>', views.indvidualQualification, name='index'),
    path('update/<int:deliveryid>/<int:score>/<str:comprof>', views.update, name='update'),
]