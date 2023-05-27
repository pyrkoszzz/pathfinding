import pygame
import math

class EventAgent():


    def __init__(self, app_instance):
        self.app = app_instance
        self.action = None

    def handleEvent(self,event, m_pos):
        if event.type == pygame.QUIT:
            self.app.running = False 
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handleMenuButtons(event, m_pos)
            self.handlePointsChoice(event, m_pos)
            
            
    def handleMenuButtons(self, event, m_pos):
        if event.button == 1:
            for action, collider in self.app.display_agent.action_buttons.items():
                    if collider.collidepoint(m_pos):
                        self.executeAction(action)

    def handlePointsChoice(self, event, m_pos):
        if self.app.maze_agent.maze != None and len(self.app.maze_agent.maze[0]) > 0:
            it = range(len(self.app.maze_agent.maze[0])) 
            for x in it:
                for y in it:
                    tmp = self.app.display_agent.maze_path_colliders[y][x]
                    if tmp is not None:
                        if tmp.collidepoint(m_pos):
                            if event.button == 1:
                                self.app.maze_agent.maze[y][x] = 3
                                self.app.solve_agent.starting_v = int(math.sqrt(self.app.maze_agent.maze_size)) * (y//2) + (x//2)
                            elif event.button == 3:
                                self.app.maze_agent.maze[y][x] = 4
                                self.app.solve_agent.ending_v = int(math.sqrt(self.app.maze_agent.maze_size)) * (y//2) + (x//2)
                            print(tmp)

    def executeAction(self, action):
        if action == "Exit":
            self.app.running = False
        elif action == "Kruskal":
            self.app.maze_agent.initializeKruskal()
        elif action == "Prim":
            self.app.maze_agent.initializePrim()
        elif action == "Next step":
            self.app.maze_agent.nextStep()
        elif action == "Fast generate":
            self.action = self.app.maze_agent.fastForward
        elif action == "Solve DFS":
            self.app.solve_agent.initializeDFS()
        elif action == "Clear layer":
            self.app.maze_agent.maze = None
        elif action == "Next step solve":
            self.app.solve_agent.nextStep()
        elif action == "Stop":
            self.action = None
        elif action == "Size +":
            self.app.maze_agent.maze_size = int(math.pow(math.sqrt(self.app.maze_agent.maze_size) + 1, 2))
        elif action == "Size -":
            self.app.maze_agent.maze_size = int(math.pow(math.sqrt(self.app.maze_agent.maze_size) - 1, 2))

    def executeActionsQueue(self):
        if self.action is not None:
            self.action()
