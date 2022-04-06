from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class PrivacyPolicy(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class User(AbstractUser):
    school = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)
    privacy_permissions = models.ForeignKey(PrivacyPolicy, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

class Course(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)
    def __str__(self):
        return self.name

class Subscription(models.Model):
    class CourseRole(models.TextChoices):
        STUDENT = 'STUDENT', _('Student')
        PROFESSOR = 'PROFESSOR', _('Professor')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_role = models.CharField(max_length=20, choices=CourseRole.choices, default=CourseRole.STUDENT)
    class Meta:
        unique_together = ('user', 'course',)

class Resource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='files')
    def __str__(self):
        return self.name

class Task(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    exercise_description = models.CharField(max_length=500, blank=True)
    def __str__(self):
        return self.name

class VRExercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    def __str__(self):
        return self.name

class VRTask(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exercise_description = models.CharField(max_length=500, blank=True)
    vr_exercise = models.ForeignKey(VRExercise, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class VRQualification(models.Model):
    vr_task = models.ForeignKey(VRTask, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(validators=[MaxValueValidator(10)], blank=True)
    professor_commentary = models.CharField(max_length=500,  blank=True)
    student_commentary = models.CharField(max_length=500,  blank=True)

class Delivery(models.Model):
    class DeliveryStatusType(models.TextChoices):
        DELIVERED = 'DELIVERED', _('Delivered')
        NO_DELIVERED = 'NO_DELIVERED', _('No delivered')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_date = models.DateTimeField()
    file = models.FileField(upload_to='files', blank=True, null=True)
    delivery_status = models.CharField(max_length=40, choices=DeliveryStatusType.choices, default=DeliveryStatusType.NO_DELIVERED)
    score = models.IntegerField(blank=True, null=True)
    professor_commentary = models.CharField(max_length=500, blank=True)
    student_commentary = models.CharField(max_length=500, blank=True)

class VRDelivery(models.Model):
    vr_task  = models.ForeignKey(VRTask, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    day_exercise_was_done = models.DateTimeField(auto_now_add=True, blank=True)
    passed_items = models.IntegerField()
    failed_items = models.IntegerField()
    score = models.IntegerField()
    performance_data = models.FileField(upload_to='files', blank=True, null=True)
    exercise_version = models.IntegerField()
    

class Pin(models.Model):
    vr_task = models.ForeignKey(VRTask, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    pin = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])