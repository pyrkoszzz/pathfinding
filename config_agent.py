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
    
    def getMainFontPath(self):
        return self.config['assets']['font']

    def getPropotionsDict(self):
        return self.config['ui_propotions']
    
    def getColors(self):
        return self.config['colors']
    
    def getTexts(self):
        return self.config['text']
    
    def getStates(self):
        return self.config['text']['state']