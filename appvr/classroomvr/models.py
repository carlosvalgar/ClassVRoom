from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class School(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    id_school = models.IntegerField()
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Inscription(models.Model):
    id_user = models.IntegerField();
    id_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    courseRole = models.CharField(max_length=20)

class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    id_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    routeResource = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    id_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    id_professor = models.IntegerField()
    deliveryDate = models.DateTimeField()
    file = models.CharField(max_length=100)
    score = models.IntegerField()
    professorCommentary = models.CharField(max_length=500)
    studentCommentary = models.CharField(max_length=500)
    def __str__(self):
        return self.file

class Pin(models.Model):
    id = models.AutoField(primary_key=True)
    id_exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    id_student = models.IntegerField()
    pin = models.IntegerField()
    def __str__(self):
        return self.pin

class PrivacyPolicy(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class PrivacyPermission(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100)
    def __str__(self):
        return self.description

class PrivacyPolicies_PrivacyPermissions(models.Model):
    id_privacyPolicy = models.ForeignKey(PrivacyPolicy, on_delete=models.CASCADE)
    id_privacyPermission = models.ForeignKey(PrivacyPermission, on_delete=models.CASCADE)