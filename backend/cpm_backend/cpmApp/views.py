from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from .cpm import *


@api_view(['POST'])
@transaction.atomic
def create_task(request):
    Task.objects.all().delete()  # usuwam taski przed wstawieniem nowych

    tasks_data = request.data.get('tasks', [])
    created_tasks = {}

    # tworzenie tasków
    for task_data in tasks_data:
        task, created = Task.objects.get_or_create(
            desc=task_data['desc'],
            defaults={'duration': task_data['duration']}
        )
        created_tasks[task_data['desc']] = task

    # przypisywanie następców
    for task_data in tasks_data:
        task = created_tasks[task_data['desc']]
        #przypisywanie następców na podstawie desc
        succ_left = created_tasks.get(task_data.get('succ_left'))
        succ_right = created_tasks.get(task_data.get('succ_right'))
        task.succ_left = succ_left
        task.succ_right = succ_right
        task.save()

    return Response({'status': 'Success', 'received_data': tasks_data})

@api_view(['GET'])
def calculate_critical_path(request):

    # konwersja najpierw
    tasks, predecessors = convert_successors_to_predecessors_format(Task.objects.all())
    calculate_time_reserves(tasks, predecessors)
    critical_path = find_critical_path(tasks)

    #serializacja i odp
    serializer = TaskSerializer(tasks, many=True)
    return Response({
        'tasks': serializer.data,
        'critical_path': critical_path
    })

