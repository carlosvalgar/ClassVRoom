from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.http import HttpRequest
from django.template import loader
from .models import *
from django.views.generic.edit import (UpdateView)
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def indvidualQualification(request,taskid,userid):
	alumn = get_object_or_404(User, pk=userid)
	task = get_object_or_404(Task, pk=taskid)
	delivery = get_object_or_404(Delivery, task=task.pk, student=userid)
	listStudent = Inscription.objects.filter(course=task.course, courseRole='ST')
	listStudentId = []

	for student in listStudent:
		listStudentId.append(student.user.pk)

	if listStudentId.index(userid) == len(listStudentId)-1:
		nextStudent = listStudentId[0]
	else:
		nextStudent = listStudentId[listStudentId.index(userid) + 1]

	prevStudent = listStudentId[listStudentId.index(userid) - 1]

	conext = {
		'Task' : task,
		'Alumn' : alumn,
		'Delivery' : delivery,
		'nextalumn' : nextStudent,
		'prevalumn' : prevStudent,
	}

	return render(request, 'individualQualification.html',conext)
@csrf_exempt
def update(request, deliveryid, score, comprof):
	delivery = get_object_or_404(Delivery, pk=deliveryid)
	delivery.score = score
	delivery.professorCommentary = comprof
	delivery.save()