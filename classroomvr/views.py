from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.http import HttpRequest
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

def indvidualQualification(request,courseid,taskid,userid):
	course= get_object_or_404(Course, pk=courseid)
	alumnCourse = Inscription.objects.filter(course=course.pk, courseRole= 'ST')
	alumn = get_object_or_404(User, pk=userid)
	task = get_object_or_404(Task, pk=taskid, course=course.pk)
	delivery = get_object_or_404(Delivery, task=task.pk, student=userid)
	context = {
        'Task' : task,
        'Delivery' : delivery,
        'Alumn' : alumn,
        'AlumnList' : alumnCourse
    }
	return render(request, 'individualQualification.html',context)


def landingPage(request):
	return render(request, 'landingPage.html')

def login(request):
	return render(request, 'login.html')

@login_required
def dashboard(request):
	alumn = request.user
	alumnCourse = Inscription.objects.filter(user=request.user.pk)
	context = {
        'Alumn' : alumn,
		'Cursos': alumnCourse,
    }
	return render(request, 'dashboard.html',context)