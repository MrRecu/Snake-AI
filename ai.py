import time

def steruj_wezem_ai(wez, dx, dy):
    # Pobierz aktualny czas
    aktualny_czas = time.time()

    # Sprawdź, czy minęła 1 sekunda od ostatniego skrętu
    if aktualny_czas - steruj_wezem_ai.ostatni_czas_skrętu >= 0.5:
        # Zaktualizuj czas ostatniego skrętu
        steruj_wezem_ai.ostatni_czas_skrętu = aktualny_czas

        # Skręt zgodnie z ruchem wskazówek zegara
        if dx == 0 and dy == -10:  # Wąż porusza się w górę
            dx, dy = 10, 0  # Skręć w prawo
        elif dx == 10 and dy == 0:  # Wąż porusza się w prawo
            dx, dy = 0, 10  # Skręć w dół
        elif dx == 0 and dy == 10:  # Wąż porusza się w dół
            dx, dy = -10, 0  # Skręć w lewo
        elif dx == -10 and dy == 0:  # Wąż porusza się w lewo
            dx, dy = 0, -10  # Skręć w górę

    return dx, dy

# Inicjalizuj zmienną czasową dla funkcji
steruj_wezem_ai.ostatni_czas_skrętu = time.time()