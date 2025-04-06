from typing import List, Tuple
import numpy as np


class Graph:
    def __init__(self, n: int, aretes: List[List[int]], ordre: List[int]) -> None:
        """
        Crée un objet de type Graph
        n: Nombre de sommets
        aretes: Matrice d'adjacence du graphe
        """
        assert len(ordre) == n == len(aretes)
        assert np.sum(ordre) == (n*(n-1))/2
        for row in aretes:
            assert len(row) == n
        self.nb_sommets = n
        self.sommets = [i for i in range(n)]
         # On défini les arêtes par une matrice d'adjacence (adjacence[0][9] == 1 s'il existe une arête entre 0 et 9, 0 sinon)
        self.adjacence = aretes
        self.ordre = ordre  # Liste des sommets dans l'ordre du début de leur intervalle t (les sommets vont de 0 à n-1)


    def coloriage_glouton_intervalles(self) -> None:
        """
        Implémente l'algorithme glouton du TP: trie les sommets selon l'ordre donné
        et applique un coloriage en assignant à chaque sommet la plus petite couleur
        non utilisée par ses voisins déjà colorés.
        """
        def disponible(couleur: int, sommet: int, coloriage: dict[int: int], aretes: List[List[int]]) -> bool:
            """
            Renvoie True si la couleur est disponible pour le sommet donné, False sinon
            couleur: La couleur à tester
            sommet: Le sommet à tester
            coloriage: Le coloriage actuel
            aretes: La matrice d'adjacence du graphe
            """
            for i, s in enumerate(aretes[sommet]):  # i représente le sommet, s la valeur dans la matrice d'adjacence entre sommet et i
                if s == 1:  # Pour chaque sommet, s'il y a une arête, on vérifie sa couleur
                    if coloriage[i] == couleur:  
                        return False  # Si la couleur est utilisée par le sommet i adjacent à notre sommet, on ne l'utilise pas
            return True  # La couleur est libre
            
        sommets_tries = self.ordre
        couleurs = [0]
        coloriage = {i: -1 for i in sommets_tries}
        for sommet in sommets_tries:  # On prend chaque sommet dans l'ordre croissant du début d'intervalle
            for couleur in couleurs:  # On prend chaque couleur dans la liste
                if disponible(couleur, sommet, coloriage, self.adjacence):
                    coloriage[sommet] = couleur  # Si la couleur est disponible, on colorie le sommet et passe au suivant
                    break
            # Si le sommet n'a pas été colorié, on crée une nouvelle couleur
            if coloriage[sommet] == -1:
                couleurs.append(couleurs[-1]+1)  # Ajout d'une nouvelle couleur
                coloriage[sommet] = couleurs[-1]
        
        print(f"Nombre de couleurs nécessaires: {len(couleurs)}")  # Affiche le nombre de couleurs
        print(f"Coloriage: {coloriage}")  # Affiche le plus grand coloriage possible sans dépasser k-couleurs (et avec le minimum de couleurs possibles)


class Intervalles:
    def __init__(self, n: int, inter: List[Tuple[int]]) -> None:
        """
        Crée un objet de type intervalle
        n: Nombre de variables
        inter: Liste des intervalles, qui sont des tuples avec un début et une fin
        """
        assert len(inter) == n
        for i in inter:
            assert len(i) == 2
        self.nb_variables = n
        self.variables = inter  # Exemple [(1, 2), (2, 4), (3, 6)], Liste des variables avec leur intervalle
        self.ordre = self.make_ordre()


    def make_ordre(self) -> np.array[int]:
        """
        Défini l'ordre des variables dans l'ordre croissant, c'est-à-dire
        classées par ordre croissant de leur instant de début
        """
        # On trie les indices des variables (0 à n-1) selon la date de début
        return np.array(sorted(range(self.nb_variables), key=lambda i: self.variables[i][0]))
    

    def make_adj(self) -> np.array[np.array[int]]:
        """
        Fait la matrice d'adjacence de l'objet Intervalles
        """
        adj = np.array([np.array([0 for _ in range(self.nb_variables)]) for _ in range(self.nb_variables)])
        for i in range(self.nb_variables):
            for j in range(i + 1, self.nb_variables):
                start_i, end_i = self.variables[i]  # Intervalle i
                start_j, end_j = self.variables[j]  # Intervalle j
                if max(start_i, start_j) <= min(end_i, end_j): # Vérifie l'intersection des deux intervalles
                    adj[i][j], adj[j][i] = 1, 1
        return adj


    def make_graph(self) -> Graph:
        """
        Fait le graphe lié à l'objet Intervalles
        """
        g =  Graph(self.nb_variables, self.make_adj(), self.ordre)
        return g


g1 = Graph(7, np.array([np.array([0, 1, 1, 0, 0, 0, 0]),  # Graphe de l'exemple du TP fait à la main
                        np.array([1, 0, 1, 1, 0, 0, 0]),
                        np.array([1, 1, 0, 1, 1, 0, 0]),
                        np.array([0, 1, 1, 0, 0, 0, 0]),
                        np.array([0, 0, 1, 0, 0, 1, 1]),
                        np.array([0, 0, 0, 0, 1, 0, 1]),
                        np.array([0, 0, 0, 0, 1, 1, 0]),]),
                        np.array([0, 1, 2, 3, 4, 5, 6]))  # Liste d'ordre (celle de l'exemple ici)

exemple = [(1, 4), (2, 6), (3, 9), (5, 7), (8, 12), (10, 13), (11, 14)]
i = Intervalles(7, exemple)  # Exemple du TP
g = i.make_graph()  # Graphe de l'exemple du TP fait par le programme

# Pour vérifier que les deux graphes sont bien les mêmes et donc que notre code pour Intervalles est bon
flag = True
for i in range(g.nb_sommets):
    for j in range(g.nb_sommets):
        if g.adjacence[i][j] != g1.adjacence[i][j]:
            flag = False
            break
print(g.nb_sommets == g1.nb_sommets and any(g.ordre) == any(g1.ordre) and flag)

g.coloriage_glouton_intervalles()
    