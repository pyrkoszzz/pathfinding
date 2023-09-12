# PathFinding

## Cel, idea, założenia

Celem tego projektu jest badanie i porównanie dwóch popularnych
algorytmów generowania labiryntów - Kruskala i Prima, oraz algorytmu DFS
(Depth-First Search) do znajdowania ścieżki w tych labiryntach. Projekt
koncentruje się na zastosowaniu tych algorytmów w kontekście generowania
labiryntów w aplikacjach komputerowych.

### Idea projektu

Idea projektu polega na eksploracji i analizie efektywności oraz różnic
w generowaniu labiryntów przy użyciu algorytmów Kruskala i Prima. Obie
metody opierają się na tworzeniu minimalnego drzewa spinającego dla
danego grafu, ale różnią się w podejściu do wyboru kolejnych krawędzi.
Przedstawię, jakie są zalety i wady obu algorytmów, jak wpływają na
strukturę labiryntu oraz jak generują różne rodzaje labiryntów.

### Założenia projektu

1.  Implementacja algorytmu Kruskala: Przeprowadzę badania nad
    algorytmem Kruskala, który wykorzystuje losowe wybieranie krawędzi i
    sprawdzanie, czy utworzą one cykl w grafie. Zbadam, jak dobrze
    generuje labirynty o różnym stopniu złożoności i konfiguracji
    ścieżek.

2.  Implementacja algorytmu Prima: Przeprowadzę badania nad algorytmem
    Prima, który wybiera losowe krawędzie, ale skupia się na rozwijaniu
    drzewa od jednego wierzchołka. Zbadam, jakie labirynty generuje ten
    algorytm i jak różnią się od tych generowanych przez Kruskala.

3.  Implementacja algorytmu DFS: Wykorzystam algorytm DFS do znajdowania
    ścieżki w wygenerowanych labiryntach. Będę analizować skuteczność i
    efektywność algorytmu DFS w odnajdywaniu ścieżek w różnych
    konfiguracjach labiryntu.

4.  Stworzenie interfejsu graficznego: Projekt zakłada stworzenie
    interfejsu graficznego, który umożliwi użytkownikowi interakcję z
    generowanymi labiryntami oraz znajdowanie ścieżek między wybranymi
    punktami. Interfejs graficzny powinien umożliwić wizualizację
    labiryntów, wybieranie punktu startowego i końcowego, oraz
    prezentację znalezionej ścieżki. Dzięki interaktywnemu interfejsowi,
    użytkownik będzie miał możliwość eksperymentowania z różnymi
    ustawieniami labiryntu i obserwować, jak algorytmy generują
    labirynty oraz znajdują ścieżki.

5.  Możliwość importowania i eksportowania labiryntów: Projekt zakłada
    dodanie funkcjonalności umożliwiającej importowanie i eksportowanie
    labiryntów w różnych formatach. Użytkownik będzie mógł zaimportować
    zewnętrzny labirynt lub eksportować wygenerowany labirynt w celu
    dalszego wykorzystania.

### Podsumowanie

W ramach tego projektu udało się zrealizować wszystkie założenia.
Przeprowadzono badania i porównano efektywność generowania labiryntów za
pomocą algorytmów Kruskala i Prima. Analizowano różnice w strukturze
generowanych labiryntów oraz zbadano skuteczność algorytmu DFS w
odnajdywaniu ścieżek w tych labiryntach. Dodatkowo, stworzono interfejs
graficzny, który umożliwia użytkownikowi interakcję z labiryntem.
Interfejs pozwala na manipulację labiryntem, wybieranie punktów
startowego i końcowego oraz wyświetlanie znalezionej ścieżki. Użytkownik
ma możliwość eksplorowania różnych ustawień labiryntu i obserwowania
generacji oraz rozwiązania labiryntów. W ramach projektu dodano również
funkcjonalność importowania i eksportowania labiryntów. Użytkownik ma
możliwość importowania labiryntów z zewnętrznych plików oraz
eksportowania wygenerowanych labiryntów. Realizacja wszystkich założeń
projektu pozwoliła na pełne zbadanie generowania labiryntów oraz
znajdowania ścieżek. Projekt dostarcza kompletnego rozwiązania, które
może być wykorzystane w różnych aplikacjach.

## Charakterystyka modelu

### Opis rozwiązywanego problemu

Model został stworzony w celu rozwiązania problemu generowania
labiryntów oraz znajdowania ścieżek w tych labiryntach. Problem
generowania labiryntów polega na wygenerowaniu struktury labiryntu,
która składa się z komórek i ścian. Celem jest stworzenie labiryntu o
określonych właściwościach, takich jak złożoność, liczba ścieżek czy
konfiguracja przeszkód. Problem znajdowania ścieżek polega na
odnalezieniu najkrótszej ścieżki pomiędzy dwoma punktami w labiryncie.

### Opis zastosowanych algorytmów

1.  Algorytm Kruskala: Algorytm Kruskala jest wykorzystywany do
    generowania labiryntów. Opiera się na połączeniu losowych krawędzi
    bez tworzenia cykli. Algorytm rozpoczyna się od wylosowania
    wszystkich ścian jako osobnych komórek, a następnie łączy losowo
    wybrane krawędzie, aż do utworzenia jednego spójnego labiryntu.
    Algorytm Kruskala generuje labirynt o losowej strukturze i
    równomiernie rozproszonej liczbie ścieżek.

2.  Algorytm Prima: Algorytm Prima również służy do generowania
    labiryntów. Opiera się na rozwijaniu drzewa od jednego wierzchołka
    poprzez dodawanie najkrótszych krawędzi. Algorytm rozpoczyna się od
    wybrania losowego wierzchołka, a następnie dołącza do drzewa
    najkrótszą krawędź z nieodwiedzonych wierzchołków. Proces powtarza
    się, aż wszystkie wierzchołki zostaną odwiedzone. Algorytm Prima
    generuje labirynt o bardziej \"zorganizowanej\" strukturze, z
    koncentracją ścieżek wokół punktu startowego.

3.  Algorytm DFS (Depth-First Search): Algorytm DFS jest wykorzystywany
    do znajdowania ścieżek w wygenerowanych labiryntach. Algorytm
    rozpoczyna się od wybranego punktu startowego i przeszukuje labirynt
    w głąb, eksplorując jedną ścieżkę aż do momentu, gdy nie można już
    kontynuować. Następnie cofa się i wybiera inną nieodwiedzoną
    ścieżkę. Proces powtarza się aż do odnalezienia ścieżki do punktu
    docelowego. Algorytm DFS znajduje ścieżki w labiryntach, jednak nie
    gwarantuje znalezienia najkrótszej ścieżki.

Zastosowane algorytmy Kruskala i Prima umożliwiają generowanie
różnorodnych labiryntów o różnej strukturze i złożoności. Algorytm DFS
jest wykorzystywany do znalezienia ścieżek w tych labiryntach, jednak
nie zapewnia optymalnej ścieżki. Kombinacja tych algorytmów pozwala na
generowanie labiryntów oraz odnajdywanie ścieżek w sposób efektywny i
zgodny z założeniami projektu.

## Środowisko

Program został stworzony w środowisku VS Code przy użyciu kilku
bibliotek, głównie pygame i pyyaml. Do implementacji interfejsu
graficznego oraz obsługi zdarzeń, takich jak kliknięcia myszką czy
klawisze, wykorzystano bibliotekę pygame. Dzięki niej możliwe jest
wyświetlanie labiryntów w oknie programu, obsługa akcji użytkownika oraz
wizualizacja generacji i rozwiązania labiryntów. Biblioteka pyyaml
została wykorzystana do wczytywania plików konfiguracyjnych, które
definiują różne ustawienia aplikacji. Dzięki temu, użytkownik może łatwo
dostosować parametry poprzez modyfikację pliku konfiguracyjnego w
formacie YAML. Wykorzystanie pliku konfiguracyjnego pozwala na łatwą
modyfikację ustawień bez konieczności ingerencji w kod programu. Dzięki
zastosowaniu środowiska VS Code oraz bibliotek pygame i pyyaml, program
dostarcza wygodne i efektywne narzędzia do generowania, rozwiązywania
oraz manipulacji labiryntami. Użycie pliku konfiguracyjnego umożliwia
elastyczność w dostosowywaniu ustawień aplikacji, a interfejs graficzny
zapewnia interaktywną i przyjazną dla użytkownika obsługę labiryntów.

## Instrukcja uruchomienia

Do uruchomienia aplikacji wymagana jest instalacja Pythona w wersji 3.10
oraz posiadanie zainstalowanych bibliotek znajdujących się w pliku
requirements.txt

1.  pygame==2.4.0

2.  PyYAML==6.0

### Instalacja

Instalacja bibliotek odbywa się poprzez wykonanie komendy

    python3 -m pip install -r requirements.txt

### Uruchomienie aplikacji

W celu uruchomienia aplikacji, należy wykonać polecenie

    python3 app.py

Aplikacja powinna się uruchomić i wyświetlić interfejs graficzny oraz
zacząć oczekiwać na interakcję z użytkownikiem. Należy korzystać z
funkcji aplikacji zgodnie z jej przeznaczeniem, np. generować labirynty,
znajdować ścieżki, eksplorować różne opcje.

### Użytkowanie

Aplikacja zapewnia użytkownikowi interaktywne menu, które umożliwia
wybór odpowiednich algorytmów generujących labirynty, algorytmów
szukających ścieżki oraz dostosowanie ustawień aplikacji. Poniżej
przedstawony opis poszczególnych menu i ich funkcjonalności:

1.  Menu wyboru algorytmu generującego: Umożliwia użytkownikowi wybór
    preferowanego algorytmu generowania labiryntu, takiego jak algorytm
    Kruskala lub algorytm Prima. Użytkownik może wybrać jeden z
    dostępnych algorytmów, które zostaną użyte do generowania labiryntu.

2.  Menu kontroli algorytmu generującego: Daje użytkownikowi kontrolę
    nad procesem generowania labiryntu. Użytkownik może uruchomić
    generowanie, zatrzymać je lub przechodzić \"krok po kroku\".

3.  Menu wyboru algorytmu szukającego ścieżki: To menu pozwala
    użytkownikowi wybrać preferowany algorytm do znajdowania ścieżki w
    wygenerowanym labiryncie. Użytkownik może wybrać algorytm BFS, który
    zostanie użyty do odnalezienia ścieżki w labiryncie.

4.  Menu kontroli algorytmu szukającego ścieżki: To interaktywne menu
    umożliwia użytkownikowi kontrolowanie procesu szukania ścieżki w
    labiryncie. Użytkownik może rozpocząć szukanie ścieżki, zatrzymać je
    lub przechodzić \"krok po kroku\".

5.  Menu ustawień aplikacji:

    1.  Czyszczenie ścieżki - wybranie tej opcji spowoduje usunięcie
        tylko znalezionej ścieżki w labiryncie, pozostawiając ściany i
        inne elementy nienaruszone. Ta opcja jest przydatna, gdy
        użytkownik chce zachować wygenerowany labirynt, ale chce
        zresetować tylko znalezioną ścieżkę.

    2.  Czyszczenie labiryntu - wszystkie ściany labiryntu zostaną
        usunięte, przywracając go do stanu początkowego.

    3.  Import - opcja umożliwia użytkownikowi importowanie labiryntu z
        zewnętrznego pliku. Użytkownik może wybrać odpowiedni plik z
        labiryntem do zaimportowania, co pozwala na łatwe wczytywanie i
        korzystanie z gotowych labiryntów.

    4.  Eksport - opcja umożliwia użytkownikowi eksportowanie aktualnego
        stanu labiryntu do pliku. Jest to przydatne, gdy użytkownik chce
        zapisać wygenerowany labirynt i udostępnić go innym
        użytkownikom.

    5.  Wyjście - wybranie tej opcji spowoduje zamknięcie aplikacji.

Wybór punktów w labiryncie,
pomiędzy którymi algorytm będzie wyszukiwał ścieżkę odbywa się poprzez:

-   Lewy przycisk myszki, aby ustawić punkt startowy (oznaczony kolorem
    zielonym)

-   Prawy przycisk myszki, aby ustawić punkt końcowy (oznaczony kolorem
    czerwonym)

Ustawienie punktów możliwe jest jedynie, gdy labirynt został już
wygenerowany i aktualnie nie jest szukana ścieżka
