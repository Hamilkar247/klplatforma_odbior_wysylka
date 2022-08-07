# - *- coding: utf-8 - *-

import os
import sys
import traceback
from datetime import datetime
import petla_programu
import time
import psutil
from dotenv import load_dotenv

def nazwa_programu():
    return "uruchom_skrypt_o_godzinie.py"

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

class ExceptionWindows(Exception):
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

def usun_flare(folder_do_sprawdzenia, flara_do_sprawdzenia):
    if os.path.isdir(folder_do_sprawdzenia):
        if os.path.exists(flara_do_sprawdzenia):
            os.remove(flara_do_sprawdzenia)
            drukuj("usuwam flare")

####################################

def sprawdz_program_o_tym_pid_dziala(pid):
    import psutil
    pid = 0
    if psutil.pid_exists(pid):
        print("a process with pid %d exists" % pid)
        return
    else:
        print("a process with pid %d does not exist" % pid)
    try:
        drukuj("sprawdz_program_o_tym_numerze_pid")
        os.kill(pid, 0) # 0 doesn't send any signal, but does error checks
    except OSError:
        drukuj("False")
        return False #print("Proc exited")
    else:
        drukuj("True")
        return True  #print("Proc is still running")

def start(flara_path):
    flara_file=open(flara_path, "w")
    flara_file.write(f"{str(os.getpid())}")
    flara_file.close()
    drukuj(data_i_godzina())
    while True:
        now = datetime.now()
        current_seconds = int(now.strftime("%S"))
        drukuj(current_seconds)
        if current_seconds == 0:
            break
        time.sleep(1)
    petla_programu.main()

def main():
    basic_path_ram=""
    flara_skryptu=""
    try:
        drukuj(f"------{nazwa_programu()}--------")
        if os.name == "posix":
            drukuj("posix")
            dotenv_path = "./.env"
            file_istnienie(dotenv_path, "dotenv_path - coś nie tak")
            load_dotenv(dotenv_path)
            basic_path_ram=zmienna_env_folder("basic_path_ram","basic_path_ram - coś nie tak")
            drukuj(f"{os.getpid()}")
            path_preflara=f"{basic_path_ram}/uruchom_skrypty_klraspi.preflara"
            if os.path.exists(path_preflara) == True:
                flara_skryptu=(f"{basic_path_ram}/{nazwa_programu()}.flara")
                if os.path.isfile(flara_skryptu) == False:
                    start(flara_skryptu)
                else:
                    drukuj("flara skryptu istnieje")
                    with open(flara_skryptu, "r") as file:
                        linie=file.readline()
                    pid=int(linie)
                    #dziala_flaga=sprawdz_program_o_tym_pid_dziala(pid)
                    print(pid)
                    if psutil.pid_exists(pid) == True:
                        drukuj("skrypt istnieje i działa - więc nie uruchamiam")
                    else:
                        #jak widać byla flara ale jej proces juz umarl
                        os.remove(flara_skryptu)
                        drukuj("usuwam plik flary i startujemy na nowo program")
                        start(flara_skryptu)
            else: 
                drukuj("czekam na skrypt update_projektu_skryptu_klraspi/utrzymanie_wersji.py")
        else:
            drukuj("obsluz tego windowsa ziom")
            raise ExceptionWindows
    except ExceptionEnvProjektu as e:
        drukuj(f"exception {e}")
        drukuj(f"czy napewno skopiowales .env.example i podmieniles tam scieszki na takie jakie maja byc w programie?")
        traceback.print_exc()
        usun_flare(basic_path_ram, flara_skryptu)
    except ExceptionWindows as e:
        drukuj(f"exception {e}")
        drukuj(f"Brak wersji oprogramowania na windowsa - wymaga analizy i/lub dopisania kodu")
        traceback.print_exc()
        usun_flare(basic_path_ram, flara_skryptu)
    except Exception as e:
        drukuj(f"exception {e}")
        drukuj(f"sprawdz czy .env widziany jest w crontabie")
        traceback.print_exc()
        usun_flare(basic_path_ram, flara_skryptu)

if __name__ == '__main__':
    main()
