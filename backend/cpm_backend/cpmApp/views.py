from django.db import transaction
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from .cpm import *

@api_view(['POST'])
@transaction.atomic
def create_task(request):
    Task.objects.all().delete() # usuwam taski przed wstawieniem nowych

    tasks_data = request.data.get('tasks', [])
    created_tasks = {}

    # tworzenie taskow
    for task_data in tasks_data:
        task, created = Task.objects.get_or_create(
            desc=task_data['desc'],
            defaults={'duration': task_data['duration']}
        )
        created_tasks[task_data['desc']] = task

    # poprzednicy
    for task_data in tasks_data:
        task = created_tasks[task_data['desc']]
        # desc do identyfikcacji, bo id sie nie nadpisuje
        predecessor_descs = task_data.get('predecessors', [])
        predecessor_tasks = [created_tasks[desc] for desc in predecessor_descs if desc in created_tasks]
        task.predecessors.set(predecessor_tasks)

    return Response({'status': 'Success', 'received_data': tasks_data})

@api_view(['GET'])
def calculate_critical_path(request):
    tasks = list(Task.objects.all())

    calculate_time_reserves(tasks)
    critical_path = find_critical_path(tasks)

    # Serializacja zadań do odpowiedzi JSON; upewnij się, że serializer jest zaktualizowany, aby obsługiwać odpowiednie pola
    serializer = TaskSerializer(tasks, many=True)
    return Response({
        'tasks': serializer.data,
        'critical_path': critical_path
    })


