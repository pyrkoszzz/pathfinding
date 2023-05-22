import pygame
import config_agent
import display_agent
import event_agent
import assets_manager
import maze_agent

class App:


    def __init__(self):
        self.running = True
        self.config_agent = config_agent.ConfigAgent()
        self.display_agent = display_agent.DisplayAgent(self)
        self.assets_manager = assets_manager.AssetsManager(self)
        self.event_agent = event_agent.EventAgent(self)
        self.maze_agent = maze_agent.MazeAgent()

if __name__ == "__main__":
    app = App()
    app.display_agent.run()