import random
import time
import matplotlib.pyplot as plt
import networkx as nx
import threading
from timeit import timeit

class TaskSystem:
    def __init__(self, tasks, precedence):
        self.tasks = tasks
        self.precedence = precedence
        self.validate_inputs()

    def getDependencies(self, nomTache):
        return list(self.precedence.get(nomTache, []))

    def runSeq(self):
        for t in self.tasks:
            t.run()
            time.sleep(0.1)

    def run(self):
        # Création d'un sémaphore pour chaque tâche, initialisé à 0
        task_semaphores = {task.name: threading.Semaphore(0) for task in self.tasks}

        # Initialisation des sémaphores pour les tâches sans dépendances
        for task in self.tasks:
            if not self.getDependencies(task.name):
                task_semaphores[task.name].release()

        # Exécution des tâches en respectant les dépendances
        for task in self.tasks:
            # Attendre que toutes les dépendances soient terminées
            for dep in self.getDependencies(task.name):
                task_semaphores[dep].acquire()

            # Exécuter la tâche
            task.run()
            time.sleep(0.1)

            # Libérer les sémaphores des tâches dépendantes
            for t in self.tasks:
                if task.name in self.getDependencies(t.name):
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
        num_runs = 10   # Nombre de fois où chaque exécution est réalisée
        seq_times = []  # Liste pour stocker les temps d'exécution en séquentiel
        par_times = []  # Liste pour stocker les temps d'exécution en parallèle

        # Mesurer les performances
        print("Début des mesures de performances...")
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
        print(f"Temps moyen en séquentiel après {num_runs} exécutions : {avg_seq_time:.4f} s")
        print(f"Temps moyen en parallèle après {num_runs} exécutions : {avg_par_time:.4f} s")