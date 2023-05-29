import config_agent
import display_agent
import event_agent
import assets_manager
import maze_agent
import solve_agent
import state_agent


class App:


    """! Główna klasa aplikacji.
    reprezentuje główną aplikację, która zarządza logiką i interakcją z użytkownikiem. 
    Jest to klasa centralna, która integruje różne komponenty i funkcje aplikacji. 
    Główna klasa aplikacji jest odpowiedzialna za uruchomienie programu, obsługę wejścia/wyjścia, 
    zarządzanie danymi, przetwarzanie logiki i interakcję z innymi komponentami aplikacji.
    """

    def __init__(self):

        """! Konstruktor klasy aplikacji.
        Inicjalizuje zmienne i komponenty używane w aplikacji.
        
        @return  Instancja klasy App zainicjalizowana podaną nazwą.
        """

        ## Zarządzanie stanem aplikacji - gdy zostanie wywołana akcja 
        # zamknięcia następuje wcześniejsze zwalnianie pamięci oraz
        # destrukcja pozostałych obiektów 
        self.running = True
        ## Instancja agenta odpowiedzialnego za operacje na plikach konfiguracyjnych
        self.config_agent = config_agent.ConfigAgent()
        ## Instancja agenta odpowiedzialnego za zarządzanie interfejsem użytkownika
        self.display_agent = display_agent.DisplayAgent(self)
        ## Instancja agenta odpowiedzialnego za operacje na plikach wykorzystywanych przez apliakcję
        self.assets_manager = assets_manager.AssetsManager(self)
        ## Instancja agenta odpowiedzialnego za przetwarzanie działań wejściowych
        self.event_agent = event_agent.EventAgent(self)
        ## Instancja agenta odpowiedzialnego za operacje na labiryntach
        self.maze_agent = maze_agent.MazeAgent(self)
        ## Instancja agenta odpowiedzialnego za wyznaczanie tras w labiryntach
        self.solve_agent = solve_agent.SolveAgent(self)
        ## Instancja agenta odpowiedzialnego za przetwarzanie aktualych statusów aplikacji oraz restrykcji działań w poszczególnych stanach
        self.state_agent = state_agent.StateAgent(self)

if __name__ == "__main__":
    app = App()
    app.display_agent.run()