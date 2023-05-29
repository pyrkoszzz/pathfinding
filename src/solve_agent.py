import math

class SolveAgent:

    """! Klasa SolveAgent jest odpowiedzialna za rozwiązywanie labiryntów w aplikacji. 
    Służy do znalezienia ścieżki i wyznaczenia optymalnego rozwiązania w labiryncie, 
    umożliwiając użytkownikowi znalezienie drogi od punktu startowego do punktu końcowego. 
    Klasa SolveAgent wykorzystuje różne algorytmy przeszukiwania grafu, 
    takie jak przeszukiwanie w głąb (DFS), aby znaleźć ścieżkę przez labirynt.
    """

    def __init__(self, app_instance):

        """! Konstruktor klasy rozwiązywania i obsługi labiryntów.
		Inicjalizuje zmienne i komponenty używane w aplikacji.
		
		@return  Instancja klasy SolveAgent zainicjalizowana podaną nazwą.
		"""
        ## Obiekt bazowej klasy aplikacji
        self.app = app_instance
        ## Początkowy wierzchołek wyszukiwania
        self.starting_v = 0
        ## Końcowy wierzchołek wyszukiwania
        self.ending_v = self.app.maze_agent.maze_size-1
        ## Położenie wierzchołka startowego w macierzy
        self.s_v = (0,0)
        ## Położenie wierzchołka końcowego w macierzy
        self.e_v = (2*int(math.sqrt(self.app.maze_agent.maze_size))-2, 2*int(math.sqrt(self.app.maze_agent.maze_size))-2)
        ## Znaleziona ścieżka w labiryncie 
        self.maze_path = None
        ## Przerywnik pętli, służący do wewnętrznego przechowywania stanu rozwiązywania przez algorytm
        self.done = False
        ## Obiekt szukania ścieżki w labiryncie
        self.obj = None

    def addEdge(self, u,v):

        """! Funkcja wspomagająca tworzenie listy sąsiedztwa
		"""

        self.m_adj_list[u].append(v)

    def createAdjListFromEgdes(self):

        """! Funkcja wspomagająca tworzenie listy sąsiedztwa
		"""

        for u,v,w in self.maze_graph:
            self.addEdge(u,v)
            self.addEdge(v,u)

    def initializeDFS(self):

        """! Funkcja inicializująca algorytm DFS do szukania ścieżki w labiryncie
		"""
        ## Resetowanie akcji agenta
        self.app.event_agent.action = None
        if self.app.maze_agent.graph is not None:
            ## Licznik ilości wykonań kroków algorytmu
            self.steps_cntr = 0
            ## Przerywnik pętli, służący do wewnętrznego przechowywania stanu szukania ścieżki przez algorytm
            self.done = False
            self.app.state_agent.log = "Maze traversal using DFS algo started"
            self.app.state_agent.updateState("solving")
            ## Obiekt wyszukiwacza ścieżki
            self.obj = DFSSolver(self)
            ## Reprezentacja grafowa labiryntu
            self.maze_graph = self.app.maze_agent.graph
            self.maze_graph = sorted(self.maze_graph, key=lambda item: item[0])
            ## Lista sąsiedztwa na podstawie labiryntu
            self.m_adj_list = {node: list() for node in range(len(self.maze_graph)+1)}     
            self.createAdjListFromEgdes()

    def nextStep(self):

        """! Funkcja wywołująca kolejny krok algorytmu
		"""

        if not self.done and self.obj != None:
            self.maze_path =  self.obj.nextStep(self.m_adj_list)
        else:
            self.obj = None
    
    def fastForward(self):

        """! Funkcja szukająca ścieżki w labiryncie, wykonuje kolejne kroki, aż do pomyślnego wykonania algorytmu przeszukiwania
		"""

        if self.obj != None:
            if not self.done:
                self.maze_path =  self.obj.nextStep(self.m_adj_list)
            else:
                self.app.event_agent.action = None

class DFSSolver:

    """! Klasa DFSSolver jest odpowiedzialna za rozwiązywanie labiryntów 
    przy użyciu algorytmu przeszukiwania w głąb (DFS - Depth-First Search). 
    Algorytm DFS jest jednym z podstawowych algorytmów przeszukiwania grafu, 
    który umożliwia odwiedzenie wszystkich wierzchołków grafu w głębokości, 
    zanim przejdzie do innych wierzchołków. W przypadku rozwiązywania labiryntów, 
    algorytm DFS jest być używany do znalezienia ścieżki od punktu startowego do punktu końcowego.
    """

    def __init__(self, solve_agent):

        """! Konstruktor klasy rozwiązywania labiryntów.
		Inicjalizuje zmienne i komponenty używane w aplikacji.
		
		@return  Instancja klasy DFSSolver zainicjalizowana podaną nazwą.
		"""

        ## Obiekt nadzorujący wyszukiwanie ścieżki
        self.solve_agent = solve_agent
        ## Początkowy wierzchołek wyszukiwania
        self.start = self.solve_agent.starting_v
        ## Końcowy wierzchołek wyszukiwania
        self.end = self.solve_agent.ending_v
        ## Stos do przechowywania krotki węzła i ścieżki
        self.stack = [(self.start, [self.start])] 
        ## Informacje o odwiedzonych wierzchołkach
        self.visited = set()

    def makeMazePath(self, path):

        """! Metoda zwracająca rozwiązanie labiryntu w postaci ścieżki od punktu startowego do punktu końcowego. 
        Ścieżka jest reprezentowana jako tablica.
        """

        if path is not None:
            n = int(math.sqrt(self.solve_agent.app.maze_agent.maze_size))
            maze = []
            [maze.append([0 for _ in range(2 * n - 1)]) for _ in range(2 * n - 1)]
            for x in range(len(path)-1):
                v = path[x]
                u = path[x+1]
                maze[2*(v // n)][2*(v % n)] = 2
                maze[u // n + v // n][u % n + v % n] = 2
                maze[2*(u // n)][2*(u % n)] = 2
            return maze
                    
    def nextStep(self, graph):

        """! Metoda rozwiązująca labirynt przy użyciu algorytmu DFS. 
        Algorytm DFS rozpoczyna od punktu startowego i przeszukuje labirynt w głąb, 
        przechodząc przez kolejne komórki i ścieżki. W trakcie przeszukiwania 
        zapisywane są odwiedzone komórki i ścieżki. 
        Jeśli algorytm znajdzie punkt końcowy, generowana jest ścieżka 
        od punktu startowego do punktu końcowego.
        """

        if self.stack:
            self.solve_agent.steps_cntr += 1
            self.solve_agent.app.state_agent.log = "Solving maze - steps: " + str(self.solve_agent.steps_cntr)
            current_node, path = self.stack.pop()

            if current_node == self.end:
                self.solve_agent.done = True
                self.solve_agent.app.state_agent.log = "Maze solved successfuly"
                self.solve_agent.app.state_agent.updateState("solved")
                return self.makeMazePath(path)

            if current_node not in self.visited:
                self.visited.add(current_node)
                for neighbor in graph[current_node]:
                    if neighbor not in self.visited:
                        self.stack.append((neighbor, path + [neighbor]))
        return self.makeMazePath(path)

        
