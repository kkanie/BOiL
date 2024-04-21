from django.db import models
from django import forms


class Task(models.Model):
    desc = models.CharField(max_length=255)
    duration = models.CharField(max_length=9)
    #predecessors = models.ManyToManyField('self', symmetrical=False)
    succ_left = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='left_successors')
    succ_right = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='right_successors')


    ES = models.IntegerField(default=0, editable=False)
    EF = models.IntegerField(default=duration, editable=False)
    LS = models.FloatField(default=999999, editable=False)
    LF = models.FloatField(default=999999, editable=False)
    slack = models.FloatField(default=0, editable=False)
    critical = models.CharField(max_length=3, blank=True, editable=False)

    def __str__(self):
        return self.desc

    def computeSlack(self):
        self.slack = self.LF - self.EF
        if self.slack > 0:
            self.critical = 'NO'
        else:
            self.critical = 'YES'
        self.save()

    def save(self, *args, **kwargs):
        duration_int = int(self.duration) if self.duration.isdigit() else 0
        if self.id is None:
            self.EF = self.ES + duration_int
        super(Task, self).save(*args, **kwargs)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['desc', 'duration', 'succ_left', 'succ_right']