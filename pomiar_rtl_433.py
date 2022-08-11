# - *- coding: utf-8 - *-

import os
import sys
import traceback
from datetime import datetime
import time
import subprocess
import shutil
from dotenv import load_dotenv
from funkcje_pomocnicze import FunkcjePomocnicze, ExceptionEnvProjektu, ExceptionNotExistFolder, ExceptionWindows

##########################

def nazwa_programu():
    return "pomiar_rtl_433.py"

def funkcje_pomocnicze_inicjalizacja():
    fp=FunkcjePomocnicze(nazwa_programu())
    return fp

##########################

class PomiarRTL433():

    def __init__(self):
        self.fp=funkcje_pomocnicze_inicjalizacja()

    def start(self,  basic_path_ram):
        self.fp.drukuj(" - - - - - - -")
        self.fp.drukuj(nazwa_programu())
        file_path=f"{basic_path_ram}/pomiary.txt"
        file=open(file_path, "a")
        command=f"rtl_433 -s 2.5e6 -f 868.5e6 -H 30 -R 75 -R 150 -F json".split(" ")
        minuta=datetime.now().minute
        print(f"{minuta}")
        with subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
            for line in p.stdout:
                #ech=lineit(" ")
                file=open(file_path, "a")
                file.write(f"{line}")
                file.close()
                self.fp.drukuj(f"minuta:{minuta}")
                obecna_minuta=datetime.now().minute
                if minuta != obecna_minuta:
                    self.fp.drukuj("kopiuje plik")
                    minuta = obecna_minuta
                    shutil.copyfile(file_path, file_path+".old")
                    os.remove(file_path)
                #print(line, end="")
                
                #print(line,end="")
                #print(line,end="")
                #print(line, end='') #process line here
    
        if p.returncode != 0:
            raise subprocess.CalledProcessError(p.returncode, p.args)
    
        #process = subprocess.Popen(command,
        #                    stdout=subprocess.PIPE,
        #                    stderr=subprocess.PIPE,
        #                    #shell=True,
        #                    #preexec_fn=os.setsid
        #                    )
        #stdout, stderr = process.communicate()
        #print(f"stdout: {stdout}")
        #file.write(str(stdout))
        #print(f"stderr: {stderr}")
        #os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        #przerwij_i_wyswietl_czas()
        #if len(stdout) > 10:
        #    drukuj("kopiuje stary plik pomiarowy by zrobić miejsce dla nowego")
        #    if os.path.exists(file_pomiar):
        #        shutil.copyfile(file_pomiar, file_pomiar+".old")
        #    file=open(file_pomiar, "w")
        #    file.write(str(stdout.decode()))
        #    file.close()
        #else:
        #    drukuj("nie kopiuje - brak nowych pomiarów")
        #    if os.name == "posix":
        #        brak_danych=open(f"{basic_path_ram}/brak_danych.txt", "a")
        #        brak_danych.write(data_i_godzina())
        #        errory=open(f"{basic_path_ram}/problemy_rtl_433.log","w")
        #        errory.write(stderr.decode())
        #    else:
        #        drukuj("nie posix - nie linuks klient - wez to obsluz")

def main():
    fp=FunkcjePomocnicze(nazwa_programu())
    basic_path_ram=""
    flara_skryptu=""
    try:
        fp.drukuj(f"------{nazwa_programu()}--------")
        if os.name=="posix":
            dotenv_path="./.env"
            fp.file_istnienie(dotenv_path, "sprawdz czy plik .env istnieje")
            load_dotenv(dotenv_path)
            basic_path_ram=fp.zmienna_env_folder("basic_path_ram", ".env - sprawdz basic_path_ram")
            
            flara_skryptu=f"{basic_path_ram}/{nazwa_programu()}.flara"
            flara_file=open(flara_skryptu,"w")
            print(f"os.getpid(): {os.getpid()}")
            flara_file.write(f"{os.getpid()}")
            flara_file.close()
            pomiarRTL433=PomiarRTL433()
            pomiarRTL433.start(basic_path_ram)
        else:
            fp.drukuj("oprogramuj tego windowsa w koncu")
            raise fp.exceptionWindows
        fp.usun_flare(basic_path_ram, flara_skryptu)
    except subprocess.CalledProcessError as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"jakies przerwanie w dzialanie")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, flara_skryptu)
    except ExceptionEnvProjektu as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"sprawdz czy dobrze wpisales dane w .env (albo czy w ogole je wpisales ...)")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, flara_skryptu)
    except ExceptionWindows as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"Brak wersji oprogramowania na windowsa - wymaga analizy i/lub dopisania kodu")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, flara_skryptu)
    except Exception as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"zwskazowka do czytającego - sprawdz czy .env widziany jest w crontabie")
        #os.remove(fal)
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, flara_skryptu)

if __name__ == "__main__":
    main()
