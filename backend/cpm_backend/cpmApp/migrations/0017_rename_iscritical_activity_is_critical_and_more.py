# Generated by Django 4.2.11 on 2024-04-21 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpmApp', '0016_rename_endactivity_task_end_activity_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='isCritical',
            new_name='is_critical',
        ),
        migrations.RenameField(
            model_name='activity',
            old_name='isEnd',
            new_name='is_end',
        ),
        migrations.RenameField(
            model_name='activity',
            old_name='isStart',
            new_name='is_start',
        ),
    ]
