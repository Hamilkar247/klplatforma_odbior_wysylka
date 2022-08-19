import os
from datetime import datetime
import sys
import traceback
from getmac import get_mac_address as gma
import time

def nazwa_programu():
    return "testy_get_time_of_create_file.py"

def data_i_godzina():
    now = datetime.now()
    current_time = now.strftime("%d/%m/%y %H:%M:%S")
    return current_time

def drukuj(obiekt_do_wydruku):
    try:
        print(data_i_godzina()+" "+nazwa_programu()+" "+str(obiekt_do_wydruku))
    except Exception as e:
        print("blad w metodzie drukuj - sprawdz czy nie wywolales funkcji bez zadnego parametru")
        print(e)
        print(traceback.print_exc())

def przerwij_i_wyswietl_czas():
    czas_teraz = datetime.now()
    current_time = czas_teraz.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    sys.exit()

def main():
    pass
    path_file=f"/home/matball/Projects/TermoHigroLightlog/klplatforma_odbior_wysylka/testy_i_stare_pliki_klraspi/{nazwa_programu()}"
    file_creation_time=""
    file_creation_time_2=""
    if os.name == "posix":
        drukuj("NIE DA SIE linuxy nie przejmuja sie data stworzenia pliku")
        file_creation_time=os.stat(path_file).st_birthname
        drukuj(file_creation_time)
        file_creation_time_2=time.strftime("%H:%M:%S", file_creation_time)
    else:
        file_creation_time=os.path.getctime(path_file)
    print(f"file create: {file_creation_time_2}")

if __name__ == "__main__":
    main()