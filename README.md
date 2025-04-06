# TPS and Graph Coloring

This small project implements various algorithms related to graph theory, focusing on two main areas:
	•	Graph Coloring: Welsh and Powell method to assign colors to graph nodes such that no adjacent nodes share the same color. These algorithms are useful in scheduling, register allocation, and network conflict resolution.
	•	Travelling Salesman Problem (TSP): Heuristics and optimization methods to find the shortest possible route visiting each node exactly once and returning to the starting point.

# How to use ?

The file `TSP.py` implements various heuristics to efficiently approximate solutions to any TSP problem.

The file `register.py` implements an algorithm to efficiently approximate a solution for register allocation, using graph coloring and being usable either with a graph structure or an interval structure.

The file `welsh_powell.py` implements the Welsh-Powell algorithm for graph coloring. It uses a graph structure and returns True along with the graph coloring if the graph can be colored with k colors, or False otherwise, in which case it prints the largest possible partial coloring.
