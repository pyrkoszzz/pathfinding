import pygame

class EventAgent():
    

    def __init__(self, app_instance):
        self.app = app_instance

    def handleEvent(self,event, m_pos):
        if event.type == pygame.QUIT:
            self.app.running = False 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for action, collider in self.app.display_agent.action_buttons.items():
                if collider.collidepoint(m_pos):
                    self.executeAction(action)

    def executeAction(self, action):
        if action == "Exit":
            self.app.running = False
        elif action == "Kruskal":
            self.app.maze_agent.initializeKruskal()
        elif action == "Next step":
            self.app.maze_agent.nextStep()
        elif action == "Fast generate":
            self.app.maze_agent.fastForward()