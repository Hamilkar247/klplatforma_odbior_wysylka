# - *- coding: utf-8 - *-
from inspect import trace
import os
from datetime import datetime, timedelta
import sys
import traceback
from typing import Type
#from requests import Session
import requests
from urllib.request import urlopen
import urllib
import json
import time
from dotenv import load_dotenv
import socket
import uuid
import psutil


def nazwa_programu():
    return "wysylanie_pomiarow_do_outsystem.py"

def data_i_godzina():
    now = datetime.now()
    current_time = now.strftime("%d/%m/%y %H:%M:%S")
    return current_time

def drukuj(obiekt_do_wydruku):
    try:
        print(data_i_godzina()+" "+nazwa_programu()+" "+str(obiekt_do_wydruku))
    except Exception as e:
        print("blad w metodzie drukuj - sprawdz czy nie wywolales funkcji bez zadnego parametru")
        print(e)
        print(traceback.print_exc())

def przerwij_i_wyswietl_czas():
    czas_teraz = datetime.now()
    current_time = czas_teraz.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    sys.exit()

class ExceptionEnvProjektu(Exception):
    pass

class ExceptionWindows(Exception):
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
##############

class KlasaWysylka(object):
    def __init__(self, inicjalna):
        #flagi do statusu
        self.flaga_pierwszej_wysylki=False #1 #1
        self.flaga_brak_danych_z_nadajnikow=False #2 #2
        self.flaga_ethernet=False #4 #3
        self.flaga_wifi=False #8 #4
        self.flaga_slaby_zasieg_wifi=False #16 #5 
        self.flaga_posiadanie_baterii_platformy=False #32 #6
        self.flaga_niski_stan_baterii_platformy=False #64 #7
        self.flaga_blad_dongla=False #128 #8
        self.flaga_blad_w_kodzie___nieokreslony_blad=False #256 #9
        self.flaga_wykrycia_not_found_device_na_outsystem=False #512 #10
        self.flaga_blad_w_zaciaganiu_plikow_z_outsystem=False #1024 #11
        self.flaga_blad_w_sortowanie_i_usrednianie_pomiarow=False #2048 #12
        self.flaga_blad_w_pomiar_rtl_433=False #4096 #13
        self.flaga_blad_w_petla_programu=False #8192 #14
        self.flaga_uzycie_ubijaj_procesy=False #16384 #15
        self.flaga_uzycie_reset_portu_usb=False #32768 #16
        self.flaga_reset_portu_usb_sie_nie_udal=False #65536 #17

        #flagi_programow
        self.flagi_procesow=False
        drukuj("class: KlasaWysylka")
        self.basic_path_ram=os.getenv('basic_path_ram')
        self.docelowy_url_dla_post_pomiarow=os.getenv('docelowy_url_dla_post_pomiarow')
        self.basic_path_project=os.getenv('basic_path_project')
        self.inicjalizacja_zmiennych_paczkowych()
        self.zaczynamy()

    def inicjalizacja_zmiennych_paczkowych(self):
        drukuj("def: inicjalizacja_zmiennych_paczkowych")
        self.wersja_json="0.7"
        self.sn_platform=self.get_mac_address() #get_numer_seryjny_platform() # do wywalenia
        self.mac_address_platform=self.get_mac_address()
        self.local_ipv4=self.getIPV4()
        self.status_platform="0"#self.wylicz_status_platform()
        self.zasieg_platform_wifi=self.wyznacz_zasieg_platform_wifi()
        self.napiecie_baterii_platform=self.metoda_napiecie_baterii_platform()


        #self.mother_serial_number=self.get_mother_serial_number()

    #trzeba zastapic libka pythonowa by uniezaleźnić od basha
    def getIPV4(self):
        try:
            str_ip="nie wyznaczono"
            drukuj("def: getIPV4")
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            print(s.getsockname()[0])
            str_ip=s.getsockname()[0]
            if str_ip is None:
                drukuj("nie udało się wyznaczyć numeru ip w sieci lokalnej")
                str_ip=f"nie wyznaczono"
                
            ###cmd='/sbin/ifconfig wlan0 | grep "inet "' #awk don't work in python3 # | awk "{print $2}"'
            ###dbm = str(os.popen(cmd).read()).strip()
            ###drukuj(f"przed:{dbm}")
            ###dbm = dbm.split(" ")[1] # biore drugi wyraz z numerem ip
            #drukuj(f"po:   {dbm}")
            
            #if dbm:
            #    drukuj(str(dbm))
            #    str_ip=f"LAN: {dbm}"
            #else:
            #    cmd='/sbin/ifconfig eth0 | grep "inet "' # awk don't work in python3 # | awk "{print $2}"'
            #    dbm = os.popen(cmd).read().strip()
            #    dbm = dbm.split(" ")[1] # biore drugi wyraz z numerem ip
            #    if dbm:
            #        drukuj(str(dbm))
            #        str_ip=f"ETH: {dbm}"
            #    else:
            #        drukuj("nie udało się wyznaczyć numeru ip w sieci lokalnej")
            #        str_ip=f"nie wyznaczono"
        except Exception as e:
            drukuj(f"getIPV4: wystapil blad {e}")
            str_ip=f"nie wyznaczono"
            traceback.print_exc()
        return str_ip

    def metoda_napiecie_baterii_platform(self):
        drukuj("def: status_baterii_rpi")
        if os.path.exists(f"{self.basic_path_ram}/dane_baterii.txt"):
            with open(f"{self.basic_path_ram}/dane_baterii.txt", "r") as file:
                text=file.read()
            drukuj(text)
            wartosc_w_V=text.split(": ")[1] #biore same liczby
            return wartosc_w_V
        return "-1"

    def czy_istnieje_plik_wysylka_log(self):
        if os.path.exists(f"{self.basic_path_ram}/wysylka.log") == False:
            self.flaga_pierwszej_wysylki=True
        
    def uzycie_reset_portu(self):
        path=f"{self.basic_path_ram}/reset_portu_usb.py.log"
        if os.path.exists(path) == True:
            self.flaga_uzycie_reset_portu_usb=True
            os.remove(path)
    
    def brak_wykrycia_reset_portu(self):
        path=f"{self.basic_path_ram}/reset_portu_usb.py.error"
        if os.path.exists(path) == True:
            self.flaga_reset_portu_usb_sie_nie_udal=True
            os.remove(path)
    
    # #DO ZMIANY
    # def podlaczenie_po_ethernecie(self):
    #     if False:
    #         self.flaga_ethernet=True
    
    # #DO ZMIANY
    # def podlaczenie_po_wifi(self):
    #     if True:
    #         self.flaga_wifi=True

    # #DO ZMIANY
    # def slaby_zasieg(self):
    #     if False:
    #         self.flaga_slaby_zasieg_wifi=True

    #DO ZMIANY
    def posiadanie_baterii_platformy(self):
        if False:
            pass
            #self.flaga

    def czy_ubity_byl_jakis_proces(self):
        path=f"{self.basic_path_ram}/ubijaj_procest.py.log"
        if os.path.exists(path) == True:
            self.flaga_uzycie_ubijaj_procesy=True
            os.remove(path)

    def przeliczenia_flag(self):
        self.czy_istnieje_plik_wysylka_log()
        self.posiadanie_baterii_platformy()
        self.czy_ubity_byl_jakis_proces()
        self.uzycie_reset_portu()
        self.brak_wykrycia_reset_portu()

    def wylicz_status_platform(self):
        status=0
        self.przeliczenia_flag()
        #if os.path.exists(f"{self.basic_path_ram}/wysylka.log") == False:
        #    self.flaga_pierwszej_wysylki=True
        #    status=status+1
        if self.flaga_pierwszej_wysylki == True:
            status=status+1
        if self.flaga_brak_danych_z_nadajnikow == True:
            status=status+2
        if self.flaga_ethernet == True:
            status=status+4
        if self.flaga_wifi == True:
            status=status+8
        if self.flaga_slaby_zasieg_wifi == True:
            status=status+16
        if self.flaga_posiadanie_baterii_platformy == True:
            status=status+32
        if self.flaga_niski_stan_baterii_platformy == True:
            status=status+64
        if self.flaga_blad_dongla == True:
            status=status+128
        if self.flaga_blad_w_kodzie___nieokreslony_blad == True:
            status=status+256
        if self.flaga_wykrycia_not_found_device_na_outsystem == True:
            status=status+512
        if self.flaga_blad_w_zaciaganiu_plikow_z_outsystem == True:
            status=status+1024
        if self.flaga_blad_w_sortowanie_i_usrednianie_pomiarow == True:
            status=status+2048
        if self.flaga_blad_w_pomiar_rtl_433 == True:
            status=status+4096
        if self.flaga_blad_w_petla_programu == True:
            status=status+8192
        if self.flaga_uzycie_ubijaj_procesy == True:
            status=status+16384
        if self.flaga_uzycie_reset_portu_usb == True:
            status=status+32768
        return str(status)

    #zastapic numerem MAC platformy
    def get_numer_seryjny_platform(self):
        sn=[]
        with open("/sys/firmware/devicetree/base/serial-number", "r") as plik_numer_seryjny:
            sn=plik_numer_seryjny.readlines()
        #ucinam ostatni bit z czymś takim - \u0000
        return sn[0][0:-1]

    def get_mac_address(self):
        mac_address_hex_bez_zeroiks="brak_mac_address"
        if os.name == "posix":
            #ahjo - gdy nie znajdzie interfejsu - zwraca losową liczbę
            ####mac_address_int = uuid.getnode()
            ####drukuj(mac_address_int)
            ####mac_address_hex = hex(mac_address_int)
            ####drukuj(mac_address_hex)
            ####mac_address_hex_bez_zeroiks=str(mac_address_hex).split("x")[1]#f"{mac_address_hex[2,-1]}"
            ####drukuj(f"MAC address:{mac_address_hex}")
            ####return mac_address_hex_bez_zeroiks
            nics = psutil.net_if_addrs()[os.getenv('interfejs_sieciowy')]
            for interface in nics:
                if interface.family == 17:
                    print(interface.address)
            return interface.address
            #return "1113uddd32"
        else:
            drukuj("brak oprogramowanego windowsa")
            return mac_address_hex_bez_zeroiks
    
    def get_model(self):
        return "TFA KlimaLogg Pro"

    # do usuniecia bashowe wywolania
    def wyznacz_zasieg_platform_wifi(self):
        #inspiracja https://stackoverflow.com/a/30585711/13231758
        drukuj("def: wyznacz_zasieg_platform_wifi")
        if os.name == "posix":
            nazwa_interfejsu=os.getenv('nazwa_interfejsu')
            #cmd=f"/usr/sbin/iwconfig {nazwa_interfejsu} | grep Signal | /usr/bin/awk '{print $4}' | /usr/bin/cut -d'=' -f2"
            cmd=f"/usr/sbin/iwconfig {nazwa_interfejsu} | grep Signal"
            dbm = os.popen(cmd).read()
            if dbm:
                dbm_z_jedn=dbm.split("level=")[1]
                try:
                    dbm_liczba=int(dbm_z_jedn.split(" ")[0])
                    drukuj(f"{dbm_liczba}")
                    quality = 2 * (dbm_liczba + 100)
                    drukuj("{0} dbm_num = {1}%".format(dbm_liczba, quality))
                    if quality < 70:
                        self.flaga_slaby_zasieg_wifi = True
                    self.flaga_wifi=True
                    self.flaga_ethernet=False #tutaj się wacham - jak są dwa co ma być w statusie
                    return str(quality)
                except Exception as e:
                    drukuj("brak liczby")
                    drukuj(f"{e}")
                    self.flaga_wifi=False
                    self.flaga_ethernet=True #nie do konca jestem tego pewien
                    traceback.print_exc()
            else:
                drukuj("Siła sygnału połączenia wifi router nie została znaleziona")
                self.flaga_wifi=False
                self.flaga_ethernet=True #nie do konca jestem tego pewien
                return str(-1)
        else:
            drukuj("wez kurde oprogramuj tego windowsa co?")
            przerwij_i_wyswietl_czas()

    def dostosuj_format_id(self, id):
        #drukuj(f"id:{id}") #81
        id=hex(id)         
        #drukuj(f"id:{id}") #0x51
        id=str(id).split("x")[1] #51
        if len(id) < 4:
            for i in range(0,3):
                id="0"+id
                if len(id)==4:
                    break
        #drukuj(f"id:{id}") #0051
        return id

    def dostosuj_format_czasu(self, czas):
        #drukuj("====================================")
        #drukuj(czas)
        #drukuj("=============%%%=======================")
        obj_datetime=datetime.strptime(czas, "%Y-%m-%d %H:%M:%S")#"%d/%m/%y %H:%M:%S"))
        #drukuj(obj_datetime)
        #drukuj(type(obj_datetime))
        #drukuj("====================================")
        format_daty_docelowy=datetime.strftime(obj_datetime, "%d/%m/%y %H:%M:%S")
        return format_daty_docelowy

    def temperatura_sama_liczba(self, temperatura_z_jednostka):
        return temperatura_z_jednostka.split(" ")[0] #ucinamy " C" z wartosc 
    
    def parsowanie_pomiarow(self, krotki_danych):
        drukuj("parsowanie_zmiennych")
        try:
            krotki_danych=krotki_danych
            lista=[]
            print(f"krotki_danych - pierwszy element: {krotki_danych[0]}")
            print(f"krotki_danych: {krotki_danych}")
            if len(krotki_danych) < 1:
                self.flaga_brak_danych_z_nadajnikow=True

            for krotka in krotki_danych:
                element_listy=[]
                #print(f"krotka: {krotka}")
                krotka=json.loads(krotka)
                sn_trasmitter=str(self.dostosuj_format_id(krotka['id'])) #klimalogi dzieci mają id w 16 a json mi to skonwertowal na decymalny
                interval="1"
                ##czujniki przesylaja w greenwitch czas - trzeba uwzglednic strefe czasowa
                time = str(self.dostosuj_format_czasu(krotka['time']))
                temp = str(self.temperatura_sama_liczba(krotka['temperature_C']))
                hum = str(krotka['humidity'])
                # skrypcie sortowanie_i_usrednianie_dodalem taki atrybut
                zasieg = str(krotka['zasieg']) #str("0") #brak tak naprawde informacji o zasiegu od nadajnika
                batt = str(krotka['battery_ok'])
                wersja_czujnika = str(krotka['model'])
                element_listy = {
                    "sn_transmitter": sn_trasmitter,
                    "interval": "1", #ustawiam na sztywno 1 - w tej wersji interval zbierania pomiarow jest ustalony na sztywno na 1
                    "time": time,
                    "temp": temp,
                    "hum": hum,
                    "zasieg": zasieg,
                    "batt": batt,
                    "wersja_czujnika": wersja_czujnika,
                    "status": "OK" #status
                }
                #drukuj(element_listy)
                lista.append(element_listy)
            drukuj(lista)
            return lista
        except TypeError as e:
            drukuj(str(e))
            traceback.print_exc()
            return None
        except Exception as e:
            drukuj(str(e))
            traceback.print_exc()
            return None

    def wyslanie_obiektu_json_z_danymi(self, json_object):
        #shutil.copy2(self.path_plik_z_krotkami_do_wysylki_file, self.path_plik_z_krotkami_do_wysylki_file+".work")
        #print(json_object)
        dict_zwracany={"status_code":"0", "sukces_zapisu":"False", "error_text":"brak"}
        try:
            docelowy_url_dla_post=self.docelowy_url_dla_post_pomiarow#"https://personal-5ndvfcym.outsystemscloud.com/KlimaLog_core/rest/V1/CreateMeasurement"
            #"https://personal-5ndvfcym.outsystemscloud.com/KlimaLog_core/rest/V1/RESTAPIMethod1"
            response = requests.post(
                docelowy_url_dla_post,
                json=json_object,
            )
            drukuj(f"response.txt: {response.text}")
            #mogę jeszcze sprawdzać Success
            print(f"response.status_code: {response.status_code}")
            if response.status_code == 200:
                drukuj("poprawna odpowiedż serwera")
                json_response=json.loads(response.text)
                print(json_response)
                dict_zwracany['status_code']="200"
                try:
                    if json_response["Success"] is not None:
                        czy_sukces=json_response["Success"]
                        if czy_sukces == True:
                            pass
                            print("jest")
                        else:
                            drukuj(f"Success:{czy_sukces}")
                        dict_zwracany["sukces_zapisu"]=str(f"{czy_sukces}")
                except KeyError as e:
                    drukuj(f"Nie ma takiego parametru w odeslanym jsonie z outsystemu {e}")
                    dict_zwracany["sukces_zapisu"]=str(f"{False}")
                #plik_z_danymi=open(self.path_plik_z_krotkami_do_wysylki_file, "w")
                #plik_z_danymi.write("")
                #plik_z_danymi.close()
            else:
                drukuj("błędna odpowiedź serwera")
                drukuj(f"response.status_code: {response.status_code}")
        except urllib.error.URLError as e:
            drukuj(f"Problem z wyslaniem pakietu: {e}")
            traceback.print_exc()
        except Exception as e:
            drukuj("zlapałem wyjatek: {e}")
            traceback.print_exc()
        drukuj(f"dict_zwracany: {type(dict_zwracany)}")
        return dict_zwracany


    def zaczynamy(self):
        drukuj("def: zaczynamy")
        try:
            scieszka=f"{self.basic_path_ram}/sort_usr"
            if os.path.isdir(f"{self.basic_path_ram}/sort_usr") == True:
                lista_plikow=os.listdir(f"{self.basic_path_ram}/sort_usr")
                drukuj(f"lista_plikow: {lista_plikow}")
                file = open(f"{self.basic_path_ram}/wysylka.log", "a")
                file.write(f"{data_i_godzina()}\n")
                lista_plikow=lista_plikow[::-1] #robie rewers na liście żeby wrzucało na outsystem od najstarszego pomiaru
                if len(lista_plikow)>0:
                    for plik in lista_plikow: 
                        drukuj(f"nazwa pliku: {plik}")
                        with open(scieszka+"/"+plik, "r") as file:
                            krotki_danych = file.readlines()
                        file.close()
                        lista_pomiarow_z_transmiterow = self.parsowanie_pomiarow(krotki_danych)
                        self.status=self.wylicz_status_platform()
                        json_data = {
                            "wersja_json": self.wersja_json,
                            #po uzgodnieniu z tomkiem sn_rpi --> sn_platformy
                            "sn_platform": self.mac_address_platform,#self.sn_platform,
                            "mac_address_platform": self.mac_address_platform,
                            "local_ipv4": self.local_ipv4,
                            #nie potrzebne#"sn_device_mother": self.mother_serial_number,
                            "status_platform": self.status,
                            "zasieg_platform_wifi": self.zasieg_platform_wifi,
                            "bateria_platform": self.napiecie_baterii_platform,
                            "data": lista_pomiarow_z_transmiterow
                        }
                        #drukuj("dziala")
                        json_object = json.dumps(json_data, indent = 4)
                        #plik będący logiem wysyłanych plików do tomka
                        path_to_json_wysylki_txt=f"{self.basic_path_project}/json_do_wysylki.txt"
                        with open(f"{path_to_json_wysylki_txt}", "a+") as outfile:
                            outfile.write("----------------------------")
                            outfile.write(str(data_i_godzina()))
                            outfile.write("\n"+json_object) 
                            #drukuj(json_object)
            
                        slownik_response=self.wyslanie_obiektu_json_z_danymi(json_data)
                        #dopisac ze zalezy od OK=200
                        drukuj(f"slownik_response: {slownik_response}")
                        drukuj(f"kurwa  {type(slownik_response)}")                        
                        drukuj(type(slownik_response['status_code'] ))
                        drukuj(type(slownik_response["sukces_zapisu"]))
                        if slownik_response['status_code'] == "200" and slownik_response["sukces_zapisu"] == "True":
                            with open(f"{self.basic_path_ram}/wysylka.log", "a") as logi:
                                logi.write(f"plik: {plik}\n")
                                logi.write(f"status_code:{slownik_response['status_code']}")
                                logi.write(f"sukces_zapisu:{slownik_response['sukces_zapisu']}\n")
                            with open(f"{self.basic_path_ram}/status.log", "a") as status_logi:
                                status_logi.write(f"------------------\n")
                                status_logi.write(f"{data_i_godzina()}\n")
                                status_logi.write(f"{self.wylicz_status_platform()}\n")
                        else:
                            drukuj("nie udalo się wyslac i poprawnie zapisać pomiarow - wysylac będę probowal ponownie w kolejnej iteracji")
                            with open(f"{self.basic_path_ram}/status.log", "a") as status_logi:
                                status_logi.write(f"------------------\n")
                                status_logi.write(f"{data_i_godzina()}\n")
                                status_logi.write(f"{self.wylicz_status_platform()}\n")
                        
                        if os.path.exists(scieszka+"/"+plik):
                            os.remove(scieszka+"/"+plik)
            else:
                drukuj("brak plikow do posortowania")

        except Exception as e:
            drukuj("przy zmiennych został wyłapany bląd "+str(e))
            traceback.print_exc()
            #przerwij_i_wyswietl_czas()

def main():
    basic_path_ram=""
    flara_skryptu=""
    try:
        drukuj(f"------{nazwa_programu()}--------")
        if os.name == "posix":
            drukuj("posix")
            dotenv_path = "./.env"
            file_istnienie(dotenv_path, "sprawdz czy plik .env istnieje")
            load_dotenv(dotenv_path)
            basic_path_ram=zmienna_env_folder('basic_path_ram', ".env - sprawdz basic_path_ram")

            flara_skryptu=f"{basic_path_ram}/{nazwa_programu()}.flara"
            with open(flara_skryptu, "w") as file:
                file.write(f"{str(os.getpid())}")
            file.close()
            inicjalna=False
            klasawysylka=KlasaWysylka(inicjalna)
        else:
            drukuj("notposix - pewnie windows - wez to czlowieku oprogramuj")
            przerwij_i_wyswietl_czas()
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
