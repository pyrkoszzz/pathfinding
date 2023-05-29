class StateAgent:

    """! Klasa StateAgent jest odpowiedzialna za zarządzanie stanem aplikacji. 
    Służy do śledzenia i aktualizowania informacji dotyczących stanu labiryntu.
    Klasa StateAgent zapewnia interfejs do manipulacji stanem labiryntu, co umożliwia 
    śledzenie postępów rozwiązania i wyświetlanie aktualnych informacji użytkownikowi.
    """

    def __init__(self, app_instance):

        """! Konstruktor klasy obsługi stanów labiryntówi aplikacji.
		Inicjalizuje zmienne i komponenty używane w aplikacji.
		
		@return  Instancja klasy StateAgent zainicjalizowana podaną nazwą.
		"""
        
        ## Obiekt bazowej klasy aplikacji
        self.app = app_instance
        ## Obiekt zawierający dopuszczale stany aplikacji
        self.states = self.app.config_agent.getStates()
        ## Status aplikacji
        self.state = None
        ## Ustawienie początkowego stanu
        self.updateState("waiting")
        ## Wiadomość dla użytkownika
        self.log = ""

    def canMazeBeSolved(self):

        """! Funkcja sprawdzająca, czy jest możliwe wykonanie operacji rozwiązywania labiryntu
        @return Możliwość wykonania operacji
        """

        return self.state == self.states['generated'] or self.state == self.states['solved']
    
    def canMazeBeExported(self):

        """! Funkcja sprawdzająca, czy jest możliwe wykonanie operacji eksportu labiryntu do pliku
        @return Możliwość wykonania operacji
        """

        return self.state == self.states['generated'] or self.state == self.states['solved']
    
    def canPointBePicked(self):

        """! Funkcja sprawdzająca, czy jest możliwe wykonanie operacji wyboru wierzchołka startowego i końcowego
        @return Możliwość wykonania operacji
        """

        return self.state == self.states['generated'] or self.state == self.states['solved']
    
    def updateState(self, state_key):

        """! Funkcja aktualizująca stan aplikacji
        """

        self.state = self.states[state_key]