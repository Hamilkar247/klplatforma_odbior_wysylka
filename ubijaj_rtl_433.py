# - *- coding: utf-8 - *-

import os
import sys
import traceback
from datetime import datetime
import time
import signal
from dotenv import load_dotenv
import reset_portu_usb
from funkcje_pomocnicze import FunkcjePomocnicze, ExceptionEnvProjektu, ExceptionNotExistFolder, ExceptionWindows
from subprocess import check_output
from subprocess import CalledProcessError

#################################

def nazwa_programu():
    return "ubijaj_rtl_433.py"

def funkcje_pomocnicze_inicjalizacja():
    fp=FunkcjePomocnicze(nazwa_programu())
    return fp

##################################

class UbijaczRTL433():

    def __init__(self):
        self.fp=funkcje_pomocnicze_inicjalizacja()

    def get_pid(self, name):
        try:
            return int(check_output(["pidof",name]).decode('utf-8'))
        except CalledProcessError as s:
            self.fp.drukuj("nie ma procesu o takiej nazwie")
            return -1

    def start(self, basic_path_ram):
        if os.path.isdir(basic_path_ram):

            file_data_pomiaru=f"{basic_path_ram}/pomiary_minuta.txt"
            if os.path.exists(file_data_pomiaru):
                fdp=open(file_data_pomiaru, "r")
                pomiary_minuta_stworzenia=fdp.read().strip()
                fdp.close()
                self.fp.drukuj(f"minuta stworzenia pliku: {pomiary_minuta_stworzenia}")
                minuta=datetime.now().minute
                if minuta == pomiary_minuta_stworzenia:
                    return False
            else:
                self.fp.drukuj(f"nie ma {file_data_pomiaru}")
                self.fp.przerwij_i_wyswietl_czas()

            if os.name == "posix": 
                numer_pid=self.get_pid("rtl_433")
                self.fp.drukuj(f"pid rtl_433: {numer_pid}")
            
                os.remove(file_data_pomiaru)
                if numer_pid > -1:
                    os.kill(int(numer_pid), signal.SIGTERM)
                    return True    
                return False
            else:
                raise ExceptionWindows
                self.fp.drukuj("brak oprogramowania windowsa")
            return False
    
    def flary_do_sprawdzenia(self):
        self.fp.drukuj("def: flary_do_sprawdzenia")
        basic_path_ram=""
        file_path=""
        try:
            if os.name == "posix":
                self.fp.drukuj("posix")
                dotenv_path="./.env"
                self.fp.file_istnienie(dotenv_path, "dotenv_path - coś nie tak")
                load_dotenv(dotenv_path)
                basic_path_ram=self.fp.zmienna_env_folder("basic_path_ram", "sprawdz basic_path_ram")
                
                self.start(basic_path_ram)
            else:
                raise ExceptionWindows
                self.fp.drukuj("obsluz windowsa w koncu")
        except ExceptionEnvProjektu as e:
            self.fp.drukuj(f"exception {e}")
            self.fp.drukuj(f"czy napewno skopiowales .env.example i podmieniles tam scieszki na takie jakie maja byc w programie?")
            traceback.print_exc()
        except ExceptionWindows as e:
            self.fp.drukuj(f"exception {e}")
            self.fp.drukuj(f"Brak wersji oprogramowania na windowsa - wymaga analizy i/lub dopisania kodu")
            traceback.print_exc()
        except Exception as e:
            self.fp.drukuj(f"{e}")
            traceback.print_exc()

def main():
    fp=FunkcjePomocnicze(nazwa_programu())
    fp.drukuj(f"------------{nazwa_programu()}-------")
    fp.drukuj("--------------------")
    fp.drukuj(nazwa_programu())
    ur=UbijaczRTL433()
    ur.flary_do_sprawdzenia()
    
if __name__ == "__main__":
    main()
