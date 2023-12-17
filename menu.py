import pygame

class Menu:
    def __init__(self, ekran, pauza=False):
        self.ekran = ekran
        self.czcionka = pygame.font.SysFont(None, 55)
        self.kolor = (255, 255, 255)  # Biały
        self.kolor_wybrany = (255, 0, 0)  # Czerwony
        if pauza:
            self.opcje = ["Kontynuuj", "Wyjście"]
        else:
            self.opcje = ["Start", "Wyjście"]
        self.wybrana_opcja = 0

    def rysuj_menu(self):
        for index, opcja in enumerate(self.opcje):
            kolor = self.kolor_wybrany if index == self.wybrana_opcja else self.kolor
            tekst = self.czcionka.render(opcja, True, kolor)
            rect = tekst.get_rect(center=(self.ekran.get_width() / 2, 100 + index * 60))
            self.ekran.blit(tekst, rect)

        # Dodaj informacje o grze
        
        instrukcje = [
            "Poruszanie: WSAD lub Strzałki",
            "F1 - Zwolnienie tempa gry",
            "F2 - Przyśpieszenie tempa gry",
            "Esc - Wyjście/Pauza",
            "Enter/Return - Zatwierdź"
        ]
        
        for i, instrukcja in enumerate(instrukcje):
            tekst = self.czcionka.render(instrukcja, True, self.kolor)
            rect = tekst.get_rect(center=(self.ekran.get_width() / 2, 360 + i * 40))
            self.ekran.blit(tekst, rect)

    def aktualizuj_wybor(self, kierunek):
        self.wybrana_opcja += kierunek
        if self.wybrana_opcja < 0:
            self.wybrana_opcja = len(self.opcje) - 1
        elif self.wybrana_opcja >= len(self.opcje):
            self.wybrana_opcja = 0

    def obsluga_zdarzenia(self, event):
        if event.type == pygame.KEYDOWN:
            print(f"Wciśnięto klawisz w Pauzie: {event.key}")
            if event.key in [pygame.K_w, pygame.K_UP]:
                print("Klawisz UP wciśnięty")
                self.aktualizuj_wybor(-1)
            elif event.key in [pygame.K_s, pygame.K_DOWN]:
                print("Klawisz DOWN wciśnięty")
                self.aktualizuj_wybor(1)
            elif event.key == pygame.K_RETURN:
                print("Klawisz ENTER wciśnięty")
                return self.opcje[self.wybrana_opcja]
            elif event.key == pygame.K_ESCAPE:
                print("Klawisz ESC wciśnięty")
                return "Wyjście"
        return None