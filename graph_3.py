import numpy as np
import sys

class Graph:
    def __init__(self, file_path, file_type):
        self.file_path = file_path
        self.file_type = file_type
        self.graph = self.load_graph()

    def load_graph(self):
        if self.file_type == "-e":
            return self.load_list_of_edges()
        elif self.file_type == "-m":
            return self.load_adjacency_matrix()
        elif self.file_type == "-l":
            return self.load_adjacency_list()
        else:
            raise ValueError("Invalid file type")

    def load_adjacency_list(self):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        num_vertices = len(lines)
        matrix = np.zeros((num_vertices, num_vertices))
        matrix[:] = np.inf
        for i, line in enumerate(lines):
            neighbors = line.strip().split()
            for neighbor in neighbors:
                matrix[i, int(neighbor) - 1] = 1
        return matrix

    def load_adjacency_matrix(self):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        num_vertices = len(lines)
        matrix = np.zeros((num_vertices, num_vertices))
        matrix[:] = np.inf
        for i, line in enumerate(lines):
            row = line.strip().split()
            for j, value in enumerate(row):
                matrix[i, j] = int(value) if int(value) != 0 else np.inf
        return matrix

    def adjacency_matrix(self):
        return self.graph

    def load_list_of_edges(self):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
        num_vertices = 0
        edges = []
        for line in lines:
            values = line.strip().split()
            if len(values) == 2:
                vertex1, vertex2 = values
                weight = 1
            else:
                vertex1, vertex2, weight = values
            edges.append((int(vertex1), int(vertex2), int(weight)))
            num_vertices = max(num_vertices, int(vertex1), int(vertex2))
        matrix = np.zeros((num_vertices, num_vertices))
        matrix[:] = np.inf
        for edge in edges:
            vertex1, vertex2, weight = edge
            matrix[vertex1 - 1, vertex2 - 1] = weight
            matrix[vertex2 - 1, vertex1 - 1] = weight
        return matrix


    def list_of_edges(self, v):
        edges = []
        for i in range(self.graph.shape[0]):
            if self.graph[v - 1, i] != np.inf:
                edges.append((v, i + 1, self.graph[v - 1, i]))
        return edges
    
    def list_of_adjacency(self):
        adjacency_list = {}
        for vertex in range(1, self.graph.shape[0] + 1):
            neighbors = []
            for i in range(self.graph.shape[1]):
                if self.graph[vertex - 1, i] != np.inf:
                    neighbors.append(i + 1)
            adjacency_list[vertex] = neighbors
        return adjacency_list


    def is_directed(self):
        return not np.array_equal(self.graph.transpose(), self.graph)
    
    def find_bridges(self):
        num_vertices = self.graph.shape[0]
        visited = np.zeros(num_vertices, dtype=bool)
        discovery_time = np.zeros(num_vertices, dtype=int)
        low_time = np.zeros(num_vertices, dtype=int)
        parent = np.zeros(num_vertices, dtype=int)
        bridges = []

        def dfs(u):
            nonlocal time
            visited[u] = True
            discovery_time[u] = low_time[u] = time
            time += 1

            for v in range(num_vertices):
                if self.graph[u, v] != np.inf:
                    if not visited[v]:
                        parent[v] = u
                        dfs(v)
                        low_time[u] = min(low_time[u], low_time[v])
                        if low_time[v] > discovery_time[u]:
                            bridges.append((u + 1, v + 1))
                    elif v != parent[u]:
                        low_time[u] = min(low_time[u], discovery_time[v])

        time = 0
        for v in range(num_vertices):
            if not visited[v]:
                dfs(v)

        return bridges
    
    def find_cut_vertices(self):
        num_vertices = self.graph.shape[0]
        visited = np.zeros(num_vertices, dtype=bool)
        discovery_time = np.zeros(num_vertices, dtype=int)
        low_time = np.zeros(num_vertices, dtype=int)
        parent = np.zeros(num_vertices, dtype=int)
        is_cut_vertex = np.zeros(num_vertices, dtype=bool)
        cut_vertices = []

        def dfs(u, is_root):
            nonlocal time
            visited[u] = True
            discovery_time[u] = low_time[u] = time
            time += 1
            children = 0

            for v in range(num_vertices):
                if self.graph[u, v] != np.inf:
                    if not visited[v]:
                        parent[v] = u
                        children += 1
                        dfs(v, False)
                        low_time[u] = min(low_time[u], low_time[v])
                        if not is_root and low_time[v] >= discovery_time[u]:
                            is_cut_vertex[u] = True
                    elif v != parent[u]:
                        low_time[u] = min(low_time[u], discovery_time[v])

            if is_root and children > 1:
                is_cut_vertex[u] = True

        time = 0
        for v in range(num_vertices):
            if not visited[v]:
                dfs(v, True)

        for v in range(num_vertices):
            if is_cut_vertex[v]:
                cut_vertices.append(v + 1)

        return cut_vertices

print("Введите ключ параметра:")
print("-e: list_of edges, \n-m: matrix, \n-l: list_of_adjacency")

key = input()
if key not in ['-m', '-e', '-l']:
    print('Неверный тип ключа!')
    sys.exit()
print("Введите название файла (в текущем каталоге):")
file = input()
print('\n')

g = Graph(file, key)

adj_matrix = g.adjacency_matrix()
np.set_printoptions(threshold=np.inf)
np.set_printoptions(edgeitems=8, suppress=True)

print("Bridges:")
bridges = g.find_bridges()
print(bridges)

print("\nCut vertices:")
cut_vertices = g.find_cut_vertices()
print(cut_vertices)




# Запись результатов в файл
with open("output.txt", 'w') as file:
    file.write("Adjacency matrix:\n")
    for row in adj_matrix:
        row_str = ' '.join(map(str, row))
        file.write(row_str + '\n')
    file.write('\n')



print("\nРезультаты записаны в файл output.txt")