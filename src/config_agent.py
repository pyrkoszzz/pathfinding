import yaml
import pygame

class ConfigAgent():

    """! Klasa jest odpowiedzialna za zarządzanie konfiguracją aplikacji. 
    Jej głównym zadaniem jest odczytywanie i udostępnianie ustawień konfiguracyjnych, 
    które mogą być wykorzystywane przez inne komponenty i moduły w aplikacji. 
    Klasa ułatwia manipulację konfiguracją, zapewniając elastyczne metody dostępu i modyfikacji ustawień.
    """
    
    def __init__(self):

        """! Konstruktor klasy konfiguracji.
        Inicjalizuje zmienne i komponenty używane w aplikacji.
        
        @return  Instancja klasy ConfigAgent zainicjalizowana podaną nazwą.
        """

        self.config = self.loadConfig()

    def loadConfig(self):

        """! Funkcja wczytująca plik konfiguracyjny YAML

        @return Zwraca obiekt pliku konfiguracyjnego
        """

        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
            return config
    
    def setDisplayMode(self):
        """! Funkcja ustawiająca rozmiar wyświetlanego okna aplikacji
        @return Zwraca docelowy rozmiar okna aplikacji 
        """
        if self.config['display']['mode'] == 0:
            return pygame.FULLSCREEN
        elif self.config['display']['mode'] == 1:
            return (1280, 720)
    
    def getMainBackgroundPath(self):
        """! Funkcja unifikacjyna
        @return Docelowy obiekt zawierający konfigurację dotyczącą tła aplikacji
        """
        return self.config['assets']['background']
    
    def getMainFontPath(self):
        """! Funkcja unifikacjyna
        @return Docelowy obiekt zawierający konfigurację dotyczącą czcionki aplikacji
        """
        return self.config['assets']['font']

    def getPropotionsDict(self):
        """! Funkcja unifikacjyna
        @return Docelowy obiekt zawierający konfigurację dotyczącą rozmieszczenia elementów w oknie aplikacji
        """
        return self.config['ui_propotions']
    
    def getColors(self):
        """! Funkcja unifikacjyna
        @return Docelowy obiekt zawierający konfigurację dotyczącą kolorów używanych w aplikacji
        """
        return self.config['colors']
    
    def getTexts(self):
        """! Funkcja unifikacjyna
        @return Docelowy obiekt zawierający konfigurację dotyczącą wyświetlanych napisów w aplikacji
        """
        return self.config['text']
    
    def getStates(self):
        """! Funkcja unifikacjyna
        @return Docelowy obiekt zawierający konfigurację dotyczącą dopuszczalnych stanów aplikacji
        """
        return self.config['text']['state']
    
    def getConstants(self):
        """! Funkcja unifikacjyna
        @return Docelowy obiekt zawierający konfigurację dotyczącą stałych używanych w aplikacji
        """
        return self.config['constants']