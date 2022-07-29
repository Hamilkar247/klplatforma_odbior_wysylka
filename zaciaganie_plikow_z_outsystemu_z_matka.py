#!/usr/bin/python3
# - *- coding: utf-8 - *-

import urllib.request, json
import hashlib
import sys
import shutil
import os
import datetime
import traceback

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

def get_mother_serial_number():
    try:
        path_to_file='/home/weewx/wk_skrypty/pliki_od_weewxa/urzadzenie_dane.json'
        data = []
        if os.path.exists(path_to_file): 
            with open(path_to_file,"r") as f: 
                data = json.load(f)
        drukuj(data['serial_number'])
        return str(data['serial_number'])
    except Exception as e:
        drukuj(e)
        drukuj(traceback.print_exc())
        return "NONE"

def plik_z_alarmami():
    #hardcode ! do poprawienia !
    url="https://personal-5ndvfcym.outsystemscloud.com/KlimaLog_core/rest/V1/GetAlarms?Rpi_serial_number="+numer_seryjny_raspberki()
    content_new=None
    with urllib.request.urlopen(url) as url:
        content_new = json.dumps(json.loads(url.read()), indent=2) #json.loads(url.read())

    path_to_file="/home/weewx/config/urzadzenia"+"/"+"mother_sn_"+get_mother_serial_number()+".json"
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
                logi_do_json_z_alarmami=open("/home/weewx/wk_skrypty/odebrane_jsony_z_alarmami.json", "a")
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
            logi_do_json_z_alarmami=open("/home/weewx/wk_skrypty/odebrane_jsony_z_alarmami.json", "a")
            logi_do_json_z_alarmami.write(f"{data_i_godzina()}")
            logi_do_json_z_alarmami.write("\n")
            logi_do_json_z_alarmami.write(str(content_new))
    else:
        drukuj("UWAGA")
        drukuj(f"Nie było do tej pory pliku {path_to_file}")
        file=open(path_to_file, "w")
        file.write(str(content_new))
        drukuj("nasluchiwanie się powiodło - stworzono nowy plik z alarmami czujników")

def plik_z_konfiguracja_raspberki():
    #hardcode ! do poprawienia !
    url="https://personal-5ndvfcym.outsystemscloud.com/KlimaLog_core/rest/V1/GetRpiConfig?Rpi_serial_number="+numer_seryjny_raspberki()
    content_new=None
    with urllib.request.urlopen(url) as url:
        content_new = json.dumps(json.loads(url.read()), indent=2) #json.loads(url.read())

    #hardcode ! do poprawienia !
    path_to_file="/home/weewx/config"+"/"+"config.json"
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
                logi_do_json_z_konfiguracjami=open("/home/weewx/wk_skrypty/odebrane_jsony_z_konfiguracjami.json", "a")
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
            logi_do_json_z_konfiguracjami=open("/home/weewx/wk_skrypty/odebrane_jsony_z_konfiguracjami.json", "a")
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
    plik_z_alarmami()
    plik_z_konfiguracja_raspberki()

def main():
    pobieranie_plikow_z_serwera()

if __name__ == "__main__":
    main()