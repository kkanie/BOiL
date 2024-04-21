from django.db import models
from django import forms

class Activity(models.Model):
    id = models.AutoField(primary_key=True)
    is_critical = models.BooleanField(default=False)
    is_start = models.BooleanField(default=False)
    is_end = models.BooleanField(default=False)
    ES = models.FloatField(default=0.0)
    EF = models.FloatField(default=0.0)
    LS = models.FloatField(default=0.0)
    LF = models.FloatField(default=0.0)
    slack = models.FloatField(default=0.0)
    tasks = models.ManyToManyField('Task', related_name='activities')

class Task(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    start_activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='starting_tasks', null=True,
                                      blank=True)
    end_activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='ending_tasks', null=True,
                                    blank=True)
    duration = models.CharField(max_length=10)
    ES = models.FloatField(default=0.0)
    EF = models.FloatField(default=0.0)
    LS = models.FloatField(default=0.0)
    LF = models.FloatField(default=0.0)
    slack = models.FloatField(default=0.0)
    is_critical = models.BooleanField(default=False)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['id', 'duration', 'start_activity', 'end_activity']
