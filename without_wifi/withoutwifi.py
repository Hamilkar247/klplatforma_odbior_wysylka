#!/usr/bin/python3
# - *- coding: utf-8 - *-

import logging
import os
import traceback
import sys
from pprint import pprint
from usim800_slideshow.usim800 import sim800_slideshow
from datetime import datetime
def nazwa_programu():
    return "withoutwifi.py"

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


class WithoutWifi:
    def __init__(self, path, baudrate, APN, sleep_to_read_bytes, reset_pin):
        try:
            drukuj("without wifi")
            drukuj(f"reset_pin: {reset_pin}")
            self.gsm = sim800_slideshow(baudrate=baudrate, path=path, APN=APN, sleep_to_read_bytes=sleep_to_read_bytes,
                                        reset_pin=reset_pin, time_packet_ftp=1)
            self.r = None
        except Exception as e:
            drukuj("Wystąpił błąd przy próbie otwarcia portu GsmSlideshow - możliwe że inny program używa już podanego portu!")
            traceback.print_exc()
        drukuj("zakonczony init")

    def wyslij_sms(self, telefon, tresc):
        try:
            self.gsm.__wyslij_sms__(telefon, tresc)
        except Exception as e:
            drukuj("Wystąpił błąd przy próbie wyslanie smsa - możliwe że inny program używa już podanego portu!")
            drukuj("lub brak uprawnień dla użytkownika do obsługiwania portu UART")
            traceback.print_exc()
        drukuj("zakonczony wysylanie_smsa")

    def wyslij_email(self, email, tresc):
        #nie wydaje się trywailne
        pass
        
    def update_zmiennych(self, path, baudrate, APN, sleep_to_read_bytes, reset_pin):
        try:
            drukuj("without_wifi  - update zmiennych")
            self.gsm.__update__(baudrate=baudrate, path=path, reset_pin=reset_pin, APN=APN,
                                sleep_to_read_bytes=sleep_to_read_bytes, time_packet_ftp=1)
        except Exception as e:
            drukuj("Wystąpił błąd przy próbie otwarcia portu Ftplideshow - możliwe że inny program używa już podanego portu!")
            traceback.print_exc()

    #updatuje zmienne ftp
    def update_variable_ftp(self, path, baudrate, reset_pin, time_packet_ftp):
        try:
           drukuj("update zmiennych ftp slideshow")
           self.gsm.__update__(baudrate=baudrate, path=path, reset_pin=reset_pin, time_packet_ftp=time_packet_ftp)
        except Exception as e:
            drukuj("Wystąpił błąd przy próbie otwarcia portu Ftplideshow - możliwe że inny program używa już podanego portu!")
            traceback.print_exc()

    #pobieranie po http
    def download_file(self, nazwa_pliku, url, sleep_to_read_bytes):
        try:
            if os.path.exists(nazwa_pliku+".download"):
                drukuj(f"usuwam dotychczasowy plik {nazwa_pliku}.download")
                os.remove(nazwa_pliku+".download")
            result = self.gsm.requests.getFile(url=url, sleep_to_read_bytes=sleep_to_read_bytes,
                                             nameOfFile=nazwa_pliku+".download")
        except Exception as e:
            drukuj("Niestety jest błąd - wyrzuciło download_file w GsmSlideshow")
            drukuj(f"{e}")
            traceback.print_exc()
            return False
        drukuj("pobralem plik")
        return True

    #pobieranie po http
    def download_file_by_parts(self, nazwa_pliku, url_folder, sleep_to_read_bytes):
        try:
            #usuwam obecny plik z zdjeciem nazwa_pliku.download
            if os.path.exists(nazwa_pliku+".download"):
                drukuj(f"usuwam dotychaczowy plik {nazwa_pliku}'.download'")
                os.remove(nazwa_pliku+".download")
            x=0
            end_picture = open(nazwa_pliku+".download", "ab")
            while True:
                drukuj(x)
                name_part = nazwa_pliku+"_"+str(x)
                drukuj(f"name_part:{name_part}")
                result = self.gsm.requests.getFile(url=url_folder + "/" + name_part,
                                                   sleep_to_read_bytes=sleep_to_read_bytes,
                                                   nameOfFile=name_part)
                if os.path.exists(name_part):
                    f = open(name_part, "rb")
                    end_picture.write(f.read())
                    #os.remove(name_part)
                else:
                    break
                x=x+1
        except Exception as e:
            drukuj("Niestety jest błąd - wyrzuciło download_file w GsmSlideshow")
            drukuj(f"{e}")
            traceback.print_exc()
            return False
        logging.debug("pobralem plik")
        return True

    #usuwam zbedne linie
    def delete_redundant_lines(tag_string):
        text_to_parse = []
        lines = tag_string.lstrip().split('\n')
        for number in range(len(lines) - 1):
            #print(f"AHJO-{number}")
            pprint(lines[number].split())
            # print(f"lines {number} {lines[number].split()}")
            if len(lines[number].split()) - 1 == 8:
                # print("dodaje linie do zbioru")
                text_to_parse.append(lines[number])
        return text_to_parse

    def get_files_metadata(self,
                         APN,
                         server_ip,
                         get_path_file,
                         nickname,
                         password,
                         port = 21,
                         mode = 0
                           ):
        logging.debug("get_files_matadata <-- FtpSlideshow")
        try:
            metadata=self.gsm.request_ftp.getFilesMetadata(APN=APN,
                                                           server_ip=server_ip,
                                                           port=port, mode=mode,
                                                           get_path_file=get_path_file,
                                                           nickname=nickname,
                                                           password=password)
            return metadata
        except Exception as e:
            print("Niestety nie udało pobrać metadanych podanego folderu")
            print(f"{e}")
            traceback.print_exc()
            return b'error'

    def get_file(self, APN, get_name_file ,server_ip,
                 nickname, password, port=21, mode=0, get_path_file="/"):
        print("get_file <-- FtpSlideshow ")
        try:
            file = self.gsm.request_ftp.getFile(APN=APN, server_ip=server_ip, port=21, mode=0,
                                         get_name_file=get_name_file, get_path_file=get_path_file,
                                         nickname=nickname, password=password)
        except Exception as e:
            print("Niestety - nie udało się wysłać wiadomości na serwer")
            print(f"{e}")
            traceback.print_exc()
            return b'error'
        return file

    def post_file(self, text_to_post, APN="internet",
                  server_ip="37.48.70.196", port=21, mode=0,
                  put_name_file="hami.json", get_name_file="hami.json",
                  put_path_file="/hamilkar.cba.pl/myhero/",
                  get_path_file="/",
                  nickname="hamilkar", password="Hamilkar0"
                  ):
        try:
            self.gsm.request_ftp.postFile(APN=APN, server_ip=server_ip, port=port,
                                          mode=mode,
                                          put_name_file=put_name_file,
                                          get_name_file=get_name_file,
                                          put_path_file=put_path_file,
                                          get_path_file=get_path_file,
                                          nickname=nickname, password=password,
                                          text_to_post=text_to_post)
        except Exception as e:
            print("Niestety - nie udało się wysłać wiadomości na serwer")
            print(f"{e}")
            traceback.print_exc()
            return False
        logging.debug("koniec pliku ")
        return True
