# - *- coding: utf-8 - *-

from genericpath import isdir
from inspect import trace
import os
import sys
import traceback
from datetime import datetime
import time
from threading import Thread, Event
import threading
import ctypes
import subprocess
from dotenv import load_dotenv
#kusowe
import wysylanie_pomiarow_do_outsystem
import sortowanie_i_usrednianie_pomiarow
import zaciaganie_plikow_z_outsystemu
import pomiar_rtl_433
import ubijaj_procesy

def nazwa_programu():
    return "petla_programu.py"

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

class ExceptionEnvProjektu(Exception):
    pass

def file_istnienie(path_to_file, komunikat):
    if os.path.isdir(path_to_file):
        drukuj(f"{komunikat}")
        raise ExceptionEnvProjektu
    return True

def folder_istnienie(path_to_folder, komunikat):
    if os.path.isdir(path_to_folder):
        drukuj(f"{komunikat}")
        raise ExceptionEnvProjektu
    return True

def zmienna_env_file(tag_in_env, komunikat):
    path_to_file=os.getenv(tag_in_env)
    if os.path.exists(path_to_file) == False:
        drukuj(f"{komunikat}, tag:{tag_in_env}, path:{path_to_file}")#sprawdz czy plik .env istnieje")
        raise ExceptionEnvProjektu
    return path_to_file

def zmienna_env_folder(tag_in_env, komunikat):
    path_to_folder=os.getenv(tag_in_env)
    if os.path.isdir(path_to_folder) == False:
        drukuj(f"{komunikat}, tag:{tag_in_env}, path:{path_to_folder}")#sprawdz czy plik .env istnieje")
        raise ExceptionEnvProjektu
    return path_to_folder

##################

class thread_with_exception(threading.Thread):
    def __init__(self, name = "", target = None, start_time = None, interval = None):
        threading.Thread.__init__(self)
        self.name = name
        self.target = target
        #unix time
        self.start_time = start_time
        #autorytarnie powiem - że w minutach powinno być
        self.interval = interval
        drukuj(f"{self.name}: def: __init__")

    def start(self, start_time = None):
        threading.Thread.start(self) 
        drukuj(f"{self.name}: def: start")
        self.set_start_time(start_time)

    def set_start_time(self, start_time = None):
        drukuj(f"{self.name}: def: set_start_time")
        self.start_time = start_time

    def get_start_time(self):
        return self.start_time

    def get_interval(self):
        return self.interval
    
    def get_attributes(self):
        drukuj("def: get_attributes")
        atrybuty = {
            "name": self.name,
            "target": self.target,
            "start_time": self.start_time,
            "interval": self.interval
        }
        print(atrybuty)
        return atrybuty

    def run(self):
        drukuj(f"{self.name}: def: run")
        # target function of the thread class
        try:
            self.target()
        finally:
            drukuj('ended')
        
    def get_id(self):
        drukuj(f"{self.name}: def: get_id")
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        drukuj(f"{self.name}: def: raise_exception")
        thread_id = self.get_id()
        drukuj(f"{self.name}: thread_id:{thread_id}")
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            drukuj(f"{self.name}: Exception raise failure")

#przemnazam ułamki minut by miec calosci i dopiero wtedy 
def dzielenie_modulo_minuty(liczba_1, liczba_2):
    #mnoże razy dwa żeby granulacje półminutową w dzieleniu modulo wziąć pod uwagę
    liczb_calk_1 = liczba_1 * 2
    liczb_calk_2 = liczba_2 * 2
    wynik = liczb_calk_1 % liczb_calk_2
    print(f" {liczb_calk_1} {liczb_calk_2} {wynik}")
    return wynik 

def start():
    drukuj(nazwa_programu)
    try:
        watki=[]
        krok=0.5 #pół minuty
        czas_wedlug_granulacji=0
        watki.append(thread_with_exception(name="sort_srednia", 
                                          target=sortowanie_i_usrednianie_pomiarow.main, 
                                          interval=0.5))
        watki.append(thread_with_exception(name="pomiar_rtl_433",
                                           target=pomiar_rtl_433.main,
                                           interval=1))
        watki.append(thread_with_exception(name="wysylka", 
                                          target=wysylanie_pomiarow_do_outsystem.main,
                                          interval=1))
        watki.append(thread_with_exception(name="zaciaganie_z_outsystem", 
                                          target=zaciaganie_plikow_z_outsystemu.main,
                                          interval=5))
        watki.append(thread_with_exception(name="ubijaj_procesy",
                                           target=ubijaj_procesy.main,
                                           interval=3))

        while True:
            print("-------------------------------")
            drukuj(f"czas:{czas_wedlug_granulacji}")
            drukuj(f"watki: {watki}")
            new_watki=[]
            for watek in watki:
                if dzielenie_modulo_minuty(czas_wedlug_granulacji, watek.get_interval()) == 0:
                    atrybuty=watek.get_attributes()
                    watek.raise_exception()
                    nowy_watek=thread_with_exception(name=atrybuty['name'], 
                                     target=atrybuty['target'],
                                     interval=atrybuty['interval'])
                    nowy_watek.start(start_time=datetime.now())
                    new_watki.append(nowy_watek)
                else:
                    new_watki.append(watek)
            watki = new_watki
            time.sleep(krok*60) #time.sleep będą w sekundach 0.5*60=30
            czas_wedlug_granulacji = czas_wedlug_granulacji + krok
            if czas_wedlug_granulacji > 60:
                drukuj("pelna godzina - od nowa")
                czas_wedlug_granulacji = 0
    except Exception as e:
        drukuj(f"Błąd: {e}")
        traceback.print_exc()

def main():
    basic_path_ram=""
    flara_skryptu=""
    try:
        drukuj(f"------{nazwa_programu()}--------")
        if os.name=="posix":
            drukuj("posix")
            dotenv_path="./.env"
            file_istnienie(dotenv_path, "dotenv_path - coś nie tak")
            load_dotenv(dotenv_path)
            basic_path_ram=zmienna_env_folder("basic_path_ram","basic_path_ram - coś nie tak")
            path_to_config=zmienna_env_folder("path_to_config", "path_to_config - coś nie tak")
            
            flara_skryptu=f"{basic_path_ram}/{nazwa_programu()}.flara"
            flara_file=open(flara_skryptu, "w")
            flara_file.write(f"{str(os.getpid())}")
            flara_file.close()
            start()
        else:
            drukuj("oprogramuj tego windowsa ziom")
    except ExceptionEnvProjektu as e:
        drukuj(f"exception {e}")
        drukuj(f"czy napewno skopiowales .env.example i podmieniles tam scieszki na takie jakie maja byc w programie?")
        traceback.print_exc()
    except Exception as e:
        drukuj(f"exception {e}")
        drukuj(f"sprawdz czy .env widziany jest w crontabie")
        traceback.print_exc()
    if os.path.isdir(basic_path_ram):
        if os.path.exists(flara_skryptu):
            os.remove(flara_skryptu)
            drukuj("usuwam flare")

if __name__ == '__main__':
    main()
