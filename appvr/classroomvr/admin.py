from django.contrib import admin
from .models import *

# Register your models here.
class SchoolAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        (None, {'fields': ['location']}),
    ]

admin.site.register(School, SchoolAdmin)
admin.site.register(Course)
admin.site.register(Inscription)
admin.site.register(Resource)
admin.site.register(Exercise)
admin.site.register(Pin)
admin.site.register(PrivacyPolicy)
admin.site.register(PrivacyPermission)
admin.site.register(PrivacyPolicies_PrivacyPermissions)