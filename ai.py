import itertools
import logging
# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def wczytaj_sciezke_hamiltona(plik):
    try:
        with open(plik, "r") as f:
            logging.info("Wczytywanie istniejącej ścieżki Hamiltona z pliku.")
            return [tuple(map(int, line.strip().split(','))) for line in f]  # Format x,y
    except FileNotFoundError:
        logging.warning("Plik ze ścieżką Hamiltona nie istnieje. Generowanie nowej ścieżki.")
        return None


class WazAI:
    def __init__(self, sciezka_plik):
        self.sciezka = wczytaj_sciezke_hamiltona(sciezka_plik)
        self.indeks_sciezki = 0

    def nastepny_ruch(self, glowa_weza):
        cel = self.sciezka[self.indeks_sciezki % len(self.sciezka)]
        dx, dy = cel[0] - glowa_weza[0], cel[1] - glowa_weza[1]
        self.indeks_sciezki += 1
        return dx, dy

def czy_sciezka_hamiltona(G, sciezka):
    if len(sciezka) != len(G):
        return False
    return all(sciezka[i] in G[sciezka[i-1]] for i in range(1, len(sciezka)))

def generuj_sciezke_hamiltona(szerokosc, wysokosc):
    sciezka = []

    # Pierwsza pętla od (0, 0) do (0, 200)
    for y in range(0, wysokosc + 1, 10):
        sciezka.append((0, y))
    
    # Druga pętla od (10, 200) do (10, 10)
    for y in range(wysokosc, 9, -10):
        sciezka.append((10, y))

    # Pozostałe pętle w dół i w górę
    for x in range(20, szerokosc + 1, 10):
        if (x // 10) % 2 == 0:
            # Ruch w dół dla parzystych kolumn
            for y in range(10, wysokosc + 1, 10):
                sciezka.append((x, y))
        else:
            # Ruch w górę do 10 dla nieparzystych kolumn
            for y in range(wysokosc, 0, -10):
                sciezka.append((x, y))
            # Dodanie punktu [x, 10]
            sciezka.append((x, 10))

    for x in range(410, 9, -10):
        sciezka.append((x, 0))

    return sciezka



# Parametry planszy
szerokosc, wysokosc = 410, 200  # Zmień według potrzeb

sciezka_hamiltona = generuj_sciezke_hamiltona(szerokosc, wysokosc)
print("Wygenerowana ścieżka Hamiltona:")
for punkt in sciezka_hamiltona:
    print(punkt)

sciezka_hamiltona = wczytaj_sciezke_hamiltona("sciezka_hamiltona.txt")

if sciezka_hamiltona is None:
    sciezka_hamiltona = generuj_sciezke_hamiltona(szerokosc, wysokosc)
    if sciezka_hamiltona:
        logging.info("Znaleziono ścieżkę Hamiltona.")
        with open("sciezka_hamiltona.txt", "w") as plik:
            for x, y in sciezka_hamiltona:
                plik.write(f"{x},{y}\n")  # Zapis bez nawiasów i spacji
    else:
        logging.error("Nie znaleziono ścieżki Hamiltona dla danej planszy.")
else:
    logging.info("Ścieżka Hamiltona została wczytana z pliku.")