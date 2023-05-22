import pygame

class DisplayAgent():


    def __init__(self, app_instance):
        self.app = app_instance
        self.display_surf = pygame.display.set_mode((0,0), self.app.config_agent.setDisplayMode())
        self.display_surf_size = self.display_surf_width, self.display_surf_height = self.display_surf.get_width(), self.display_surf.get_height()
        pygame.init()

    def render(self):
        self.ui_painter.drawUI()
        pygame.display.update()

    def cleanUp(self):
        pygame.quit()

    def run(self):
        self.ui_painter = UIPainter(self)
        while self.app.running:
            for event in pygame.event.get():
                self.app.event_agent.handleEvent(event)
            self.render()
        self.cleanUp()

class UIPainter:


    def __init__(self, display_instance):
        self.display = display_instance
        self.ui_propotions = self.display.app.config_agent.getPropotionsDict()
        self.colors = self.display.app.config_agent.getColors()
        self.font = pygame.font.Font(self.display.app.assets_manager.main_font, 
                                     int(self.display.display_surf_height * self.ui_propotions['font']))
        self.text = self.display.app.config_agent.getTexts()
    
    def drawBackground(self):
        self.display.display_surf.blit(self.display.app.assets_manager.main_background, (0,0))

    def drawInfoBars(self):
        top_bar = pygame.Rect(
            self.display.display_surf_width * self.ui_propotions['bars']['topbar']['pos_x'], 
            self.display.display_surf_height * self.ui_propotions['bars']['topbar']['pos_y'], 
            self.display.display_surf_width * self.ui_propotions['bars']['width'], 
            self.display.display_surf_height * self.ui_propotions['bars']['height'])
        shape_surf = pygame.Surface(pygame.Rect(top_bar).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, self.colors['info_bars'], shape_surf.get_rect())
        app_name = self.font.render(self.text['app_name'], True, self.colors['text'])
        shape_surf.blit(app_name, 
                        (shape_surf.get_height() * self.ui_propotions['bars']['text_offset'],
                         shape_surf.get_height() * self.ui_propotions['bars']['text_offset']))
        self.display.display_surf.blit(shape_surf, top_bar)

        bottom_bar = pygame.Rect(
            self.display.display_surf_width * self.ui_propotions['bars']['bottombar']['pos_x'], 
            self.display.display_surf_height * self.ui_propotions['bars']['bottombar']['pos_y'], 
            self.display.display_surf_width * self.ui_propotions['bars']['width'], 
            self.display.display_surf_height * self.ui_propotions['bars']['height'])
        shape_surf = pygame.Surface(pygame.Rect(bottom_bar).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, self.colors['info_bars'], shape_surf.get_rect())
        app_status = self.font.render(self.text['status']['status'] + ": " + self.text['status']['working'], True, self.colors['text'])
        shape_surf.blit(
            app_status, 
            (shape_surf.get_height() * self.ui_propotions['bars']['text_offset'],
             shape_surf.get_height() * self.ui_propotions['bars']['text_offset']))
        self.display.display_surf.blit(shape_surf, bottom_bar)

    def drawMazeContainer(self):
        self.maze_container = pygame.Rect(self.display.display_surf_width - self.display.display_surf_height * self.ui_propotions['maze_container']['pos_x'] - self.display.display_surf_height * self.ui_propotions['maze_container']['height'],
                            self.display.display_surf_height * self.ui_propotions['maze_container']['pos_y'], 
                            self.display.display_surf_height * self.ui_propotions['maze_container']['width'], 
                            self.display.display_surf_height * self.ui_propotions['maze_container']['height'])
        shape_surf = pygame.Surface(pygame.Rect(self.maze_container).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, self.colors['maze_container'], shape_surf.get_rect(), border_radius=self.ui_propotions['border_radius'])
        self.display.display_surf.blit(shape_surf, self.maze_container)

    def drawUI(self):
        self.drawBackground()
        self.drawInfoBars()
        self.drawMazeContainer()

class MazePainter(UIPainter):

    def drawMazeBackground(self):
      pygame.draw.rect(self.shape_surf, (255, 255, 255, 70), self.shape_surf.get_rect(), border_radius=10)
      self.screen.blit(self.shape_surf, self.maze_bg)

    def rect_round(self, x1, y1, w, h):
      r_x1 = round(x1)
      r_y1 = round(y1)
      r_w = round(x1 - r_x1 + w)
      r_h = round(y1 - r_y1 + h)
      return pygame.Rect(r_x1, r_y1, r_w, r_h)
    
