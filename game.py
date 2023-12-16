import pygame
import sys
import random
from menu import Menu

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
szerokosc = 640
wysokosc = 480
ekran = pygame.display.set_mode((szerokosc, wysokosc))

# Kolory
CZARNY = (0, 0, 0)
ZIELONY = (0, 255, 0)
CZERWONY = (255, 0, 0)

# Ustawienia węża
rozmiar_weza = 10
wez = [[100, 50], [90, 50], [80, 50]]

# Ustawienia jedzenia
jedzenie = [random.randrange(1, (szerokosc//10)) * 10, random.randrange(1, (wysokosc//10)) * 10]
jedzenie_na_ekranie = True

# Kierunek ruchu węża
dx = 10
dy = 0

# Zegar
zegar = pygame.time.Clock()

# Funkcje pomocnicze
def rysuj_weza(wez):
    for segment in wez:
        pygame.draw.rect(ekran, ZIELONY, [segment[0], segment[1], rozmiar_weza, rozmiar_weza])

def rysuj_jedzenie(x, y):
    pygame.draw.rect(ekran, CZERWONY, [x, y, rozmiar_weza, rozmiar_weza])

def sprawdz_kolizje(x, y, lista):
    for segment in lista:
        if x == segment[0] and y == segment[1]:
            return True
    return False

# Utworzenie instancji menu
menu = Menu(ekran)
w_grze = False
pauza = False
w_menu_startowym = True

# Główna pętla gry
while True:
    if not w_grze and w_menu_startowym:
        ekran.fill(CZARNY)  # Czyszczenie ekranu
        menu.rysuj_menu()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            akcja = menu.obsluga_zdarzenia(event)
            if akcja == "Start":
                w_grze = True
                w_menu_startowym = False
                wez = [[100, 50], [90, 50], [80, 50]]  # Reset węża
                dx, dy = 10, 0  # Reset kierunku
                menu = Menu(ekran, pauza=False)  # Reset menu
            elif akcja == "Wyjście":
                pygame.quit()
                sys.exit()

    elif not w_grze and pauza:
        ekran.fill(CZARNY)
        menu.rysuj_menu()
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            akcja = menu.obsluga_zdarzenia(event)
            if akcja == "Kontynuuj":
                w_grze = True
                pauza = False
            elif akcja == "Wyjście":
                w_grze = False
                pauza = False
                w_menu_startowym = True
                menu = Menu(ekran, pauza=False)

    elif w_grze:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    w_grze = False
                    pauza = True
                    menu = Menu(ekran, pauza=True)
                elif event.key == pygame.K_w and dy != 10:
                    dx, dy = 0, -10
                elif event.key == pygame.K_s and dy != -10:
                    dx, dy = 0, 10
                elif event.key == pygame.K_a and dx != 10:
                    dx, dy = -10, 0
                elif event.key == pygame.K_d and dx != -10:
                    dx, dy = 10, 0

        glowa = [wez[0][0] + dx, wez[0][1] + dy]
        wez.insert(0, glowa)

        if wez[0][0] == jedzenie[0] and wez[0][1] == jedzenie[1]:
            jedzenie_na_ekranie = False
        else:
            wez.pop()

        if not jedzenie_na_ekranie:
            jedzenie = [random.randrange(1, (szerokosc//10)) * 10, random.randrange(1, (wysokosc//10)) * 10]
            jedzenie_na_ekranie = True

        if wez[0][0] < 0 or wez[0][0] > szerokosc-10 or wez[0][1] < 0 or wez[0][1] > wysokosc-10 or sprawdz_kolizje(wez[0][0], wez[0][1], wez[1:]):
            w_grze = False
            w_menu_startowym = True
            menu = Menu(ekran)  # Powrót do menu głównego

        ekran.fill(CZARNY)
        rysuj_weza(wez)
        rysuj_jedzenie(jedzenie[0], jedzenie[1])

        pygame.display.update()
        zegar.tick(15)
