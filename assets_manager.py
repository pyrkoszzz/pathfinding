import pygame
import os 

class AssetsManager:
    

    def __init__(self,app_instance):
        self.app = app_instance
        self.main_background = pygame.image.load(os.path.join(*self.app.config_agent.getMainBackgroundPath()))
        self.main_font = os.path.join(*self.app.config_agent.getMainFontPath())
        self.rescaleAssets()
    
    def rescaleAssets(self):
        self.main_background = pygame.transform.scale(self.main_background, self.app.display_agent.display_surf_size)