#!/usr/bin/python3
# - *- coding: utf-8 - *-
import os
import shutil
import hashlib
from datetime import datetime, timedelta
import sys
import logging
import traceback
from without_wifi.withoutwifi import WithoutWifi


def nazwa_programu():
    return "powiadomienia_sms_email.py"

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


class Klasa_GSM(object):
    def __init__(self):
        drukuj("init - Klasa_GSM")
        #self.without_wifi = WithoutWifi(path=args.path_gsm, baudrate=args.baudrate, APN=args.APN,sleep_to_read_bytes=self.time_download_file_gsm, reset_pin=self.reset_pin)
        path_gsm="/dev/serial0"
        baudrate=115200
        APN="internet"
        sleep_to_read_bytes=100
        reset_pin=36
        #telefon="+48532819627"
        self.without_wifi = WithoutWifi(path=path_gsm, baudrate=baudrate, APN=APN,sleep_to_read_bytes=sleep_to_read_bytes, reset_pin=reset_pin)
        drukuj("koniec") 
    
    def wyslij_smsa(self, telefon, tresc):
        drukuj("wyslij_smsa")
        self.without_wifi.wyslij_sms(telefon, tresc)

    def wyslij_email(self, email, tresc):
        drukuj("wyslij_email")
        self.without_wifi.wyslij_email(email, tresc)


class PowiadomienieSmsEmail(object):

    def __init__(self):
        self.klasa_gsm = Klasa_GSM()

        tresc="NIE DOSTALISMY PUNKTA OD UKRAINY NA EUROWIZJI!"
        telefon="+48532819627"
        email="bodmelkart96@gmail.com"
        drukuj("------ POWIADOMIENIA --------")
        self.wyslij_smsa(telefon, tresc)
        self.wyslij_mejla(email, tresc)

    def wyslij_mejla(self, email, tresc):
        drukuj("wyślij_mejla " +tresc)
        self.klasa_gsm.wyslij_email(email, tresc)

    def wyslij_smsa(self, telefon, tresc):
        drukuj("wyślij_smsa "+tresc)
        self.klasa_gsm.wyslij_smsa(telefon, tresc)
    

def main():
    powiadomienie_sms_email=PowiadomienieSmsEmail()


if __name__ == "__main__":
    drukuj("------ POWIADOMIENIA --------")
    main()