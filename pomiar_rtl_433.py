# - *- coding: utf-8 - *-

import os
import sys
import traceback
from datetime import datetime
import time
import subprocess
import shutil
from dotenv import load_dotenv

def nazwa_programu():
    return "pomiar_rtl_433.py"

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

def start(basic_path_ram):
    drukuj(" - - - - - - -")
    drukuj(nazwa_programu())
    file_pomiar=f"{basic_path_ram}/pomiary.txt"

    command=f"timeout 55 rtl_433 -s 2.5e6 -f 868.5e6 -H 30 -R 75 -R 150 -F json".split(" ")
    process = subprocess.Popen(command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        #shell=True,
                        #preexec_fn=os.setsid
                        )
    stdout, stderr = process.communicate()
    print(f"stdout: {stdout}")
    #file.write(str(stdout))
    print(f"stderr: {stderr}")
    #os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    #przerwij_i_wyswietl_czas()
    if len(stdout) > 10:
        drukuj("kopiuje stary plik pomiarowy by zrobić miejsce dla nowego")
        if os.path.exists(file_pomiar):
            shutil.copyfile(file_pomiar, file_pomiar+".old")
        file=open(file_pomiar, "w")
        file.write(str(stdout.decode()))
        file.close()
    else:
        drukuj("nie kopiuje - brak nowych pomiarów")
        if os.name == "posix":
            brak_danych=open(f"{basic_path_ram}/brak_danych.txt", "a")
            brak_danych.write(data_i_godzina())
            errory=open(f"{basic_path_ram}/problemy_rtl_433.log","w")
            errory.write(stderr.decode())
        else:
            drukuj("nie posix - nie linuks klient - wez to obsluz")

def main():
    basic_path_ram=""
    flara_skryptu=""
    try:
        drukuj(f"------{nazwa_programu()}--------")
        dotenv_path="./.env"
        load_dotenv(dotenv_path)
        if os.name=="posix":
            drukuj("posix")
            basic_path_ram=os.getenv('basic_path_ram')
            drukuj(f"basic_path_ram: {basic_path_ram}")
        else:
            drukuj("notposix - pewnie windows - wez to czlowieku oprogramuj")
            przerwij_i_wyswietl_czas()
        flara_skryptu=f"{basic_path_ram}/{nazwa_programu()}.flara"
        flara_file=open(flara_skryptu,"w")
        print(f"os.getpid(): {os.getpid()}")
        flara_file.write(f"{os.getpid()}")
        flara_file.close()
        start(basic_path_ram)
        if os.path.exists(flara_skryptu):
            os.remove(flara_skryptu)
    except Exception as e:
        drukuj(f"exception {e}")
        drukuj(f"zwskazowka do czytającego - sprawdz czy .env widziany jest w crontabie")
        #os.remove(fal)
        traceback.print_exc()
        if os.path.exists(basic_path_ram):
            os.remove(flara_skryptu)
            drukuj("usuwam flare")

if __name__ == "__main__":
    main()
