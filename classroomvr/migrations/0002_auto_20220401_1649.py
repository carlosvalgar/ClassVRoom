# Generated by Django 3.2 on 2022-04-01 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroomvr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=150),
        ),
    ]
