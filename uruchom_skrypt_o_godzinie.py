# - *- coding: utf-8 - *-

import os
import sys
import traceback
from datetime import datetime
import petla_programu
import time
import psutil
from dotenv import load_dotenv
from funkcje_pomocnicze import FunkcjePomocnicze, ExceptionEnvProjektu, ExceptionNotExistFolder, ExceptionWindows
import psutil
import signal

#########################

def nazwa_programu():
    return "uruchom_skrypt_o_godzinie.py"

def funkcje_pomocnicze_inicjalizacja():
    fp=FunkcjePomocnicze(nazwa_programu())
    return fp

##########################

class UruchamiaczSkryptu():
    
    def __init__(self):
        self.fp=funkcje_pomocnicze_inicjalizacja()
    
    def start(self, flara_path):
        flara_file=open(flara_path, "w")
        flara_file.write(f"{str(os.getpid())}")
        flara_file.close()
        self.fp.drukuj(self.fp.data_i_godzina())
        while True:
            now = datetime.now()
            current_seconds = int(now.strftime("%S"))
            self.fp.drukuj(current_seconds)
            if current_seconds == 0:
                break
            time.sleep(1)
        petla_programu.main()

def main():
    fp=FunkcjePomocnicze(nazwa_programu())
    basic_path_ram=""
    flara_skryptu=""
    try:
        fp.drukuj(f"------{nazwa_programu()}--------")
        if os.name == "posix":
            fp.drukuj("posix")
            dotenv_path = "../env_programu"
            if os.path.exists(dotenv_path):
                load_dotenv(dotenv_path)
            else:
                fp.drukuj("nie udalo sie zaladowac env_programu - wez ogarnij go dobra?!")
                raise ExceptionEnvProjektu
            basic_path_ram=os.getenv("basic_path_ram")
            if os.path.exists(basic_path_ram):
                fp.drukuj(f"pid tego programu {os.getpid()}")
                path_preflara=f"{basic_path_ram}/utrzymanie_wersji.py.preflara"
                fp.drukuj("przed")
                us=UruchamiaczSkryptu()
                if os.path.exists(path_preflara) == True:
                    flara_skryptu=(f"{basic_path_ram}/{nazwa_programu()}.flara")
                    fp.drukuj("sprawdzam czy istnieje flara tego programu")

                    print(os.listdir(f"{basic_path_ram}"))
                    if os.path.exists(flara_skryptu) == False:
                        fp.drukuj("nie ma pliku - rozpoczynamy dzialanie")
                        us.start(flara_skryptu)
                    else:
                        fp.drukuj("flara skryptu istnieje")
                        with open(flara_skryptu, "r") as file:
                            linie=file.readline()
                        pid=int(linie)
                        #dziala_flaga=sprawdz_program_o_tym_pid_dziala(pid)
                        fp.drukuj(f"{pid}")
                        processIsAlive=fp.sprawdz_czy_program_o_tym_pid_dziala(pid)
                        if processIsAlive == True:
                            fp.drukuj("skrypt istnieje i wydaje sie ze powinien dzialać - nic nie robie")
                            #TYMCZASOWO

                            ##obecny_czas=time.mktime(datetime.now().timetuple())
                            ##if os.path.exists(f"{basic_path_ram}/pomiary.txt"):
                            ##    czas_pliku_pomiary_txt=os.path.getmtime(f"{basic_path_ram}/pomiary.txt")
                            ##    fp.drukuj(czas_pliku_pomiary_txt)
                            ##    if czas_pliku_pomiary_txt > obecny_czas - 120:
                            ##        os.kill(pid, signal.SIGTERM)
                            ##        os.remove(flara_skryptu)
                            ##        fp.drukuj("mała liczba pomiarow - skilowalem i uruchamiam raz jeszcze")
                            ##        us.start(flara_skryptu)
                            ##else:
                            ##    fp.drukuj("na razie wydaje sie ze dziala - odmeldowuje się")
                        else:
                            fp.drukuj("skrypt ktorego flare znalazl juz umarl - usuwam flare i będę startował")
                            #jak widać byla flara ale jej proces juz umarl
                            os.remove(flara_skryptu)
                            fp.drukuj("usuwam plik flary i startujemy na nowo program")
                            us.start(flara_skryptu)
                else:
                    fp.drukuj(f"czekam na flare skryptu {path_preflara}")
            else:
                fp.drukuj("nie ma basic_path_ram - albo nie zostal stworzony folder TermoHigroLightlog")
                raise ExceptionEnvProjektu
        else:
            fp.drukuj("obsluz tego windowsa ziom")
            raise ExceptionWindows
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
    fp.drukuj("koniec programu")

if __name__ == '__main__':
    main()
