# Generated by Django 4.2.11 on 2024-03-27 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpmApp', '0004_alter_task_lf_alter_task_ls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='EF',
            field=models.IntegerField(default=None, editable=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='ES',
            field=models.IntegerField(default=None, editable=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='LF',
            field=models.FloatField(default=None, editable=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='LS',
            field=models.FloatField(default=None, editable=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='slack',
            field=models.FloatField(default=None, editable=False),
        ),
    ]