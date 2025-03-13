from Task import *
from TaskSystem import *

def runT1():
    global X
    X = 1
def runT2():
    global Y
    Y = 2
def runTsomme():
    global X, Y, Z
    Z = X + Y

t1 = Task("T1", ["X"], [], runT1)
t2 = Task("T2", ["Y"], [], runT2)
tSomme = Task("Somme", ["X", "Y"], ["Z"], runTsomme)

precedence = {
    "T1": [],
    "T2": [],
    "Somme": ["T1", "T2"]
}

# Créer une instance de TaskSystem
task_system = TaskSystem(tasks=[t1, t2, tSomme], precedence=precedence)

# Afficher le graphe de précédence
task_system.parCost()

task_system.draw()