import random
import math

class MazeAgent:


	def __init__(self, app_instance):
		self.app = app_instance
		self.maze = None
		self.graph = None
		self.maze_size = 144
		self.done = False
		self.steps_cntr = 0
		self.obj = None

	def initializeKruskal(self):
		self.obj = Kruskal(self.maze_size, self)
		self.maze, self.graph = self.obj.generateMazeArray()
		self.app.status = "Maze generation using Kruskal's algo started"
		self.steps_cntr = 0
		self.done = False

	def nextStep(self):
		if not self.done and self.obj != None:
			self.maze, self.graph =  self.obj.kruskalMSTStep()

	def fastForward(self):
		if self.obj != None:
			while not self.done:
				self.maze, self.graph =  self.obj.kruskalMSTStep()

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


	def __init__(self, vertices, maze_agent):
		super().__init__(vertices)
		self.result = []
		self.i = 0
		self.e = 0
		self.graph = sorted(self.graph, key = lambda item: item[2])
		self.parent = []
		self.rank = []
		self.maze_agent = maze_agent

		for node in range(self.V):
			self.parent.append(node)
			self.rank.append(0)

	def kruskalMSTStep(self):
		if self.e < self.V - 1:
			u, v, w = self.graph[self.i]
			self.i += 1
			x = self.find(self.parent, u)
			y = self.find(self.parent, v)
			if x != y:
				self.maze_agent.steps_cntr += 1
				self.maze_agent.app.status = "Generating maze - steps: " + str(self.maze_agent.steps_cntr)
				self.e += 1
				self.result.append([u, v, w])
				self.union(self.parent, self.rank, x, y)
				return self.generateMazeArray()
			else:
				self.kruskalMSTStep()
		if self.e >= self.V - 1:
			self.maze_agent.done = True
			self.maze_agent.app.status = "Maze generated successfuly"
		return self.generateMazeArray()
	
	def generateMazeArray(self):
		n = int(math.sqrt(self.V))
		maze = []
		[maze.append([0 for _ in range(2 * n - 1)]) for _ in range(2 * n - 1)]

		for y in range(2 * n - 1):
			for x in range(2 * n - 1):
				if(not y % 2 and not x % 2):
					maze[y][x] = 1

		for u, v, w in self.result:
			maze[u // n + v // n][u % n + v % n] = 1
		return maze, self.result