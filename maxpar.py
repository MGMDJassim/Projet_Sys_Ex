class Task:
    def __init__(self, name, reads, writes, run):
        self.name = name
        self.reads = reads 
        self.writes = writes
        self.run = run

class TaskSystem:
    def __init__(self, tasks, precedence):
        self.tasks = tasks
        self.precedence = precedence
        



    def getDependencies(self, nomTache):
        # retourne la liste des tâches qui doivent être exécuter avant nomTache
        return self.precedence.get(nomTache, [])

    def runSeq(self):
        # exécution séquentielle
        for t in self.tasks:
            t.run()
    

    def run(self):
        # exécution parallèle
        # initialisation des variables partagées
        for t in self.tasks:
            for r in t.reads:
                globals()[r] = None
            for w in t.writes:
                globals()[w] = None

# def runT1():
#     global X
#     X = X

# def runT2():
#     global Y
#     Y = 2

# def runTsomme():
#     global X, Y, Z
#     Z = X + Y

