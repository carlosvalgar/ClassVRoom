from queue import Empty
from django.http import JsonResponse
from django.urls import path
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from .models import *
import random, json, os

@api_view(['GET'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def pin_request(request):
    try:
        request_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "status"    : "ERROR",
            "message"   : "VRtaskID is required"
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
    else:
        validPin = False
        while not validPin:
            possiblePin = random.randint(1000, 9999)
            if not Pin.objects.filter(pin = possiblePin).exists():
                validPin = True

        userVrTask = Pin(vr_task = vrTask, student = request.user, pin = possiblePin)
        userVrTask.save()

        return JsonResponse({
            "status"    : "OK",
            "message"   : userVrTask.pin,
        })

@api_view(['GET'])
def start_vr_exercise(request):
    try:
        request_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "status"    : "ERROR",
            "message"   : "PIN is required"
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
            "message"   : "PIN is required"
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

urlpatterns = [
    path('pin_request', pin_request),
    path('start_vr_exercise', start_vr_exercise),
    path('finish_vr_exercise', finish_vr_exercise)
]