import pygame
import sys
import random
import time
from menu import Menu
from ai import proste_ai

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu i scoreboardu
szerokosc = 400  # 40 segmentów x 10 pikseli na segment
wysokosc_planszy = 200  # 20 segmentów x 10 pikseli na segment
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
wez = [[30, 30], [20, 30], [10, 30]]
# Kierunek ruchu węża
dx = 0
dy = 10
zmiana_kierunku = False
nowy_kierunek = False
obecny_kierunek = False
# Prędkość węża
predkosc = 15

# Ustawienia jedzenia
jedzenie = [random.randrange(1, (szerokosc//10)) * 10, random.randrange(1, (wysokosc_planszy//10)) * 10]
jedzenie_na_ekranie = True
sciezka_do_owocu =False

# Ustawienia ekstra owocu
ekstra_owoc = None
czas_ekstra_owocu = 0
czas_do_pojawienia_nowego_owocu = 0
czas_pojawienia_owocu = time.time() + random.randint(5, 15)

# Zegar
zegar = pygame.time.Clock()

# Wynik
start_czasu_gry = None
czas_rozpoczecia_pauzy = None
zebrane_owoce = 0
zebrane_owoce_premium = 0
wynik = 0
mnoznik_punktow = 1.0

# Funkcje pomocnicze

def wypisz_pozycje_weza(wez):
    print(f"Głowa węża: {wez[0]}")
    print("Pozostałe segmenty węża:")
    for segment in wez[1:]:
        print(segment)

def wypisz_pozycje_owocu(owoc):
    print(f"Pozycja owocu: {owoc}")


def rysuj_weza(wez, dx, dy):
    for index, segment in enumerate(wez):
        # Rysowanie obwódki
        pygame.draw.rect(ekran, SZARY, [segment[0], segment[1], rozmiar_weza, rozmiar_weza])

        # Rysowanie wewnętrznej części segmentu
        wewnetrzny_rozmiar = rozmiar_weza - 2  # Odejmujemy kilka pikseli na obwódkę
        if index == 0:
            # Głowa węża w innym kolorze
            kolor_glowy = (0, 255, 0)  # Jaśniejszy zielony
            pygame.draw.rect(ekran, kolor_glowy, [segment[0] + 1, segment[1] + 1, wewnetrzny_rozmiar, wewnetrzny_rozmiar])

            # Dodanie oka
            kolor_oka = (0, 0, 0)  # Czarne
            if dx > 0:  # Wąż porusza się w prawo
                pozycja_oka = (segment[0] + rozmiar_weza - 3, segment[1] + 3)
            elif dx < 0:  # Wąż porusza się w lewo
                pozycja_oka = (segment[0] + 3, segment[1] + 3)
            elif dy > 0:  # Wąż porusza się w dół
                pozycja_oka = (segment[0] + 3, segment[1] + rozmiar_weza - 3)
            else:  # Wąż porusza się w górę
                pozycja_oka = (segment[0] + 3, segment[1] + 3)
            pygame.draw.circle(ekran, kolor_oka, pozycja_oka, 2)  # Małe oko
        else:
            # Reszta ciała
            pygame.draw.rect(ekran, ZIELONY, [segment[0] + 1, segment[1] + 1, wewnetrzny_rozmiar, wewnetrzny_rozmiar])

def rysuj_ramke():
    pygame.draw.rect(ekran, CIEMNO_ZIELONY, [1, 1, szerokosc-1, wysokosc_planszy-1], 10)

def rysuj_jedzenie(x, y):
    pygame.draw.rect(ekran, CZERWONY, [x, y, rozmiar_weza, rozmiar_weza])

def rysuj_ekstra_owoc():
    if ekstra_owoc:
        pygame.draw.rect(ekran, FIOLETOWY, [ekstra_owoc[0], ekstra_owoc[1], rozmiar_weza, rozmiar_weza])

def generuj_owoc(wez, szerokosc, wysokosc_planszy):
    while True:
        pozycja = [random.randrange(10, szerokosc - 10, 10), random.randrange(10, wysokosc_planszy - 10, 10)]
        if pozycja not in wez:
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
            return float(plik.read())
    except FileNotFoundError:
        return 0

def wyswietl_scoreboard():
    czcionka = pygame.font.SysFont(None, 30)
    aktualny_czas = time.time() - start_czasu_gry if start_czasu_gry else 0
    minuty, sekundy = divmod(aktualny_czas, 60)
    sekundy, setne = divmod(sekundy, 1)

    tekst_mnoznik_punktow = czcionka.render(f"{mnoznik_punktow} x", True, SZARY)
    tekst_predkosc = czcionka.render(f"Speed: {predkosc}", True, SZARY)
    tekst_czasu = czcionka.render(f"Czas: {int(minuty):02d}:{int(sekundy):02d}:{int(setne * 100):02d}", True, SZARY)
    tekst_zebranych_owocow = czcionka.render(f"Owoce: {zebrane_owoce}", True, CZERWONY)
    tekst_owocow_premium = czcionka.render(f"Premium: {zebrane_owoce_premium}", True, FIOLETOWY)
    tekst_wyniku = czcionka.render(f"Wynik: {round(wynik,2)} | Najlepszy Wynik: {round(najlepszy_wynik,2)}", True, SZARY)
    
    if ekstra_owoc:
        pozostaly_czas = max(0, int(czas_ekstra_owocu - time.time()))
        tekst_pozostalego_czasu = czcionka.render(f"Pozostały czas premium: {pozostaly_czas}s", True, FIOLETOWY)
        ekran.blit(tekst_pozostalego_czasu, (szerokosc - 400, wysokosc_planszy + 55))

    ekran.blit(tekst_predkosc, (szerokosc - 400, wysokosc_planszy + 5))
    ekran.blit(tekst_mnoznik_punktow, (szerokosc - 50, wysokosc_planszy + 5))
    ekran.blit(tekst_czasu, (5, wysokosc_planszy + 5))
    ekran.blit(tekst_zebranych_owocow, (5, wysokosc_planszy + 30))
    ekran.blit(tekst_owocow_premium, (5, wysokosc_planszy + 55))
    ekran.blit(tekst_wyniku, (5, wysokosc_planszy + 80))

#GAME OVER
def wyswietl_menu_konca_gry(wynik):
    ekran.fill(CZARNY)
    czcionka = pygame.font.SysFont(None, 50)
    tekst_game_over = czcionka.render("GAME OVER", True, CZERWONY)
    tekst_wyniku = czcionka.render(f"Wynik: {wynik}", True, SZARY)
    ekran.blit(tekst_game_over, (szerokosc // 2 - 100, wysokosc // 2 - 50))
    ekran.blit(tekst_wyniku, (szerokosc // 2 - 100, wysokosc // 2))
    pygame.display.update()
    time.sleep(2)

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
    zmiana_kierunku = False
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
                ai = False
                w_menu_startowym = False
                start_czasu_gry = time.time()
                wez = [[30, 30], [20, 30], [10, 30]]
                dx, dy = 10, 0
                wynik = 0
                predkosc = 15
                zebrane_owoce = 0
                zebrane_owoce_premium = 0
                menu = Menu(ekran, pauza=False)
            
            elif akcja == "Ai":
                w_grze = True
                ai = True
                w_menu_startowym = False
                start_czasu_gry = time.time()
                wez = [[30, 30], [20, 30], [10, 30]]
                dx, dy = 10, 0
                wynik = 0
                predkosc = 15
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
        # wyswietl_scoreboard()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            akcja = menu.obsluga_zdarzenia(event)
            if akcja == "Kontynuuj":
                if czas_rozpoczecia_pauzy is not None:
                    czas_trwania_pauzy = time.time() - czas_rozpoczecia_pauzy
                    start_czasu_gry += czas_trwania_pauzy  # Aktualizacja czasu rozpoczęcia gry
                    czas_rozpoczecia_pauzy = None  # Reset czasu rozpoczęcia pauzy
                w_grze = True
                pauza = False
            elif akcja == "Wyjście":
                w_grze = False
                pauza = False
                w_menu_startowym = True
                menu = Menu(ekran, pauza=False)

    # Gra
    elif w_grze and ai == False:

        ####### wypisz_pozycje_weza(wez)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
            elif event.type == pygame.KEYDOWN and not zmiana_kierunku:
                # Zapisz obecny kierunek ruchu
                obecny_kierunek = (dx, dy)
                if event.key == pygame.K_ESCAPE:
                    print("Klawisz ESC został wciśnięty - pauza")
                    if not pauza:
                        czas_rozpoczecia_pauzy = time.time()  # Zapisz czas rozpoczęcia pauzy
                    w_grze = False
                    pauza = True
                    menu = Menu(ekran, pauza=True)
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    nowy_kierunek = (0, -10)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    nowy_kierunek = (0, 10)
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    nowy_kierunek = (-10, 0)
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    nowy_kierunek = (10, 0)
                elif event.key == pygame.K_F2:
                    if predkosc <= 100:
                        predkosc += 5
                elif event.key == pygame.K_F1:
                    if predkosc > 5:
                        predkosc -= 5
                else:
                    continue

                # Zmień kierunek tylko jeśli nie jest przeciwny do obecnego
                if nowy_kierunek[0] != -obecny_kierunek[0] and nowy_kierunek[1] != -obecny_kierunek[1]:
                    dx, dy = nowy_kierunek
                    zmiana_kierunku = True
                


        glowa = [wez[0][0] + dx, wez[0][1] + dy]
        wez.insert(0, glowa)


        # Zdefiniuj bazowy mnożnik punktów i bazową prędkość
        bazowy_mnoznik = 1.0
        bazowa_predkosc = 15

        # Oblicz mnożnik w zależności od aktualnej prędkości
        mnoznik_punktow = round(1.0 + max(0, (predkosc - bazowa_predkosc) // 5) * 0.1, 2)

        # Oblicz ile punktów zdobyłeś za zebranie owocu i zaokrągl wynik do 2 miejsc po przecinku
        punkty_za_owoc = round(100 * mnoznik_punktow, 2)

        if wez[0][0] == jedzenie[0] and wez[0][1] == jedzenie[1]:
            wynik += punkty_za_owoc
            zebrane_owoce += 1
            jedzenie_na_ekranie = False
        elif ekstra_owoc and wez[0][0] == ekstra_owoc[0] and wez[0][1] == ekstra_owoc[1]:
            wynik += punkty_za_owoc * 2  # Za ekstra owoc zdobywasz podwójną ilość punktów
            zebrane_owoce_premium += 1
            ekstra_owoc = None
            # Resetujemy czas pojawienia się kolejnego owocu premium
            czas_pojawienia_owocu = time.time() + random.randint(5, 15)
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

        if wez[0][0] < 10 or wez[0][0] >= szerokosc-10 or wez[0][1] < 10 or wez[0][1] >= wysokosc_planszy-10 or sprawdz_kolizje(wez[0][0], wez[0][1], wez[1:]):
            if wynik > najlepszy_wynik:
                najlepszy_wynik = wynik
                zapisz_najlepszy_wynik(najlepszy_wynik)
            wyswietl_menu_konca_gry(wynik)
            w_grze = False
            w_menu_startowym = True
            menu = Menu(ekran)

        ekran.fill(CZARNY)
        rysuj_ramke()
        rysuj_weza(wez, dx, dy)
        rysuj_jedzenie(jedzenie[0], jedzenie[1])
        rysuj_ekstra_owoc()
        wyswietl_scoreboard()
        pygame.display.update()
        zegar.tick(predkosc)
    
    # GRA AI
    elif w_grze and ai == True:
        wypisz_pozycje_weza(wez)
        wypisz_pozycje_owocu(jedzenie)

        if ekstra_owoc:
            wypisz_pozycje_owocu(ekstra_owoc)

        if proste_ai:
            dx, dy = proste_ai(wez, jedzenie, ekstra_owoc, szerokosc, wysokosc_planszy)
        else:
            print("__________brak sciezki_____________")
            # Jeśli nie ma ścieżki, zatrzymaj węża
            dx, dy = 10, 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
 
            elif event.type == pygame.KEYDOWN :
                # Zapisz obecny kierunek ruchu
                obecny_kierunek = (dx, dy)
                if event.key == pygame.K_ESCAPE:
                    print("Klawisz ESC został wciśnięty - pauza")
                    if not pauza:
                        czas_rozpoczecia_pauzy = time.time()  # Zapisz czas rozpoczęcia pauzy
                    w_grze = False
                    pauza = True
                    menu = Menu(ekran, pauza=True)
                elif event.key == pygame.K_F2:
                    if predkosc <= 1000:
                        predkosc += 10
                elif event.key == pygame.K_F1:
                    if predkosc > 100:
                        predkosc -= 100

        glowa = [wez[0][0] + dx, wez[0][1] + dy]
        wez.insert(0, glowa)


        # Zdefiniuj bazowy mnożnik punktów i bazową prędkość
        bazowy_mnoznik = 1.0
        bazowa_predkosc = 15

        # Oblicz mnożnik w zależności od aktualnej prędkości
        mnoznik_punktow = round(1.0 + max(0, (predkosc - bazowa_predkosc) // 5) * 0.1, 2)

        # Oblicz ile punktów zdobyłeś za zebranie owocu i zaokrągl wynik do 2 miejsc po przecinku
        punkty_za_owoc = round(10 * mnoznik_punktow, 2)

        if wez[0][0] == jedzenie[0] and wez[0][1] == jedzenie[1]:
            wynik += punkty_za_owoc
            zebrane_owoce += 1
            jedzenie_na_ekranie = False
        elif ekstra_owoc and wez[0][0] == ekstra_owoc[0] and wez[0][1] == ekstra_owoc[1]:
            wynik += punkty_za_owoc * 2  # Za ekstra owoc zdobywasz podwójną ilość punktów
            zebrane_owoce_premium += 1
            ekstra_owoc = None
            # Resetujemy czas pojawienia się kolejnego owocu premium
            czas_pojawienia_owocu = time.time() + random.randint(5, 15)
        else:
            wez.pop()

        if not jedzenie_na_ekranie:
            jedzenie = generuj_owoc(wez, szerokosc, wysokosc_planszy)
            jedzenie_na_ekranie = True

        if ekstra_owoc is None and time.time() > czas_pojawienia_owocu:
            ekstra_owoc = generuj_owoc(wez, szerokosc, wysokosc_planszy)
            czas_ekstra_owocu = time.time() + random.randint(5, 15)

        if ekstra_owoc and time.time() > czas_ekstra_owocu:
            ekstra_owoc = None
            czas_pojawienia_owocu = time.time() + random.randint(5, 15)

        if wez[0][0] < 10 or wez[0][0] >= szerokosc-10 or wez[0][1] < 10 or wez[0][1] >= wysokosc_planszy-10 or sprawdz_kolizje(wez[0][0], wez[0][1], wez[1:]):
            if wynik > najlepszy_wynik:
                najlepszy_wynik = wynik
                zapisz_najlepszy_wynik(najlepszy_wynik)
            wyswietl_menu_konca_gry(wynik)
            w_grze = False
            w_menu_startowym = True
            menu = Menu(ekran)

        ekran.fill(CZARNY)
        rysuj_ramke()
        rysuj_weza(wez, dx, dy)
        rysuj_jedzenie(jedzenie[0], jedzenie[1])
        rysuj_ekstra_owoc()
        wyswietl_scoreboard()
        pygame.display.update()
        zegar.tick(predkosc)