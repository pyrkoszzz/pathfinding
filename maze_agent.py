import random
import math
import sys

class MazeAgent:


	def __init__(self, app_instance):
		self.app = app_instance
		self.maze = None
		self.graph = None
		self.maze_size = 25
		self.done = False
		self.steps_cntr = 0
		self.obj = None

	def initializeKruskal(self):
		self.obj = Kruskal(self.maze_size, self)
		self.maze, self.graph = self.obj.generateMazeArray()
		self.app.state_agent.log = "Maze generation using Kruskal's algo started"
		self.app.state_agent.updateState("generating")
		self.steps_cntr = 0
		self.done = False

	def initializePrim(self):
		self.obj = Prim(self.maze_size, self)
		self.maze, self.graph = self.obj.generateMazeArray()
		self.app.state_agent.log = "Maze generation using Prim's algo started"
		self.app.state_agent.updateState("generating")
		self.steps_cntr = 0
		self.done = False

	def nextStep(self):
		if not self.done and self.obj != None:
			self.maze, self.graph =  self.obj.nextStep()
		else:
			self.obj = None

	def fastForward(self):
		if self.obj != None:
			if not self.done:
				self.maze, self.graph =  self.obj.nextStep()
			else:
				self.app.event_agent.action = None
	
	def importMaze(self, f):
		self.maze_size = int(f.readline())
		self.done = False
		self.obj = MazeImporter(f, self.maze_size, self)
		self.maze, self.graph = self.obj.generateMazeArray()
		self.obj = None


class MazeGraph:


	def __init__(self, vertices):
		self.V = vertices
		self.graph = []
		self.size = int(math.sqrt(vertices))
		print(self.__class__.__name__)
		if self.__class__.__name__ == "Kruskal":
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
		
		elif self.__class__.__name__ == "Prim":
			self.graph = [[] for _ in range(self.V)]
			it = 2* ((self.size - 1) * self.size)
			cntr = 0
			for _ in range(self.size):
				for _ in range(self.size - 1):
					self.addEdgeAdj(cntr, cntr + 1, random.randint(1, it))
					cntr += 1
				cntr += 1

			cntr = 0
			for _ in range((self.size - 1) * self.size):
				self.addEdgeAdj(cntr, cntr + self.size, random.randint(1, it))
				cntr += 1
	
	def addEdgeAdj(self, u, v, w):
		self.graph[u].append((v, w))
		self.graph[v].append((u, w))

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

	def printArr(parent, n):
			for i in range(1, n):
				print("% d - % d" % (parent[i], i))
 
class MazeImporter(MazeGraph):


	def __init__(self, f, vertices, maze_agent):
		super().__init__(vertices)
		self.result = []
		self.maze_agent = maze_agent

		for line in f:
			u,v,w = line.split()
			self.result.append([int(u), int(v), int(w)])
		self.done = True
		self.maze_agent.app.state_agent.log = "Maze imported successfuly"
		self.maze_agent.app.state_agent.updateState("generated")

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

	def nextStep(self):
		if self.e < self.V - 1:
			u, v, w = self.graph[self.i]
			self.i += 1
			x = self.find(self.parent, u)
			y = self.find(self.parent, v)
			if x != y:
				self.maze_agent.steps_cntr += 1
				self.maze_agent.app.state_agent.log = "Generating maze - steps: " + str(self.maze_agent.steps_cntr)
				self.e += 1
				self.result.append([u, v, w])
				self.union(self.parent, self.rank, x, y)
				return self.generateMazeArray()
			else:
				self.nextStep()
		if self.e >= self.V - 1:
			self.maze_agent.done = True
			self.maze_agent.app.state_agent.log = "Maze generated successfuly"
			self.maze_agent.app.state_agent.updateState("generated")
		return self.generateMazeArray()

class Prim(MazeGraph):


	def __init__(self, vertices, maze_agent):
		super().__init__(vertices)
		self.result = []
		self.maze_agent = maze_agent
		self.num_nodes = len(self.graph)
		self.selected = [False] * self.num_nodes  # Track which nodes are included in the minimum spanning tree
		self.selected[0] = True  # Start with the first node
		self.e = 0
		# Initialize arrays to track the minimum weights and corresponding edges for each node
		self.min_weights = [sys.maxsize] * self.num_nodes
		self.min_weights[0] = 0
		self.min_edges = [None] * self.num_nodes	

	def nextStep(self):
		if self.e in range(self.num_nodes - 1):
				self.e += 1
				min_weight = sys.maxsize
				min_node = 0

				# Find the node with the minimum weight that is not yet self.selected
				for node in range(self.num_nodes):
						if not self.selected[node] and self.min_weights[node] < min_weight:
								min_weight = self.min_weights[node]
								min_node = node

				self.selected[min_node] = True  # Include the self.selected node in the minimum spanning tree

				# Update the minimum weights and corresponding edges for the neighboring nodes
				for neighbor, weight in self.graph[min_node]:
						if not self.selected[neighbor] and weight < self.min_weights[neighbor]:
								self.min_weights[neighbor] = weight
								self.min_edges[neighbor] = (min_node, neighbor)
				self.maze_agent.steps_cntr += 1
				self.maze_agent.app.state_agent.log = "Generating maze - steps: " + str(self.maze_agent.steps_cntr)
			# Build the minimum spanning tree
		else:
			self.maze_agent.done = True
			self.maze_agent.app.state_agent.log = "Maze generated successfuly"
			self.maze_agent.app.state_agent.updateState("generated")
		
		minimum_spanning_tree = []
		for node in self.min_edges:
			if node is not None:
				minimum_spanning_tree.append((node[0], node[1], 1))

		# for node in range(1, self.e - 1):
		# 		minimum_spanning_tree.append((self.min_edges[node][0], self.min_edges[node][1], self.min_weights[node]))
		self.result = minimum_spanning_tree
		return self.generateMazeArray()