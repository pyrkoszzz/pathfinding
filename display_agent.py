import pygame
import math

class DisplayAgent():


    def __init__(self, app_instance):
        self.app = app_instance
        self.display_surf = pygame.display.set_mode((0,0),self.app.config_agent.setDisplayMode())
        self.display_surf_size = self.display_surf_width, self.display_surf_height = self.display_surf.get_width(), self.display_surf.get_height()
        self.buttons_groups =  {
            "Generate" : ["Kruskal", "Prim"],
            "Solve": ["Solve DFS"],
            "SolveControl": ["Next step", "Fast solve", "Stop"],
            "Settings": ["Clear path", "Clear layer", "Import", "Export", "Size +", "Size -", "Exit"],
            "GenerateControl": ["Next step", "Fast generate", "Stop"]
        }
        self.action_buttons = {
            "Kruskal": None,
            "Prim": None,
            "Solve DFS": None,
            "Clear layer": None,
            "Clear path": None,
            "Next step solve": None,
            "Size +": None,
            "Size -": None,
            "Exit": None,
            "Next step": None,
            "Fast generate": None,
            "Stop": None,
            "Import": None,
            "Export": None
        }
        self.maze_path_colliders = []
        pygame.init()

    def render(self):
        self.ui_painter.drawUI()
        pygame.display.update()

    def cleanUp(self):
        pygame.quit()

    def loop(self):
        self.app.event_agent.executeActionsQueue()

    def run(self):
        self.ui_painter = UIPainter(self)
        while self.app.running:
            for event in pygame.event.get():
                self.app.event_agent.handleEvent(event, pygame.mouse.get_pos())
            self.loop()
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
        self.constants = self.display.app.config_agent.getConstants()
        n = int(math.sqrt(self.display.app.maze_agent.maze_size))
        [self.display.maze_path_colliders.append([None for _ in range(2 * n - 1)]) for _ in range(2 * n - 1)]
    
    def drawBackground(self):
        self.display.display_surf.blit(self.display.app.assets_manager.main_background, (0,0))

    def drawInfoBars(self):
        top_bar = pygame.Rect(
            self.display.display_surf_width * self.ui_propotions['bars']['topbar']['pos_x'], 
            self.display.display_surf_height * self.ui_propotions['bars']['topbar']['pos_y'], 
            self.display.display_surf_width * self.ui_propotions['bars']['topbar']['width'], 
            self.display.display_surf_height * self.ui_propotions['bars']['topbar']['height'])
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
            self.display.display_surf_width * self.ui_propotions['bars']['bottombar']['width'], 
            self.display.display_surf_height * self.ui_propotions['bars']['bottombar']['height'])
        shape_surf = pygame.Surface(pygame.Rect(bottom_bar).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, self.colors['info_bars'], shape_surf.get_rect())
        app_status = self.font.render(self.text['state']['status'] + ": " + self.display.app.status, True, self.colors['text'])
        shape_surf.blit(
            app_status, 
            (shape_surf.get_height() * self.ui_propotions['bars']['text_offset'],
             shape_surf.get_height() * self.ui_propotions['bars']['text_offset']))
        self.display.display_surf.blit(shape_surf, bottom_bar)

    def drawMazeContainer(self):
        self.maze_container = pygame.Rect(
            self.display.display_surf_width - self.display.display_surf_height * self.ui_propotions['maze_container']['height'] - self.display.display_surf_width * self.ui_propotions['maze_container']['pos_x'],
            self.display.display_surf_height * self.ui_propotions['maze_container']['pos_y'], 
            self.display.display_surf_height * self.ui_propotions['maze_container']['width'], 
            self.display.display_surf_height * self.ui_propotions['maze_container']['height'])
        self.maze_surf = pygame.Surface(pygame.Rect(self.maze_container).size, pygame.SRCALPHA)
        pygame.draw.rect(self.maze_surf, self.colors['maze_container'],  self.maze_surf.get_rect(), border_radius=self.ui_propotions['border_radius'])
        self.display.display_surf.blit( self.maze_surf, self.maze_container)

    def drawMaze(self):
        if self.display.app.maze_agent.maze != None and self.display.app.maze_agent.graph != None:
            maze_size = len(self.display.app.maze_agent.maze[0])
            self.rect_size = (self.maze_surf.get_width() / maze_size)
            for x in range(maze_size):
                for y in range(maze_size):
                    rect = self.rect_round(x * self.rect_size, y * self.rect_size, self.rect_size, self.rect_size)
                    if not self.display.app.maze_agent.maze[y][x]:
                        pygame.draw.rect(self.maze_surf,"black", rect)
                    elif (y,x) == self.display.app.solve_agent.s_v:
                        pygame.draw.rect(self.maze_surf, "green", rect)
                    elif (y,x) == self.display.app.solve_agent.e_v:
                        pygame.draw.rect(self.maze_surf, "red", rect)
                    elif self.display.app.solve_agent.maze_path != None and self.display.app.solve_agent.maze_path[y][x] == self.constants['s_path']:
                        pygame.draw.rect(self.maze_surf, self.colors['maze_path'], rect)
                    else:
                        rect = rect.move(self.maze_container.x, self.maze_container.y)
                        self.display.maze_path_colliders[y][x] = rect
            self.display.display_surf.blit(self.maze_surf, self.maze_container)

    def drawMenuButton(self, action, button_idx, container):
        m_pos = pygame.mouse.get_pos()
        button = pygame.Rect(
            container.left + self.ui_propotions['selection_button']['pos_x'],
            container.top + self.display.display_surf_height * self.ui_propotions['selection_button']['pos_y'] * button_idx + (button_idx * self.display.display_surf_height * self.ui_propotions['buttons_padding']), 
            self.display.display_surf_width * self.ui_propotions['selection_button']['width'],
            self.display.display_surf_height * self.ui_propotions['selection_button']['height'])
        button_surf = pygame.Surface(pygame.Rect(button).size, pygame.SRCALPHA)
        color = self.colors['button_hover'] if button.collidepoint(m_pos) else self.colors['button']
        pygame.draw.rect(button_surf, color, button_surf.get_rect(), border_radius=self.ui_propotions['border_radius'])
        caption = self.font.render(action, True, self.colors['text'])
        button_surf.blit(caption, 
                        (button_surf.get_height() * self.ui_propotions['selection_button']['text_offset'],
                        button_surf.get_height() * self.ui_propotions['selection_button']['text_offset']))
        self.display.display_surf.blit(button_surf, button)
        return button
    
    def drawMenuCointainers(self):
        def createContainer(propotions_group, group):
            container = pygame.Rect(
                self.display.display_surf_width * propotions_group['pos_x'],
                self.display.display_surf_height * propotions_group['pos_y'],
                self.display.display_surf_width * propotions_group['width'],
                len(self.display.buttons_groups[group]) * 
                self.display.display_surf_height * 
                self.ui_propotions['selection_button']['height'] +
                (len(self.display.buttons_groups[group])-1) * self.ui_propotions['buttons_padding'] * self.display.display_surf_height)
            shape_surf = pygame.Surface(pygame.Rect(container).size, pygame.SRCALPHA)
            pygame.draw.rect(shape_surf, self.colors['menu_container'], shape_surf.get_rect(), border_radius=self.ui_propotions['border_radius'])
            self.display.display_surf.blit(shape_surf, container)
            return container
        
        self.menu_container = createContainer(self.ui_propotions['side_menu'], "Generate")
        self.control_menu_container = createContainer(self.ui_propotions['control_menu'], "GenerateControl")
        self.solve_container = createContainer(self.ui_propotions['solve_menu'], "Solve")
        self.settings_container = createContainer(self.ui_propotions['settings_menu'], "Settings")
        self.solve_control_container = createContainer(self.ui_propotions['solve_control_menu'], "SolveControl")

        def switchMenuSurface(category):
            if category == "Generate":
                return self.menu_container
            elif category == "GenerateControl":
                return self.control_menu_container
            elif category == "Solve":
                return self.solve_container
            elif category == "Settings":
                return self.settings_container
            elif category == "SolveControl":
                return self.solve_control_container

        for category, values in self.display.buttons_groups.items():
            button_idx = 0
            for action in values:
                collider = self.drawMenuButton(action, button_idx, switchMenuSurface(category))
                self.display.action_buttons.update({action: collider})
                button_idx += 1
        
    def drawControlMenu(self):
        button_idx = 0
        buttons_to_draw = self.display.buttons_groups["GenerateControl"]
        for action in self.display.action_buttons.keys():
            if action in buttons_to_draw:
                collider = self.drawMenuButton(action, button_idx, self.control_menu_cointainer)
                self.display.action_buttons.update({action: collider})
                button_idx += 1

    def drawUI(self):
        self.drawBackground()
        self.drawInfoBars()
        self.drawMenuCointainers()
        self.drawMazeContainer()
        self.drawMaze()

    def rect_round(self, x1, y1, w, h):
      r_x1 = round(x1)
      r_y1 = round(y1)
      r_w = round(x1 - r_x1 + w)
      r_h = round(y1 - r_y1 + h)
      return pygame.Rect(r_x1, r_y1, r_w, r_h)
