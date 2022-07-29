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

def sprawdz_program_o_tym_pid_dziala(pid):
    import psutil
    pid = 12345
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
    os.remove(flara_path)

def main():
    basic_path_ram=""
    flara_skryptu=""
    drukuj("kuzwa")
    try:
        drukuj(f"------{nazwa_programu()}--------")
        dotenv_path = "./.env"
        load_dotenv(dotenv_path)
        if os.name == "posix":
            drukuj(f"{os.getpid()}")
            begin_path_ram=os.getenv('basic_path_ram')
        flara_path=(f"{begin_path_ram}/{nazwa_programu()}.flara")
        if os.path.isfile(flara_path) == False:
            start(flara_path)
        else:
            drukuj("flara skryptu istnieje")
            with open(flara_path, "r") as file:
                linie=file.readline()
            pid=int(linie)
            #dziala_flaga=sprawdz_program_o_tym_pid_dziala(pid)
            print(pid)
            if psutil.pid_exists(pid) == True:
                drukuj("skrypt istnieje i działa - więc nie uruchamiam")
            else:
                os.remove(flara_path)
                drukuj("usuwam plik flary i startujemy na nowo program")
                start(flara_path)
    except Exception as e:
        drukuj(f"exception {e}")
        drukuj(f"sprawdz czy .env widziany jest w crontabie")
        #os.remove(fal)
        traceback.print_exc()
        if os.path.exists(basic_path_ram):
            os.remove(flara_skryptu)
            drukuj("usuwam flare")

if __name__ == '__main__':
    main()
