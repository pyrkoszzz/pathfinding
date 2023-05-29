import pygame
import math
import time
import tkinter as tk
from tkinter import filedialog

class EventAgent():

    """! Klasa jest odpowiedzialna za zarządzanie zdarzeniami (eventami) w aplikacji. 
    Służy do przechwytywania, przetwarzania i reagowania na różne rodzaje zdarzeń, takich jak kliknięcia myszy, naciśnięcia klawiszy, zmiany stanu aplikacji itp. 
    Głównym celem klasy jest monitorowanie i obsługa zdarzeń, które występują w trakcie działania aplikacji.
    """

    def __init__(self, app_instance):

        """! Konstruktor klasy obsługi zdarzeń.
        Inicjalizuje zmienne i komponenty używane w aplikacji.
        
        @return  Instancja klasy EventAgent zainicjalizowana podaną nazwą.
        """

        ## Obiekt bazowej klasy aplikacji
        self.app = app_instance
        ## Aktualna akcja do wykonania (asynchronicznie)
        self.action = None
        ## Obiekt zawierający stałe używanye w aplikacji
        self.constants = self.app.config_agent.getConstants()

    def handleEvent(self,event, m_pos):

        """! Główna funkcja przetwarzająca akcje użytkownika
        """

        if event.type == pygame.QUIT:
            self.app.running = False 
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handleActionButtons(event, m_pos)
            self.handlePointsChoice(event, m_pos)
            
            
    def handleActionButtons(self, event, m_pos):
        """! Funkcja rozpoznająca przycisk, który został kliknięty przez użytkownika
        """
        if event.button == 1:
            for action, collider in self.app.display_agent.action_buttons.items():
                    if collider is not None and collider.collidepoint(m_pos):
                        self.executeAction(action)

    def handlePointsChoice(self, event, m_pos):
        """! Funkcja rozpoznająca wierzchołek labiryntu, który został wybrany przez użytkownika
        """
        if self.app.state_agent.canPointBePicked() and self.app.maze_agent.maze != None and len(self.app.maze_agent.maze[0]) > 0:
            it = range(len(self.app.maze_agent.maze[0])) 
            for x in it:
                for y in it:
                    tmp = self.app.display_agent.maze_path_colliders[y][x]
                    if tmp is not None:
                        if tmp.collidepoint(m_pos):
                            if event.button == 1:
                                if self.app.solve_agent.e_v != (y,x) and self.app.maze_agent.maze[y][x]:
                                    self.app.solve_agent.s_v = (y,x)
                                    self.app.solve_agent.starting_v = int(math.sqrt(self.app.maze_agent.maze_size)) * (y//2) + (x//2)
                            elif event.button == 3:
                                if self.app.solve_agent.s_v != (y,x) and self.app.maze_agent.maze[y][x]:
                                    self.app.solve_agent.e_v = (y,x)
                                    self.app.solve_agent.ending_v = int(math.sqrt(self.app.maze_agent.maze_size)) * (y//2) + (x//2)

    def executeAction(self, action):
        """! Funkcja uruchamiająca odpowiednie akcje względem przycisku, który został kliknięty przez użytkownika
        """
        if action == "Exit":
            self.app.running = False
        elif action == "Kruskal":
            self.app.solve_agent.maze_path = None
            self.app.maze_agent.initializeKruskal()
        elif action == "Prim":
            self.app.solve_agent.maze_path = None
            self.app.maze_agent.initializePrim()
        elif action == "Next step":
            self.app.maze_agent.nextStep()
        elif action == "Fast generate":
            self.action = self.app.maze_agent.fastForward
        elif action == "Solve DFS" and self.app.state_agent.canMazeBeSolved():
            self.app.solve_agent.initializeDFS()
        elif action == "Clear maze":
            self.app.maze_agent.maze = None
            self.app.solve_agent.maze_path = None
        elif action == "Clear path":
            self.app.solve_agent.maze_path = None
        elif action == "Next step solve":
            self.app.solve_agent.nextStep()
        elif action == "Fast solve":
            self.action = self.app.solve_agent.fastForward
        elif action == "Stop solving" or action == "Stop generating":
            self.action = None
        elif action == "Size +":
            self.app.maze_agent.maze_size = int(math.pow(math.sqrt(self.app.maze_agent.maze_size) + 1, 2))
            self.app.solve_agent.ending_v = self.app.maze_agent.maze_size-1
            self.app.solve_agent.e_v = (2*int(math.sqrt(self.app.maze_agent.maze_size))-2, 2*int(math.sqrt(self.app.maze_agent.maze_size))-2)
        elif action == "Size -":
            self.app.maze_agent.maze_size = int(math.pow(math.sqrt(self.app.maze_agent.maze_size) - 1, 2))
            self.app.solve_agent.ending_v = self.app.maze_agent.maze_size-1
            self.app.solve_agent.e_v = (2*int(math.sqrt(self.app.maze_agent.maze_size))-2, 2*int(math.sqrt(self.app.maze_agent.maze_size))-2)
        elif action == "Export":
            if self.app.state_agent.canMazeBeExported():
                self.exportToFile()
        elif action == "Import":
            self.app.solve_agent.maze_path = None
            self.importFromFile()

    def executeActionsQueue(self):
        """! Funkcja wykonująca zadanie z kolejki 
        """
        if self.action is not None:
            self.action()

    def exportToFile(self):
        """! Funkcja eksportująca labirynt do pliku .maze
        """
        fname = "../" + str(int(time.time())) + ".maze"
        with open(fname, "w") as f:
            f.write(str(self.app.maze_agent.maze_size) + '\n')
            for u,v,w in self.app.maze_agent.graph:
                f.write("%d %d %d\n" % (u,v,w))
            f.close()
            self.app.state_agent.log = "Maze exported successfully"
    
    def importFromFile(self):
        """! Funkcja importująca labirynt z pliku .maze
        """
        self.app.state_agent.log = "Maze import started"
        self.app.state_agent.updateState("generating")
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        root.quit()
        with open(file_path, "r") as f:
            self.app.maze_agent.importMaze(f)
        

