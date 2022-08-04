# - *- coding: utf-8 - *-

import os
import sys
import traceback
from datetime import datetime
import time
import signal
from dotenv import load_dotenv
import reset_portu_usb

def nazwa_programu():
    return "ubijaj_procesy.py"

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

def start(file_path, nazwa_flary, czas_dzialania):
    basic_path_ram=os.getenv("basic_path_ram")
    if os.path.exists(file_path):
        file=open(file_path, "r")
        numer_pid=file.read()
        file.close()
        czas_pliku=os.path.getmtime(file_path)
        obecny_czas=time.mktime(datetime.now().timetuple())
        drukuj(f"czas_pliku: {czas_pliku}")
        drukuj(f"obecny_czas: {obecny_czas}")
        drukuj(f"obecny_czas+{czas_dzialania}: {obecny_czas+czas_dzialania}")
        if nazwa_flary == "pomiar_rtl_433.py.flara":
            if os.path.exists(f"{basic_path_ram}/problemy_rtl_433.log"):
                drukuj("reset portu")
                reset_portu_usb.main()
                os.remove(f"{basic_path_ram}/problemy_rtl_433.log")
                #return False
                with open(f"{basic_path_ram}/ubijaj_procesy.py.log", "w") as f:
                    f.write("\n")
        if obecny_czas > czas_dzialania + czas_pliku:
            if True:#numer_pid != "" and numer_pid is not None:
                if os.name == "posix":
                    drukuj("przed killowaniem")
                    os.kill(int(numer_pid), signal.SIGTERM)
                    #os.kill(int(numer_pid), signal.SIGKILL)
                    #os.remove(file_path)
                    drukuj("po killowaniu")
                    #
                    #return 
                    with open(f"{basic_path_ram}/ubijaj_procesy.py.ubite", "w") as f:
                        f.write("\n")
                else:
                    pass
            else:
                drukuj("cos nie tak z pidem zapisanym w pliku - usuwam flare")
                os.remove(file_path)
        else:
            pass

def flary_do_sprawdzenia():
    try:
        lista = [
                ["pomiar_rtl_433.py.flara", 80],
                ["wysylanie_pomiarow_do_outsystem.py.flara", 480],
                ["zaciaganie_plikow_z_outsystemu.py.flara", 480],
                ["sortowanie_i_usrednianie_pomiarow.py.flara", 480]
                ]
        if os.name == "posix":
            basic_path_ram=""
            file_path=""
            drukuj("posix")
            dotenv_path="./.env"
            file_istnienie(dotenv_path, "dotenv_path - coś nie tak")
            load_dotenv(dotenv_path)
            basic_path_ram=zmienna_env_folder("basic_path_ram", "sprawdz basic_path_ram")
            
            for element_listy in lista:
                file_path=f"{basic_path_ram}/{element_listy[0]}"
                czas_dzialania=element_listy[1]
                if os.path.exists(file_path):
                    start(
                        file_path=file_path, 
                        nazwa_flary=element_listy[0], 
                        czas_dzialania=czas_dzialania
                        )
                else:
                    drukuj("nie ma plikow z pid")
        else:
            drukuj("obsluz windowsa w koncu")
    except ExceptionEnvProjektu as e:
        drukuj(f"exception {e}")
        drukuj(f"czy napewno skopiowales .env.example i podmieniles tam scieszki na takie jakie maja byc w programie?")
        traceback.print_exc()
    except Exception as e:
        drukuj(f"{e}")
        traceback.print_exc()

def main():
    drukuj("--------------------")
    drukuj(nazwa_programu())
    flary_do_sprawdzenia()
    
if __name__ == "__main__":
    main()
