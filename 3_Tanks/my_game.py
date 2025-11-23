# TANK BATTLE GAME
# Gra w czołgi - strzelanka 2D stworzona w Pygame
# Autor: [Student]
# Data: 2025-11-21

# Importowanie niezbędnych bibliotek
import pygame  # Główna biblioteka do tworzenia gier
import sys     # Do zarządzania systemem (wyjście z gry)
import random  # Do generowania losowych wartości

# STAŁE GRY - wartości, które nie zmieniają się podczas gry
WIDTH, HEIGHT = 640, 480  # Szerokość i wysokość okna gry w pikselach
TILE_SIZE = 20            # Rozmiar czołgów i gracza w pikselach

# Zmienne globalne dla ruchu czerwonego prostokąta (demonstracja)
speed_x = 2  # Prędkość pozioma
speed_y = 1  # Prędkość pionowa


# KLASA GRACZA - reprezentuje kontrolowany przez użytkownika czołg
class Player:
    def __init__(self, x, y):
        """Konstruktor klasy Player - inicjalizuje gracza na pozycji (x, y)"""
        self.x = x                # Pozycja pozioma gracza
        self.y = y                # Pozycja pionowa gracza
        self.direction = 'UP'     # Kierunek gracza (do ewentualnego użycia)
        self.speed = 3            # Prędkość ruchu gracza (pikseli na klatkę)
        self.health = 3           # Punkty życia gracza
        self.max_health = 3       # Maksymalne punkty życia

    def move(self, keys):
        """Porusza gracza na podstawie wciśniętych klawiszy"""
        # Ruch w lewo (klawisz A) z kontrolą granic ekranu
        if keys[pygame.K_a] and self.x > 0:
            self.x -= self.speed
            self.direction = 'LEFT'
        # Ruch w prawo (klawisz D) z kontrolą granic ekranu
        if keys[pygame.K_d] and self.x < WIDTH - TILE_SIZE:
            self.x += self.speed
            self.direction = 'RIGHT'

    def draw(self, screen):
        """Rysuje gracza na ekranie wraz z paskiem zdrowia"""
        # Rysuj niebieskiego gracza (prostokąt)
        pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, TILE_SIZE, TILE_SIZE))
        
        # Rysuj pasek zdrowia nad graczem
        health_bar_width = TILE_SIZE   # Szerokość paska zdrowia
        health_bar_height = 4          # Wysokość paska zdrowia
        health_ratio = self.health / self.max_health  # Stosunek obecnego do max zdrowia (0.0 - 1.0)
        
        # Kolor paska zależy od ilości zdrowia
        if health_ratio <= 0.33:      # Mało zdrowia = czerwony
            health_color = (255, 0, 0)
        elif health_ratio <= 0.66:    # Średnio zdrowia = żółty
            health_color = (255, 255, 0)
        else:                          # Dużo zdrowia = zielony
            health_color = (0, 255, 0)
        
        # Rysuj tło paska zdrowia (szare)
        pygame.draw.rect(screen, (128, 128, 128), (self.x, self.y - 8, health_bar_width, health_bar_height))
        # Rysuj aktualny poziom zdrowia (kolorowy)
        pygame.draw.rect(screen, health_color, (self.x, self.y - 8, health_bar_width * health_ratio, health_bar_height))
    
    def get_rect(self):
        """Zwraca prostokąt reprezentujący granice gracza (do wykrywania kolizji)"""
        return pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
    
    def take_damage(self):
        """Zadaje 1 punkt obrażeń graczowi
        Zwraca:
            bool: True jeśli gracz umarł (zdrowie <= 0), False w przeciwnym razie
        """
        self.health -= 1
        return self.health <= 0  # Zwróć True jeśli gracz nie ma już zdrowia



# KLASA CZOŁGU WROGA - reprezentuje wrogich czołgów sterowanych przez komputer
class Tank:
    def __init__(self, x, y):
        """Konstruktor klasy Tank - tworzy wrogi czołg na pozycji (x, y)"""
        self.x = x                     # Pozycja pozioma czołgu
        self.y = y                     # Pozycja pionowa czołgu (zwykle zaczyna powyżej ekranu)
        self.direction = 'DOWN'        # Kierunek ruchu (zawsze w dół)
        self.speed = 1                 # Prędkość ruchu (wolniejszy niż gracz)
        self.shoot_timer = 0           # Licznik czasu do następnego strzału
        self.shoot_delay = 120         # Opóźnienie między strzałami (2 sekundy przy 60 FPS)
        self.health = 3                # Punkty życia czołgu
        self.max_health = 3            # Maksymalne punkty życia

    def move(self):
        """Porusza czołg w dół ekranu"""
        if self.direction == 'DOWN':
            self.y += self.speed  # Przesuń w dół o wartość prędkości
    
    def update_shooting(self, tank_bullets):
        """Zarządza strzelaniem czołgu
        Args:
            tank_bullets (list): Lista pocisków czołgów do której dodamy nowy pocisk
        """
        self.shoot_timer += 1  # Zwiększ licznik czasu
        
        # Jeśli minął odpowiedni czas, wystrzel pocisk
        if self.shoot_timer >= self.shoot_delay:
            # Stwórz nowy pocisk na środku czołgu, lecący w dół
            bullet = Bullet(self.x + TILE_SIZE // 2, self.y + TILE_SIZE, 'DOWN')
            tank_bullets.append(bullet)  # Dodaj pocisk do listy
            self.shoot_timer = 0          # Zresetuj licznik czasu

    def draw(self, screen):
        """Rysuje czołg na ekranie wraz z paskiem zdrowia"""
        # Rysuj zielonego czołgu (prostokąt)
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, TILE_SIZE, TILE_SIZE))
        
        # Rysuj pasek zdrowia nad czołgiem (podobnie jak u gracza)
        health_bar_width = TILE_SIZE
        health_bar_height = 4
        health_ratio = self.health / self.max_health
        
        # Kolor paska zależy od ilości zdrowia
        if health_ratio <= 0.33:
            health_color = (255, 0, 0)      # Czerwony
        elif health_ratio <= 0.66:
            health_color = (255, 255, 0)    # Żółty  
        else:
            health_color = (0, 255, 0)      # Zielony
            
        # Rysuj tło i wypełnienie paska zdrowia
        pygame.draw.rect(screen, (128, 128, 128), (self.x, self.y - 8, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, health_color, (self.x, self.y - 8, health_bar_width * health_ratio, health_bar_height))
    
    def get_rect(self):
        """Zwraca prostokąt reprezentujący granice czołgu (do wykrywania kolizji)"""
        return pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
    
    def is_off_screen(self):
        """Sprawdza czy czołg wyjechał poza dolną krawędź ekranu
        Zwraca:
            bool: True jeśli czołg jest poza ekranem
        """
        return self.y > HEIGHT
    
    def take_damage(self):
        """Zadaje 1 punkt obrażeń czołgowi
        Zwraca:
            bool: True jeśli czołg został zniszczony (zdrowie <= 0)
        """
        self.health -= 1
        return self.health <= 0


# KLASA POCISKU - reprezentuje pociski wystrzeliwane przez gracza i czołgi
class Bullet:    
    def __init__(self, x, y, direction):
        """Konstruktor klasy Bullet
        Args:
            x (int): Pozycja pozioma początku pocisku
            y (int): Pozycja pionowa początku pocisku
            direction (str): Kierunek lotu ('UP', 'DOWN', 'LEFT', 'RIGHT')
        """
        self.x = x                    # Pozycja pozioma pocisku
        self.y = y                    # Pozycja pionowa pocisku
        self.direction = direction    # Kierunek lotu pocisku
        self.speed = 5                # Prędkość pocisku (szybszy niż czołgi)
    
    def move(self):
        """Porusza pocisk w jego kierunku"""
        if self.direction == 'UP':
            self.y -= self.speed      # W górę (pociski gracza)
        elif self.direction == 'DOWN':
            self.y += self.speed      # W dół (pociski czołgów)
        elif self.direction == 'LEFT':
            self.x -= self.speed      # W lewo (nie używane obecnie)
        elif self.direction == 'RIGHT':
            self.x += self.speed      # W prawo (nie używane obecnie)
    
    def draw(self, screen):
        """Rysuje pocisk jako żółte kółko na ekranie"""
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 3)
    
    def is_off_screen(self):
        """Sprawdza czy pocisk wyleciał poza granice ekranu
        Zwraca:
            bool: True jeśli pocisk jest poza ekranem (można go usunąć)
        """
        return self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT
    
    def get_rect(self):
        """Zwraca prostokąt reprezentujący pocisk (do wykrywania kolizji)
        Pocisk ma rozmiar 6x6 pikseli wyśrodkowany na jego pozycji
        """
        return pygame.Rect(self.x - 3, self.y - 3, 6, 6)

# FUNKCJE WYKRYWANIA KOLIZJI

def check_collision(rect1, rect2):
    """Sprawdza kolizję między dwoma prostokątami
    Args:
        rect1, rect2: Obiekty pygame.Rect do porównania
    Returns:
        bool: True jeśli prostokąty się przecinają
    """
    return rect1.colliderect(rect2)

def handle_bullet_tank_collisions(bullets, tanks):
    """Obsługuje kolizje między pociskami gracza a czołgami wrogów
    
    Ta funkcja sprawdza czy którykolwiek pocisk gracza trafił w którykolwiek czołg.
    Jeśli tak, usuwa pocisk i zadaje obrażenia czołgowi.
    Jeśli czołg zostaje zniszczony, usuwa go i zwiększa wynik.
    
    Args:
        bullets (list): Lista pocisków gracza
        tanks (list): Lista czołgów wrogów
        
    Returns:
        int: Liczba zniszczonych czołgów w tej klatce
    """
    destroyed_count = 0  # Licznik zniszczonych czołgów
    
    # Iteruj przez kopie list, żeby móc bezpiecznie usuwać elementy
    for bullet in bullets[:]:
        for tank in tanks[:]:
            # Sprawdź kolizję między tym pociskiem a tym czołgiem
            if check_collision(bullet.get_rect(), tank.get_rect()):
                bullets.remove(bullet)  # Usuń pocisk (został zużyty)
                
                # Zadaj obrażenia czołgowi i sprawdź czy został zniszczony
                if tank.take_damage():
                    tanks.remove(tank)     # Usuń zniszczony czołg
                    destroyed_count += 1   # Zwiększ licznik
                    
                break  # Jeden pocisk może trafić tylko jeden czołg
                
    return destroyed_count

def handle_tank_bullet_player_collisions(tank_bullets, player):
    """Sprawdza kolizje między pociskami czołgów a graczem
    
    Args:
        tank_bullets (list): Lista pocisków wystrzeliwanych przez czołgi
        player (Player): Obiekt gracza
        
    Returns:
        bool: True jeśli gracz został zabity tym trafieniem
    """
    for bullet in tank_bullets[:]:
        if check_collision(bullet.get_rect(), player.get_rect()):
            tank_bullets.remove(bullet)  # Usuń pocisk który trafił
            return player.take_damage()   # Zadaj obrażenia i zwróć czy gracz umarł
    return False

def handle_player_tank_collisions(player, tanks):
    """Sprawdza bezpośrednią kolizję między graczem a czołgami
    
    Args:
        player (Player): Obiekt gracza
        tanks (list): Lista czołgów wrogów
        
    Returns:
        bool: True jeśli gracz został zabity tym zderzeniem
    """
    for tank in tanks[:]:
        if check_collision(player.get_rect(), tank.get_rect()):
            return player.take_damage()  # Zadaj obrażenia za zderzenie
    return False

# GŁÓWNA FUNKCJA GRY
def main():
    """Główna funkcja gry - inicjalizuje Pygame i uruchamia pętlę gry"""
    
    # === INICJALIZACJA PYGAME ===
    pygame.init()  # Inicjalizuj wszystkie moduły Pygame
    
    # Stwórz okno gry o określonym rozmiarze
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.setCaption = "Tanks Game"  # Ustaw tytuł okna
    
    # Stwórz obiekt Clock do kontroli liczby klatek na sekundę (FPS)
    clock = pygame.time.Clock()
    
    # === INICJALIZACJA OBIEKTÓW GRY ===
    
    # Stwórz gracza na dole ekranu, na środku
    player = Player(WIDTH // 2, HEIGHT - 50)
    
    # Listy do przechowywania wszystkich obiektów w grze
    bullets = []       # Pociski wystrzeliwane przez gracza
    tanks = []         # Czołgi wrogów
    tank_bullets = []  # Pociski wystrzeliwane przez czołgi
    
    # Dodaj pierwszy czołg wroga na górze ekranu w losowej pozycji poziomej
    tank = Tank(random.randint(0, WIDTH - TILE_SIZE), -TILE_SIZE)
    tanks.append(tank)
    
    # === STAN GRY ===
    game_over = False          # Czy gra się skończyła?
    font = pygame.font.Font(None, 74)        # Duża czcionka do napisów "GAME OVER"
    score_font = pygame.font.Font(None, 36)  # Średnia czcionka do wyniku
    
    # System punktacji
    destroyed_tanks = 0  # Liczba zniszczonych czołgów

    # === GŁÓWNA PĘTLA GRY ===
    # Ta pętla działa w nieskończoność, aż do zamknięcia gry
    while True:
        # === OBSŁUGA ZDARZEŃ ===
        # Sprawdź wszystkie zdarzenia (kliknięcia, naciśnięcia klawiszy itp.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Użytkownik zamknął okno
                pygame.quit()  # Zamknij Pygame
                sys.exit()     # Wyjdź z programu
                
            elif event.type == pygame.KEYDOWN:  # Użytkownik nacisnął klawisz
                # Strzał (spacja) - tylko gdy gra nie jest skończona
                if event.key == pygame.K_SPACE and not game_over:
                    # Stwórz pocisk na środku gracza, lecący w górę
                    bullet = Bullet(player.x + TILE_SIZE // 2, player.y, 'UP')
                    bullets.append(bullet)  # Dodaj pocisk do listy
                    
                # Restart gry (klawisz R) - tylko gdy gra się skończyła
                elif event.key == pygame.K_r and game_over:
                    # Zresetuj wszystkie zmienne gry do stanu początkowego
                    game_over = False
                    destroyed_tanks = 0  # Wyzeruj wynik
                    player = Player(WIDTH // 2, HEIGHT - 50)  # Nowy gracz z pełnym zdrowiem
                    
                    # Wyczyść wszystkie listy obiektów
                    bullets.clear()
                    tank_bullets.clear()
                    tanks.clear()
                    
                    # Stwórz pierwszego czołga
                    tank = Tank(random.randint(0, WIDTH - TILE_SIZE), -TILE_SIZE)
                    tanks.append(tank)

        # Obsługa klawiszy dla gracza (tylko gdy gra nie jest skończona)
        if not game_over:
            keys = pygame.key.get_pressed()
            player.move(keys)
            
            # Aktualizuj pociski
            for bullet in bullets[:]:
                bullet.move()
                if bullet.is_off_screen():
                    bullets.remove(bullet)
            
            # Aktualizuj tanki
            for tank in tanks[:]:
                tank.move()
                tank.update_shooting(tank_bullets)
                if tank.is_off_screen():
                    tanks.remove(tank)
            
            # Aktualizuj pociski tanków
            for bullet in tank_bullets[:]:
                bullet.move()
                if bullet.is_off_screen():
                    tank_bullets.remove(bullet)
            
            # Sprawdź kolizje pocisków gracza z tankami
            destroyed_tanks += handle_bullet_tank_collisions(bullets, tanks)
            
            # Sprawdź kolizje pocisków tanków z graczem
            if handle_tank_bullet_player_collisions(tank_bullets, player):
                print("Gracz został trafiony! Pozostało życie:", player.health)
                if player.health <= 0:
                    game_over = True
            
            # Sprawdź kolizje gracza z tankami
            if handle_player_tank_collisions(player, tanks):
                print("Gracz zderzył się z tankiem! Pozostało życie:", player.health)
                if player.health <= 0:
                    game_over = True
            
            # Dodaj nowy tank jeśli wszystkie zostały zniszczone
            if len(tanks) == 0:
                new_tank = Tank(random.randint(0, WIDTH - TILE_SIZE), -TILE_SIZE)
                tanks.append(new_tank)

        # Przesuń prostokąt
        # rect.x += speed_x
        # rect.y += speed_y

        # Wyczyść ekran
        screen.fill((0, 0, 0))  # czarne tło

        # Narysuj prostokąt
        # pygame.draw.rect(screen, color, rect)
        
        # Narysuj gracza
        player.draw(screen)
        
        # Narysuj tanki
        for tank in tanks:
            tank.draw(screen)
        
        # Narysuj pociski
        for bullet in bullets:
            bullet.draw(screen)
            
        # Narysuj pociski tanków
        for bullet in tank_bullets:
            bullet.draw(screen)
        
        # Wyświetl wynik
        score_text = score_font.render(f"Tanks Destroyed: {destroyed_tanks}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # Wyświetl ekran game over jeśli gra się skończyła
        if game_over:
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            final_score_text = score_font.render(f"Final Score: {destroyed_tanks} tanks", True, (255, 255, 0))
            restart_text = score_font.render("Press R to restart", True, (255, 255, 255))
            screen.blit(game_over_text, (WIDTH//2 - 150, HEIGHT//2 - 50))
            screen.blit(final_score_text, (WIDTH//2 - 120, HEIGHT//2 - 10))
            screen.blit(restart_text, (WIDTH//2 - 100, HEIGHT//2 + 30))

        # === AKTUALIZACJA EKRANU ===
        # Wyświetl wszystko co zostało narysowane na ekranie
        pygame.display.flip()  # Odśwież cały ekran
        
        # === KONTROLA FPS ===
        # Ograniczenie do 60 klatek na sekundę (gra działa płynnie i stabilnie)
        clock.tick(60)


# === URUCHOMIENIE GRY ===
# Ten kod uruchamia się tylko gdy plik jest uruchomiony bezpośrednio
# (nie gdy jest importowany jako moduł)
if __name__ == "__main__":
    main()  # Uruchom główną funkcję gry
