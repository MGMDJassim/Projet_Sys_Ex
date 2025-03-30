from Task import *
from TaskSystem import *
import cProfile

X = None
Y = None
Z = None
def runT1():
    global X
    X = 1
def runT2():
    global Y
    Y = 2
def runTsomme():
    global X, Y, Z
    Z = X + Y

t1 = Task(name="T1", writes=["X"], run=runT1)
t2 = Task(name="T2", writes=["Y"], run=runT2)
tSomme = Task(name="Somme", reads=["X", "Y"], writes=["Z"], run=runTsomme)

precedence_parallele = {
    "T1": [],
    "T2": [],
    "Somme": ["T1", "T2"]
}
# Créer une instance de TaskSystem
task_system = TaskSystem(tasks=[t1, t2, tSomme], precedence=precedence_parallele)
task_system.parCost()
