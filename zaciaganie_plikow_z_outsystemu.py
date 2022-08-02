# - *- coding: utf-8 - *-

from inspect import trace
import urllib.request, json
import hashlib
import sys
import shutil
import os
import datetime
import traceback
from dotenv import load_dotenv
import uuid
import psutil

def nazwa_programu():
    return "zaciaganie_plikow_z_outsystemu.py"

def data_i_godzina():
    now = datetime.datetime.now()
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

def numer_seryjny_raspberki():
    sn=[]
    with open("/sys/firmware/devicetree/base/serial-number", "r") as plik_numer_seryjny:
        sn=plik_numer_seryjny.readlines()
    #ucinam ostatni bit z czymś takim - \u0000
    #powinniśmy dostać coś w tym stylu
    return sn[0][0:-1]

def get_mac_address():
    #mac_address_int = uuid.getnode()
    #drukuj(mac_address_int)
    #mac_address_hex = hex(mac_address_int)
    #drukuj(mac_address_hex)
    #mac_address_hex_bez_zeroiks=str(mac_address_hex).split("x")[1]#f"{mac_address_hex[2,-1]}"
    #drukuj(f"MAC address:{mac_address_hex}")
    #return mac_address_hex_bez_zeroiks
    nics = psutil.net_if_addrs()[os.getenv('interfejs_sieciowy')]
    for interface in nics:
        if interface.family == 17:
            print(interface.address)
    return interface.address

# def get_mother_serial_number():
#     try:
#         path_to_file='/home/klraspi/klraspi/pliki_od_weewxa/urzadzenie_dane.json'
#         data = []
#         if os.path.exists(path_to_file): 
#             with open(path_to_file,"r") as f: 
#                 data = json.load(f)
#         drukuj(data['serial_number'])
#         return str(data['serial_number'])
#     except Exception as e:
#         drukuj(e)
#         drukuj(traceback.print_exc())
#         return "NONE"


class PobranieOutsystem(object):
    def __init__(self):
        pass
        drukuj("class: PobranieOutsystem")
        #przyklad zawartosci /ram/user/1000
        self.basic_path_ram=os.getenv('basic_path_ram')
        #przykład zawartosci https://personal-5ndvfcym.outsystemscloud.com/KlimaLog_core/rest/V1/GetAlarms?Rpi_serial_number=
        self.url_do_pobrania_alarmow=os.getenv('url_do_pobrania_alarmow')
        #przykład zawartosci https://personal-5ndvfcym.outsystemscloud.com/KlimaLog_core/rest/V1/GetRpiConfig?Rpi_serial_number=
        self.url_do_pobrania_konfiguracji=os.getenv('url_do_pobrania_konfiguracji')
        #przykład zawartosci /home/klraspi/skrypty_klraspi
        self.basic_path_project=os.getenv('basic_path_project')
        #przykładowa zawartosc /home/klraspi/config/urzadzenia
        self.path_to_config=os.getenv('path_to_config')

    def plik_z_alarmami(self):
        url=f"{self.url_do_pobrania_alarmow}{get_mac_address()}"
        content_new=None
        try:
            with urllib.request.urlopen(url) as url:
                content_new = json.dumps(json.loads(url.read()), indent=2) #json.loads(url.read())
        except Exception as e:
            drukuj(f"EEEEEEEEEERRRRRROOOOOOOORRRR")
            drukuj(f"{e}")
            drukuj(f"sprawdz link: {url}")
            traceback.print_exc()

        urzadzenia_path = f"{self.path_to_config}/urzadzenia"
        if os.path.isdir(urzadzenia_path) == True:
            pass
        else:
            os.mkdir(urzadzenia_path)
        path_to_file=f"{urzadzenia_path}/{get_mac_address()}.json" #"mother_sn_"+get_mother_serial_number()+".json"
        if os.path.exists(path_to_file):
            drukuj(os.stat(path_to_file).st_size)
            if os.stat(path_to_file).st_size > 30:
                old_file = open(path_to_file, "r")
                content_old = json.dumps(json.loads(old_file.read()), indent=2)
                old_file.close()

                #drukuj(content_new)
                #drukuj(content_old)
                if content_new != content_old:
                    file=open(path_to_file, "w")
                    file.write(str(content_new))
                    drukuj("nasluchiwanie się powiodło - nadpisano plik z alarmami czujników")
                    #logi
                    logi_do_json_z_alarmami=open(f"{self.basic_path_project}/odebrane_jsony_z_alarmami.json", "a")
                    logi_do_json_z_alarmami.write(f"{data_i_godzina()}")
                    logi_do_json_z_alarmami.write("\n")
                    logi_do_json_z_alarmami.write(str(content_new))
                else:
                    drukuj("brak nowego pliku z alarmami i intervalem") 
            else:
                drukuj(f"plik jaki się znajdował - był prawdopodobnie pusty {path_to_file}")
                file=open(path_to_file, "w")
                file.write(str(content_new))
                drukuj("nasluchiwanie się powiodło - nadpisano plik z alarmami czujników")
                #logi
                logi_do_json_z_alarmami=open(f"{self.basic_path_project}/odebrane_jsony_z_alarmami.json", "a")
                logi_do_json_z_alarmami.write(f"{data_i_godzina()}")
                logi_do_json_z_alarmami.write("\n")
                logi_do_json_z_alarmami.write(str(content_new))
        else:
            drukuj("UWAGA")
            drukuj(f"Nie było do tej pory pliku {path_to_file}")
            file=open(path_to_file, "w")
            file.write(str(content_new))
            drukuj("nasluchiwanie się powiodło - stworzono nowy plik z alarmami czujników")

    def plik_z_konfiguracja_raspberki(self):
        url=f"{self.url_do_pobrania_konfiguracji}{get_mac_address()}"
        content_new=None
        with urllib.request.urlopen(url) as url:
            content_new = json.dumps(json.loads(url.read()), indent=2) #json.loads(url.read())

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
                    drukuj("nasluchiwanie się powiodło - skopiowano nowy plik z konfiguracją")
                    #logi
                    logi_do_json_z_konfiguracjami=open(f"{self.basic_path_project}/odebrane_jsony_z_konfiguracjami.json", "a")
                    logi_do_json_z_konfiguracjami.write("\n")
                    logi_do_json_z_konfiguracjami.write(str(content_new))
                    logi_do_json_z_konfiguracjami.close()
                else:
                    drukuj("brak nowego pliku konfiguracyjnego") 
            else:
                drukuj(f"Plik {path_to_file} byl prawdopodobnie pusty")
                file=open(path_to_file, "w")
                file.write(str(content_new))
                drukuj("nasluchiwanie się powiodło - stworzono nowy plik z konfiguracja")
                #logi
                logi_do_json_z_konfiguracjami=open(f"{self.basic_path_project}/odebrane_jsony_z_konfiguracjami.json", "a")
                logi_do_json_z_konfiguracjami.write("\n")
                logi_do_json_z_konfiguracjami.write(str(content_new))
                logi_do_json_z_konfiguracjami.close()
        else:
            drukuj("UWAGA")
            drukuj(f"plik {path_to_file} nie istniał, tudzież był pusty")
            file=open(path_to_file, "w")
            file.write(str(content_new))
            drukuj("nasluchiwanie się powiodło - stworzono nowy plik z konfiguracja")

def pobieranie_plikow_z_serwera():
    pobieramy=PobranieOutsystem()
    pobieramy.plik_z_alarmami()
    pobieramy.plik_z_konfiguracja_raspberki()

def main():
    basic_path_ram=""
    flara_skryptu=""
    try:
        drukuj(f"--------{nazwa_programu()}-------------")
        dotenv_path = "./.env"
        load_dotenv(dotenv_path)
        if os.name == "posix":
            drukuj("posix")
            basic_path_ram=os.getenv('basic_path_ram')
        else:
            drukuj("notposix - pewnie windows - wez to czlowieku oprogramuj")
            przerwij_i_wyswietl_czas()
        if os.path.isdir(f"{basic_path_ram}") == True:
            flara_skryptu=f"{basic_path_ram}/{nazwa_programu()}.flara"
            with open(flara_skryptu, "w") as file:
                if os.name=="posix":
                    file.write(f"{str(os.getpid())}")
                else:
                    file.write("notposix")
            file.close()
            pobieranie_plikow_z_serwera()
            if os.path.exists(flara_skryptu):
                os.remove(flara_skryptu)
        else:
            drukuj("BRAK SCIESZKI - sprawdż czy .env i folder roboczy wiedza o swoim istnieniu")
    except Exception as e:
        drukuj(f"exception {e}")
        drukuj(f"sprawdz czy .env widziany jest w crontabie")
        #os.remove(fal)
        traceback.print_exc()
        if os.path.isdir(basic_path_ram):
            os.remove(flara_skryptu)
            drukuj("usuwam flare")


if __name__ == "__main__":
    main()