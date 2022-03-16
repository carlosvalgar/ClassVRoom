from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

from django.contrib import admin
# Register your models here.


class SchoolAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(SchoolAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name="admin_centro").exists():
            return qs.filter(name=request.user.school)


class CourseAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(CourseAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs       
        if request.user.groups.filter(name="admin_centro").exists():
            return qs.filter(school=request.user.school)



class InscriptionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = Inscription.objects.filter(course__school=request.user.school)
        if request.user.is_superuser:
            qs = super(InscriptionAdmin, self).get_queryset(request)
            return qs
        if request.user.groups.filter(name="admin_centro").exists():
            return qs

class ResourceAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = Resource.objects.filter(course__school=request.user.school)
        if request.user.is_superuser:
            qs = super(ResourceAdmin, self).get_queryset(request)
            return qs
        if request.user.groups.filter(name="admin_centro").exists():
            return qs

class ExerciseAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = Exercise.objects.filter(course__school=request.user.school)
        if request.user.is_superuser:
            qs = super(ExerciseAdmin, self).get_queryset(request)
            return qs
        if request.user.groups.filter(name="admin_centro").exists():
            return qs

class PinAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = Pin.objects.filter(exercise__course__school=request.user.school)
        if request.user.is_superuser:
            qs = super(PinAdmin, self).get_queryset(request)
            return qs
        if request.user.groups.filter(name="admin_centro").exists():
            return qs

class CustomUserAdmin(UserAdmin):
    def get_queryset(self, request):
        qs = super(CustomUserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name="admin_centro").exists():
            return qs.filter(school=request.user.school)

admin.site.register(User,CustomUserAdmin)
admin.site.register(School,SchoolAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Inscription,InscriptionAdmin)
admin.site.register(Resource,ResourceAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Pin,PinAdmin)
admin.site.register(PrivacyPolicy)
admin.site.register(PrivacyPermission)
admin.site.register(PrivacyPolicies_PrivacyPermissions)