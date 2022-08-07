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

def usun_flare(folder_do_sprawdzenia, flara_do_sprawdzenia):
    if os.path.isdir(folder_do_sprawdzenia):
        if os.path.exists(flara_do_sprawdzenia):
            os.remove(flara_do_sprawdzenia)
            drukuj("usuwam flare")

############################


def start(basic_path_ram):
    drukuj(" - - - - - - -")
    drukuj(nazwa_programu())
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
            drukuj(f"minuta:{minuta}")
            obecna_minuta=datetime.now().minute
            if minuta != obecna_minuta:
                drukuj("kopiuje plik")
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
    basic_path_ram=""
    flara_skryptu=""
    try:
        drukuj(f"------{nazwa_programu()}--------")
        if os.name=="posix":
            dotenv_path="./.env"
            file_istnienie(dotenv_path, "sprawdz czy plik .env istnieje")
            load_dotenv(dotenv_path)
            basic_path_ram=zmienna_env_folder("basic_path_ram", ".env - sprawdz basic_path_ram")
            
            flara_skryptu=f"{basic_path_ram}/{nazwa_programu()}.flara"
            flara_file=open(flara_skryptu,"w")
            print(f"os.getpid(): {os.getpid()}")
            flara_file.write(f"{os.getpid()}")
            flara_file.close()
            start(basic_path_ram)
        else:
            drukuj("oprogramuj tego windowsa w koncu")
        usun_flare(basic_path_ram, flara_skryptu)
    except subprocess.CalledProcessError as e:
        drukuj(f"exception {e}")
        drukuj(f"jakies przerwanie w dzialanie")
    except ExceptionEnvProjektu as e:
        drukuj(f"exception {e}")
        drukuj(f"sprawdz czy dobrze wpisales dane w .env (albo czy w ogole je wpisales ...)")
        traceback.print_exc()
        usun_flare(basic_path_ram, flara_skryptu)
    except Exception as e:
        drukuj(f"exception {e}")
        drukuj(f"zwskazowka do czytającego - sprawdz czy .env widziany jest w crontabie")
        #os.remove(fal)
        traceback.print_exc()
        usun_flare(basic_path_ram, flara_skryptu)

if __name__ == "__main__":
    main()
