#pojedyncze zadanie
class CritPathCalc(object):
    def __init__(self, desc, duration):
        self.desc = desc
        self.predecessors = []
        self.duration = duration
        self.ES = 0
        self.EF = duration
        self.LS = float('inf')
        self.LF = float('inf')
        self.slack = 0
        self.critical = ''

    #Slack = LF - EF lub Slack = LF - LS
    def computeSlack(self):
        self.slack = self.LF - self.EF
        if self.slack > 0:
            self.critical = 'NO'
        else:
            self.critical = 'YES'

    def add_pre(self, task):
        self.predecessors.append(task)

#wszystkie taski
class Tasks:
    def __init__(self):
        self.tasks = []

    #dodanie taska do listy taskow
    def add_task(self, t):
        self.tasks.append(t)
        print(t.desc)

    #sciezka krytyczna -> najwczesniejsze start i zakonczenia
    def calc_critical_path(self):
        if not self.tasks:  # Check if the list of tasks is empty
            print("No tasks to calculate a critical path for.")
            return []

        for t in self.tasks:
            for pre in t.predecessors:
                if t.ES < pre.EF:
                    t.ES = pre.EF
            t.EF = t.ES + t.duration

    #najpozniejsze zakonczenia - inicjalizacja
        latest_finish = max(t.EF for t in self.tasks)
        print(latest_finish)
        for t in self.tasks:
            t.LF = latest_finish
            t.LS = t.LF - t.duration

    #najpozniejsze
        for t in reversed(self.tasks):
            for pre in t.predecessors:
                # zaktualizuj tylko jesli nowy LF dla poprzednika jest mniejszy niz aktualny
                if pre.LF > t.LS:
                    pre.LF = t.LS
                    pre.LS = pre.LF - pre.duration



        print('TASK             ES         LS       EF         LF')
        for t in self.tasks:
            print(t.desc, '      ', t.ES, '      ', t.LS, '     ',t.EF, '      ',t.LF)
        for t in self.tasks:
            t.computeSlack()  # Compute slack and determine critical status

        critical_path = [t.desc for t in self.tasks if t.critical == 'YES']
        return critical_path

    def get_critical_path(self):
        return self.calc_critical_path()


def calculate_time_reserves(tasks):
    if not tasks:
        return []

    # inicjalizacja ES i EF
    for t in tasks:
        for pre in t.predecessors.all():
            if t.ES < pre.EF:
                t.ES = pre.EF
        t.EF = t.ES + t.duration
        t.save()
        print(f"Task {t.desc}: ES={t.ES}, EF={t.EF}")

    # ustalenie maksymalnego EF jako LF dla zadań końcowych
    latest_finish = max(t.EF for t in tasks)

    # Inicjalizacja LF i LS dla wszystkich zadań
    for t in tasks:
        print(t, t.duration, t.predecessors.all())
        t.LF = latest_finish
        t.LS = t.LF - t.duration
        t.save()


    # najpozniejsze
    for t in reversed(tasks):
        print(t, t.duration, t.predecessors.all())
        for pre in t.predecessors.all():
            print(pre.desc,pre.duration)
            # zaktualizuj tylko jesli nowy LF dla poprzednika jest mniejszy niz aktualny
            if pre.LF > t.LS:
                pre.LF = t.LS
                pre.LS = pre.LF - pre.duration
            pre.save()

    # obliczenie slacka dla każdego zadania i aktualizacja atrybutu krytycznego
    for t in tasks:
        t.computeSlack()

def find_critical_path(tasks):
    # iteruje po taskach i zwraca sciezke krytyczna
    return [t.desc for t in tasks if t.critical == 'YES']
