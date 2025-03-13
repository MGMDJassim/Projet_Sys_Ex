import random
import time
import matplotlib.pyplot as plt
import networkx as nx
import threading

class TaskSystem:
    def __init__(self, tasks, precedence):
        self.tasks = tasks
        self.precedence = precedence
        self.validate_inputs()
        self.graph = self.build_graph()

    #Cette fonction retourne la liste des tâches qui doivent être exécutées avant la tâche 
    def getDependencies(self, nomTache):
        return list(self.precedence.get(nomTache, []))

    #Cette fonction exécute les tâches en séquentiel
    def runSeq(self):
        for t in self.tasks:
            t.run()
    
    #Cette fonction exécute les tâches en parallèle
    def run(self):
        # Obtient une liste ordonnée des tâches en suivant l'ordre topologique du graphe de précédence
        ordered_tasks = list(nx.topological_sort(self.graph))
        threads = []
        task_dict = {task.name: task for task in self.tasks}
        
        # Pour chaque tâche, créer un thread pour l'exécuter et l'ajouter à la liste de threads
        for task_name in ordered_tasks:
            task = task_dict.get(task_name)
            if task is None:
                raise ValueError(f"Tâche {task_name} non trouvée dans la liste des tâches")
            thread = threading.Thread(target=task.run)
            thread.start()
            threads.append(thread)
    
        # Attendre la fin de l'exécution de tous les threads
        for thread in threads:
            thread.join()

    # Cette fonction construit le graphe de précédence à partir des informations fournies
    def build_graph(self):
        G = nx.DiGraph()
        for task in self.tasks:
            G.add_node(task.name)
            for dep in self.precedence[task.name]:
                G.add_edge(dep, task.name)
        return G

    #Cette fonction vérifie la validité des entrées fournies pour le système de tâches
    def validate_inputs(self):
        # Vérification des noms de tâches uniques
        task_names = []
        for task in self.tasks:
            task_names.append(task.name)
        if len(task_names) != len(set(task_names)):
            raise ValueError("Noms de tâches en double")

        # Vérification de la précedence des tâches
        for task_name in self.precedence.keys():
            if task_name not in task_names:
                raise ValueError(
                    f"Le nom de tâche {task_name} n'est pas dans le dictionnaire de précédence")

    #Cette fonction dessine le graphe de précédence
    def draw(self):
        # Dessine le graphe de précédence
        G = self.graph
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold",
                width=2, edge_color="gray")
        plt.title("Graphe de précédence des tâches")
        plt.show()
    
    # Test randominsé de deterministe
    def detTestRnd(self):
        num_tests = 1000
        for _ in range(num_tests):
            # Générer des valeurs aléatoires pour les variables X, Y et Z
            X = random.randint(1, 100)
            Y = random.randint(1, 100)
            Z = X + Y

            # Exécuter les tâches en parallèle avec le premier jeu de valeurs
            self.run()
            result1 = (X, Y, Z)

            # Réinitialiser les variables avec les mêmes valeurs aléatoires
            X = random.randint(1, 100)
            Y = random.randint(1, 100)
            Z = X + Y

            # Exécuter les tâches en parallèle avec le second jeu de valeurs
            self.run()
            result2 = (X, Y, Z)

            # Comparer les résultats des deux exécutions parallèles
            if result1 != result2:
                print("Le système n'est pas déterministe")
                return
        print(f"Aucune indétermination détectée après {num_tests} tests")
    
    # Cette fonction compare les temps d'exécution en séquentiel et en parallèle
    def parCost(self):
        num_runs = 100  # Nombre de fois où chaque exécution est réalisée
        seq_times = []  # Liste pour stocker les temps d'exécution en séquentiel
        par_times = []  # Liste pour stocker les temps d'exécution en parallèle

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

        # Afficher les temps d'exécution moyens pour chaque méthode
        print(f"Temps d'exécution moyen en séquentiel : {avg_seq_time:.4f} s")
        print(f"Temps d'exécution moyen en parallèle : {avg_par_time:.4f} s")