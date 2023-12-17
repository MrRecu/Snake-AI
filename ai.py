def wczytaj_trase(plik):
    with open(plik, "r") as f:
        trasa = [tuple(map(int, line.strip().split(", "))) for line in f]
    return trasa

def generuj_sciezke(start_x, start_y, szerokosc, wysokosc, krok):
    sciezka = []
    x, y = start_x, start_y
    kierunek = 10  # W prawo

    while y <= wysokosc - krok:
        while 10 <= x <= szerokosc - krok and (x, y) not in sciezka:
            sciezka.append((x, y))
            x += kierunek

        # Zmiana kierunku i przesunięcie w dół
        kierunek *= -1
        y += krok
        if 10 <= y <= wysokosc - krok:
            x += kierunek

    return sciezka

def steruj_wezem_ai(wez, sciezka):
    glowa_weza = wez[0]
    if glowa_weza in sciezka:
        # Pobierz indeks aktualnej pozycji głowy w ścieżce
        indeks = sciezka.index(glowa_weza)

        # Sprawdź, czy to nie jest ostatni punkt w ścieżce
        if indeks < len(sciezka) - 1:
            nastepny_punkt = sciezka[indeks + 1]
            dx = nastepny_punkt[0] - glowa_weza[0]
            dy = nastepny_punkt[1] - glowa_weza[1]
            return dx, dy
    return 0, 0

def znajdz_sciezke(wez, cel, szerokosc, wysokosc, krok):
    # Tworzenie siatki planszy
    plansza = [[0 for _ in range(szerokosc // krok)] for _ in range(wysokosc // krok)]
    
    # Oznaczenie pozycji węża jako zajętej
    for segment in wez:
        x, y = segment
        plansza[y // krok][x // krok] = 1

    # Kolejka do przechowywania ścieżek do sprawdzenia
    kolejka = [(wez[0], [])]

    while kolejka:
        (x, y), sciezka = kolejka.pop(0)

        # Sprawdzenie, czy dotarto do celu
        if (x, y) == cel:
            return sciezka

        # Sprawdzenie możliwych kierunków
        for dx, dy in [(0, krok), (krok, 0), (0, -krok), (-krok, 0)]:
            nx, ny = x + dx, y + dy

            # Sprawdzenie, czy nowa pozycja jest w granicach planszy i wolna
            if 0 <= nx < szerokosc and 0 <= ny < wysokosc and plansza[ny // krok][nx // krok] == 0:
                plansza[ny // krok][nx // krok] = 1  # Oznacz jako zajęte
                kolejka.append(((nx, ny), sciezka + [(dx, dy)]))

    return None