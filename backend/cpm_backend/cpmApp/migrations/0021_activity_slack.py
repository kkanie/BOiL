# Generated by Django 4.2.11 on 2024-04-21 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpmApp', '0020_task_slack'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='slack',
            field=models.FloatField(default=0.0),
        ),
    ]
