# Code to check if a directed graph is a DAG using DFS

class Graph:
    def __init__(self, edges, n):
        # Create adjacency list
        self.adjList = [[] for _ in range(n)]

        # Add edges
        for src, dest in edges:
            self.adjList[src].append(dest)


# DFS function
def DFS(graph, v, discovered, departure, time):
    # Mark current node as discovered
    discovered[v] = True

    # Visit all adjacent vertices
    for u in graph.adjList[v]:
        if not discovered[u]:
            time = DFS(graph, u, discovered, departure, time)

    # Set departure time
    departure[v] = time
    return time + 1


# Function to check if graph is DAG
def isDAG(graph, n):
    discovered = [False] * n
    departure = [-1] * n

    time = 0

    # Perform DFS for all nodes
    for i in range(n):
        if not discovered[i]:
            time = DFS(graph, i, discovered, departure, time)

    # Check for back edges
    for u in range(n):
        for v in graph.adjList[u]:
            if departure[u] <= departure[v]:
                return False

    return True


# Main function
if __name__ == '__main__':
    edges = [
        (0, 1), (0, 3), (1, 2), (1, 3),
        (3, 2), (3, 4), (3, 0),  # cycle here
        (5, 6), (6, 3)
    ]

    n = 7

    graph = Graph(edges, n)

    if isDAG(graph, n):
        print("The graph is a DAG")
    else:
        print("The graph is NOT a DAG")
