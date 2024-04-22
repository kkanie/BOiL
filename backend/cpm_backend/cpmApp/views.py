from rest_framework.response import Response
from django.db import transaction
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Activity, Task
from .utils import *
from .serializers import ActivitySerializer, TaskSerializer
from django.db.models import Max

@api_view(['POST'])
@transaction.atomic
def create_task(request):
    Task.objects.all().delete()
    Activity.objects.all().delete()
    tasks_data = request.data.get('tasks', []) if isinstance(request.data, dict) else request.data

    activity_dict = {}

    for task_data in tasks_data:
        # Extract data
        czynnosc = task_data['czynnosc']
        duration = task_data['czas_trwania']
        start_activity_id = task_data.get('nastepstwoL')
        end_activity_id = task_data.get('nastepstwoP')


        start_activity, _ = Activity.objects.get_or_create(id=start_activity_id)
        end_activity, _ = Activity.objects.get_or_create(id=end_activity_id)


        activity_dict[start_activity_id] = start_activity
        activity_dict[end_activity_id] = end_activity


        task, created = Task.objects.update_or_create(
            id=czynnosc,
            defaults={
                'duration': duration,
                'start_activity': start_activity,
                'end_activity': end_activity
            }
        )

        start_activity.tasks.add(task)
        end_activity.tasks.add(task)


    return Response({'status': 'Success', 'received_data': tasks_data})


def update_activity_based_on_tasks(activity):
    activity.is_critical = any(t.is_critical for t in activity.tasks.all())
    activity.save()


@api_view(['GET'])
@transaction.atomic
def calculate_critical_path(request):
    try:
        tasks = Task.objects.all()
        activities = Activity.objects.all()

        reset_activities(activities)

        for task in tasks:
            calculate_task_times(task)

        for task in tasks:
            calculate_task_times(task)

        for activity in activities:
            update_activity_times(activity)

        latest_finish = activities.aggregate(Max('EF'))['EF__max']

        # Ustawienie LF i LS dla wszystkich zadań na podstawie najpóźniejszego czasu zakończenia
        for task in tasks:
            task.LF = latest_finish
            task.LS = task.LF - int(task.duration)
            task.save()

        # Iteracja w odwrotnej kolejności dla obliczenia LF i LS
        for task in reversed(list(tasks)):
            # Dla każdej aktywności związanej z zadaniem jako end_activity
            for related_task in task.end_activity.starting_tasks.all():
                if related_task.LS < task.LF:
                    task.LF = related_task.LS
                    task.LS = task.LF - int(task.duration)
                    task.save()

        # Obliczenie slacka dla każdego zadania
        for task in tasks:
            task.slack = task.LF - task.EF
            if task.slack == 0:
                task.is_critical = True
            task.save()

        # Ustalenie najpóźniejszego zakończenia jako maksymalnego EF
        latest_finish = activities.aggregate(Max('EF'))['EF__max'] or 0

        # Ustawienie LF dla aktywności i LS oparte na LF
        for activity in activities:
            activity.LF = latest_finish
            activity.save()

        # Obliczenie LF i LS dla aktywności w odwrotnej kolejności
        for activity in reversed(activities):
            connected_tasks = activity.starting_tasks.all()
            for task in connected_tasks:
                if task.end_activity and task.end_activity.LF < activity.LF:
                    activity.LF = task.end_activity.LF
            activity.LS = activity.LF - (activity.EF - activity.ES)
            activity.save()

        for activity in activities:
            activity.slack = activity.LF - activity.EF
            activity.save()

        Activity.objects.bulk_update(activities, ['ES', 'EF', 'is_critical', 'is_start', 'is_end', 'LS', 'LF', 'slack'])
        Task.objects.bulk_update(tasks, ['ES', 'EF', 'LS', 'LF', 'slack'])

        activities_data = ActivitySerializer(activities, many=True).data
        tasks_data = TaskSerializer(tasks, many=True).data
        return Response({
            'activities': activities_data,
            'tasks': tasks_data
        })

    except Exception as e:
        return Response({'error': str(e)}, status=400)

def reset_activities(activities):
    for activity in activities:
        activity.ES = activity.EF = activity.LS = activity.LF = activity.slack = 0
        activity.is_critical = activity.is_start = activity.is_end = False
        activity.save()
