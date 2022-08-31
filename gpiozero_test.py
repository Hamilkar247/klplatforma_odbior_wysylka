# - *- coding: utf-8 - *-
from gpiozero import LED
from time import sleep
import traceback
from datetime import datetime, timedelta
import sys
import os
from without_wifi.withoutwifi import WithoutWifi
from funkcje_pomocnicze import FunkcjePomocnicze, ExceptionEnvProjektu, ExceptionNotExistFolder, ExceptionWindows
###################33

def nazwa_programu():
    return "gpiozero_test.py"

def funkcje_pomocnicze_inicjalizacja():
    fp=FunkcjePomocnicze(nazwa_programu())
    return fp

######################

class Klasa_GSM(object):
    def __init__(self):
        fp=funkcje_pomocnicze_inicjalizacja()
        fp.drukuj("ziemia dla ziemniakow")
        #self.without_wifi = WithoutWifi(path=args.path_gsm, baudrate=args.baudrate, APN=args.APN,sleep_to_read_bytes=self.time_download_file_gsm, reset_pin=self.reset_pin)
        path_gsm="/dev/serial0"
        baudrate=115200
        APN="internet"
        sleep_to_read_bytes=15000
        reset_pin=36
        self.without_wifi = WithoutWifi(path=path_gsm, baudrate=baudrate, APN=APN,sleep_to_read_bytes=sleep_to_read_bytes, reset_pin=reset_pin)
        fp.drukuj("koniec") 

def main():
    fp=funkcje_pomocnicze_inicjalizacja()
    fp.drukuj("czemu te karabiny nie strzelają!")
    klasa_gsm = Klasa_GSM()
 
if __name__ == "__main__":
    obecny_folder = os.getcwd()
    main()

