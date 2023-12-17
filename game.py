import pygame
import sys
import random
import time
from menu import Menu

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu i scoreboardu
szerokosc = 640
wysokosc_planszy = 480
wysokosc_scoreboard = 100
wysokosc = wysokosc_planszy + wysokosc_scoreboard
ekran = pygame.display.set_mode((szerokosc, wysokosc))

# Kolory
CZARNY = (0, 0, 0)
ZIELONY = (0, 255, 0)
CZERWONY = (255, 0, 0)
FIOLETOWY = (128, 0, 128)
CIEMNO_ZIELONY = (0, 100, 00)
SZARY = (128, 128, 128)
CYAN = (0, 255, 255)

# Ustawienia węża
rozmiar_weza = 10
wez = [[100, 50], [90, 50], [80, 50]]

# Ustawienia jedzenia
jedzenie = [random.randrange(1, (szerokosc//10)) * 10, random.randrange(1, (wysokosc_planszy//10)) * 10]
jedzenie_na_ekranie = True

# Ustawienia ekstra owocu
ekstra_owoc = None
czas_ekstra_owocu = 0
czas_pojawienia_owocu = time.time() + random.randint(5, 15)

# Kierunek ruchu węża
dx = 10
dy = 0

# Zegar
zegar = pygame.time.Clock()

# Wynik
start_czasu_gry = None
zebrane_owoce = 0
zebrane_owoce_premium = 0
wynik = 0

# Funkcje pomocnicze


def rysuj_weza(wez):
    for segment in wez:
        pygame.draw.rect(ekran, ZIELONY, [segment[0], segment[1], rozmiar_weza, rozmiar_weza])

def rysuj_ramke():
    pygame.draw.rect(ekran, CIEMNO_ZIELONY, [0, 0, szerokosc, wysokosc_planszy], 10)

def rysuj_jedzenie(x, y):
    pygame.draw.rect(ekran, CZERWONY, [x, y, rozmiar_weza, rozmiar_weza])

def rysuj_ekstra_owoc():
    if ekstra_owoc:
        pygame.draw.rect(ekran, FIOLETOWY, [ekstra_owoc[0], ekstra_owoc[1], rozmiar_weza, rozmiar_weza])

def generuj_owoc():
    while True:
        pozycja = [random.randrange(1, (szerokosc // 10)) * 10, random.randrange(1, (wysokosc_planszy // 10)) * 10]
        if pozycja not in wez and pozycja[0] < szerokosc - rozmiar_weza and pozycja[1] < wysokosc_planszy - rozmiar_weza:
            return pozycja

def sprawdz_kolizje(x, y, lista):
    for segment in lista:
        if x == segment[0] and y == segment[1]:
            return True
    return False

def zapisz_najlepszy_wynik(wynik):
    with open("najlepszy_wynik.txt", "w") as plik:
        plik.write(str(wynik))

def odczytaj_najlepszy_wynik():
    try:
        with open("najlepszy_wynik.txt", "r") as plik:
            return int(plik.read())
    except FileNotFoundError:
        return 0

def wyswietl_scoreboard():
    czcionka = pygame.font.SysFont(None, 30)
    aktualny_czas = time.time() - start_czasu_gry if start_czasu_gry else 0
    minuty, sekundy = divmod(aktualny_czas, 60)
    sekundy, setne = divmod(sekundy, 1)
    
    tekst_czasu = czcionka.render(f"Czas: {int(minuty):02d}:{int(sekundy):02d}:{int(setne * 100):02d}", True, SZARY)
    tekst_zebranych_owocow = czcionka.render(f"Owoce: {zebrane_owoce}", True, CZERWONY)
    tekst_owocow_premium = czcionka.render(f"Premium: {zebrane_owoce_premium}", True, FIOLETOWY)
    tekst_wyniku = czcionka.render(f"Wynik: {wynik} | Najlepszy Wynik: {najlepszy_wynik}", True, SZARY)
    

    ekran.blit(tekst_czasu, (5, wysokosc_planszy + 5))
    ekran.blit(tekst_zebranych_owocow, (5, wysokosc_planszy + 30))
    ekran.blit(tekst_owocow_premium, (5, wysokosc_planszy + 55))
    ekran.blit(tekst_wyniku, (5, wysokosc_planszy + 80))
# Inicjalizacja najlepszego wyniku
najlepszy_wynik = odczytaj_najlepszy_wynik()

# Utworzenie instancji menu
menu = Menu(ekran)
w_grze = False
pauza = False
w_menu_startowym = True
ekran_konca_gry = False

# Główna pętla gry
while True:
    # Menu Startowe
    if not w_grze and w_menu_startowym:
        # Logika menu startowego
        ekran.fill(CZARNY)
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
                start_czasu_gry = time.time()
                wez = [[100, 50], [90, 50], [80, 50]]
                dx, dy = 10, 0
                wynik = 0
                zebrane_owoce = 0
                zebrane_owoce_premium = 0
                menu = Menu(ekran, pauza=False)
            elif akcja == "Wyjście":
                pygame.quit()
                sys.exit()

    # Pauza
    elif not w_grze and pauza:
        ekran.fill(CZARNY)
        menu.rysuj_menu()
        wyswietl_scoreboard()
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

    # Gra
    elif w_grze:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
            elif event.type == pygame.KEYDOWN:
                print(f"Wciśnięto klawisz w grze: {event.key}")
                if event.key == pygame.K_ESCAPE:
                    print("Klawisz ESC został wciśnięty - pauza")
                    w_grze = False
                    pauza = True
                    menu = Menu(ekran, pauza=True)
                elif event.key in [pygame.K_w, pygame.K_UP] and dy != 10:
                    print("Klawisz UP wciśnięty")
                    dx, dy = 0, -10
                elif event.key in [pygame.K_s, pygame.K_DOWN] and dy != -10:
                    print("Klawisz DOWN wciśnięty")
                    dx, dy = 0, 10
                elif event.key in [pygame.K_a, pygame.K_LEFT] and dx != 10:
                    print("Klawisz LEFT wciśnięty")
                    dx, dy = -10, 0
                elif event.key in [pygame.K_d, pygame.K_RIGHT] and dx != -10:
                    print("Klawisz RIGHT wciśnięty")
                    dx, dy = 10, 0

        glowa = [wez[0][0] + dx, wez[0][1] + dy]
        wez.insert(0, glowa)

        if wez[0][0] == jedzenie[0] and wez[0][1] == jedzenie[1]:
            wynik += 100
            zebrane_owoce += 1
            jedzenie_na_ekranie = False
        elif ekstra_owoc and wez[0][0] == ekstra_owoc[0] and wez[0][1] == ekstra_owoc[1]:
            wynik += 250
            zebrane_owoce_premium += 1
            ekstra_owoc = None
        else:
            wez.pop()

        if not jedzenie_na_ekranie:
            jedzenie = generuj_owoc()
            jedzenie_na_ekranie = True

        if ekstra_owoc is None and time.time() > czas_pojawienia_owocu:
            ekstra_owoc = generuj_owoc()
            czas_ekstra_owocu = time.time() + random.randint(5, 15)

        if ekstra_owoc and time.time() > czas_ekstra_owocu:
            ekstra_owoc = None
            czas_pojawienia_owocu = time.time() + random.randint(5, 15)

        if wez[0][0] < 10 or wez[0][0] >= szerokosc-10 or wez[0][1] < 10 or wez[0][1] >= 480-10 or sprawdz_kolizje(wez[0][0], wez[0][1], wez[1:]):
            if wynik > najlepszy_wynik:
                najlepszy_wynik = wynik
                zapisz_najlepszy_wynik(najlepszy_wynik)
            w_grze = False
            w_menu_startowym = True
            menu = Menu(ekran)

        ekran.fill(CZARNY)
        rysuj_ramke()
        rysuj_weza(wez)
        rysuj_jedzenie(jedzenie[0], jedzenie[1])
        rysuj_ekstra_owoc()
        wyswietl_scoreboard()
        pygame.display.update()
        zegar.tick(15)
