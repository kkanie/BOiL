from .models import Task
from collections import defaultdict

def calculate_time_reserves(tasks, predecessors):
    if not tasks:
        return []


    # inicjalizacja ES i EF
    for t in tasks:

        for pre_id in predecessors.get(t.id, []):
            pre = next((task for task in tasks if task.id == pre_id), None)
            if pre and t.ES < pre.EF:
                t.ES = pre.EF
        t.EF = t.ES + int(t.duration)
        t.save()

    # ustalenie maksymalnego EF jako LF dla zadań końcowych
    latest_finish = max(t.EF for t in tasks)

    # inicjalizacja LF i LS dla wszystkich zadań
    for t in tasks:
        t.LF = latest_finish
        t.LS = t.LF - int(t.duration)
        t.save()

    # najpozniejsze
    for t in reversed(tasks):
        for pre_id in predecessors.get(t.id, []):
            pre = next((task for task in tasks if task.id == pre_id), None)
            if pre and pre.LF > t.LS:
                pre.LF = t.LS
                pre.LS = pre.LF - int(pre.duration)
                pre.save()

    # obliczenie slacka dla każdego zadania
    for t in tasks:
        t.computeSlack()

def convert_successors_to_predecessors_format(tasks):
    task_dict = {task.id: task for task in tasks}
    predecessors = defaultdict(list)

    for task in tasks:
        if task.succ_left:
            predecessors[task.succ_left.id].append(task.id)
        if task.succ_right:
            predecessors[task.succ_right.id].append(task.id)

    return tasks, predecessors


def find_critical_path(tasks):
    # iteruje po taskach i zwraca sciezke krytyczna
    return [t.desc for t in tasks if t.critical == 'YES']