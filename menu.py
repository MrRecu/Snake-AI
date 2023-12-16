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

    def aktualizuj_wybor(self, kierunek):
        self.wybrana_opcja += kierunek
        if self.wybrana_opcja < 0:
            self.wybrana_opcja = len(self.opcje) - 1
        elif self.wybrana_opcja >= len(self.opcje):
            self.wybrana_opcja = 0

    def obsluga_zdarzenia(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_w, pygame.K_UP]:
                self.aktualizuj_wybor(-1)
            elif event.key in [pygame.K_s, pygame.K_DOWN]:
                self.aktualizuj_wybor(1)
            elif event.key == pygame.K_RETURN:
                return self.opcje[self.wybrana_opcja]
            elif event.key == pygame.K_ESCAPE:
                return "Wyjście"
        return None
