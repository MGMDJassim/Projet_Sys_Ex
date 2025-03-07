import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import threading
import random
import time

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
        # retourne la liste des tâches qui doivent être exécuter avant la tâche
        return self.precedence.get(nomTache, [])

    def runSeq(self):
        # exécution séquentielle
        for t in self.tasks:
            t.run()
    
    def run(self):
        # Obtient une liste ordonnée des tâches en suivant l'ordre topologique du graphe de précédence
        ordered_tasks = list(nx.topological_sort(self.graph))
        threads = []
        # Pour chaque tâche, créer un thread pour l'exécuter et l'ajouter à la liste de threads
        for task_name in ordered_tasks:
            task = next(t for t in self.tasks if t.name == task_name)
            thread = threading.Thread(target=task.run)
            thread.start()
            threads.append(thread)

        # Attendre la fin de l'exécution de tous les threads
        for thread in threads:
            thread.join()

    # vérification les entrées des tâches
    def _valide_input(self):
        #détection des doublons
        task_names = set(self.tasks.keys())
        if len(task_names) != len(self.tasks):
            raise ValueError("Doublons dans les noms de tâches")
        
        #détection des dépendances avec des tâches inexistantes
        for t in self.tasks:
            for d in self.tasks[t].reads + self.tasks[t].writes:
                if d not in task_names:
                    raise ValueError(f"Tâche {t} dépend de tâche inexistante {d}")

    def build_graph(self):
        # Crée un graphe orienté vide
        G = nx.DiGraph()
        # Ajoute chaque tâche comme un nœud dans le graphe
        for task in self.tasks:
            G.add_node(task.name)
            # Pour chaque dépendance de la tâche, ajoute un arc dans le graphe
            for dep in self.precedence[task.name]:
                G.add_edge(dep, task.name)
        return G
    

    def draw(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=2000,
                node_color="skyblue", font_size=10, font_weight="bold")
        plt.show()



def runT1():
    global X
    X = X

def runT2():
    global Y
    Y = 2

def runTsomme():
    global X, Y, Z
    Z = X + Y

T1 = Task("T1", [], ["X"], runT1)
T2 = Task("T2", [], ["Y"], runT2)
Tsomme = Task("Tsomme", ["X", "Y"], ["Z"], runTsomme)

precedence = {
    "T1": [],
    "T2": [],
    "Tsomme": ["T1", "T2"]
}

# Créer une instance de TaskSystem
task_system = TaskSystem(tasks=[T1, T2, Tsomme], precedence=precedence)

# Construire le graphe de précédence
task_system.graph = task_system.build_graph()

# Afficher le graphe de précédence
task_system.draw()

# Exécuter les tâches en séquentiel
task_system.runSeq()

# Exécuter les tâches en parallèle
task_system.run()