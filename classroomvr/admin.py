from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib import admin

# Register your models here.

# Inlines
class InscriptionInline(admin.TabularInline):
    model = Inscription
    extra = 1
class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1
class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

# Admin view
class SchoolAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(SchoolAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.groups.filter(name="admin_centro").exists():
            return qs.filter(name=request.user.school)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'school',);
    inlines = [InscriptionInline, ResourceInline, TaskInline,]

    def get_queryset(self, request):
        qs = super(CourseAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs       
        if request.user.groups.filter(name="admin_centro").exists():
            return qs.filter(school=request.user.school)

class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'courseRole',);
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
class TaskAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = Task.objects.filter(course__school=request.user.school)
        if request.user.is_superuser:
            qs = super(TaskAdmin, self).get_queryset(request)
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

CustomUserAdmin.list_display += ('school', 'permissions')
CustomUserAdmin.list_filter += ('school', 'permissions')
CustomUserAdmin.fieldsets += ((None, {'fields': ['school', 'permissions']}),)
CustomUserAdmin.add_fieldsets += ((None, {'fields': ['school', 'permissions']}),)

admin.site.register(User,CustomUserAdmin)
admin.site.register(School,SchoolAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Inscription,InscriptionAdmin)
admin.site.register(Resource,ResourceAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Delivery)
admin.site.register(Pin,PinAdmin)
admin.site.register(PrivacyPolicy)
admin.site.register(PrivacyPermission)
admin.site.register(PrivacyPolicies_PrivacyPermissions)