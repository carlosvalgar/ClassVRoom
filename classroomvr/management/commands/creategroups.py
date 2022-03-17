# This script creates the permission groups necessary for the application to work

import logging
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

GROUPS = ['schoolAdmin', 'professor',]
MODELS = ['course', 'delivery', 'inscription', 'pin', 'resource', 'school', 'task', 'user']
ALL_PERMISSIONS = ['view', 'add', 'delete', 'change',]
VIEW_PERMISSIONS = ['view',]
VIEW_CHANGE_PERMISSIONS = ['view', 'change',]

class Command(BaseCommand):
    help = 'Creates the permissions groups for users'

    def handle(self, *args, **options):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in MODELS:
                if (group == 'schoolAdmin' and model == 'school'):
                    addPermission(new_group, model, VIEW_CHANGE_PERMISSIONS)
                elif (group == 'professor' and model == 'school'):
                    addPermission(new_group, model, VIEW_PERMISSIONS)
                else:
                    addPermission(new_group, model, ALL_PERMISSIONS)
        print("Created default group and permissions.")

def addPermission (new_group, model, PERMISSIONS):
    for permission in PERMISSIONS:
        name = 'Can {} {}'.format(permission, model)
        print("Creating {}".format(name))

        try:
            model_add_perm = Permission.objects.get(name=name)
        except Permission.DoesNotExist:
            logging.warning("Permission not found with name '{}'.".format(name))
            continue

        new_group.permissions.add(model_add_perm)
