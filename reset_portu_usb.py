# - *- coding: utf-8 - *-
import sys
import os
from datetime import datetime

import traceback
from usb.core import find as finddev
from dotenv import load_dotenv
from funkcje_pomocnicze import FunkcjePomocnicze, ExceptionEnvProjektu, ExceptionNotExistFolder, ExceptionWindows

############################

def nazwa_programu():
    return "reset_portu_usb.py"

def funkcje_pomocnicze_inicjalizacja():
    fp=FunkcjePomocnicze(nazwa_programu())
    return fp

############################

class ResetPortuUsb():

    def __init__(self):
        self.fp=funkcje_pomocnicze_inicjalizacja()

    def start(self):
        basic_path_ram=os.getenv("basic_path_ram")
        vendor_id=0x0bda
        product_id=0x2838
        flaga_wykonania=False
        try:
            dev = finddev(idVendor=vendor_id, idProduct=product_id)
            self.fp.drukuj(f"dev: {dev}")
            dev.reset()
            self.fp.drukuj("dokonano resetu na podanym porcie")
            with open(f"{basic_path_ram}/reset_portu_usb.py.log", "w") as f:
                f.write("\n")
            error_file=f"{basic_path_ram}/reset_portu_usb.py.error"
            if os.path.exists(error_file):
                os.remove(error_file)
            flaga_wykonania=True
        except Exception as e:
            flaga_wykonania=False
            self.fp.drukuj(f"mozliwy brak odczytu rtl-sdr na portach usb - sprawdz lsusb czy sa takie numery fabryczne {vendor_id} {product_id}")
            self.fp.drukuj(f"Exception {e}")
            traceback.print_exc()
            with open(f"{basic_path_ram}/reset_portu_usb.py.error", "a") as f:
                f.write(f"{self.fp.data_i_godzina()}")
                f.write("\n")

        with open(f"{basic_path_ram}/reset_portu_usb.py.log", "a") as f:
            f.write(f"{self.fp.data_i_godzina()}\n")
            f.write(f"flaga_dokonania_resetu: {flaga_wykonania}\n")o
def main():
    fp=FunkcjePomocnicze(nazwa_programu())
    basic_path_ram=""
    flara_skryptu=f"{nazwa_programu()}.flara"
    try:
        fp.drukuj(f"------------{nazwa_programu()}-------------")
        if os.name=="posix":
            dotenv_path = "../env_programu"
            fp.file_istnienie(dotenv_path, "sprawdz czy plik env_programu istnieje")
            load_dotenv(dotenv_path)
            basic_path_ram=fp.zmienna_env_folder("basic_path_ram", "env_programu - sprawdz basic_path_ram")
            
            flara_skryptu=f"{basic_path_ram}/{nazwa_programu()}.flara"
            with open(flara_skryptu, "w") as f:
                f.write("\n")
            rpu=ResetPortuUsb()
            rpu.start()
        else:
            drukuj("oprogramuj tego windowsa")
            raise ExceptionWindows
        fp.usun_flare(basic_path_ram, flara_skryptu)
    except ExceptionEnvProjektu as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"sprawdz czy dobrze wpisales dane w env_programu (albo czy w ogole je wpisales ...)")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, flara_skryptu)
    except ExceptionWindows as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"nie oprogramowales czegos na windowsa - uzupelnij")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, flara_skryptu)
    except Exception as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"sprawdz czy env_programu widziany jest w crontabie")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, flara_skryptu)

if __name__ == "__main__":
    main()