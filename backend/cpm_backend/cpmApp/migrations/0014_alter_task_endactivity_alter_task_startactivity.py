# Generated by Django 4.2.11 on 2024-04-21 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpmApp', '0013_alter_task_endactivity_alter_task_startactivity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='endActivity',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='task',
            name='startActivity',
            field=models.CharField(max_length=10),
        ),
    ]
