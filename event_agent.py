import pygame

class EventAgent():
    

    def __init__(self, app_instance):
        self.app = app_instance
        
    def handleEvent(self,event):
        if event.type == pygame.QUIT:
            self.app.running = False
    