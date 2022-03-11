from re import M
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=30)
class School(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    def __str__(self):
        return self.name
class PrivacyPolicy(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class PrivacyPermission(models.Model):
    description = models.CharField(max_length=100)
    def __str__(self):
        return self.description
class PrivacyPolicies_PrivacyPermissions(models.Model):
    privacyPolicy = models.ForeignKey(PrivacyPolicy, on_delete=models.CASCADE)
    privacyPermission = models.ForeignKey(PrivacyPermission, on_delete=models.CASCADE)
class User(AbstractUser):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    permissions = models.ForeignKey(PrivacyPolicy, on_delete=models.CASCADE, blank=True, null=True)
class Course(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Inscription(models.Model):
    class CourseRole(models.TextChoices):
        STUDENT = 'ST', _('Student')
        PROFESSOR = 'PF', _('Professor')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    courseRole = models.CharField(max_length=20, choices=CourseRole.choices, default=CourseRole.STUDENT)
    class Meta:
        unique_together = ('user', 'course',)
class Resource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    routeResource = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class Exercise(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    professor = models.ForeignKey(User, on_delete=models.CASCADE)
    deliveryDate = models.DateTimeField()
    file = models.CharField(max_length=100)
    score = models.IntegerField()
    professorCommentary = models.CharField(max_length=500)
    studentCommentary = models.CharField(max_length=500)
    def __str__(self):
        return self.file
class Pin(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.IntegerField()
    def __str__(self):
        return self.pin