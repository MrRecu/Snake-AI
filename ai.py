def proste_ai(wez, jedzenie, ekstra_owoc, szerokosc, wysokosc):
    cel = znajdz_najblizszy_cel(wez[0], jedzenie, ekstra_owoc)
    
    glowa = wez[0]
    kierunki = [(10, 0), (-10, 0), (0, 10), (0, -10)]
    najlepszy_kierunek = (0, 0)
    najmniejsza_odleglosc = float('inf')

    for k in kierunki:
        nowa_pozycja = [glowa[0] + k[0], glowa[1] + k[1]]
        odleglosc_do_celu = odleglosc(cel, nowa_pozycja)
        if sprawdz_bezpieczenstwo_ruchu(wez, k, szerokosc, wysokosc) and odleglosc_do_celu < najmniejsza_odleglosc:
            najlepszy_kierunek = k
            najmniejsza_odleglosc = odleglosc_do_celu

    return najlepszy_kierunek

def odleglosc(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def znajdz_najblizszy_cel(glowa_weza, jedzenie, ekstra_owoc):
    odleglosc_do_jedzenia = odleglosc(glowa_weza, jedzenie)
    odleglosc_do_ekstra_owocu = odleglosc(glowa_weza, ekstra_owoc) if ekstra_owoc else float('inf')

    if odleglosc_do_jedzenia <= 100 or odleglosc_do_ekstra_owocu > 100:
        return jedzenie
    return ekstra_owoc

def sprawdz_bezpieczenstwo_ruchu(wez, kierunek, szerokosc, wysokosc):
    glowa = wez[0]
    nowa_pozycja = [glowa[0] + kierunek[0], glowa[1] + kierunek[1]]

    # Sprawdzenie, czy ruch nie wychodzi poza granice planszy
    if not (10 <= nowa_pozycja[0] < szerokosc - 10 and 10 <= nowa_pozycja[1] < wysokosc - 10):
        return False

    # Sprawdzenie, czy ruch nie powoduje kolizji z ciałem węża
    if nowa_pozycja in wez:
        return False

    # Sprawdzenie, czy wąż ma wystarczająco dużo przestrzeni, aby kontynuować ruch
    wez_po_ruchu = [nowa_pozycja] + wez[:-1]
    wolne_kratki = 0
    for k in [(20, 0), (-20, 0), (0, 20), (0, -20)]:  # Sprawdzanie wolnych pól o dwa ruchy od głowy
        kolejna_pozycja = [nowa_pozycja[0] + k[0], nowa_pozycja[1] + k[1]]
        if kolejna_pozycja not in wez_po_ruchu and 10 <= kolejna_pozycja[0] < szerokosc - 10 and 10 <= kolejna_pozycja[1] < wysokosc - 10:
            wolne_kratki += 1

    return wolne_kratki > 0  # Zwraca True, jeśli istnieje przynajmniej jedna wolna kratka do ruchu

