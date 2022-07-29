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
    flara_skryptu=f"{nazwa_programu()}.flara"
    try:
        drukuj(f"------------{nazwa_programu()}-------------")
        dotenv_path = "./.env"
        load_dotenv(dotenv_path)
        basic_path_ram=os.getenv("basic_path_ram")
        flara_skryptu=f"{basic_path_ram}/{nazwa_programu()}.flara"
        with open(flara_skryptu, "w") as f:
            f.write("\n")
        start()
        if os.path.exists(flara_skryptu):
            os.remove(flara_skryptu)
    except Exception as e:
        drukuj(f"{e}")
        traceback.print_exc()
        if os.path.exists(flara_skryptu):
            os.remove(flara_skryptu)

if __name__ == "__main__":
    main()