# - *- coding: utf-8 - *-

import os
import sys
import traceback
from datetime import datetime

def nazwa_programu():
    return "commit_file_update.py"

def data_i_godzina():
    now = datetime.now()
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

def main():
    a=open("commit.txt", "w")
    a.write(data_i_godzina())
    a.close()

if __name__ == "__main__":
    main()