from django.http import JsonResponse
from django.urls import path
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from .models import *
import random
import json

@api_view(['GET'])
@authentication_classes([TokenAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def pin_request(request):
    if not 'VRtaskID' in request.GET:
        return JsonResponse({
            "status"    : "ERROR",
            "message"   : "VRtaskID is required",
        })
    if Task.objects.filter(pk = request.GET["VRtaskID"]).exists():
        vrTask = Task.objects.get(pk = request.GET["VRtaskID"])
    else:
        return JsonResponse({
            "status"    : "ERROR",
            "message"   : "That VR task does not exist",
        })
    if Pin.objects.filter(exercise = vrTask, student = request.user).exists():
        userVrTask = Pin.objects.get(exercise = vrTask, student = request.user)
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

        userVrTask = Pin(exercise = vrTask, student = request.user, pin = possiblePin)
        userVrTask.save()

        return JsonResponse({
            "status"    : "OK",
            "message"   : userVrTask.pin,
        })

@api_view(['GET'])
def start_vr_exercise(request):
    if not 'PIN' in request.GET:
        return JsonResponse({
            "status"    : "ERROR",
            "message"   : "PIN is required",
        })
    if Pin.objects.filter(pin = request.GET['PIN']).exists():
        userVrTask = Pin.objects.get(pin = request.GET['PIN'])
        return JsonResponse({
            "status"                : "OK",
            "username"              : userVrTask.student.username,
            "VRexerciseID"          : userVrTask.exercise.pk,
            "minExerciseVersion"    : userVrTask.exercise.exerciseVersion,
        })
    else:
        return JsonResponse({
            "status"    : "ERROR",
            "message"   : "The PIN provided does not exist"
        })

@api_view(['POST'])
def finish_vr_exercise(request):
    request_data = json.loads(request.body)
    data_needed = ["PIN", "record", "VRexerciseID", "exerciseVersion", "metadata"]
    data_validated = checkIfDataExistInJson(data_needed, request_data)
    if data_validated["status"] != "OK":
        return JsonResponse(data_validated)

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