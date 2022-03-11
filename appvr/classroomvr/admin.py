from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.

class InscriptionInline(admin.TabularInline):
    model = Inscription
class ResourceInline(admin.TabularInline):
    model = Resource
    # readonly_fields = ('routeResource',)
class ExerciseInline(admin.TabularInline):
    model = Exercise
    # readonly_fields = ('file',)
class SchoolInline(admin.StackedInline):
    model = School
    extra = 3

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'school',);
    inlines = [InscriptionInline, ResourceInline, ExerciseInline,]

class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'courseRole',);

UserAdmin.list_display += ('school', 'role', 'permissions')
UserAdmin.list_filter += ('school', 'role', 'permissions')
UserAdmin.fieldsets += ((None, {'fields': ['school','role', 'permissions']}),)
UserAdmin.add_fieldsets += ((None, {'fields': ['school', 'role', 'permissions']}),)

admin.site.register(User, UserAdmin)
admin.site.register(School)
admin.site.register(Course, CourseAdmin)
admin.site.register(Inscription, InscriptionAdmin)
admin.site.register(Resource)
admin.site.register(Exercise)
admin.site.register(Pin)
admin.site.register(PrivacyPolicy)
admin.site.register(PrivacyPermission)
admin.site.register(PrivacyPolicies_PrivacyPermissions)