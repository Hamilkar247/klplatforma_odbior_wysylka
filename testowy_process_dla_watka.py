# - *- coding: utf-8 - *-
import os
from datetime import datetime, timedelta
import sys
import traceback
from typing import Type
from requests import Session
import requests
from urllib.request import urlopen
import json
import time
from dotenv import load_dotenv
from funkcje_pomocnicze import FunkcjePomocnicze, ExceptionEnvProjektu, ExceptionNotExistFolder, ExceptionWindows

####################

def nazwa_programu():
    return "testowy_process_dla_watka.py"

def funkcje_pomocnicze_inicjalizacja():
    fp=FunkcjePomocnicze(nazwa_programu())
    return fp

class Testowy(object):
    def __init__(self):
        fp=funkcje_pomocnicze_inicjalizacja()
        liczba=0
        while True:
            liczba=liczba+1
            if liczba > 60:
                break

    def start(self):
        self.fp.drukuj(self.fp.data_i_godzina())

def main():
    fp=funkcje_pomocnicze_inicjalizacja()
    basic_path_ram=""
    flara_skryptu=""
    try:
        fp.drukuj(f"------{nazwa_programu()}--------")
        testowy=Testowy()
    except Exception as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"sprawdz czy .env widziany jest w crontabie")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, flara_skryptu)

if __name__ == "__main__":
    main()