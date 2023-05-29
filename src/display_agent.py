import pygame
import math

class DisplayAgent():

    """!Klasa DisplayAgent jest odpowiedzialna za zarządzanie wyświetlaniem danych i interakcją z użytkownikiem w aplikacji. 
    Służy do prezentacji informacji, grafiki, komunikatów, formularzy itp. oraz odbierania interakcji użytkownika, takich jak kliknięcia, wprowadzanie danych itp. 
    Głównym celem klasy DisplayAgent jest zapewnienie interfejsu użytkownika, który umożliwia łatwe przekazywanie informacji użytkownikowi i rejestrowanie jego działań.
    """

    def __init__(self, app_instance):

        """! Konstruktor klasy wyświetlającej.
        Inicjalizuje zmienne i komponenty używane w aplikacji.
        
        @return  Instancja klasy DisplayAgent zainicjalizowana podaną nazwą.
        """
        ## Obiekt bazowej klasy aplikacji
        self.app = app_instance
        ## Obiekt głównego okna aplikacji
        self.display_surf = pygame.display.set_mode((0,0),self.app.config_agent.setDisplayMode())
        ## Przechowuje aktualne rozmiary okna aplikacji
        self.display_surf_size = self.display_surf_width, self.display_surf_height = self.display_surf.get_width(), self.display_surf.get_height()
        ## Słownik grup przycisków wyświetlanych w oddzielnych kontenerach menu
        self.buttons_groups =  {
            "Generate" : ["Kruskal", "Prim"],
            "Solve": ["Solve DFS"],
            "SolveControl": ["Next step solve", "Fast solve", "Stop solving"],
            "Settings": ["Clear path", "Clear maze", "Import", "Export", "Exit"],
            "GenerateControl": ["Next step", "Fast generate", "Stop generating"]
        }
        ## Definiuje wszystkie przyciski znajdujące się w aplikacji wraz z obiektami kolidera
        self.action_buttons = {
            "Kruskal": None,
            "Prim": None,
            "Solve DFS": None,
            "Clear maze": None,
            "Clear path": None,
            "Next step solve": None,
            # "Size +": None,
            # "Size -": None,
            "Exit": None,
            "Next step": None,
            "Fast generate": None,
            "Stop generating": None,
            "Stop solving"
            "Import": None,
            "Export": None
        }
        ## Lista koliderów obiektów rysowanych w kontenerze labiryntu, służąca do wykrywania wybieranych wierzachołków labiryntu 
        self.maze_path_colliders = []
        ## Inicjalizacja silnika pygame służącego do obsługi wizualnej aplikacji
        pygame.init()

    def render(self):
        """! Funkcja służąca do aktualizacji elementó graficznych w oknie aplikacji 
        """
        self.ui_painter.drawUI()
        pygame.display.update()

    def cleanUp(self):
        """! Funkcja czyszcząca pozostałe zasoby przed zamknięciem aplikacji
        """
        pygame.quit()

    def loop(self):
        """! Pętla obsługująca wszystkie akcje dziejące się w tle aplikcaji
        """
        self.app.event_agent.executeActionsQueue()

    def run(self):
        """! Główna funkcja uruchamiająca interfejs graficzny aplikacji
        """
        ## Obiekt rysujący elementy w oknie aplikacji
        self.ui_painter = UIPainter(self)
        while self.app.running:
            for event in pygame.event.get():
                self.app.event_agent.handleEvent(event, pygame.mouse.get_pos())
            self.loop()
            self.render()
        self.cleanUp()

class UIPainter:

    """! Klasa UIPainter jest odpowiedzialna za malowanie interfejsu użytkownika (UI) w aplikacji. 
    Służy do tworzenia i renderowania elementów UI, takich jak przyciski, etykiety, listy, menu itp. 
    Klasa UIPainter zapewnia narzędzia do projektowania i prezentowania interaktywnych elementów UI, które są widoczne i dostępne dla użytkownika.
    """

    def __init__(self, display_instance):

        """! Konstruktor klasy rysującej.
        Inicjalizuje zmienne i komponenty używane w aplikacji.
        
        @return  Instancja klasy UIPainter zainicjalizowana podaną nazwą.
        """

        ## Obiekt klasy wyświetlającej
        self.display = display_instance
        ## Obiekt przechowywujący rozmieszczenia elementów ui w oknie aplikacji
        self.ui_propotions = self.display.app.config_agent.getPropotionsDict()
        ## Obiekt przechowywujący kolory używane w aplikacji
        self.colors = self.display.app.config_agent.getColors()
        ## Obiekt przechowywujący czcionki aplikacji
        self.font = pygame.font.Font(self.display.app.assets_manager.main_font, 
                                     int(self.display.display_surf_height * self.ui_propotions['font']))
        ## Obiekt zawierający wyświetlane napisy w aplikacji
        self.text = self.display.app.config_agent.getTexts()
        ## Obiekt zawierający stałe używanye w aplikacji
        self.constants = self.display.app.config_agent.getConstants()
        [self.display.maze_path_colliders.append([None for _ in range(1001)]) for _ in range(1001)]
    
    def drawBackground(self):

        """! Funkcja tworząca tło okna aplikacji
        """

        self.display.display_surf.blit(self.display.app.assets_manager.main_background, (0,0))

    def drawInfoBars(self):
        """!Funkcja tworząca widgety na ekranie
            Rysuje dolny i górny pasek"""
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
        app_status = self.font.render(self.text['state']['status'] + ": " + self.display.app.state_agent.log, True, self.colors['text'])
        shape_surf.blit(
            app_status, 
            (shape_surf.get_height() * self.ui_propotions['bars']['text_offset'],
             shape_surf.get_height() * self.ui_propotions['bars']['text_offset']))
        self.display.display_surf.blit(shape_surf, bottom_bar)

    def drawMazeContainer(self):
        """! Funkcja tworząca kontener labiryntu
        """
        self.maze_container = pygame.Rect(
            self.display.display_surf_width - self.display.display_surf_height * self.ui_propotions['maze_container']['height'] - self.display.display_surf_width * self.ui_propotions['maze_container']['pos_x'],
            self.display.display_surf_height * self.ui_propotions['maze_container']['pos_y'], 
            self.display.display_surf_height * self.ui_propotions['maze_container']['width'], 
            self.display.display_surf_height * self.ui_propotions['maze_container']['height'])
        self.maze_surf = pygame.Surface(pygame.Rect(self.maze_container).size, pygame.SRCALPHA)
        pygame.draw.rect(self.maze_surf, self.colors['maze_container'],  self.maze_surf.get_rect(), border_radius=self.ui_propotions['border_radius'])
        self.display.display_surf.blit( self.maze_surf, self.maze_container)

    def drawMaze(self):
        """! Funkcja rysująca ścieżki, ściany oraz mapę przejścia przez labirynt
        """
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
        """! Funkcja tworząca instancję przycisku menu
        """
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
        """! Funkcja tworząca kontenery na oddzielne menu 
        """
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
        ## Kontener grupy przycisków służących do generowania labiryntu
        self.menu_container = createContainer(self.ui_propotions['side_menu'], "Generate")
        ## Kontener grupy przycisków służących do kontroli generowania labiryntu
        self.control_menu_container = createContainer(self.ui_propotions['control_menu'], "GenerateControl")
        ## Kontener grupy przycisków służących do rozwiązywania labiryntu
        self.solve_container = createContainer(self.ui_propotions['solve_menu'], "Solve")
        ## Kontener grupy przycisków służących do zmiany ustawień
        self.settings_container = createContainer(self.ui_propotions['settings_menu'], "Settings")
        ## Kontener grupy przycisków służących do kontroli rozwiązywania labiryntu
        self.solve_control_container = createContainer(self.ui_propotions['solve_control_menu'], "SolveControl")

        def switchMenuSurface(category):
            """! Funkcja przyporządkowywująca grupie przycisków kontener, w którym ten ma się znajdować
            """
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

    def drawUI(self):
        """! Funkcja unifikacyjna do zbiorczego rysowania wszystkich elementów ui
        """
        self.drawBackground()
        self.drawInfoBars()
        self.drawMenuCointainers()
        self.drawMazeContainer()
        self.drawMaze()

    def rect_round(self, x1, y1, w, h):
      """! Funkcja zaokrąglająca wymiary z postaci zmienno-przecinkowej do stało-przecinkowej, jednocześnie nie zmniejszająć wymiarów
      """
      r_x1 = round(x1)
      r_y1 = round(y1)
      r_w = round(x1 - r_x1 + w)
      r_h = round(y1 - r_y1 + h)
      return pygame.Rect(r_x1, r_y1, r_w, r_h)
