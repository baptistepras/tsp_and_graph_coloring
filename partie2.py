from typing import List, Tuple
import numpy as np
from copy import deepcopy
import random


class Graph:
    def __init__(self, n: int, aretes: List[List[int]]) -> None:
        """
        Crée un objet de type Graph
        n: Nombre de sommets
        aretes: Matrice d'adjacence du graphe
        """
        self.nb_sommets = n
        self.sommets = [i for i in range(n)]
        # On défini les arêtes par une matrice d'adjacence (adjacence[0][9] == x s'il existe une arête de poids x entre 0 et 9, 0 sinon)
        self.adjacence = aretes


    def naive_complet(self):
        """
        Résout de manière naïve le problème du Voyageur avec SLPP
        Ne marche que sur les graphes complets et connexes
        """
        visites = {i: False for i in range(self.nb_sommets)}
        visites[0] = True  # On commence au sommet 0
        chemin = [0]
        cout = 0
        sommet_actuel = 0

        for _ in range(self.nb_sommets - 1):
            # On choisit le chemin vers un autre sommet non visité avec la distance minimale
            min_dist = np.inf
            s_min = -1
            for i, dist in enumerate(self.adjacence[sommet_actuel]):  
                if not visites[i] and dist > 0 and dist < min_dist:
                    min_dist = dist
                    s_min = i
            chemin.append(s_min)
            cout += min_dist
            visites[s_min] = True
            sommet_actuel = s_min

        # Retour à l'origine
        cout += self.adjacence[sommet_actuel][0]
        chemin.append(0)
    
        return chemin, cout
    

    def naive_non_complet(self):
        """
        Résout de manière naïve le problème du Voyageur sur un graphe non-complet en trouvant le premier chemin possible
        Ne marche que sur les graphes connexes
        """
        def helper(sommet_actuel: int, visites: dict[int: int], chemin: List[int], cout_actuel: int):
            """
            Sous-fonction pour réaliser le backtracking
            sommet_actuel: Le sommet sur lequel on se trouve
            visites: Le dictionnaire des sommets visités, False si pas visité, True sinon
            chemin: La liste des sommets visités jusqu'à ici, dans l'ordre
            cout_actuel: Le coût actuel du chemin
            """
            if len(chemin) == self.nb_sommets:  # On a fait tous les sommets donc on vérifie si on peut revenir au départ
                retour = self.adjacence[sommet_actuel][0]
                if retour > 0:  # Il existe un chemin qui va du sommet actuel à l'origine
                    return chemin + [0], cout_actuel + retour
                else:
                    return None, np.inf

            # On choisit le premier chemin possible vers un autre sommet non visité
            for i, dist in enumerate(self.adjacence[sommet_actuel]):
                if not visites[i] and dist > 0:
                    visites[i] = True
                    chemin.append(i)
                    chemin_retour, cout_retour = helper(i, visites, chemin, cout_actuel + dist)
                    if chemin_retour is not None:  # On a trouvé un chemin
                        return chemin_retour, cout_retour
                    # Backtrack si l'on n'a pas trouvé de chemin
                    visites[i] = False
                    chemin.pop()

            return None, np.inf

        visites = {i: False for i in range(self.nb_sommets)}
        visites[0] = True
        chemin, cout = helper(0, visites, [0], 0)

        if chemin is None:  # Si aucun chemin n'existe (la graphe est potentiellement non-connexe)
            print("Aucun chemin trouvé")
        return chemin, cout
    

    def inversion(self):
        """
        Résout avec une descente par inversion de sous-tours le problème du Voyageur
        Ne marche que sur les graphes connexes
        """
        chemin, cout = self.naive_non_complet()
        if chemin is None:
            print("Pas de chemin initial, impossible d'appliquer l'inversion.")
            return None, np.inf

        def calcul_cout(chemin):
            """
            Calcule le coût d'un chemin
            chemin: Le chemin actuel
            """
            total = 0
            for i in range(len(chemin) - 1):
                a, b = chemin[i], chemin[i + 1]
                dist = self.adjacence[a][b]
                if dist == 0:  # S'il n'y a pas d’arête entre deux sommets
                    return np.inf  # Le chemin est impossible
                total += dist
            return total

        amelioration = True
        while amelioration:  # Tant qu'une inversion améliore le coût
            amelioration = False
            meilleur_gain = 0
            meilleur_chemin = chemin

            for i in range(1, self.nb_sommets - 1):
                for j in range(i + 1, self.nb_sommets):
                    # On inverse les sommets i et j
                    nouveau_chemin = deepcopy(chemin)  # Crée un nouveau chemin sans toucher le chemin actuel
                    nouveau_chemin[i:j+1] = reversed(nouveau_chemin[i:j+1])  # Fait l'inversion
                    nouveau_cout = calcul_cout(nouveau_chemin)
                    gain = cout - nouveau_cout  # = -inf si le chemin est impossible
                    if gain > meilleur_gain:  # Si le chemin est possible et meilleur
                        meilleur_gain = gain
                        meilleur_chemin = nouveau_chemin
                        amelioration = True

            if amelioration:  # On a un chemin qui a amélioré le coût, on va continuer avec ce dernier
                chemin = meilleur_chemin
                cout = calcul_cout(chemin)

        return chemin, cout
    


    def recuit_simule(self, T_init=1000, alpha=0.995, max_iter=1000):
        """
        Résout le problème du TSP avec recuit simulé.
        Ne marche que sur les graphes connexes.
        T_init: Température initiale
        alpha: Facteur de décroissance de la température
        max_iter: Nombre d’itérations à faire au total
        """
        chemin, cout = self.naive_non_complet()
        if chemin is None:
            print("Pas de chemin initial, impossible d'appliquer le recuit simulé.")
            return None, np.inf

        def calcul_cout(chemin):
            """
            Calcule le coût d'un chemin
            chemin: Le chemin actuel
            """
            total = 0
            for i in range(len(chemin) - 1):
                a, b = chemin[i], chemin[i + 1]
                dist = self.adjacence[a][b]
                if dist == 0:  # S'il n'y a pas d’arête entre deux sommets
                    return np.inf  # Le chemin est impossible
                total += dist
            return total

        def voisin(chemin):
            """
            Génère une solution voisine de la solution actuelle
            chemin: Le chemin actuel
            """
            i, j = sorted(random.sample(range(1, self.nb_sommets), 2))  # On ne bouge pas le sommet de départ (0)
            new_chemin = chemin[:]
            new_chemin[i:j+1] = reversed(new_chemin[i:j+1])  # Inverse i et j
            return new_chemin

        T = T_init
        meilleur_chemin = chemin[:]
        meilleur_cout = cout
        current_chemin = chemin[:]
        current_cout = cout

        # On fait autant d'itérations que demandées 
        for _ in range(max_iter):
            candidat = voisin(current_chemin)  # Choisit un nouveau voisin
            candidat_cout = calcul_cout(candidat)  # Si c'est un chemin impossible, le coût est inf
            delta = candidat_cout - current_cout  # Si la solution est meilleure, c'est négatif

            if delta < 0 or random.random() < np.exp(-delta / T):  # Si la solution est meilleure, ou si elle est acceptée
                current_chemin = candidat
                current_cout = candidat_cout
                if current_cout < meilleur_cout:  # On sauvegarde le meilleur chemin possible
                    meilleur_chemin = current_chemin
                    meilleur_cout = current_cout
            T *= alpha  # On réduit T à chaque itération pour accepter de moins en moins de mouvement

        return meilleur_chemin, meilleur_cout
            

g_complet = Graph(4, np.array([np.array([0, 10, 8, 9]),  
                               np.array([10, 0, 7, 11]),  
                               np.array([8, 7, 0, 12]),  
                               np.array([9, 11, 12, 0])]))
g_non_complet = Graph(7, np.array([np.array([0, 12, 10, 0, 0, 0, 12]),
                       np.array([12, 0, 8, 12, 0, 0, 0]),
                       np.array([10, 8, 0, 11, 3, 0, 9]),
                       np.array([0, 12, 11, 0, 11, 10, 0]),
                       np.array([0, 0, 3, 11, 0, 6, 7]),
                       np.array([0, 0, 0, 10, 6, 0, 9]),
                       np.array([12, 0, 9, 0, 7, 9, 0])]))
# print(g.sommets)
# print(g.adjacence)
# print(g.degres)
print(f"g_complet sur naive_complet(): {g_complet.naive_complet()}")
print(f"g_non_complet sur naive_non_complet(): {g_non_complet.naive_non_complet()}")
print(f"g_complet sur naive_non_complet(): {g_complet.naive_non_complet()}")
print(f"g_non_complet sur inversion(): {g_non_complet.inversion()}")
print(f"g_non_complet sur recuit_simule(): {g_non_complet.recuit_simule(10, alpha=0.995, max_iter=1000)}")


