import pygame

class DisplayAgent():


    def __init__(self, app_instance):
        self.app = app_instance
        self.display_surf = pygame.display.set_mode((0,0), self.app.config_agent.setDisplayMode())
        self.display_surf_size = self.display_surf_width, self.display_surf_height = self.display_surf.get_width(), self.display_surf.get_height()
        pygame.init()

    def render(self):
        self.display_surf.blit(self.app.assets_manager.main_background, (0,0))
        pygame.display.update()

    def cleanUp(self):
        pygame.quit()

    def run(self):
        while self.app.running:
            for event in pygame.event.get():
                self.app.event_agent.handleEvent(event)
            self.render()
        self.cleanUp()