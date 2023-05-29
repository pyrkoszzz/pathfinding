import pygame
import os 

class AssetsManager:
    
    """! Klasa odpowiedzialna za zarządzanie aktywami (zasobami) w aplikacji. 
    Służy do przechowywania, różnych typów aktywów, takich jak obrazy, czcionki 
    Głównym celem klasy AssetsManager jest ułatwienie dostępu do aktywów i zapewnienie spójności w ich zarządzaniu.
    """

    def __init__(self,app_instance):

        """! Konstruktor klasy do zarządzania zasobami.
        Inicjalizuje zmienne i komponenty używane w aplikacji.
        
        @return  Instancja klasy AssetsManager zainicjalizowana podaną nazwą.
        """
        ## Obiekt bazowej klasy aplikacji
        self.app = app_instance
        ## Obiekt tła aplikacji
        self.main_background = pygame.image.load(os.path.join(*self.app.config_agent.getMainBackgroundPath()))
        ## Obiekt czcionki wykorzystywanej w aplikacji
        self.main_font = os.path.join(*self.app.config_agent.getMainFontPath())
        self.rescaleAssets()
    
    def rescaleAssets(self):

        """! Funkcja skalująca obrazy względem aktualnego rozmiaru okna aplikacji
        """

        self.main_background = pygame.transform.scale(self.main_background, self.app.display_agent.display_surf_size)