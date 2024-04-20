from .models import Task

def calculate_time_reserves(tasks):
    if not tasks:
        return []

    # inicjalizacja ES i EF
    for t in tasks:
        #print(t.predecessors.all())
        for pre in t.predecessors.all():
            #print("w if ", t.ES, pre.EF, t.ES < pre.EF)
            if t.ES < pre.EF:
                t.ES = pre.EF
        t.EF = t.ES + t.duration
        t.save()
        #print(f"Task {t.desc}: ES={t.ES}, EF={t.EF}")

    # ustalenie maksymalnego EF jako LF dla zadań końcowych
    latest_finish = max(t.EF for t in tasks)

    # Inicjalizacja LF i LS dla wszystkich zadań
    for t in tasks:
        #print(t, t.duration, t.predecessors.all())
        t.LF = latest_finish
        t.LS = t.LF - t.duration
        t.save()
        #print(t.desc, 'Inicjalizacja: t.LF ', t.LF, 't.LS', t.LS)


    # najpozniejsze
    for t in reversed(tasks):
        #print(t, t.duration, t.predecessors.all())
        for pre in t.predecessors.all():
            #print(pre.desc, pre.duration)
            # zaktualizuj tylko jesli nowy LF dla poprzednika jest mniejszy niz aktualny
            pre.refresh_from_db()
            if pre.LF > t.LS:
                #print('W if ',pre.desc, pre.LF,t.desc, t.LS, pre.LF > t.LS)
                for task in tasks:
                    if task.desc == pre.desc:
                        task.LF = t.LS
                        task.LS = task.LF - task.duration
                pre.LF = t.LS
                pre.LS = pre.LF - pre.duration
                #print('Po zmianie ',pre.desc, pre.LS)
            pre.save()
        #print(t.desc, 'Obliczone: t.LF ', t.LF, ' t.LS', t.LS)

    # obliczenie slacka dla każdego zadania i aktualizacja atrybutu krytycznego
    for t in tasks:
        t.computeSlack()

    latest_finish = max(t.EF for t in tasks)
    end_task = Task(desc='End', duration=0, ES=latest_finish, EF=latest_finish)
    tasks.append(end_task)
    end_task.LF = end_task.EF
    end_task.LS = end_task.LF - end_task.duration
    end_task.save()

def find_critical_path(tasks):
    # iteruje po taskach i zwraca sciezke krytyczna
    return [t.desc for t in tasks if t.critical == 'YES']
