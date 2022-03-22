from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpRequest
from django.template import loader
from .models import *
import os
import mimetypes

# Create your views here.

def indvidualQualification(request,courseid,taskid,userid):
	course= get_object_or_404(Course, pk=courseid)
	alumnCourse = Subscription.objects.filter(course=course.pk, course_role= 'STUDENT')
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