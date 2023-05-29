import random
import math
import sys

class MazeAgent:

	"""! Klasa MazeAgent jest odpowiedzialna za zarządzanie generowaniem i przygotowanie do prezentacji labiryntów w aplikacji. 
	Służy do tworzenia różnych typów labiryntów oraz przygotowania do wizualizacji labiryntów dla użytkownika.
	"""

	def __init__(self, app_instance):

		"""! Konstruktor klasy generowania i obsługi labiryntów.
		Inicjalizuje zmienne i komponenty używane w aplikacji.
		
		@return  Instancja klasy MazeAgent zainicjalizowana podaną nazwą.
		"""
		## Obiekt bazowej klasy aplikacji
		self.app = app_instance
		## Tablica reprezentująca labirynt
		self.maze = None
		## Macierz sąsiedztwa wierzchołków labiryntu
		self.graph = None
		## Rozmiar labiryntu - ilość wierzchołków
		self.maze_size = 625
		## Przerywnik pętli, służący do wewnętrznego przechowywania stanu generowania przez algorytm
		self.done = False
		## Licznik ilości wykonań kroków algorytmu
		self.steps_cntr = 0
		## Obiekt generatora labiryntu
		self.obj = None

	def initializeKruskal(self):

		"""! Funkcja inicializująca algorytm Kruskal'a do generowania labiryntu
		"""
		## Obiekt bazowej klasy generowania i obsługi labiryntów
		self.app.event_agent.action = None
		## Obiekt generatora labiryntu
		self.obj = Kruskal(self.maze_size, self)
		self.maze, self.graph = self.obj.generateMazeArray()
		self.app.state_agent.log = "Maze generation using Kruskal's algo started"
		self.app.state_agent.updateState("generating")
		## Licznik ilości wykonań kroków algorytmu
		self.steps_cntr = 0
		## Przerywnik pętli, służący do wewnętrznego przechowywania stanu generowania przez algorytm
		self.done = False

	def initializePrim(self):

		"""! Funkcja inicializująca algorytm Prim'a do generowania labiryntu
		"""

		## Obiekt bazowej klasy generowania i obsługi labiryntów
		self.app.event_agent.action = None
		## Obiekt generatora labiryntu
		self.obj = Prim(self.maze_size, self)
		self.maze, self.graph = self.obj.generateMazeArray()
		self.app.state_agent.log = "Maze generation using Prim's algo started"
		self.app.state_agent.updateState("generating")
		## Licznik ilości wykonań kroków algorytmu
		self.steps_cntr = 0
		## Przerywnik pętli, służący do wewnętrznego przechowywania stanu generowania przez algorytm
		self.done = False

	def nextStep(self):

		"""! Funkcja wywołująca kolejny krok algorytmu
		"""

		if not self.done and self.obj != None:
			self.maze, self.graph =  self.obj.nextStep()
		else:
			self.obj = None

	def fastForward(self):

		"""! Funkcja generująca kompletny labirynt, wykonuje kolejne kroki, aż do pomyślnego wykonania algorytmu generacji
		"""

		if self.obj != None:
			if not self.done:
				self.maze, self.graph =  self.obj.nextStep()
			else:
				self.app.event_agent.action = None
	
	def importMaze(self, f):

		"""! Funkcja inicializująca importowanie labiryntu
		"""
		## Odczytana z pliku liczba wierzchołków labiryntu
		self.maze_size = int(f.readline())
		## Ustawienie końcowego wierzchołka do szukania ścieżki na ostatni (prawy dolny)
		self.app.solve_agent.ending_v = self.maze_size - 1
		self.app.solve_agent.e_v = (2*int(math.sqrt(self.maze_size))-2, 2*int(math.sqrt(self.maze_size))-2)
		## Przerywnik pętli, służący do wewnętrznego przechowywania stanu generowania przez algorytm
		self.done = False
		## Obiekt importera labiryntu
		self.obj = MazeImporter(f, self.maze_size, self)
		self.maze, self.graph = self.obj.generateMazeArray()


class MazeGraph:

	"""! Klasa MazeGraph jest odpowiedzialna za reprezentację labiryntu jako grafu w aplikacji. 
	Służy do tworzenia grafowych struktur danych, które reprezentują labirynt jako zbiór węzłów i krawędzi, umożliwiając analizę i manipulację strukturą labiryntu.
	Klasa MazeGraph udostępnia metody do dodawania węzłów, tworzenia krawędzi między nimi oraz analizy grafu.
	"""

	def __init__(self, vertices):

		"""! Konstruktor klasy generowania i obsługi labiryntów.
		Inicjalizuje zmienne i komponenty używane w aplikacji.
		
		@return  Instancja klasy MazeGraph zainicjalizowana podaną nazwą.
		"""
		## Ilość wierzchołków grafu
		self.V = vertices
		## Reprezentacja grafu
		self.graph = []
		## Ilość wierzchołków w rzędzie
		self.size = int(math.sqrt(vertices))

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

		"""! Funkcja wspomagająca tworzenie listy sąsiedztwa
		"""

		self.graph[u].append((v, w))
		self.graph[v].append((u, w))

	def addEdge(self, u, v, w):

		"""! Funkcja wspomagająca tworzenie listy sąsiedztwa
		"""

		self.graph.append([u, v, w])

	def find(self, parent, i):

		"""! Funkcja znajdująca bozepośredniego rodzica wierzchołka
		"""

		if parent[i] != i:
			parent[i] = self.find(parent, parent[i])
		return parent[i]



	def union(self, parent, rank, x, y):

		"""! Funkcja do łączenia dwóch zbiorów elementów.
		@param parent: Tablica reprezentująca strukturę zbiorów elementów.
		@param rank: Tablica przechowująca rangi (wysokości) poszczególnych zbiorów.
    @param x: Element, który należy do pierwszego zbioru.
		@param y: Element, który należy do drugiego zbioru.
		"""

		if rank[x] < rank[y]:
			parent[x] = y
		elif rank[x] > rank[y]:
			parent[y] = x
		else:
			parent[y] = x
			rank[x] += 1
	
	def generateMazeArray(self):

		"""! Funkcja przygotowywująca tablicę labiryntu - przekazywana do agenta wyświetlania
		@return Tablicę labiryntu
		@return Macież sąsiedztwa labiryntu
		"""

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
 
class MazeImporter(MazeGraph):

	"""! Klasa MazeImporter jest odpowiedzialna za importowanie labiryntów z zewnętrznych źródeł do aplikacji. 
	Służy do odczytywania plików lub innych formatów danych, które zawierają informacje o strukturze labiryntu
	i konwertowania ich na wewnętrzną reprezentację labiryntu używaną przez aplikację. 
	Klasa MazeImporter umożliwia łatwe załadowanie różnych labiryntów do aplikacji, co pozwala na dynamiczne generowanie i rozwiązywanie różnych typów labiryntów.
	"""

	def __init__(self, f, vertices, maze_agent):
		
		"""! Konstruktor klasy importowania labiryntów.
		Inicjalizuje zmienne i komponenty używane w aplikacji.
		
		@return  Instancja klasy MazeImporter zainicjalizowana podaną nazwą.
		"""

		super().__init__(vertices)
		## Wczytany labirynt
		self.result = []
		## Obiekt generatora labiryntu
		self.maze_agent = maze_agent

		for line in f:
			u,v,w = line.split()
			self.result.append([int(u), int(v), int(w)])
		self.done = True
		self.maze_agent.app.state_agent.log = "Maze imported successfuly"
		self.maze_agent.app.state_agent.updateState("generated")

class Kruskal(MazeGraph):

	"""! Klasa KruskalGenerate jest odpowiedzialna za generowanie labiryntów przy użyciu algorytmu Kruskala. 
	Algorytm Kruskala jest jednym z popularnych algorytmów generowania labiryntów, 
	który tworzy losowy labirynt poprzez stopniowe usuwanie ścian między komórkami labiryntu. 
	Klasa KruskalGenerate implementuje logikę tego algorytmu, umożliwiając wygenerowanie labiryntu o określonym rozmiarze i strukturze.
	"""

	def __init__(self, vertices, maze_agent):

		"""! Konstruktor klasy generowania labiryntów za pomocą algorytmu Kruskala.
		Inicjalizuje zmienne i komponenty używane w aplikacji.
		
		@return  Instancja klasy Kruskal zainicjalizowana podaną nazwą.
		"""

		super().__init__(vertices)
		## Wygenerowany labirynt
		self.result = []
		## Licznik wspomagający
		self.i = 0
		## Licznik wspomagający
		self.e = 0
		## Posortowana lista sąsiedztwa wierzchołków labiryntu
		self.graph = sorted(self.graph, key = lambda item: item[2])
		## tablica wspomagająca przechowywująca rodziców aktualnego wierzchołka
		self.parent = []
		## tablica wspomagająca przechowywująca stopień aktualnego wierzchołka
		self.rank = []
		## Obiiekt generatora labiryntów
		self.maze_agent = maze_agent

		for node in range(self.V):
			self.parent.append(node)
			self.rank.append(0)

	def nextStep(self):

		"""! Funkcja generująca labirynt przy użyciu algorytmu Kruskala. 
		Algorytm rozpoczyna się od utworzenia siatki komórek labiryntu. 
		Następnie inicjalizowane są zbiory komórek jako osobne grupy. 
		Algorytm losowo wybiera ścianę, sprawdza czy komórki po obu stronach ściany należą do różnych grup,
		jeśli tak, usuwa tę ścianę i łączy grupy komórek. 
		Proces powtarza się, aż wszystkie komórki są połączone w jedną grupę, tworząc połączenia między nimi.
		"""

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

	"""! Klasa PrimGenerate jest odpowiedzialna za generowanie labiryntów przy użyciu algorytmu Prima. 
	Algorytm Prima jest algorytmem grafowym wykorzystywanym do tworzenia minimalnego drzewa spinającego dla danego grafu. 
	W przypadku generowania labiryntów, algorytm Prima jest używany do losowego tworzenia ścieżek między komórkami labiryntu, 
	tworząc połączenia między nimi.
	"""

	def __init__(self, vertices, maze_agent):

		"""! Konstruktor klasy generowania labiryntów za pomocą algorytmu Prima.
		Inicjalizuje zmienne i komponenty używane w aplikacji.
		
		@return  Instancja klasy Prim zainicjalizowana podaną nazwą.
		"""

		super().__init__(vertices)
		## Wygenerowany labirynt
		self.result = []
		## Obiekt generatora labiryntów
		self.maze_agent = maze_agent
		## Ilość wierzchołków grafu
		self.num_nodes = len(self.graph)
		## Śledzenie, które węzły są zawarte w minimalnym drzewie rozpinającym.
		self.selected = [False] * self.num_nodes
		self.selected[0] = True
		## Licznik wspomagający
		self.e = 0
		# Tablice do śledzenia minimalnych wag i odpowiadających im krawędzi dla każdego węzła.
		self.min_weights = [sys.maxsize] * self.num_nodes
		self.min_weights[0] = 0
		self.min_edges = [None] * self.num_nodes	

	def nextStep(self):

		"""! Metoda generująca labirynt przy użyciu algorytmu Prima. 
		Algorytm rozpoczyna się od wybrania losowej komórki jako początkowej.  
		W każdej iteracji pobierana jest ściana o najmniejszej wadze z kolejki, 
		a jeśli ta ściana łączy dwie różne grupy komórek, zostaje usunięta, 
		tworząc połączenie między nimi. Proces kontynuowany jest, 
		aż wszystkie komórki są połączone w jedną grupę, tworząc połączenia między nimi.
		"""

		if self.e in range(self.num_nodes - 1):
				self.e += 1
				min_weight = sys.maxsize
				min_node = 0

				for node in range(self.num_nodes):
						if not self.selected[node] and self.min_weights[node] < min_weight:
								min_weight = self.min_weights[node]
								min_node = node

				self.selected[min_node] = True

				for neighbor, weight in self.graph[min_node]:
						if not self.selected[neighbor] and weight < self.min_weights[neighbor]:
								self.min_weights[neighbor] = weight
								self.min_edges[neighbor] = (min_node, neighbor)
				self.maze_agent.steps_cntr += 1
				self.maze_agent.app.state_agent.log = "Generating maze - steps: " + str(self.maze_agent.steps_cntr)

		else:
			self.maze_agent.done = True
			self.maze_agent.app.state_agent.log = "Maze generated successfuly"
			self.maze_agent.app.state_agent.updateState("generated")
		
		minimum_spanning_tree = []
		for node in self.min_edges:
			if node is not None:
				minimum_spanning_tree.append((node[0], node[1], 1))

		self.result = minimum_spanning_tree
		return self.generateMazeArray()