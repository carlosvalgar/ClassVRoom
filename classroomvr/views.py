from urllib import response
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse, HttpRequest
from django.template import loader
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.edit import (UpdateView)
from django.views.decorators.csrf import csrf_exempt
from .models import *
import os
import mimetypes

from rest_framework import status
# Comprobate role of actual user to acces.
#def role_check(user):
#	rolUser = get_object_or_404(Subscription, user=request.user, course=task.course)

# Create your views here.
@login_required(login_url="/login")
@csrf_exempt
def indvidualQualification(request,taskid,userid):
	alumn = get_object_or_404(User, pk=userid)
	task = get_object_or_404(Task, pk=taskid)
	delivery = get_object_or_404(Delivery, task=task.pk, student=userid)
	listStudent = Subscription.objects.filter(course=task.course, course_role='STUDENT')
	listStudentId = []

	rolUser = get_object_or_404(Subscription, user=request.user, course=task.course)
	nameUser = get_object_or_404(User, email=request.user)
	course= get_object_or_404(Course, name=task.course)

	for student in listStudent:
		listStudentId.append(student.user.pk)

	if listStudentId.index(userid) == len(listStudentId)-1:
		nextStudent = listStudentId[0]
	else:
		nextStudent = listStudentId[listStudentId.index(userid) + 1]

	prevStudent = listStudentId[listStudentId.index(userid) - 1]

	breadcrumbs = [
		{'url':'/dashboard','name':'Inicio'},
		{'url':'/course/{}'.format(course.pk),'name':course.name},
		{'url':'','name':task.name},
	]
	
	context = {
		'Task' : task,
		'Alumn' : alumn,
		'Delivery' : delivery,
		'nextalumn' : nextStudent,
		'prevalumn' : prevStudent,
		'actualCourse': course,
		'actualUserRol': rolUser,
		'actualUserName': nameUser,
		'Breadcrumbs': breadcrumbs,
	}
	if rolUser.course_role == 'STUDENT':
		return render(request, 'individualQualificationStudent.html',context)
	return render(request, 'individualQualification.html',context)

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
	delivery.professor_commentary = comprof
	delivery.save()
@csrf_exempt
def vrupdate(request, qualificationid, score, comprof):
	qualification = get_object_or_404(VRQualification, pk=qualificationid)
	qualification.score = score
	qualification.professor_commentary = comprof
	qualification.save()

def landingPage(request):
	if request.user.is_authenticated:
		return redirect('dashboard')
	else:
		return render(request, 'landingPage.html')

def login(request):
	return render(request, 'login.html')

@login_required(login_url="/login")
def dashboard(request):
	if request.user.is_authenticated: 
		userSubscriptions = Subscription.objects.filter(user=request.user.pk)
		userCourses = Course.objects.filter(subscription__in=userSubscriptions)
		context = {
			'Courses': userCourses,
		}
	return render(request, 'dashboard.html',context)

@login_required(login_url="/login")
def courses(request,courseID):
	userRol = Subscription.objects.filter(course=courseID, user=request.user.pk)[0]
	resources = Resource.objects.filter(course=courseID)
	tasks = Task.objects.filter(course=courseID)
	vrTasks = VRTask.objects.filter(course=courseID)
	firstId = Subscription.objects.filter(course=courseID,course_role='STUDENT')[0]
	
	context = {
		'firstId'	: firstId,
		'userRol'	: userRol,
		'resources'	: resources,
		'tasks'		: tasks,
		'vrTasks'	: vrTasks
	}
	return render(request, 'courses.html',context)
def taskAllAlumns(request, taskid):
	task = get_object_or_404(Task, pk=taskid)
	delivery = Delivery.objects.filter(task=task.id)
	course = Course.objects.get(pk=task.course.pk)

	breadcrumbs = [
		{'url':'/dashboard','name':'Inicio'},
		{'url':'/course/{}'.format(course.pk),'name':course.name},
		{'url':'','name':task.name},
	]

	context = {
		'Tarea': task,
		'Entrega': delivery,
		'Breadcrumbs':breadcrumbs,
		'Course':course.name,
	}
	return render(request, 'taskAllAlumns.html',context)

@login_required(login_url="/login")
def allTasksPerCoursePerStudent(request, course_id):
	if not Subscription.objects.filter(course = course_id, course_role = 'STUDENT', user = request.user).exists():
		return redirect('dashboard')
	course = get_object_or_404(Course, pk = course_id)
	professor = Subscription.objects.get(course = course, course_role = "PROFESSOR").user
	tasks = Task.objects.all().filter(course = course)
	student_tasks_deliveries = []
	for task in tasks:
		delivery = Delivery.objects.get(task = task, student = request.user)
		student_tasks_deliveries.append({"task" : task, "delivery" : delivery})
	
	breadcrumbs = [
		{'url':'/dashboard','name':'Inicio'},
		{'url':'/course/{}'.format(course.pk),'name':course.name},
		{'url':'','name':'Todas las tareas'},
	]

	context = {
		'course'					: course,
		'professor'					: professor,
		'student'					: request.user,
		'student_tasks_deliveries'	: student_tasks_deliveries,
		'Breadcrumbs'				: breadcrumbs,
	}
	return render(request, 'allTasksPerCoursePerStudent.html',context)

def taskVrIndividualQualification(request,vrtaskid,userid):
	alumn = get_object_or_404(User, pk=userid)
	vrtask = get_object_or_404(VRTask, pk=vrtaskid)
	course = get_object_or_404(Course, name=vrtask.course)
	vrdeliveries = VRDelivery.objects.filter(vr_task=vrtaskid, student=userid)
	listStudent = Subscription.objects.filter(course=vrtask.course, course_role='STUDENT')
	listStudentId = []
	for student in listStudent:
		listStudentId.append(student.user.pk)

	if listStudentId.index(userid) == len(listStudentId)-1:
		nextStudent = listStudentId[0]
	else:
		nextStudent = listStudentId[listStudentId.index(userid) + 1]
	prevStudent = listStudentId[listStudentId.index(userid) - 1]
	
	qualification = VRQualification.objects.filter( vr_task=vrtaskid, student=userid)[0]
	
	breadcrumbs = [
		{'url':'/dashboard','name':'Inicio'},
		{'url':'/course/{}'.format(course.pk),'name':course.name},
		{'url':'','name':vrtask.name},
	]
	
	context = {
		'Alumn' 						: alumn,
		'ListStudents'					: listStudent,
		'ListDeliveries'				: vrdeliveries,
		'VRTask'						: vrtask,
		'NextStudent' 					: nextStudent,
		'PrevStudent' 					: prevStudent,
		'Qualification'					: qualification,
		'Breadcrumbs'					: breadcrumbs,
		
	}
	return render(request, 'vrIndividualQualification.html',context)

def vrTaskAllAlumns(request, vrtaskid):
	vrtask = get_object_or_404(VRTask, pk=vrtaskid)
	vrdeliveries = VRDelivery.objects.filter(vr_task=vrtaskid)
	vrqualifications = VRQualification.objects.filter(vr_task=vrtaskid)
	course = Course.objects.get(name=vrtask.course)
	breadcrumbs = [
		{'url':'/dashboard','name':'Inicio'},
		{'url':'/course/{}'.format(course.pk),'name':course.name},
		{'url':'','name':vrtask.name},
	]

	context={
		'VRTask'			: vrtask,
		'VRDeliveries'		: vrdeliveries,
		'VRQualifications'	: vrqualifications,
		'Course'			: course,
	}
	return render(request, 'vrTaskAllAlumns.html',context)
