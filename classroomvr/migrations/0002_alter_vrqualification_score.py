# Generated by Django 3.2 on 2022-04-01 17:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroomvr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vrqualification',
            name='score',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(10)]),
        ),
    ]
