from email import message
import re
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from django.urls import path
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password,make_password
from queue import Empty
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import *
import random, json, os

@api_view(['POST'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def pin_request(request):
    try:
        request_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "status"    : "ERROR",
            "message"   : "No JSON has been sended"
        })

    data_needed = ["VRtaskID"]
    data_validated = checkIfDataExistInJson(data_needed, request_data)
    if data_validated["status"] != "OK":
        return JsonResponse(data_validated)

    if VRTask.objects.filter(pk = request_data["VRtaskID"]).exists():
        vrTask = VRTask.objects.get(pk = request_data["VRtaskID"])
    else:
        return JsonResponse({
            "status"    : "ERROR",
            "message"   : "That VR task does not exist",
        })
        
    if Pin.objects.filter(vr_task = vrTask, student = request.user).exists():
        userVrTask = Pin.objects.get(vr_task = vrTask, student = request.user)
        return JsonResponse({
            "status"    : "OK",
            "PIN"       : userVrTask.pin,
            })

    pin = createNewPin()

    userVrTask = Pin(vr_task = vrTask, student = request.user, pin = pin)
    userVrTask.save()

    return JsonResponse({
        "status"    : "OK",
        "message"   : userVrTask.pin,
    })

def createNewPin():
    while True:
        possiblePin = possiblePin = random.randint(1000, 9999)
        if not Pin.objects.filter(pin = possiblePin).exists():
            return possiblePin

@api_view(['POST'])
def start_vr_exercise(request):
    try:
        request_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "status"    : "ERROR",
            "message"   : "No JSON has been sended"
        })
    data_needed = ["PIN"]
    data_validated = checkIfDataExistInJson(data_needed, request_data)
    if data_validated["status"] != "OK":
        return JsonResponse(data_validated)
    if Pin.objects.filter(pin = request_data['PIN']).exists():
        userVrTask = Pin.objects.get(pin = request_data['PIN'])
        return JsonResponse({
            "status"                : "OK",
            "username"              : userVrTask.student.username,
            "VRexerciseID"          : userVrTask.vr_task.pk,
            "minExerciseVersion"    : userVrTask.vr_task.exercise_version,
        })
    else:
        return JsonResponse({
            "status"    : "ERROR",
            "message"   : "The PIN provided does not exist"
        })

@api_view(['POST'])
def finish_vr_exercise(request):
    try:
        request_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "status"    : "ERROR",
            "message"   : "No JSON has been sended"
        })
    data_needed = ["PIN", "auto_grade", "VRexerciseID", "exerciseVersion", "performance_data"]
    data_validated = checkIfDataExistInJson(data_needed, request_data)
    if data_validated["status"] != "OK":
        return JsonResponse(data_validated)
    data_needed = ["passed_items", "failed_items", "score"]
    data_validated = checkIfDataExistInJson(data_needed, request_data["auto_grade"])
    if data_validated["status"] != "OK":
        return JsonResponse(data_validated)
    if not Pin.objects.filter(pin = request_data["PIN"]).exists():
        return JsonResponse({
            "status"    : "ERROR",
            "message"   : "The PIN provided does not exist",
            })
    pin = Pin.objects.get(pin = request_data["PIN"])
    
    os.makedirs(os.path.dirname("files/vr_task/test.json"), exist_ok=True)

    with open("files/test.json", "w+") as outfile:
        formatted_json = json.dumps(request_data["performance_data"], indent = 4)
        print(json.dump( formatted_json, outfile))

    vr_delivery = VRDelivery(
        vr_task = pin.vr_task,
        student = pin.student,
        passed_items = request_data["auto_grade"]["passed_items"],
        failed_items = request_data["auto_grade"]["failed_items"],
        score = request_data["auto_grade"]["score"],
        performance_data = "files/test.json",
        exercise_version = request_data["exerciseVersion"],
        professor_commentary = "",
        student_commentary = "",
        )
    vr_delivery.save()
    return JsonResponse({
        "status"    : "OK",
        "message"   : "Exercise data succesfully stored"
    })

def checkIfDataExistInJson(values, json):
    for value in values:
        if value not in json:
            return {
                "status"    : "ERROR",
                "message"   : "{} is required".format(value)
            }
    return {"status" : "OK"}

@api_view(['POST'])
def login(request):
    try:
        request_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "status"    : "ERROR",
            "message"   : "No JSON has been sended"
        })
    email = request_data['email']
    password = request_data['password']
    try:
        user = User.objects.get(email=email)
    except:
        return JsonResponse({
            "status"    : 'ERROR',
            "message"   : 'Wrong credentials.',
            })
    if user.check_password(password) == False:
        return JsonResponse({
            "status"    : 'ERROR',
            "message"   : 'Wrong credentials',
            })
    token = Token.objects.get_or_create(user=user)
    return JsonResponse({
            "status"    : 'OK',
            "session_token" : str(token[0])
            })

@api_view(['POST'])
def logout(request):
    request_data = json.loads(request.body)
    sessionToken = request_data['session_token']
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

@api_view(['POST'])
def get_courses(request):
    request_data = json.loads(request.body)
    sessionToken = request_data['session_token']
    try:
        token = Token.objects.get(key=sessionToken)
        user = User.objects.get(email=token.user)
        Subscriptions = Subscription.objects.filter(user=user.pk)
        courseList=[]
        for courseid in Subscriptions:
            courseList.append(Course.objects.get(pk=courseid.course.pk))
        message = []
        for course in courseList:
            proffList = Subscription.objects.filter(course=course.pk, course_role='PROFESSOR')
            teachers = []
            for prof in proffList:
                teachers.append({
                    "first_name"    : prof.user.first_name,
                    "last_name" : prof.user.last_name
                    })
            message.append({
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
            "course_list"   : message
        })
    except:
        return JsonResponse({
            "status"    : 'ERROR',
            "message"   : 'session_token is required',
        })

@api_view(['POST'])
def get_courses_detail(request):
    request_data = json.loads(request.body)
    sessionToken = request_data['session_token']
    courseID = request_data['courseID']
    if type(courseID) != int:
        return JsonResponse({
                "status"    : 'ERROR',
                "message"   : 'courseID is required.',
                })
    token = Token.objects.get(key=sessionToken)
    roluser = Subscription.objects.get(course=courseID, user=token.user.pk)
    if roluser.course_role == 'STUDENT':
        return JsonResponse({
                "status"    : 'ERROR',
                "message"   : 'Insufficient permissions.',
                })
    course = Course.objects.get(pk=courseID)
    resource = Resource.objects.filter(course=course.pk)
    resourceList = []
    for recurso in resource:
        resourceList.append(recurso.name)
    task = Task.objects.filter(course=course.pk)
    vrTask = Task.objects.filter(course=course.pk)
    taskvrList = []
    taskList = []
    for tarea in task:
            taskList.append(tarea.name)
    for tareavr in vrTask:
        taskvrList.append(tareavr.name)

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
    path('pin_request', pin_request),
    path('start_vr_exercise', start_vr_exercise),
    path('finish_vr_exercise', finish_vr_exercise),
    path('login', login ),
    path('logout', logout),
    path('get_courses', get_courses),
    path('get_courses_detail', get_courses_detail),
]