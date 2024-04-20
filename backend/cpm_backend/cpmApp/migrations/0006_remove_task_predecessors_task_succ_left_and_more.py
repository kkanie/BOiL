# Generated by Django 4.2.11 on 2024-04-20 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cpmApp', '0005_alter_task_ef_alter_task_es_alter_task_lf_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='predecessors',
        ),
        migrations.AddField(
            model_name='task',
            name='succ_left',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='left_successors', to='cpmApp.task'),
        ),
        migrations.AddField(
            model_name='task',
            name='succ_right',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='right_successors', to='cpmApp.task'),
        ),
        migrations.AlterField(
            model_name='task',
            name='EF',
            field=models.IntegerField(default=models.IntegerField(), editable=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='ES',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='LF',
            field=models.FloatField(default=999999, editable=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='LS',
            field=models.FloatField(default=999999, editable=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='slack',
            field=models.FloatField(default=0, editable=False),
        ),
    ]