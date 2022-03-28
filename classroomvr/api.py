import re
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.urls import path
from rest_framework.authtoken.models import Token
from .models import User, Course, Subscription, Resource, Task
from django.contrib.auth.hashers import check_password
import json

@api_view(['GET'])
def login(request):
    request_data = json.loads(request.body)
    try:
        user = User.objects.get(email=request_data['email'])
    except:
        return JsonResponse({
            "status"    : 'ERROR',
            "message"   : 'Wrong credentials.',
            })
    if check_password(user.password,request_data['password']) == False:
        return JsonResponse({
            "status"    : 'ERROR',
            "message"   : 'Wrong credentials',
            })
    token = Token.objects.get_or_create(user=user)
    return JsonResponse({
            "status"    : 'OK',
            "session_token" : str(token[0])
            })

@api_view(['GET'])
def logout(request):
    sessionToken = request.GET['session_token']
    try:
        token = Token.objects.get(key=sessionToken)
        return JsonResponse({
            "status"    : 'OK',
            "message"   : 'session successfully closed',
            })
    except:
        return JsonResponse({
            "status"    : 'ERROR',
            "message"   : 'session_token is required',
            })

@api_view(['GET'])
def get_courses(request):
    request_data = json.loads(request.body)
    try:
        token = Token.objects.get(key=request_data['session_token'])
        user = User.objects.get(email=token.user)
        Subscriptions = Subscription.objects.filter(user=user.pk)
        courseList=[]
        for courseid in Subscriptions:
            courseList.append(Course.objects.get(pk=courseid.course.pk))
        json = []
        for course in courseList:
            proffList = Subscription.objects.filter(course=course.pk, course_role='PROFESSOR')
            teachers = []
            for prof in proffList:
                teachers.append({
                        "first_name"    : prof.user.first_name,
                        "last_name" : prof.user.last_name
                    })
            json.append({
                "courseID"  : course.pk,
                "institutionID"  : course.school.pk,
                "title"  : course.name,
                #"description"  : course.description
                "subscribers"   : {
                    "teachers"  : teachers
                },
            })
        return JsonResponse({
            "status"    : 'OK',
            "course_list"   : json
            })
    except:
        return JsonResponse({
            "status"    : 'ERROR',
            "message"   : 'session_token is required',
            })
            
@api_view(['GET'])
def get_courses_detail(request):
    sessionToken = request.GET['session_token']
    request_data = json.loads(request.body)
    if request_data['courseID'].isnumeric() != True:
        return JsonResponse({
                "status"    : 'ERROR',
                "message"   : 'courseID is required.',
                })
    token = Token.objects.get(key=request_data['session_token'])
    roluser = Subscription.objects.get(course=request_data['courseID'], user=token.user.pk)
    if roluser.course_role == 'STUDENT':
        return JsonResponse({
                "status"    : 'ERROR',
                "message"   : 'Insufficient permissions.',
                })
    course = Course.objects.get(pk=request_data['courseID'])
    resource = Resource.objects.filter(course=course.pk)
    resourceList = []
    for recurso in resource:
        resourceList.append(recurso.name)
    task = Task.objects.filter(course=course.pk)
    taskvrList = []
    taskList = []
    for tarea in task:
        if tarea.type == 'VR':
            taskvrList.append(tarea.name)
        else:
            taskList.append(tarea.name)
    return JsonResponse({
                "status"    : 'OK',
                "course"    :{
                    "title" : course.name,
                    #"description"   : course.description,
                    "courseID"  : course.pk,
                    "institutionID" : course.school.pk,
                    "elements"  : resourceList,
                    "tasks" : taskList,
                    "vr_tasks"  :   taskvrList,

                }
            })

urlpatterns = [
    path('login', login ),
    path('logout', logout),
    path('get_courses', get_courses),
    path('get_courses_detail', get_courses_detail),
]