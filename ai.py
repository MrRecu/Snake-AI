def proste_ai(wez, cel, szerokosc, wysokosc):
    glowa = wez[0]
    kierunek_x, kierunek_y = 0, 0

    # Sprawdzenie bezpiecznych ruchów
    bezpieczny_ruch_w_prawo = glowa[0] + 10 < szerokosc - 10 and [glowa[0] + 10, glowa[1]] not in wez
    bezpieczny_ruch_w_lewo = glowa[0] - 10 >= 10 and [glowa[0] - 10, glowa[1]] not in wez
    bezpieczny_ruch_w_dol = glowa[1] + 10 < wysokosc - 10 and [glowa[0], glowa[1] + 10] not in wez
    bezpieczny_ruch_w_gore = glowa[1] - 10 >= 10 and [glowa[0], glowa[1] - 10] not in wez

    # Kierowanie węża w poziomie
    if glowa[0] < cel[0] and bezpieczny_ruch_w_prawo:
        kierunek_x = 10  # Idź w prawo
    elif glowa[0] > cel[0] and bezpieczny_ruch_w_lewo:
        kierunek_x = -10  # Idź w lewo

    # Kierowanie węża w pionie
    if glowa[1] < cel[1] and bezpieczny_ruch_w_dol:
        kierunek_y = 10  # Idź w dół
    elif glowa[1] > cel[1] and bezpieczny_ruch_w_gore:
        kierunek_y = -10  # Idź w górę

    # Wybór kierunku z unikaniem stykania się z własnym ciałem
    if kierunek_x != 0 and (kierunek_y == 0 or len(wez) < 3):
        return kierunek_x, 0
    elif kierunek_y != 0:
        return 0, kierunek_y
    else:
        # Ostatnia deska ratunku: unikanie stykania się z ciałem
        if bezpieczny_ruch_w_prawo:
            return 10, 0
        elif bezpieczny_ruch_w_lewo:
            return -10, 0
        elif bezpieczny_ruch_w_dol:
            return 0, 10
        elif bezpieczny_ruch_w_gore:
            return 0, -10

    # Jeśli żaden ruch nie jest możliwy bez stykania się z ciałem, zatrzymaj się
    return 0, 0
