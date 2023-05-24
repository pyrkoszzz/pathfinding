import math

class SolveAgent:
    def __init__(self, app_instance):
        self.app = app_instance
        self.roadmap = None
        self.statring_v = 0
        self.ending_v = self.app.maze_agent.maze_size-1
    
    def makeMazePath(self):
        n = int(math.sqrt(self.app.maze_agent.maze_size))

        for x in range(len(self.roadmap)-1):
            v = self.roadmap[x]
            u = self.roadmap[x+1]
            self.app.maze_agent.maze[2*(v // n)][2*(v % n)] = 2
            self.app.maze_agent.maze[2*(u // n)][2*(u % n)] = 2
            self.app.maze_agent.maze[u // n + v // n][u % n + v % n] = 2
        print(self.app.maze_agent.maze)

    def runDfs(self):
        
        def createAdjListFromEgdes():
            for u,v,w in self.maze_graph:
                addEdge(u,v)
                addEdge(v,u)

        def addEdge(u,v):
            self.m_adj_list[u].add((v,1))

        def dfs(start, target, path = [], visited = set()):
            path.append(start)
            visited.add(start)
            if start == target:
                return path
            for (neighbour, weight) in self.m_adj_list[start]:
                if neighbour not in visited:
                    result = dfs(neighbour, target, path, visited)
                    if result is not None:
                        return result
            path.pop()
            return None
                    
        self.maze_graph = self.app.maze_agent.graph
        self.maze_graph = sorted(self.maze_graph, key=lambda item: item[0])
        self.m_adj_list = {node: set() for node in range(len(self.maze_graph)+1)}     
        createAdjListFromEgdes()

        self.roadmap = dfs(self.statring_v, self.ending_v)
        self.makeMazePath()

        
