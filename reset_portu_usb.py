# - *- coding: utf-8 - *-
import sys
import os
from datetime import datetime

import traceback
from usb.core import find as finddev
from dotenv import load_dotenv

def nazwa_programu():
    return "reset_portu_usb.py"

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

###############

def start():
    basic_path_ram=os.getenv("basic_path_ram")
    vendor_id=0x0bda
    product_id=0x2838
    try:
        dev = finddev(idVendor=vendor_id, idProduct=product_id)
        print(f"dev: {dev}")
        dev.reset()
        print("dokonano resetu na podanym porcie")
        with open(f"{basic_path_ram}/reset_portu_usb.py.log", "w") as f:
            f.write("\n")
        error_file=f"{basic_path_ram}/reset_portu_usb.py.error"
        if os.path.exists(error_file):
            os.remove(error_file)
    except Exception as e:
        print(f"mozliwy brak odczytu rtl-sdr na portach usb - sprawdz lsusb czy sa takie numery fabryczne {vendor_id} {product_id}")
        print(f"Exception {e}")
        traceback.print_exc()
        with open(f"{basic_path_ram}/reset_portu_usb.py.log", "a") as f:
            f.write(f"{data_i_godzina()}")
            f.write("\n")
        with open(f"{basic_path_ram}/reset_portu_usb.py.error", "a") as f:
            f.write(f"{data_i_godzina()}")
            f.write("\n")

def main():
    basic_path_ram=""
    flara_skryptu=f"{nazwa_programu()}.flara"
    try:
        drukuj(f"------------{nazwa_programu()}-------------")
        if os.name=="posix":
            dotenv_path = "./.env"
            file_istnienie(dotenv_path, "sprawdz czy plik .env istnieje")
            load_dotenv(dotenv_path)
            basic_path_ram=zmienna_env_folder("basic_path_ram", ".env - sprawdz basic_path_ram")
            
            flara_skryptu=f"{basic_path_ram}/{nazwa_programu()}.flara"
            with open(flara_skryptu, "w") as f:
                f.write("\n")
            start()
        else:
            drukuj("oprogramuj tego windowsa")
        usun_flare(basic_path_ram, flara_skryptu)
    except ExceptionEnvProjektu as e:
        drukuj(f"exception {e}")
        drukuj(f"sprawdz czy dobrze wpisales dane w .env (albo czy w ogole je wpisales ...)")
        traceback.print_exc()
        usun_flare(basic_path_ram, flara_skryptu)
    except Exception as e:
        drukuj(f"exception {e}")
        drukuj(f"sprawdz czy .env widziany jest w crontabie")
        traceback.print_exc()
        usun_flare(basic_path_ram, flara_skryptu)

if __name__ == "__main__":
    main()