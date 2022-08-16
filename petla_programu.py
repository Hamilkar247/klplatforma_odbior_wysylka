# - *- coding: utf-8 - *-

from distutils.command.config import config
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
from funkcje_pomocnicze import FunkcjePomocnicze, ExceptionEnvProjektu, ExceptionNotExistFolder, ExceptionWindows

#####################

def nazwa_programu():
    return "petla_programu.py"

def funkcje_pomocnicze_inicjalizacja():
    fp=FunkcjePomocnicze(nazwa_programu())
    return fp

##################

class thread_with_exception(threading.Thread):
    def __init__(self, name = "", target = None, start_time = None, interval = None):
        threading.Thread.__init__(self)

        self.fp=funkcje_pomocnicze_inicjalizacja()

        self.name = name
        self.target = target
        #unix time
        self.start_time = start_time
        #autorytarnie powiem - że w minutach powinno być
        self.interval = interval
        self.fp.drukuj(f"{self.name}: def: __init__")

    def start(self, start_time = None):
        threading.Thread.start(self) 
        self.fp.drukuj(f"{self.name}: def: start")
        self.set_start_time(start_time)

    def set_start_time(self, start_time = None):
        self.fp.drukuj(f"{self.name}: def: set_start_time")
        self.start_time = start_time

    def get_start_time(self):
        return self.start_time

    def get_interval(self):
        return self.interval
    
    def get_attributes(self):
        self.fp.drukuj("def: get_attributes")
        atrybuty = {
            "name": self.name,
            "target": self.target,
            "start_time": self.start_time,
            "interval": self.interval
        }
        print(atrybuty)
        return atrybuty

    def run(self):
        self.fp.drukuj(f"{self.name}: def: run")
        # target function of the thread class
        try:
            self.target()
        finally:
            self.fp.drukuj('ended')
        
    def get_id(self):
        self.fp.drukuj(f"{self.name}: def: get_id")
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        self.fp.drukuj(f"{self.name}: def: raise_exception")
        thread_id = self.get_id()
        self.fp.drukuj(f"{self.name}: thread_id:{thread_id}")
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            self.fp.drukuj(f"{self.name}: Exception raise failure")

class ProgramPetla():

    def __init__(self):
        self.fp=funkcje_pomocnicze_inicjalizacja()
        #twe=thread_with_exception()
    
    #przemnazam ułamki minut by miec calosci i dopiero wtedy 
    def dzielenie_modulo_minuty(self, liczba_1, liczba_2):
        #mnoże razy dwa żeby granulacje półminutową w dzieleniu modulo wziąć pod uwagę
        liczb_calk_1 = liczba_1 * 2
        liczb_calk_2 = liczba_2 * 2
        wynik = liczb_calk_1 % liczb_calk_2
        self.fp.drukuj(f" {liczb_calk_1} {liczb_calk_2} {wynik}")
        return wynik 
    
    def start(self):
        self.fp.drukuj(nazwa_programu)
        try:
            watki=[]
            krok=0.5 #pół minuty
            czas_wedlug_granulacji=0
            watki.append(thread_with_exception(name="sort_srednia", 
                                              target=sortowanie_i_usrednianie_pomiarow.main, 
                                              interval=0.5))
            watki.append(thread_with_exception(name="pomiar_rtl_433",
                                               target=pomiar_rtl_433.main,
                                               interval=100))
            watki.append(thread_with_exception(name="wysylka", 
                                              target=wysylanie_pomiarow_do_outsystem.main,
                                              interval=1))
            watki.append(thread_with_exception(name="zaciaganie_z_outsystem", 
                                              target=zaciaganie_plikow_z_outsystemu.main,
                                              interval=5))
            #tymczasowo nie pasuje mi do koncepcji - refactor potrzebny
            #watki.append(thread_with_exception(name="ubijaj_procesy",
            #                                   target=ubijaj_procesy.main,
            #                                   interval=5))
    
            while True:
                print("-------------------------------")
                self.fp.drukuj(f"czas:{czas_wedlug_granulacji}")
                self.fp.drukuj(f"watki: {watki}")
                new_watki=[]
                for watek in watki:
                    if self.dzielenie_modulo_minuty(czas_wedlug_granulacji, watek.get_interval()) == 0:
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
                    self.fp.drukuj("pelna godzina - od nowa")
                    czas_wedlug_granulacji = 0
        except Exception as e:
            self.fp.drukuj(f"Błąd: {e}")
            traceback.print_exc()

def main():
    fp=FunkcjePomocnicze(nazwa_programu())
    basic_path_ram=""
    flara_skryptu=""
    try:
        fp.drukuj(f"------{nazwa_programu()}--------")
        if os.name=="posix":
            fp.drukuj("posix")
            dotenv_path="./.env"
            fp.file_istnienie(dotenv_path, "dotenv_path - coś nie tak")
            load_dotenv(dotenv_path)
            basic_path_ram=fp.zmienna_env_folder("basic_path_ram","basic_path_ram - coś nie tak")
            config_folder="config_klplatforma"
            if os.path.isdir(f"../{config_folder}") == False:
                os.mkdir(f"../{config_folder}")
            #rozbija na scieszke i ogon - a wiec reszte scieszki i koncowy element
            head, tail = os.path.split(os.getcwd())
            path_to_config=f"{head}/{config_folder}" #zmienna_env_folder("path_to_config", "path_to_config - coś nie tak")
            
            flara_skryptu=f"{basic_path_ram}/{nazwa_programu()}.flara"
            fp.stworz_flare_z_pid(flara_skryptu)
            pp=ProgramPetla()
            pp.start()
        else:
            drukuj("oprogramuj tego windowsa ziom")
        fp.usun_flare(basic_path_ram, flara_skryptu)
    except ExceptionEnvProjektu as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"czy napewno skopiowales .env.example i podmieniles tam scieszki na takie jakie maja byc w programie?")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, flara_skryptu)
    except ExceptionWindows as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"Brak wersji oprogramowania na windowsa - wymaga analizy i/lub dopisania kodu")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, flara_skryptu)
    except Exception as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"sprawdz czy .env widziany jest w crontabie")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, flara_skryptu)

if __name__ == '__main__':
    main()
