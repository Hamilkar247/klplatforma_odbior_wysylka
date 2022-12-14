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
import ubijaj_rtl_433
import testowy_process_dla_watka
from funkcje_pomocnicze import FunkcjePomocnicze, ExceptionEnvProjektu, ExceptionNotExistFolder, ExceptionWindows

#####################

def nazwa_programu():
    return "petla_programu.py"

def funkcje_pomocnicze_inicjalizacja():
    fp=FunkcjePomocnicze(nazwa_programu())
    return fp

##################

class thread_with_exception(threading.Thread):
    def __init__(self, name = "", target = None, start_time = None, interval = None, steady_going = None):
        threading.Thread.__init__(self)

        self.fp=funkcje_pomocnicze_inicjalizacja()

        self.name = name
        self.target = target
        #unix time
        self.start_time = start_time
        #autorytarnie powiem - że w minutach powinno być
        self.interval = interval
        self.steady_going = steady_going
        self.fp.drukuj(f"{self.name}: def: __init__")

    def start(self, start_time = None):
        threading.Thread.start(self) 
        self.fp.drukuj(f"{self.name}: def: start")
        self.set_start_time(start_time)

    def set_start_time(self, start_time = None):
        self.fp.drukuj(f"{self.name}: def: set_start_time")
        self.start_time = start_time

    def get_name(self):
        return self.name

    def get_target(self):
        return self.target

    def get_start_time(self):
        return self.start_time

    def get_interval(self):
        return self.interval

    def get_steady_going(self):
        return self.steady_going
    
    def get_attributes(self):
        self.fp.drukuj("def: get_attributes")
        atrybuty = {
            "name": self.name,
            "target": self.target,
            "start_time": self.start_time,
            "interval": self.interval,
            "steady_going": self.steady_going
        }
        print(atrybuty)
        return atrybuty

    def run(self):
        self.fp.drukuj(f"{self.name}: def: run")
        # target function of the thread class
        try:
            self.target()
        finally:
            self.fp.drukuj(f'koniec watku {self.name}')
        
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

    def __init__(self, basic_path_ram):
        self.fp=funkcje_pomocnicze_inicjalizacja()
        #twe=thread_with_exception()
        self.basic_path_ram = basic_path_ram
    
    #przemnazam ułamki minut by miec calosci i dopiero wtedy 
    def dzielenie_modulo_minuty(self, liczba_1, liczba_2, watek_name):
        #mnoże razy dwa żeby granulacje półminutową w dzieleniu modulo wziąć pod uwagę
        liczb_calk_1 = liczba_1 * 2
        liczb_calk_2 = liczba_2 * 2
        wynik = liczb_calk_1 % liczb_calk_2
        self.fp.drukuj(f"name: {watek_name} czas_gran: {liczb_calk_1} interval: {liczb_calk_2} wynik_modulo: {wynik}")
        return wynik 
    
    def start(self):
        self.fp.drukuj(nazwa_programu)
        try:
            watki=[]
            krok=0.5 #pół minuty
            czas_wedlug_granulacji=0
            watki.append(thread_with_exception(name="sort_srednia", 
                                              target=sortowanie_i_usrednianie_pomiarow.main, 
                                              interval=0.5,
                                              steady_going=False))
            watki.append(thread_with_exception(name="pomiar_rtl_433",
                                               target=pomiar_rtl_433.main,
                                               interval=1,#0.5,
                                               steady_going=True))
            watki.append(thread_with_exception(name="wysylka", 
                                              target=wysylanie_pomiarow_do_outsystem.main,
                                              interval=1,
                                              steady_going=False))
            watki.append(thread_with_exception(name="zaciaganie_z_outsystem",
                                              target=zaciaganie_plikow_z_outsystemu.main,
                                              interval=5,
                                              steady_going=False))
            watki.append(thread_with_exception(name="ubijaj_rtl_433",
                                              target=ubijaj_rtl_433.main,
                                              interval=0.5,#0.5,
                                              steady_going=False))
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
                    self.fp.drukuj(f"id wątku!: {watek.get_id()}")  
                    self.fp.drukuj(f"name: {watek.get_name()} , start_time: {watek.get_start_time()}")
                    if self.dzielenie_modulo_minuty(czas_wedlug_granulacji, watek.get_interval(), watek.get_name()) == 0:
                        atrybuty=watek.get_attributes()
                        watek.raise_exception()
                        nowy_watek=thread_with_exception(name=atrybuty['name'], 
                                         target=atrybuty['target'],
                                         interval=atrybuty['interval'],
                                         steady_going=atrybuty['steady_going'])
                        nowy_watek.start(start_time=datetime.now())
                        new_watki.append(nowy_watek)                        
                    else:
                        new_watki.append(watek)
                    if watek.get_steady_going() == True:
                        self.fp.drukuj("parametr stead_going")
                        path_pomiary_minuta = f"{self.basic_path_ram}/pomiary_minuta.txt"
                        if os.path.exists(path_pomiary_minuta) == False:
                            new_watki.append(nowy_watek)
                            self.fp.drukuj("wyglada na to ze nie ma pomiaru - otwieram nowy watek")
                        else:
                            self.fp.drukuj("trwa pomiar - nie odpalam nowego programu do pomiaru ")
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
            dotenv_path="../env_programu"
            if os.path.exists(dotenv_path) == True:
                load_dotenv(dotenv_path)
            else:
                raise ExceptionEnvProjektu
            basic_path_ram=fp.zmienna_env_folder("basic_path_ram","basic_path_ram - coś nie tak")
            config_folder="config_klplatforma"
            if os.path.isdir(f"../{config_folder}") == False:
                os.mkdir(f"../{config_folder}")
            #rozbija na scieszke i ogon - a wiec reszte scieszki i koncowy element
            head, tail = os.path.split(os.getcwd())
            path_to_config=f"{head}/{config_folder}" #zmienna_env_folder("path_to_config", "path_to_config - coś nie tak")
            
            flara_skryptu=f"{basic_path_ram}/{nazwa_programu()}.flara"
            fp.stworz_flare_z_pid(flara_skryptu)
            pp=ProgramPetla(basic_path_ram)
            pp.start()
        else:
            fp.drukuj("oprogramuj tego windowsa ziom")
        fp.usun_flare(basic_path_ram, flara_skryptu)
    except ExceptionEnvProjektu as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"czy napewno skopiowales env_programu.example i podmieniles tam scieszki na takie jakie maja byc w programie?")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, flara_skryptu)
    except ExceptionWindows as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"Brak wersji oprogramowania na windowsa - wymaga analizy i/lub dopisania kodu")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, flara_skryptu)
    except Exception as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"sprawdz czy env_programu widziany jest w crontabie")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, flara_skryptu)

if __name__ == '__main__':
    main()
