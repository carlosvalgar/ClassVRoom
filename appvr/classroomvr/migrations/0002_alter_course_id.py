# Generated by Django 3.2 on 2022-03-10 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroomvr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
