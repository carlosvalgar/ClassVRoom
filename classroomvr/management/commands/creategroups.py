# This script creates the permission groups necessary for the application to work

import logging
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

GROUPS = ['schoolAdmin', 'professor',]
MODELS = ['course', 'subscription', 'resource', 'task', 'delivery', 'vr task', 'vr delivery', 'vr qualification']
PERMISSIONS = ['view', 'add', 'delete', 'change',]

class Command(BaseCommand):
    help = 'Creates the permissions groups for users'

    def handle(self, *args, **options):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in MODELS:
                addPermission(new_group, model, PERMISSIONS)
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
