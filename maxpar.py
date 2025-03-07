import random
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import threading

class Task:
    def __init__(self, name, reads, writes, run_function):
        self.name = name
        self.reads = reads
        self.writes = writes
        self.run_function = run_function

    def run(self):
        self.run_function()

class TaskSystem:
    def __init__(self, tasks, precedence):
        self.tasks = tasks
        self.precedence = precedence
        self.validate_inputs()
        self.graph = self.build_graph()
        
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

    def validate_inputs(self):
        # Vérification des noms de tâches uniques
        task_names = [task.name for task in self.tasks]
        if len(task_names) != len(set(task_names)):
            raise ValueError("Les noms des tâches doivent être uniques")

        # Vérification de la cohérence des noms de tâches dans le graphe de précédence
        for task_name in self.precedence.keys():
            if task_name not in task_names:
                raise ValueError(
                    f"Le nom de tâche {task_name} dans le dictionnaire de précédence n'est pas dans la liste des tâches")

    def draw(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_size=2000,
                node_color="skyblue", font_size=10, font_weight="bold")
        plt.show()
    
    # Test randominsé de deterministe
    def detTestRn(self):
        num_tests = 1000
        for _ in range(num_tests):
            # Générer des valeurs aléatoires pour les variables X, Y et Z
            self.X = random.randint(1, 100)
            self.Y = random.randint(1, 100)
            self.Z = self.X + self.Y

            # Exécuter les tâches en parallèle avec le premier jeu de valeurs
            self.run()
            result1 = (self.X, self.Y, self.Z)

            # Réinitialiser les variables avec les mêmes valeurs aléatoires
            self.X = random.randint(1, 100)
            self.Y = random.randint(1, 100)
            self.Z = self.X + self.Y

            # Exécuter les tâches en parallèle avec le second jeu de valeurs
            self.run()
            result2 = (self.X, self.Y, self.Z)

            # Comparer les résultats des deux exécutions parallèles
            if result1 != result2:
                print("Le système n'est pas déterministe")
        print(f"Aucune indétermination détectée après {num_tests} tests")

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
    "T3": [],
    "Somme": ["T1", "T3"]
}

# Créer une instance de TaskSystem
task_system = TaskSystem(tasks=[t1, t2, tSomme], precedence=precedence)

# Construire le graphe de précédence
task_system.graph = task_system.build_graph()

# Afficher le graphe de précédence
task_system.draw()

# Exécuter les tâches en séquentiel
task_system.runSeq()

# Exécuter les tâches en parallèle
task_system.run()