import yaml
import pygame

class ConfigAgent():

    
    def __init__(self):
        self.config = self.loadConfig()

    def loadConfig(self):
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
            return config
    
    def setDisplayMode(self):
        if self.config['display']['mode'] == 0:
            return pygame.FULLSCREEN
    
    def getMainBackgroundPath(self):
        return self.config['assets']['background']