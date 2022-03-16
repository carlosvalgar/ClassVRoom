from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.http import HttpRequest
from django.template import loader
from .models import *

# Create your views here.

def indvidualQualification(request,courseid,taskid,userid):
	course= get_object_or_404(Course, pk=courseid)
	alumnCourse = Inscription.objects.filter(course=course.pk, courseRole= 'ST')
	alumn = get_object_or_404(User, pk=userid)
	task = get_object_or_404(Task, pk=taskid, course=course.pk)
	delivery = get_object_or_404(Delivery, task=task.pk, student=userid)
	conext = {
        'Task' : task,
        'Delivery' : delivery,
        'Alumn' : alumn,
        'AlumnList' : alumnCourse
    }
	return render(request, 'individualQualification.html',conext)
