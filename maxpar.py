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
        return self.precedence.get(nomTache, [])

    def runSeq(self):
        pass

    def run():
        pass

def runT1():
    global X
    X = X

def runT2():
    global Y
    Y = 2

def runTsomme():
    global X, Y, Z
    Z = X + Y

