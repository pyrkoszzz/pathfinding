import math

class SolveAgent:


    def __init__(self, app_instance):
        self.app = app_instance
        self.starting_v = 0
        self.ending_v = self.app.maze_agent.maze_size-1
        self.s_v = (0,0)
        self.e_v = (2*int(math.sqrt(self.app.maze_agent.maze_size))-2, 2*int(math.sqrt(self.app.maze_agent.maze_size))-2)
        self.maze_path = None
    
    def addEdge(self, u,v):
        self.m_adj_list[u].append(v)

    def createAdjListFromEgdes(self):
        for u,v,w in self.maze_graph:
            self.addEdge(u,v)
            self.addEdge(v,u)

    def initializeDFS(self):
        if self.app.maze_agent.graph is not None:
            self.done = False
            self.obj = DFSSolver(self)
            self.maze_graph = self.app.maze_agent.graph
            self.maze_graph = sorted(self.maze_graph, key=lambda item: item[0])
            self.m_adj_list = {node: list() for node in range(len(self.maze_graph)+1)}     
            self.createAdjListFromEgdes()

    def nextStep(self):
        if not self.done and self.obj != None:
            self.maze_path =  self.obj.nextStep(self.m_adj_list)
    
    def fastForward(self):
        if self.obj != None:
            if not self.done:
                self.maze_path =  self.obj.nextStep(self.m_adj_list)
            else:
                self.app.event_agent.action = None

class DFSSolver:


    def __init__(self, solve_agent):
        self.solve_agent = solve_agent
        self.start = self.solve_agent.starting_v
        self.end = self.solve_agent.ending_v

        self.stack = [(self.start, [self.start])]  # Stack stores tuples of node and path
        self.visited = set()

    def makeMazePath(self, path):
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
        if self.stack:
            current_node, path = self.stack.pop()

            if current_node == self.end:
                self.solve_agent.done = True
                return self.makeMazePath(path)

            if current_node not in self.visited:
                self.visited.add(current_node)
                for neighbor in graph[current_node]:
                    if neighbor not in self.visited:
                        self.stack.append((neighbor, path + [neighbor]))
        return self.makeMazePath(path)

        
