# - *- coding: utf-8 - *-

import os
import sys
import traceback
from datetime import datetime
import time
import signal
from dotenv import load_dotenv
import reset_portu_usb
from funkcje_pomocnicze import FunkcjePomocnicze, ExceptionEnvProjektu, ExceptionNotExistFolder, ExceptionWindows

#################################

def nazwa_programu():
    return "ubijaj_procesy.py"

def funkcje_pomocnicze_inicjalizacja():
    fp=FunkcjePomocnicze(nazwa_programu())
    return fp

##################################

class UbijaczProcesow():

    def __init__(self):
        self.fp=funkcje_pomocnicze_inicjalizacja()

    def start(self, file_path, nazwa_flary, czas_dzialania):
        basic_path_ram=self.fp.zmienna_env_file("basic_path_ram", "cos nie tak z basic_path_ram")
        if os.path.exists(file_path):
            file=open(file_path, "r")
            numer_pid=file.read()
            file.close()
            czas_pliku=os.path.getmtime(file_path)
            obecny_czas=time.mktime(datetime.now().timetuple())
            self.fp.drukuj(f"czas_pliku: {czas_pliku}")
            self.fp.drukuj(f"obecny_czas: {obecny_czas}")
            self.fp.drukuj(f"obecny_czas+{czas_dzialania}: {obecny_czas+czas_dzialania}")
            if nazwa_flary == "pomiar_rtl_433.py.flara":
                czas_pliku_pomiary_txt=os.path.getmtime(f"{basic_path_ram}/pomiary.txt")
                if obecny_czas > czas_pliku_pomiary_txt+120:
                    self.fp.drukuj("plik pomiary.txt cos dlugo sie zasiedzial - podejrzenie zaciecia LIVEUSB ERROR")
                    reset_portu_usb.main()
                    os.remove(f"{basic_path_ram}/ubijaj_procesy.py.log")#"ubijaj_procesy.py.log")
                    with open(f"{basic_path_ram}/ubijaj_procesy.py.log", "w") as f:
                        f.write("\n")
#                if os.path.exists(f"{basic_path_ram}/problemy_rtl_433.log"):
#                    self.fp.drukuj("reset portu")
#                    reset_portu_usb.main()
#                    os.remove(f"{basic_path_ram}/problemy_rtl_433.log")
#                    #return False
#                    with open(f"{basic_path_ram}/ubijaj_procesy.py.log", "w") as f:
#                        f.write("\n")
            if obecny_czas > czas_dzialania + czas_pliku:
                if True:#numer_pid != "" and numer_pid is not None:
                    if os.name == "posix":
                        self.fp.drukuj("przed killowaniem")
                        os.kill(int(numer_pid), signal.SIGTERM)
                        #os.kill(int(numer_pid), signal.SIGKILL)
                        #os.remove(file_path)
                        self.fp.drukuj("po killowaniu")
                        #
                        #return 
                        with open(f"{basic_path_ram}/ubijaj_procesy.py.ubite.log", "w") as f:
                            f.write("\n")
                    else:
                        pass
                else:
                    drukuj("cos nie tak z pidem zapisanym w pliku - usuwam flare")
                    os.remove(file_path)
            else:
                pass
    
    def flary_do_sprawdzenia(self):
        basic_path_ram=""
        file_path=""
        try:
            lista = [
                    ["pomiar_rtl_433.py.flara", 400],
                    ["wysylanie_pomiarow_do_outsystem.py.flara", 480],
                    ["zaciaganie_plikow_z_outsystemu.py.flara", 480],
                    ["sortowanie_i_usrednianie_pomiarow.py.flara", 480]
                    ]
            if os.name == "posix":
                self.fp.drukuj("posix")
                dotenv_path="../env_programu"
                self.fp.file_istnienie(dotenv_path, "dotenv_path - coś nie tak")
                load_dotenv(dotenv_path)
                basic_path_ram=self.fp.zmienna_env_folder("basic_path_ram", "sprawdz basic_path_ram")
                
                for element_listy in lista:
                    file_path=f"{basic_path_ram}/{element_listy[0]}"
                    czas_dzialania=element_listy[1]
                    if os.path.exists(file_path):
                        self.start(
                            file_path=file_path, 
                            nazwa_flary=element_listy[0], 
                            czas_dzialania=czas_dzialania
                            )
                    else:
                        self.fp.drukuj("nie ma plikow z pid")
            else:
                raise ExceptionWindows
                self.fp.drukuj("obsluz windowsa w koncu")
        except ExceptionEnvProjektu as e:
            self.fp.drukuj(f"exception {e}")
            self.fp.drukuj(f"czy napewno skopiowales env_programu.example i podmieniles tam scieszki na takie jakie maja byc w programie?")
            traceback.print_exc()
        except ExceptionWindows as e:
            self.fp.drukuj(f"exception {e}")
            self.fp.drukuj(f"Brak wersji oprogramowania na windowsa - wymaga analizy i/lub dopisania kodu")
            traceback.print_exc()
        except Exception as e:
            self.fp.drukuj(f"{e}")
            traceback.print_exc()

def main():
    fp=FunkcjePomocnicze(nazwa_programu())
    fp.drukuj(f"------------{nazwa_programu()}-------")
    fp.drukuj("--------------------")
    fp.drukuj(nazwa_programu())
    ub=UbijaczProcesow()
    ub.flary_do_sprawdzenia()
    
if __name__ == "__main__":
    main()
