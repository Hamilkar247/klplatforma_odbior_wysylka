# - *- coding: utf-8 - *-

from inspect import trace
import urllib.request, json
import sys
import os
from datetime import datetime, timedelta
import traceback
from dotenv import load_dotenv
import psutil
from funkcje_pomocnicze import FunkcjePomocnicze, ExceptionEnvProjektu, ExceptionNotExistFolder, ExceptionWindows

#######################3

def nazwa_programu():
    return "zaciaganie_plikow_z_outsystemu.py"


def funkcje_pomocnicze_inicjalizacja():
    fp=FunkcjePomocnicze(nazwa_programu())
    return fp

####################

class PobranieOutsystem(object):
    def __init__(self):

        self.fp=funkcje_pomocnicze_inicjalizacja()

        self.fp.drukuj("class: PobranieOutsystem")
        #przyklad zawartosci /ram/user/1000
        self.basic_path_ram=os.getenv('basic_path_ram')
        #przykład zawartosci https://personal-5ndvfcym.outsystemscloud.com/KlimaLog_core/rest/V1/GetAlarms?Rpi_serial_number=
        self.url_do_pobrania_alarmow=os.getenv('url_do_pobrania_alarmow')
        #przykład zawartosci https://personal-5ndvfcym.outsystemscloud.com/KlimaLog_core/rest/V1/GetRpiConfig?Rpi_serial_number=
        self.url_do_pobrania_konfiguracji=os.getenv('url_do_pobrania_konfiguracji')
        #przykład zawartosci /home/klraspi/skrypty_klraspi
        self.basic_path_project=os.getenv('basic_path_project')
        #przykładowa zawartosc /home/klraspi/config_klplatforma/urzadzenia
        config_folder="config_klplatforma"
        head, tail = os.path.split(os.getcwd())
        self.fp.drukuj(f"config_folder:  {head}/{config_folder}")
        self.path_to_config=f"{head}/{config_folder}"

    #def numer_seryjny_raspberki(self):
    #    sn=[]
    #    with open("/sys/firmware/devicetree/base/serial-number", "r") as plik_numer_seryjny:
    #        sn=plik_numer_seryjny.readlines()
    #    #ucinam ostatni bit z czymś takim - \u0000
    #    #powinniśmy dostać coś w tym stylu
    #    return sn[0][0:-1]
    
    def get_mac_address(self):
        self.fp.drukuj("def: get_mac_address")
        #mac_address_int = uuid.getnode()
        #drukuj(mac_address_int)
        #mac_address_hex = hex(mac_address_int)
        #drukuj(mac_address_hex)
        #mac_address_hex_bez_zeroiks=str(mac_address_hex).split("x")[1]#f"{mac_address_hex[2,-1]}"
        #drukuj(f"MAC address:{mac_address_hex}")
        #return mac_address_hex_bez_zeroiks
        interfejs_return=""
        try:
            nics = psutil.net_if_addrs()[os.getenv('interfejs_sieciowy')]
            interfejs_return=""
            for interface in nics:
                if interface.family == 17:
                    self.fp.drukuj(interface.address)
                    interfejs_return=interface.address
        except KeyError as e:
            self.fp.drukuj(f"exception: {e}")
            raise self.exceptionEnvProjektu
        return interfejs_return


    def plik_z_alarmami(self):
        url=f"{self.url_do_pobrania_alarmow}{self.get_mac_address()}"
        content_new=None
        try:
            with urllib.request.urlopen(url) as url:
                content_new = json.dumps(json.loads(url.read()), indent=2) #json.loads(url.read())
        except Exception as e:
            self.fp.drukuj(f"EEEEEEEEEERRRRRROOOOOOOORRRR")
            self.fp.drukuj(f"{e}")
            self.fp.drukuj(f"sprawdz link: {url}")
            traceback.print_exc()

        urzadzenia_path = f"{self.path_to_config}/urzadzenia"
        if os.path.isdir(urzadzenia_path) == True:
            pass
        else:
            os.mkdir(urzadzenia_path)
        path_to_file=f"{urzadzenia_path}/{self.get_mac_address()}.json" #"mother_sn_"+get_mother_serial_number()+".json"
        if os.path.exists(path_to_file):
            self.fp.drukuj(os.stat(path_to_file).st_size)
            if os.stat(path_to_file).st_size > 30:
                old_file = open(path_to_file, "r")
                content_old = json.dumps(json.loads(old_file.read()), indent=2)
                old_file.close()

                #drukuj(content_new)
                #drukuj(content_old)
                if content_new != content_old:
                    file=open(path_to_file, "w")
                    file.write(str(content_new))
                    self.fp.drukuj("nasluchiwanie się powiodło - nadpisano plik z alarmami czujników")
                    #logi
                    logi_do_json_z_alarmami=open(f"{self.basic_path_project}/odebrane_jsony_z_alarmami.json", "a+")
                    logi_do_json_z_alarmami.write(f"{self.fp.data_i_godzina()}")
                    logi_do_json_z_alarmami.write("\n")
                    logi_do_json_z_alarmami.write(str(content_new))
                else:
                    self.fp.drukuj("brak nowego pliku z alarmami i intervalem") 
            else:
                self.fp.drukuj(f"plik jaki się znajdował - był prawdopodobnie pusty {path_to_file}")
                file=open(path_to_file, "w")
                file.write(str(content_new))
                self.fp.drukuj("nasluchiwanie się powiodło - nadpisano plik z alarmami czujników")
                #logi
                logi_do_json_z_alarmami=open(f"{self.basic_path_project}/odebrane_jsony_z_alarmami.json", "a+")
                logi_do_json_z_alarmami.write(f"{self.fp.data_i_godzina()}")
                logi_do_json_z_alarmami.write("\n")
                logi_do_json_z_alarmami.write(str(content_new))
        else:
            self.fp.drukuj("UWAGA")
            self.fp.drukuj(f"Nie było do tej pory pliku {path_to_file}")
            file=open(path_to_file, "w")
            file.write(str(content_new))
            self.fp.drukuj("nasluchiwanie się powiodło - stworzono nowy plik z alarmami czujników")

    def plik_z_konfiguracja_raspberki(self):
        url=f"{self.url_do_pobrania_konfiguracji}{self.get_mac_address()}"
        content_new=None
        try:
            with urllib.request.urlopen(url) as url:
                content_new = json.dumps(json.loads(url.read()), indent=2) #json.loads(url.read())
        except Exception as e:
            self.fp.drukuj(f"EEEEEEEEEERRRRRROOOOOOOORRRR")
            self.fp.drukuj(f"{e}")
            self.fp.drukuj(f"sprawdz link: {url}")
            traceback.print_exc()

        path_to_file=f"{self.path_to_config}/config.json"
        if os.path.exists(path_to_file):
            if os.stat(path_to_file).st_size > 30:
                old_file = open(path_to_file, "r")
                content_old = json.dumps(json.loads(old_file.read()), indent=2)
                old_file.close()

                #drukuj(content_new)
                #drukuj(content_old)
                if content_new != content_old:
                    file=open(path_to_file, "w")
                    file.write(str(content_new))
                    self.fp.drukuj("nasluchiwanie się powiodło - skopiowano nowy plik z konfiguracją")
                    #logi
                    logi_do_json_z_konfiguracjami=open(f"{self.basic_path_project}/odebrane_jsony_z_konfiguracjami.json", "a+")
                    logi_do_json_z_konfiguracjami.write("\n")
                    logi_do_json_z_konfiguracjami.write(str(content_new))
                    logi_do_json_z_konfiguracjami.close()
                else:
                    self.fp.drukuj("brak nowego pliku konfiguracyjnego") 
            else:
                self.fp.drukuj(f"Plik {path_to_file} byl prawdopodobnie pusty")
                file=open(path_to_file, "w")
                file.write(str(content_new))
                self.fp.drukuj("nasluchiwanie się powiodło - stworzono nowy plik z konfiguracja")
                #logi
                logi_do_json_z_konfiguracjami=open(f"{self.basic_path_project}/odebrane_jsony_z_konfiguracjami.json", "a+")
                logi_do_json_z_konfiguracjami.write("\n")
                logi_do_json_z_konfiguracjami.write(str(content_new))
                logi_do_json_z_konfiguracjami.close()
        else:
            self.fp.drukuj("UWAGA")
            self.fp.drukuj(f"plik {path_to_file} nie istniał, tudzież był pusty")
            file=open(path_to_file, "w")
            file.write(str(content_new))
            self.fp.drukuj("nasluchiwanie się powiodło - stworzono nowy plik z konfiguracja")

def pobieranie_plikow_z_serwera():
    pobieramy=PobranieOutsystem()
    pobieramy.plik_z_alarmami()
    pobieramy.plik_z_konfiguracja_raspberki()

def main():
    fp=FunkcjePomocnicze(nazwa_programu())
    basic_path_ram=""
    flara_skryptu=""
    try:
        fp.drukuj(f"--------{nazwa_programu()}-------------")
        if os.name=="posix":
            fp.drukuj("posix")
            dotenv_path = "./.env"
            fp.file_istnienie(dotenv_path, "dotenv_path - coś nie tak")
            load_dotenv(dotenv_path)
            basic_path_ram=fp.zmienna_env_folder('basic_path_ram', ".env - sprawdz basic_path_ram")

            flara_skryptu=f"{basic_path_ram}/{nazwa_programu()}.flara"
            with open(flara_skryptu, "w") as file:
                file.write(f"{str(os.getpid())}")
            file.close()
            pobieranie_plikow_z_serwera()
        else:
            raise ExceptionWindows
        fp.usun_flare(basic_path_ram, flara_skryptu)
    except ExceptionEnvProjektu as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"sprawdz czy dobrze wpisales dane w .env (albo czy w ogole je wpisales ...)")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, flara_skryptu)
    except ExceptionWindows as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"nie oprogramowales czegos na windowsa - uzupelnij")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, flara_skryptu)
    except Exception as e:
        fp.drukuj(f"exception {e}")
        fp.drukuj(f"sprawdz czy .env widziany jest w crontabie")
        traceback.print_exc()
        fp.usun_flare(basic_path_ram, flara_skryptu)

if __name__ == "__main__":
    main()
