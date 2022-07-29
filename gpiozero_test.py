# - *- coding: utf-8 - *-
from gpiozero import LED
from time import sleep
import traceback
from datetime import datetime, timedelta
import sys
import os
from without_wifi.withoutwifi import WithoutWifi

def nazwa_programu():
    return "gpiozero_test.py"

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

# red = LED(4)

# while True:
#     red.on()
#     print("wlaczone")
#     sleep(3)
#     red.off()
#     print("wylaczone")
#     sleep(3)

class Klasa_GSM(object):
    def __init__(self):
        drukuj("ziemia dla ziemniakow")
        #self.without_wifi = WithoutWifi(path=args.path_gsm, baudrate=args.baudrate, APN=args.APN,sleep_to_read_bytes=self.time_download_file_gsm, reset_pin=self.reset_pin)
        path_gsm="/dev/serial0"
        baudrate=115200
        APN="internet"
        sleep_to_read_bytes=15000
        reset_pin=36
        self.without_wifi = WithoutWifi(path=path_gsm, baudrate=baudrate, APN=APN,sleep_to_read_bytes=sleep_to_read_bytes, reset_pin=reset_pin)
        drukuj("koniec") 

def main():
    drukuj("czemu te karabiny nie strzelają!")
    klasa_gsm = Klasa_GSM()
 
if __name__ == "__main__":
    obecny_folder = os.getcwd()
    main()
    przerwij_i_wyswietl_czas()

