import random
import math
import pygame

class MazeAgent:


	def __init__(self, app_instance):
		self.app = app_instance
		self.maze = None
		self.graph = None
		self.maze_size = 625
		self.done = False
		self.steps_cntr = 0
		self.obj = None

	def initializeKruskal(self):
		self.obj = Kruskal(self.maze_size, self)
		self.maze, self.graph = self.obj.generateMazeArray()
		self.app.status = "Maze generation using Kruskal's algo started"
		self.steps_cntr = 0
		self.done = False

	def initializePrim(self):
		self.obj = Prim(self.maze_size, self)
		self.maze, self.graph = self.obj.generateMazeArray()
		self.app.status = "Maze generation using Prim's algo started"
		self.steps_cntr = 0
		self.done = False

	def nextStep(self):
		if not self.done and self.obj != None:
			self.maze, self.graph =  self.obj.nextStep()

	def fastForward(self):
		if self.obj != None:
			if not self.done:
				self.maze, self.graph =  self.obj.kruskalMSTStep()
			else:
				self.app.event_agent.action = None

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

class Heap():
 
    def __init__(self):
        self.array = []
        self.size = 0
        self.pos = []
 
    def newMinHeapNode(self, v, dist):
        minHeapNode = [v, dist]
        return minHeapNode
 
    # A utility function to swap two nodes of
    # min heap. Needed for min heapify
    def swapMinHeapNode(self, a, b):
        t = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = t
 
    # A standard function to heapify at given idx
    # This function also updates position of nodes
    # when they are swapped. Position is needed
    # for decreaseKey()
    def minHeapify(self, idx):
        smallest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2
 
        if left < self.size and self.array[left][1] < self.array[smallest][1]:
            smallest = left
 
        if right < self.size and self.array[right][1] < self.array[smallest][1]:
            smallest = right
 
        # The nodes to be swapped in min heap
        # if idx is not smallest
        if smallest != idx:
 
            # Swap positions
            self.pos[self.array[smallest][0]] = idx
            self.pos[self.array[idx][0]] = smallest
 
            # Swap nodes
            self.swapMinHeapNode(smallest, idx)
 
            self.minHeapify(smallest)
 
    # Standard function to extract minimum node from heap
    def extractMin(self):
 
        # Return NULL wif heap is empty
        if self.isEmpty() == True:
            return
 
        # Store the root node
        root = self.array[0]
 
        # Replace root node with last node
        lastNode = self.array[self.size - 1]
        self.array[0] = lastNode
 
        # Update position of last node
        self.pos[lastNode[0]] = 0
        self.pos[root[0]] = self.size - 1
 
        # Reduce heap size and heapify root
        self.size -= 1
        self.minHeapify(0)
 
        return root
 
    def isEmpty(self):
        return True if self.size == 0 else False
 
    def decreaseKey(self, v, dist):
        # Get the index of v in  heap array
        i = self.pos[v]
        # Get the node and update its dist value
        self.array[i][1] = dist
        # Travel up while the complete tree is not
        # heapified. This is a O(Logn) loop
        while i > 0 and self.array[i][1] < self.array[(i - 1) // 2][1]:
 
            # Swap this node with its parent
            self.pos[self.array[i][0]] = (i-1)/2
            self.pos[self.array[(i-1)//2][0]] = i
            self.swapMinHeapNode(i, (i - 1)//2)
 
            # move to parent index
            i = (i - 1) // 2
 
    # A utility function to check if a given vertex
    # 'v' is in min heap or not
    def isInMinHeap(self, v):
        if self.pos[v] < self.size:
            return True
        return False

class Prim(MazeGraph):


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
				V = self.V
				key = []
				parent = []
				minHeap = Heap()

				for v in range(V):
						parent.append(-1)
						key.append(1e7)
						minHeap.array.append(minHeap.newMinHeapNode(v, key[v]))
						minHeap.pos.append(v)

				minHeap.pos[0] = 0
				key[0] = 0
				minHeap.decreaseKey(0, key[0])
				minHeap.size = V

				# In the following loop, min heap contains all nodes
				# not yet added in the MST.
				while minHeap.isEmpty() == False:
						newHeapNode = minHeap.extractMin()
						u = newHeapNode[0]

						for pCrawl in self.graph[u]:
								v = pCrawl[0]
								if minHeap.isInMinHeap(v) and pCrawl[1] < key[v]:
										key[v] = pCrawl[1]
										parent[v] = u
										minHeap.decreaseKey(v, key[v])
				self.printArr(parent, V)