from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.http import HttpRequest
from django.template import loader
from .models import *

# Create your views here.

def indvidualQualification(request,taskid,userid):
	alumn= get_object_or_404(User, pk=userid)
	task=get_object_or_404(Task, pk=taskid)
	delivery = get_object_or_404(Delivery, task=taskid, student=alumn)
	conext = {
		'Task' : task,
		'Alumn' : alumn,
		'Delivery' : delivery,
	}
	return render(request, 'individualQualification.html',conext)

