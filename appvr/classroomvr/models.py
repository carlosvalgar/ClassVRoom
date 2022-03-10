from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    id_school = models.IntegerField()
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name