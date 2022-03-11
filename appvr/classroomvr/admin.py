from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class SchoolInline(admin.StackedInline):
    model = School
    extra = 3

class CourseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
    ]

UserAdmin.list_display += ('school', 'role', 'permissions')
UserAdmin.list_filter += ('school', 'role', 'permissions')
UserAdmin.fieldsets += ((None, {'fields': ['school','role', 'permissions']}),)
UserAdmin.add_fieldsets += ((None, {'fields': ['school', 'role', 'permissions']}),)

admin.site.register(User, UserAdmin)
admin.site.register(School)
admin.site.register(Course)
admin.site.register(Inscription)
admin.site.register(Resource)
admin.site.register(Exercise)
admin.site.register(Pin)
admin.site.register(PrivacyPolicy)
admin.site.register(PrivacyPermission)
admin.site.register(PrivacyPolicies_PrivacyPermissions)