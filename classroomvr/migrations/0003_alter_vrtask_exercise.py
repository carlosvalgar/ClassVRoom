# Generated by Django 3.2 on 2022-04-01 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classroomvr', '0002_auto_20220401_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vrtask',
            name='exercise',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='classroomvr.vrexercise'),
            preserve_default=False,
        ),
    ]
