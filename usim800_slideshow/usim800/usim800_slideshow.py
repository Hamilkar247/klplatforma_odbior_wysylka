
#!/usr/bin/python3
# - *- coding: utf-8 - *-

import logging
import traceback
import sys

import serial
from usim800_slideshow.usim800.Communicate_slideshow import communicate_slideshow
from usim800_slideshow.usim800.Request_slideshow import request_httpconnection
from usim800_slideshow.usim800.Request_slideshow import request_ftpconnection
from usim800_slideshow.usim800.Sms import sms

from datetime import datetime
def nazwa_programu():
    return "usim800_slideshow.py"

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

class sim800_slideshow(communicate_slideshow):
    TIMEOUT = 1

    def __init__(self, baudrate, path, APN, sleep_to_read_bytes,
                 reset_pin, time_packet_ftp):
        drukuj("usim800_slideshow http, ftp, sms")
        self.port = serial.Serial(path, baudrate, timeout=sim800_slideshow.TIMEOUT)
        #drukuj("wchodzimy do sms")
        #self.modul_sms = sms(self.port)
        #drukuj("i za sms-em")

        #self.modul_sms.send(telefon, tresc)

        #drukuj("port: " + str(self.port))
        #super().__init__(self.port)

        #self.requests = request_httpconnection(self.port)
        #self.requests.set_reset_pin(reset_pin)
        #self.requests.set_APN(APN)
        #self.requests.set_sleep_to_read_bytes(sleep_to_read_bytes=sleep_to_read_bytes)

        #self.request_ftp = request_ftpconnection(self.port)
        #self.request_ftp.set_time_packet_ftp(time_packet_ftp=time_packet_ftp)
        #self.request_ftp.set_reset_pin(reset_pin)
        
        #self.info = info(self.port)
    

    def __wyslij_sms__(self, telefon, tresc):
        drukuj("__wyslij_sms__"+str(telefon)+" "+str(tresc))
        self.modul_sms = sms(self.port)
        #drukuj("i za sms-em")
        self.modul_sms.send(telefon, tresc)
  
    def __wyslij_email__(self, email, tresc):
        drukuj("wyslij_email")

    def __update__(self, baudrate, path, APN, sleep_to_read_bytes,
                   reset_pin, time_packet_ftp):
        drukuj("ftp")
        self.port = serial.Serial(path, baudrate, timeout=sim800_slideshow.TIMEOUT)
        drukuj("port: " + str(self.port))
        super().__init__(self.port)

        self.requests.set_APN(APN=APN)
        self.requests.set_sleep_to_read_bytes(sleep_to_read_bytes=sleep_to_read_bytes)
        self.requests.set_reset_pin(reset_pin)

        self.request_ftp = request_ftpconnection(self.port)
        self.request_ftp.set_time_packet_ftp(time_packet_ftp)
        self.request_ftp.set_reset_pin(reset_pin)
