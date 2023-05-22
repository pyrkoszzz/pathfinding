import random
import math

class MazeAgent:
    def generateKruskal(self, vertices):
        return Kruskal(vertices).kruskalMST()
        

class MazeGraph:


    def __init__(self, vertices):
        self.V = vertices
        self.graph = []
        self.size = int(math.sqrt(vertices))

        it = 2* ((self.size - 1) * self.size)
        cntr = 0
        for _ in range(self.size):
            for _ in range(self.size - 1):
                self.addEdge(cntr, cntr + 1, random.randint(1, it))
                cntr += 1
            cntr += 1

        cntr = 0
        for _ in range((self.size - 1) * self.size):
            self.addEdge(cntr, cntr + self.size, random.randint(1, it))
            cntr += 1
 
    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])
 
    def find(self, parent, i):
        if parent[i] != i:
            parent[i] = self.find(parent, parent[i])
        return parent[i]
 
    def union(self, parent, rank, x, y):
        if rank[x] < rank[y]:
            parent[x] = y
        elif rank[x] > rank[y]:
            parent[y] = x
        else:
            parent[y] = x
            rank[x] += 1
 
class Kruskal(MazeGraph):


  def __init__(self, vertices):
      super().__init__(vertices)

  def kruskalMST(self):
    self.result = []
    i = 0
    e = 0
    self.graph = sorted(self.graph, key = lambda item: item[2])
    parent = []
    rank = []

    for node in range(self.V):
        parent.append(node)
        rank.append(0)

    while e < self.V - 1:
        u, v, w = self.graph[i]
        i = i + 1
        x = self.find(parent, u)
        y = self.find(parent, v)
        if x != y:
            e = e + 1
            self.result.append([u, v, w])
            self.union(parent, rank, x, y)
    
    n = int(math.sqrt(self.V))
    maze = []
    [maze.append([0 for _ in range(2 * n - 1)]) for _ in range(2 * n - 1)]

    for y in range(2 * n - 1):
        for x in range(2 * n - 1):
            if(not y % 2 and not x % 2):
                maze[y][x] = 1

    for u, v, w in self.result:
        maze[u // n + v // n][u % n + v % n] = 1
    return {"maze_arr": maze, "maze_graph": self.result}