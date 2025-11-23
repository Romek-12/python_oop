# CONWAY'S GAME OF LIFE
# Symulacja automatu komórkowego w Pygame
# Implementacja z użyciem programowania obiektowego
# Autor: [Student]
# Data: 2025-11-21

# Importowanie niezbędnych bibliotek
import pygame  # Główna biblioteka do tworzenia gier i grafiki
import sys     # Do zarządzania systemem (wyjście z programu)
import random  # Do generowania losowych stanów początkowych

# STAŁE GRY - wartości konfiguracyjne
WINDOW_WIDTH = 800      # Szerokość okna w pikselach
WINDOW_HEIGHT = 600     # Wysokość okna w pikselach
CELL_SIZE = 10          # Rozmiar jednej komórki w pikselach
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE   # Liczba komórek w poziomie
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE # Liczba komórek w pionie

# KOLORY (RGB)
BLACK = (0, 0, 0)       # Kolor tła i martwych komórek
WHITE = (255, 255, 255) # Kolor żywych komórek
GRAY = (128, 128, 128)  # Kolor siatki


# KLASA KOMÓRKI - reprezentuje pojedynczą komórkę w siatce
class Cell:
    def __init__(self, x, y, alive=False):
        """Konstruktor komórki
        Args:
            x (int): Pozycja w siatce (kolumna)
            y (int): Pozycja w siatce (rząd)
            alive (bool): Czy komórka jest żywa na początku
        """
        self.x = x                    # Pozycja X w siatce
        self.y = y                    # Pozycja Y w siatce
        self.alive = alive            # Aktualny stan (żywa/martwa)
        self.next_state = alive       # Stan w następnej generacji
        
    def set_next_state(self, next_alive):
        """Ustawia stan komórki w następnej generacji
        Args:
            next_alive (bool): Czy komórka będzie żywa w następnej generacji
        """
        self.next_state = next_alive
        
    def update(self):
        """Aktualizuje stan komórki do następnej generacji"""
        self.alive = self.next_state
        
    def toggle(self):
        """Przełącza stan komórki (żywa <-> martwa)"""
        self.alive = not self.alive
        self.next_state = self.alive


# KLASA SIATKI - zarządza wszystkimi komórkami i regułami gry
class Grid:
    def __init__(self, width, height):
        """Konstruktor siatki
        Args:
            width (int): Szerokość siatki (liczba komórek)
            height (int): Wysokość siatki (liczba komórek)
        """
        self.width = width
        self.height = height
        self.generation = 0           # Numer aktualnej generacji
        
        # Tworzenie dwuwymiarowej listy komórek
        self.cells = []
        for y in range(height):
            row = []
            for x in range(width):
                # Każda komórka zaczyna jako martwa
                cell = Cell(x, y, False)
                row.append(cell)
            self.cells.append(row)
    
    def get_cell(self, x, y):
        """Pobiera komórkę na danej pozycji
        Args:
            x, y (int): Współrzędne komórki
        Returns:
            Cell lub None: Komórka lub None jeśli poza siatką
        """
        # Sprawdź czy współrzędne są w granicach siatki
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return None
    
    def count_neighbors(self, x, y):
        """Liczy żywych sąsiadów komórki
        Args:
            x, y (int): Współrzędne komórki
        Returns:
            int: Liczba żywych sąsiadów (0-8)
        """
        count = 0
        
        # Sprawdź wszystkie 8 kierunków wokół komórki
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                # Pomiń samą komórkę (dx=0, dy=0)
                if dx == 0 and dy == 0:
                    continue
                
                # Oblicz pozycję sąsiada
                neighbor_x = x + dx
                neighbor_y = y + dy
                
                # Pobierz sąsiada
                neighbor = self.get_cell(neighbor_x, neighbor_y)
                
                # Jeśli sąsiad istnieje i jest żywy, zwiększ licznik
                if neighbor and neighbor.alive:
                    count += 1
        
        return count
    
    def calculate_next_generation(self):
        """Oblicza następną generację według reguł Conway'a
        
        Reguły Game of Life:
        1. Żywa komórka z 2-3 sąsiadami pozostaje żywa
        2. Martwa komórka z dokładnie 3 sąsiadami staje się żywa
        3. W pozostałych przypadkach komórka umiera lub pozostaje martwa
        """
        # Przejdź przez wszystkie komórki
        for y in range(self.height):
            for x in range(self.width):
                cell = self.cells[y][x]
                neighbors = self.count_neighbors(x, y)
                
                # Zastosuj reguły Conway'a
                if cell.alive:
                    # Komórka żywa
                    if neighbors == 2 or neighbors == 3:
                        cell.set_next_state(True)   # Pozostaje żywa
                    else:
                        cell.set_next_state(False)  # Umiera (za mało lub za dużo sąsiadów)
                else:
                    # Komórka martwa
                    if neighbors == 3:
                        cell.set_next_state(True)   # Narodziny
                    else:
                        cell.set_next_state(False)  # Pozostaje martwa
    
    def update(self):
        """Aktualizuje siatkę do następnej generacji"""
        self.calculate_next_generation()
        
        # Zaktualizuj wszystkie komórki
        for y in range(self.height):
            for x in range(self.width):
                self.cells[y][x].update()
        
        # Zwiększ numer generacji
        self.generation += 1
    
    def toggle_cell(self, x, y):
        """Przełącza stan komórki na danej pozycji
        Args:
            x, y (int): Współrzędne komórki
        """
        cell = self.get_cell(x, y)
        if cell:
            cell.toggle()
    
    def randomize(self, probability=0.3):
        """Losowo ustawia stan komórek
        Args:
            probability (float): Prawdopodobieństwo że komórka będzie żywa (0.0-1.0)
        """
        for y in range(self.height):
            for x in range(self.width):
                # Losowo decyduj czy komórka ma być żywa
                self.cells[y][x].alive = random.random() < probability
                self.cells[y][x].next_state = self.cells[y][x].alive
        
        # Zresetuj licznik generacji
        self.generation = 0
    
    def clear(self):
        """Czyści siatkę (wszystkie komórki stają się martwe)"""
        for y in range(self.height):
            for x in range(self.width):
                self.cells[y][x].alive = False
                self.cells[y][x].next_state = False
        
        self.generation = 0


# KLASA RENDERERA - odpowiedzialna za rysowanie na ekranie
class Renderer:
    def __init__(self, screen, cell_size):
        """Konstruktor renderera
        Args:
            screen: Powierzchnia Pygame do rysowania
            cell_size (int): Rozmiar komórki w pikselach
        """
        self.screen = screen
        self.cell_size = cell_size
        self.font = pygame.font.Font(None, 36)  # Czcionka do tekstu
    
    def draw_grid(self, grid):
        """Rysuje siatkę komórek
        Args:
            grid (Grid): Siatka do narysowania
        """
        # Wyczyść ekran
        self.screen.fill(BLACK)
        
        # Rysuj wszystkie komórki
        for y in range(grid.height):
            for x in range(grid.width):
                cell = grid.cells[y][x]
                
                # Oblicz pozycję komórki na ekranie
                rect_x = x * self.cell_size
                rect_y = y * self.cell_size
                
                # Wybierz kolor na podstawie stanu komórki
                color = WHITE if cell.alive else BLACK
                
                # Narysuj komórkę
                pygame.draw.rect(self.screen, color, 
                               (rect_x, rect_y, self.cell_size, self.cell_size))
                
                # Narysuj ramkę komórki (opcjonalnie)
                pygame.draw.rect(self.screen, GRAY, 
                               (rect_x, rect_y, self.cell_size, self.cell_size), 1)
    
    def draw_ui(self, grid, paused):
        """Rysuje interfejs użytkownika
        Args:
            grid (Grid): Siatka (do pobrania informacji o generacji)
            paused (bool): Czy symulacja jest wstrzymana
        """
        # Informacje o stanie gry
        generation_text = self.font.render(f"Generation: {grid.generation}", True, WHITE)
        status_text = self.font.render("PAUSED" if paused else "RUNNING", True, WHITE)
        
        # Instrukcje
        instructions = [
            "SPACE - Play/Pause",
            "R - Randomize", 
            "C - Clear",
            "Click - Toggle cell"
        ]
        
        # Rysuj teksty
        self.screen.blit(generation_text, (10, 10))
        self.screen.blit(status_text, (10, 50))
        
        # Rysuj instrukcje
        for i, instruction in enumerate(instructions):
            text = pygame.font.Font(None, 24).render(instruction, True, WHITE)
            self.screen.blit(text, (10, WINDOW_HEIGHT - 100 + i * 20))


# GŁÓWNA KLASA GRY - zarządza całą aplikacją
class GameOfLife:
    def __init__(self):
        """Konstruktor głównej klasy gry"""
        # Inicjalizacja Pygame
        pygame.init()
        
        # Tworzenie okna
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Conway's Game of Life")
        
        # Zegar do kontroli FPS
        self.clock = pygame.time.Clock()
        
        # Komponenty gry
        self.grid = Grid(GRID_WIDTH, GRID_HEIGHT)
        self.renderer = Renderer(self.screen, CELL_SIZE)
        
        # Stan gry
        self.running = True    # Czy aplikacja działa
        self.paused = True     # Czy symulacja jest wstrzymana
        self.speed = 10        # Prędkość symulacji (generacji na sekundę)
        
        # Losowy stan początkowy
        self.grid.randomize(0.25)
    
    def handle_events(self):
        """Obsługuje zdarzenia (klawisze, mysz, zamknięcie okna)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Użytkownik zamknął okno
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Spacja - przełącz pauzę
                    self.paused = not self.paused
                
                elif event.key == pygame.K_r:
                    # R - losowy stan
                    self.grid.randomize()
                    self.paused = True
                
                elif event.key == pygame.K_c:
                    # C - wyczyść siatkę
                    self.grid.clear()
                    self.paused = True
                
                elif event.key == pygame.K_ESCAPE:
                    # Escape - wyjście
                    self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Lewy przycisk myszy
                    # Przełącz komórkę pod kursorem
                    mouse_x, mouse_y = event.pos
                    grid_x = mouse_x // CELL_SIZE
                    grid_y = mouse_y // CELL_SIZE
                    
                    self.grid.toggle_cell(grid_x, grid_y)
    
    def update(self):
        """Aktualizuje stan gry"""
        # Aktualizuj siatkę tylko jeśli gra nie jest wstrzymana
        if not self.paused:
            self.grid.update()
    
    def render(self):
        """Rysuje całą scenę"""
        # Narysuj siatkę
        self.renderer.draw_grid(self.grid)
        
        # Narysuj interfejs użytkownika
        self.renderer.draw_ui(self.grid, self.paused)
        
        # Odśwież ekran
        pygame.display.flip()
    
    def run(self):
        """Główna pętla gry"""
        print("=== CONWAY'S GAME OF LIFE ===")
        print("Sterowanie:")
        print("SPACE - Play/Pause")
        print("R - Randomize")
        print("C - Clear")
        print("Mouse Click - Toggle cell")
        print("ESC - Exit")
        print("=============================")
        
        # Główna pętla
        while self.running:
            # Obsługa zdarzeń
            self.handle_events()
            
            # Aktualizacja logiki
            self.update()
            
            # Renderowanie
            self.render()
            
            # Kontrola prędkości (FPS)
            self.clock.tick(self.speed)
        
        # Zamknięcie Pygame
        pygame.quit()
        sys.exit()


# === URUCHOMIENIE GRY ===
# Ten kod uruchamia się tylko gdy plik jest uruchomiony bezpośrednio
def main():
    """Główna funkcja - tworzy i uruchamia grę"""
    try:
        # Stwórz i uruchom grę
        game = GameOfLife()
        game.run()
    except Exception as e:
        print(f"Błąd: {e}")
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
