from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib import admin

class SubscriptionInline(admin.TabularInline):
    model = Subscription
    extra = 1
class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1
class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
class VRTaskInline(admin.TabularInline):
    model = VRTask
    extra = 1
class CourseAdmin(admin.ModelAdmin):
    inlines = [SubscriptionInline, ResourceInline, TaskInline, VRTaskInline]
    def get_queryset(self, request):
        qs = Course.objects
        if request.user.is_superuser:
            return qs 

        if request.user.groups.filter(name="schoolAdmin").exists():
            return qs.filter(school = request.user.school)

        if request.user.groups.filter(name="professor").exists():
            subscriptions = request.user.subscription_set.filter(course_role='PROFESSOR')
            return qs.filter(subscription__in = subscriptions)

class DeliveryInline(admin.TabularInline):
    model = Delivery
    extra = 1
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    inlines = [DeliveryInline,]
    def get_queryset(self, request):
        qs = Task.objects
        if request.user.is_superuser:
            return qs

        if request.user.groups.filter(name="schoolAdmin").exists():
            courses = Course.objects.filter(school = request.user.school)
            return qs.filter(course__in = courses)

        if request.user.groups.filter(name="professor").exists():
            subscriptions = request.user.subscription_set.filter(course_role='PROFESSOR')
            courses = Course.objects.filter(subscription__in = subscriptions)
            return qs.filter(course__in = courses)

class VRDeliveryInline(admin.TabularInline):
    model = VRDelivery
    extra = 1
class VRQualificationInline(admin.TabularInline):
    model = VRQualification
    extra = 1
class VRTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'course')
    inlines = [VRDeliveryInline,VRQualificationInline,]
    def get_queryset(self, request):
        qs = VRTask.objects
        if request.user.is_superuser:
            return qs

        if request.user.groups.filter(name="schoolAdmin").exists():
            courses = Course.objects.filter(school = request.user.school)
            return qs.filter(course__in = courses)

        if request.user.groups.filter(name="professor").exists():
            subscriptions = request.user.subscription_set.filter(course_role='PROFESSOR')
            courses = Course.objects.filter(subscription__in = subscriptions)
            return qs.filter(course__in = courses)

class CustomUserAdmin(UserAdmin):
    pass



CustomUserAdmin.list_display += ('school', )
CustomUserAdmin.fieldsets += ((None, {'fields': ['school']}),)
CustomUserAdmin.add_fieldsets += ((None, {'fields': ['school','email','first_name','last_name']}),)

admin.site.register(User, CustomUserAdmin)
admin.site.register(School)
admin.site.register(Course, CourseAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(VRTask, VRTaskAdmin)
admin.site.register(VRExercise)

admin.site.register(Pin)
admin.site.register(PrivacyPolicy)
