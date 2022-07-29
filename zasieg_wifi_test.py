# - *- coding: utf-8 - *-

import subprocess
from math import log10
import sys
import os
import traceback
from datetime import datetime
from dotenv import load_dotenv

def nazwa_programu():
    return "zasieg_wifi_test.py"

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
    dotenv_path = "./.env"
    load_dotenv(dotenv_path)
    nazwa_interfejsu=os.getenv('nazwa_interfejsu')
    print(nazwa_interfejsu)
    cmd=f"/usr/sbin/iwconfig {nazwa_interfejsu} | grep Signal"# | /usr/bin/awk '{print $4}' | /usr/bin/cut -d'=' -f2"
    #cmd="/usr/sbin/iwconfig wlan0 | grep Signal | /usr/bin/awk '{print $4}' | /usr/bin/cut -d'=' -f2"
    dbm = os.popen(cmd).read()
    if dbm:
        drukuj(f"dbm:{dbm}")
        #spodziewane
        #          Link Quality=56/70  Signal level=-54 dBm  
        dbm_z_jedn=dbm.split("level=")[1]
        try:
            dbm_liczba=int(dbm_z_jedn.split(" ")[0])
            drukuj(f"{dbm_liczba}")
            quality = 2 * (dbm_liczba + 100)
            drukuj("{0} dbm_num = {1}%".format(dbm_liczba, quality))
            return str(quality)
        except Exception as e:
            drukuj("brak liczby")
            drukuj(f"{e}")
            traceback.print_exc()
        
        #dbm_num = int(dbm)
        #quality = 2 * (dbm_num + 100)
        #drukuj("{0} dbm_num = {1}%".format(dbm_num, quality))
        #return str(quality)
    else:
        drukuj("Siła sygnału połączenia wifi router nie została znaleziona")
        #return str(-1)


if __name__ == "__main__":
    main()