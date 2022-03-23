from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpRequest
from django.template import loader
from django.views.generic.edit import (UpdateView)
from django.views.decorators.csrf import csrf_exempt
from .models import *
import os
import mimetypes

# Create your views here.

def indvidualQualification(request,taskid,userid):
	alumn = get_object_or_404(User, pk=userid)
	task = get_object_or_404(Task, pk=taskid)
	delivery = get_object_or_404(Delivery, task=task.pk, student=userid)
	listStudent = Subscription.objects.filter(course=task.course, course_role='STUDENT')
	listStudentId = []

	for student in listStudent:
		listStudentId.append(student.user.pk)
	
	print(len(listStudentId))
	print(listStudent)

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

def downloadFile(request, filename=''):
	if filename != '':
		try:
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			filepath = BASE_DIR + '/files/' + filename
			path = open(filepath, 'rb')
			mime_type, _ = mimetypes.guess_type(filepath)
			response = HttpResponse(path, content_type=mime_type)
			response['Content-Disposition'] = "attachment; filename=%s" % filename
			return response
		except FileNotFoundError:
			return HttpResponseNotFound('Error 404 File not found')
	else:
		return render(request, 'file.html')
@csrf_exempt
def update(request, deliveryid, score, comprof):
	delivery = get_object_or_404(Delivery, pk=deliveryid)
	delivery.score = score
	delivery.professorCommentary = comprof
	delivery.save()
