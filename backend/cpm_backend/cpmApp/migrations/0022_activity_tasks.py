# Generated by Django 4.2.11 on 2024-04-21 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpmApp', '0021_activity_slack'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='tasks',
            field=models.ManyToManyField(to='cpmApp.activity'),
        ),
    ]
