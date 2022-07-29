#!/usr/bin/python3
# - *- coding: utf-8 - *-
import os
import shutil
import hashlib
from datetime import datetime, timedelta
import sys
import logging
import traceback
from typing import Type
from requests import Session
import requests
from urllib.request import urlopen
import json
import subprocess
import time
import pprint
import json

def nazwa_programu():
    return "sortowanie_i_usrednianie_pomiarow.py"

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
    pass
    path="/run/user/1000/pomiary.txt.old"
    with open(path, "r") as file:
        krotki=file.readlines()
    drukuj(f"{krotki}")
    for krotka in krotki:
        drukuj(krotka)
        obj_json=json.loads(krotka)
        przerwij_i_wyswietl_czas()

    

if __name__ == "__main__":
    drukuj("------testy_json_loads_na_pliku.py--------")
    main()
