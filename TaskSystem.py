import random
import time
from timeit import timeit
import matplotlib.pyplot as plt
import networkx as nx
import threading

class TaskSystem:
    def __init__(self, tasks, precedence):
        self.tasks = tasks
        self.precedence = precedence
        self.validate_inputs()
        self.graph = self.build_graph()

    def getDependencies(self, nomTache):
        """
        Retourne la liste des dépendances pour une tâche donnée.
        Si la tâche n'a pas de dépendances, retourne une liste vide.
        """
        if nomTache not in self.precedence:
            raise ValueError(f"La tâche '{nomTache}' n'existe pas dans le dictionnaire de précédence.")
        return self.precedence.get(nomTache, [])

    def runSeq(self):
        """
        Exécution en séquentiel des tâches.
        Chaque tâche est exécutée dans l'ordre défini par le dictionnaire de précédence.
        """
        for t in self.tasks:
            t.run()

    def run(self):
        task_dependencies = {task.name: self.getDependencies(task.name) for task in self.tasks}
        task_semaphores = {task.name: threading.Semaphore(0) for task in self.tasks}
    
        for task in self.tasks:
            if not task_dependencies[task.name]:
                task_semaphores[task.name].release()
    
        for task in self.tasks:
            for dep in task_dependencies[task.name]:
                task_semaphores[dep].acquire()
    
            task.run()
    
            for t in self.tasks:
                if task.name in task_dependencies[t.name]:
                    task_semaphores[t.name].release()

    def build_graph(self):
        G = nx.DiGraph()
        for task in self.tasks:
            G.add_node(task.name)
            for dep in self.precedence.get(task.name, []):
                G.add_edge(dep, task.name)
        return G

    def validate_inputs(self):
        task_names = {task.name for task in self.tasks}
        if len(task_names) != len(self.tasks):
            raise ValueError("Noms de tâches en double")
        for task_name in self.precedence.keys():
            if task_name not in task_names:
                raise ValueError(f"Le nom de tâche {task_name} n'est pas dans le dictionnaire de précédence")

    def draw(self):
        G = self.graph
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold", width=2, edge_color="gray")
        plt.title("Graphe de précédence des tâches")
        plt.show()
    
    def detTestRnd(self):
        num_tests = 10
        for _ in range(num_tests):
            X = random.randint(1, 100)
            Y = random.randint(1, 100)
            Z = X + Y
            self.run()
            result1 = (X, Y, Z)
            X, Y, Z = result1
            Z = X + Y
            self.run()
            result2 = (X, Y, Z)
            if result1 != result2:
                print("Le système n'est pas déterministe")
                return
        print(f"Aucune indétermination détectée après {num_tests} tests")
    
    def parCost(self):
        num_runs = 100   # Nombre de fois où chaque exécution est réalisée
        seq_times = []  # Liste pour stocker les temps d'exécution en séquentiel
        par_times = []  # Liste pour stocker les temps d'exécution en parallèle

        # Mesurer les performances en séquentiel et en parallèle
        for _ in range(num_runs):
            # Mesurer le temps d'exécution en séquentiel
            start_time = time.perf_counter()
            self.runSeq()
            end_time = time.perf_counter()
            seq_times.append(end_time - start_time)

            # Mesurer le temps d'exécution en parallèle
            start_time = time.perf_counter()
            self.run()
            end_time = time.perf_counter()
            par_times.append(end_time - start_time)

        # Calculer le temps d'exécution moyen pour chaque méthode
        avg_seq_time = sum(seq_times) / num_runs
        avg_par_time = sum(par_times) / num_runs

        # Afficher les résultats
        print(f"Temps moyen en séquentiel après {num_runs} exécutions : {avg_seq_time:.6f} s")
        print(f"Temps moyen en parallèle après {num_runs} exécutions : {avg_par_time:.6f} s")
