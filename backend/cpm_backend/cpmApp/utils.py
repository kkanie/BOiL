
def find_start_activity(tasks):
    print(tasks)
    result = {
        'status': False,
        'startId': 0,
        'endId': 0,
        'error': ''
    }

    start_ids = []
    end_ids = []

    for task in tasks:
        print(task.id, task.start_activity, task.end_activity)
        if task.start_activity not in start_ids:
            start_ids.append(task.start_activity)
        if task.end_activity not in end_ids:
            end_ids.append(task.end_activity)

    start_activities = [activity.id for activity in start_ids if activity not in end_ids]
    print('start_activites ', start_activities)
    end_activities = [activity.id for activity in end_ids if activity not in start_ids]
    print('end_activites ', end_activities)

    if not start_activities:
        result['error'] = 'Start activity not found'
    elif len(start_activities) == 1:
        result.update({'status': True, 'startId': start_activities[0]})
    else:
        result['error'] = 'More than one start activity'

    if not result['status']:
        return result

    if not end_activities:
        result['error'] = 'End activity not found'
    elif len(end_activities) == 1:
        result.update({'status': True, 'endId': end_activities[0]})
    else:
        result['error'] = 'More than one end activity'

    return result




def update_activity_times(activity):
    if activity.starting_tasks.exists():
        activity.ES = min(task.ES for task in activity.starting_tasks.all())
        activity.EF = activity.ES + max(int(task.duration) for task in activity.starting_tasks.all())
    if activity.ending_tasks.exists():
        activity.LF = max(task.LF for task in activity.ending_tasks.all())
        activity.LS = activity.LF - max(int(task.duration) for task in activity.ending_tasks.all())
    activity.slack = activity.LF - activity.EF
    activity.is_critical = (activity.slack == 0)
    activity.save()

def calculate_task_times(task):
    if task.start_activity:
        task.ES = task.start_activity.ES
    if task.end_activity:
        task.EF = task.ES + int(task.duration)
        task.end_activity.ES = task.EF
        task.end_activity.save()
    task.LS = task.end_activity.LS
    task.LF = task.LS + int(task.duration)
    task.slack = task.LF - task.EF
    task.save()

