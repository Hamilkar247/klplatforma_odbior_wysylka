#!/usr/bin/python3
# - *- coding: utf-8 - *-

import os
import shutil
import traceback
import datetime
import sys

def nazwa_programu():
    return "pliki_z_logami_programu_i_ich_utylizacja.py"

def data_i_godzina():
    now = datetime.datetime.now()
    current_time = now.strftime("%d/%m/%y %H:%M:%S")
    return current_time

def drukuj(obiekt_do_wydruku):
    try:
        print(data_i_godzina()+" "+nazwa_programu()+" "+str(obiekt_do_wydruku))
    except Exception as e:
        print(e)
        print(traceback.print_exc())

def przerwij_i_wyswietl_czas():
    czas_teraz = datetime.now()
    current_time = czas_teraz.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    sys.exit()

def czy_plik_przekracza_dopuszczalny_rozmiar(element):
    scieszka_do_pliku=element[0]
    max_rozmiar_dla_tego_pliku=element[1]
    badany_plik = os.stat(scieszka_do_pliku)
    if int(badany_plik.st_size) > int(max_rozmiar_dla_tego_pliku):
        drukuj(f"plik o scieszce {scieszka_do_pliku}")
        drukuj(f"max rozmiar dla tego pliku {max_rozmiar_dla_tego_pliku}")
        drukuj(f"rozmiar pliku {badany_plik.st_size}")
        #kopiuje obecny plik jako stary - a ten stary zastapi
        shutil.copy(scieszka_do_pliku, scieszka_do_pliku+".old")
        #zeruje stary plik na nowe logi
        file=open(scieszka_do_pliku, "w")
        file.write("\n")
        file.close()

def main():
    tablica_plikow_i_max_zakresy=[
        ["/home/weewx/wk_skrypty/wyslane_krotki.json", 50000],
        ["/home/weewx/wk_skrypty/odebrane_jsony_z_alarmami.json", 10000],
        ["/home/weewx/wk_skrypty/odebrane_jsony_z_konfiguracjami.json", 10000],
        ["/home/weewx/wk_skrypty/plik_z_krotkami_logi.json", 20000]
        ]
    drukuj("sprawdzam rozmiar plikow z logami")
    for plik_do_sprawdzenia in tablica_plikow_i_max_zakresy:
         czy_plik_przekracza_dopuszczalny_rozmiar(plik_do_sprawdzenia)

if __name__ == "__main__":
    main()