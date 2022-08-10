# - *- coding: utf-8 - *-

from inspect import trace
import urllib.request, json
import sys
import os
import datetime
import traceback
from dotenv import load_dotenv
import psutil

def nazwa_programu():
    return "zaciaganie_plikow_z_outsystemu.py"

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

class ExceptionNotExistFolder(Exception):
    pass

class ExceptionWindows(Exception):
    pass

def file_istnienie(path_to_file, komunikat):
    if os.path.exists(path_to_file) == False:
        drukuj(f"{komunikat}")
        raise ExceptionEnvProjektu
    return True

def folder_istnienie(path_to_folder, komunikat):
    if os.path.isdir(path_to_folder) == False:
        drukuj(f"{komunikat}")
        raise ExceptionEnvProjektu
    return True

def folder_istnienie_2(path_to_folder, komunikat):
    if os.path.isdir(path_to_folder) == False:
        drukuj(f"{komunikat}")
        raise ExceptionNotExistFolder
    return path_to_folder

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

####################

def numer_seryjny_raspberki():
    sn=[]
    with open("/sys/firmware/devicetree/base/serial-number", "r") as plik_numer_seryjny:
        sn=plik_numer_seryjny.readlines()
    #ucinam ostatni bit z czymś takim - \u0000
    #powinniśmy dostać coś w tym stylu
    return sn[0][0:-1]

def get_mac_address():
    drukuj("def: get_mac_address")
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
                drukuj(interface.address)
                interfejs_return=interface.address
    except KeyError as e:
        drukuj(f"exception: {e}")
        raise ExceptionEnvProjektu
    return interfejs_return

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
        config_folder="config_klraspi"
        head, tail = os.path.split(os.getcwd())
        drukuj(f"config_folder:  {head}/{config_folder}")
        self.path_to_config=folder_istnienie_2(f"{head}/{config_folder}", "nie ma folderu do configu! sprawdz czy istnieje!")
        przerwij_i_wyswietl_czas()

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
        try:
            with urllib.request.urlopen(url) as url:
                content_new = json.dumps(json.loads(url.read()), indent=2) #json.loads(url.read())
        except Exception as e:
            drukuj(f"EEEEEEEEEERRRRRROOOOOOOORRRR")
            drukuj(f"{e}")
            drukuj(f"sprawdz link: {url}")
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
        if os.name=="posix":
            drukuj("posix")
            dotenv_path = "./.env"
            file_istnienie(dotenv_path, "dotenv_path - coś nie tak")
            load_dotenv(dotenv_path)
            basic_path_ram=zmienna_env_folder('basic_path_ram', ".env - sprawdz basic_path_ram")

            flara_skryptu=f"{basic_path_ram}/{nazwa_programu()}.flara"
            with open(flara_skryptu, "w") as file:
                file.write(f"{str(os.getpid())}")
            file.close()
            pobieranie_plikow_z_serwera()
        else:
            drukuj("oprogramowanie tego Windowsa ziom")
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
