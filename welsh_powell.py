from typing import List, Tuple
import numpy as np


class Graph:
    def __init__(self, n: int, aretes: List[List[int]]) -> None:
        """
        Crée un objet de type Graph
        n: Nombre de sommets
        aretes: Matrice d'adjacence du graphe
        """
        self.nb_sommets = n
        self.sommets = [i for i in range(n)]
         # On défini les arêtes par une matrice d'adjacence (adjacence[0][9] == 1 s'il existe une arête entre 0 et 9, 0 sinon)
        self.adjacence = aretes
        self.degres = [np.sum(aretes[i]) for i in range(n)]


    def coloriage(self, k: int) -> bool:
        """
        Renvoie True si le graphe est K-coloriable, False sinon
        Affiche également le meilleur coloriage en utilisant au plus k-couleurs
        k: Nombre de couleurs maximales pouvant être utilisées
        """
        # On trie les sommets par ordre décroissant par rapport à leur degré
        sommets_tries = sorted(self.sommets, key = lambda i : self.degres[i], reverse=True)
        
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
                
        # Maintenant, on colorie chaque sommet avec la première couleur disponible
        # Une couleur est disponible si le sommet à colorier ne touche pas d'autre sommet de cette couleur
        couleurs = [0]
        coloriage = {i: -1 for i in sommets_tries}
        for sommet in sommets_tries:  # On prend chaque sommet dans l'ordre décroissant de leur degré
            for couleur in couleurs:  # On prend chaque couleur dans la liste
                if disponible(couleur, sommet, coloriage, self.adjacence):
                    coloriage[sommet] = couleur  # Si la couleur est disponible, on colorie le sommet et passe au suivant
                    break
            # Si le sommet n'a pas été colorié, on crée une nouvelle couleur si et seulement si on n'a pas déjà k couleurs
            if coloriage[sommet] == -1 and len(couleurs) < k:  
                couleurs.append(couleurs[-1]+1)  # Ajout d'une nouvelle couleur
                coloriage[sommet] = couleurs[-1]
        
        print(f"Nombre de couleurs nécessaires: {len(couleurs)}")  # Affiche le nombre de couleurs
        print(f"Coloriage: {coloriage}")  # Affiche le plus grand coloriage possible sans dépasser k-couleurs (et avec le minimum de couleurs possibles)
        return len(couleurs) <= k


g = Graph(9, np.array([np.array([0, 0, 1, 1, 0, 1, 0, 0, 1]),
                        np.array([0, 0, 1, 0, 1, 0, 1, 1, 0]),
                        np.array([1, 1, 0, 1, 1, 1, 1, 0, 0]),
                        np.array([1, 0, 1, 0, 0, 0, 1, 0, 0]),
                        np.array([0, 1, 1, 0, 0, 1, 0, 0, 0]),
                        np.array([1, 0, 1, 0, 1, 0, 0, 0, 0]),
                        np.array([0, 1, 1, 1, 0, 0, 0, 0, 0]),
                        np.array([0, 1, 0, 0, 0, 0, 0, 0, 0]),
                        np.array([1, 0, 0, 0, 0, 0, 0, 0, 0])]))
# print(g.sommets)
# print(g.adjacence)
# print(g.degres)
print("Avec k=4")
print(g.coloriage(4))


    
