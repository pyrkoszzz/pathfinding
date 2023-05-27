import math

class SolveAgent:


    def __init__(self, app_instance):
        self.app = app_instance
        self.roadmap = None
        self.starting_v = 0
        self.ending_v = self.app.maze_agent.maze_size-1
    
    def addEdge(self, u,v):
        self.m_adj_list[u].add((v,1))

    def createAdjListFromEgdes(self):
        for u,v,w in self.maze_graph:
            self.addEdge(u,v)
            self.addEdge(v,u)

    def initializeDFS(self):
        if self.app.maze_agent.graph is not None:
            print(self.starting_v, self.ending_v)
            self.obj = DFSSolver(self)
            self.maze_graph = self.app.maze_agent.graph
            self.maze_graph = sorted(self.maze_graph, key=lambda item: item[0])
            self.m_adj_list = {node: set() for node in range(len(self.maze_graph)+1)}     
            self.createAdjListFromEgdes()

            self.roadmap = self.obj.dfs(self.starting_v, self.ending_v, [], set())
            self.makeMazePath()

    def makeMazePath(self):
        n = int(math.sqrt(self.app.maze_agent.maze_size))

        for x in range(len(self.roadmap)-1):
            v = self.roadmap[x]
            u = self.roadmap[x+1]
            self.app.maze_agent.maze[2*(v // n)][2*(v % n)] = 2
            self.app.maze_agent.maze[u // n + v // n][u % n + v % n] = 2
        self.app.maze_agent.maze[2*(u // n)][2*(u % n)] = 2

class DFSSolver:


    def __init__(self, solve_agent):
        self.solve_agent = solve_agent

    def dfs(self, start, target, path, visited):
        path.append(start)
        visited.add(start)
        if start == target:
            return path
        for (neighbour, weight) in self.solve_agent.m_adj_list[start]:
            if neighbour not in visited:
                result = self.dfs(neighbour, target, path, visited)
                if result is not None:
                    return result
        path.pop()
        return None
                    
        

        
