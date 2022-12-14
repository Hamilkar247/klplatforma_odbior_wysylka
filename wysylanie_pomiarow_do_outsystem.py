# - *- coding: utf-8 - *-
from importlib.resources import path
from inspect import trace
import os
from datetime import datetime
import traceback
from typing import Type
#from requests import Session
import requests
from urllib.request import urlopen
import urllib
import json
from dotenv import load_dotenv
import socket
from funkcje_pomocnicze import FunkcjePomocnicze, ExceptionEnvProjektu, ExceptionNotExistFolder, ExceptionWindows
from pytz import timezone
from getmac import get_mac_address as gma

###############

def nazwa_programu():
    return "wysylanie_pomiarow_do_outsystem.py"

def funkcje_pomocnicze_inicjalizacja():
    fp=FunkcjePomocnicze(nazwa_programu())
    return fp

###############

class KlasaWysylka(object):
    def __init__(self, inicjalna):
        self.fp=funkcje_pomocnicze_inicjalizacja()
        #flagi do statusu
        # odnośnik https://lightlog.atlassian.net/wiki/spaces/LIG/pages/270630932/Tablica+Status+w
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
        #18 #262144 - uzywane w pobranie nowerj wersji programu klplatforma_odbior_wysylka
        #19 #524288 - używane w klplatforma utrzymanie wersji - do stworzenie nowego virtualenva w klplaf
        self.flaga_pobranie_nowej_wersji_programu_klplatforma_odbior_wysylka=False 

        #flagi_programow
        self.flagi_procesow=False
        self.fp.drukuj("class: KlasaWysylka")
        self.basic_path_ram=os.getenv('basic_path_ram')
        self.docelowy_url_dla_post_pomiarow=os.getenv('docelowy_url_dla_post_pomiarow')
        self.basic_path_project=os.getenv('basic_path_project')
        self.inicjalizacja_zmiennych_paczkowych()
        self.zaczynamy()

    def inicjalizacja_zmiennych_paczkowych(self):
        self.fp.drukuj("def: inicjalizacja_zmiennych_paczkowych")
        self.wersja_json="0.8"
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
            self.fp.drukuj("def: getIPV4")
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            self.fp.drukuj(s.getsockname()[0])
            str_ip=s.getsockname()[0]
            if str_ip is None:
                self.fp.drukuj("nie udało się wyznaczyć numeru ip w sieci lokalnej")
                str_ip=f"nie wyznaczono"
                
        except Exception as e:
            self.fp.drukuj(f"getIPV4: wystapil blad {e}")
            str_ip=f"nie wyznaczono"
            traceback.print_exc()
        return str_ip

    def metoda_napiecie_baterii_platform(self):
        self.fp.drukuj("def: status_baterii_rpi")
        if os.path.exists(f"{self.basic_path_ram}/dane_baterii.txt"):
            with open(f"{self.basic_path_ram}/dane_baterii.txt", "r") as file:
                text=file.read()
            self.fp.drukuj(text)
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

    def get_mac_address(self):
        if os.name == "posix":
            self.fp.drukuj(f"mac_address:{gma()}")
            return gma()
        else:
            drukuj("brak oprogramowanego windowsa")
            raise ExceptionWindows
    
    def get_model(self):
        return "TFA KlimaLogg Pro"

    # do usuniecia bashowe wywolania
    def wyznacz_zasieg_platform_wifi(self):
        #inspiracja https://stackoverflow.com/a/30585711/13231758
        self.fp.drukuj("def: wyznacz_zasieg_platform_wifi")
        if os.name == "posix":
            nazwa_interfejsu=os.getenv('nazwa_interfejsu')
            #cmd=f"/usr/sbin/iwconfig {nazwa_interfejsu} | grep Signal | /usr/bin/awk '{print $4}' | /usr/bin/cut -d'=' -f2"
            cmd=f"/usr/sbin/iwconfig {nazwa_interfejsu} | grep Signal"
            dbm = os.popen(cmd).read()
            if dbm:
                dbm_z_jedn=dbm.split("level=")[1]
                try:
                    dbm_liczba=int(dbm_z_jedn.split(" ")[0])
                    self.fp.drukuj(f"{dbm_liczba}")
                    quality = 2 * (dbm_liczba + 100)
                    self.fp.drukuj("{0} dbm_num = {1}%".format(dbm_liczba, quality))
                    if quality < 70:
                        self.flaga_slaby_zasieg_wifi = True
                    self.flaga_wifi=True
                    self.flaga_ethernet=False #tutaj się wacham - jak są dwa co ma być w statusie
                    return str(quality)
                except Exception as e:
                    self.fp.drukuj("brak liczby")
                    self.fp.drukuj(f"{e}")
                    self.flaga_wifi=False
                    self.flaga_ethernet=True #nie do konca jestem tego pewien
                    traceback.print_exc()
            else:
                self.fp.drukuj("Siła sygnału połączenia wifi router nie została znaleziona")
                self.flaga_wifi=False
                self.flaga_ethernet=True #nie do konca jestem tego pewien
                return str(-1)
        else:
            raise ExceptionWindows
            self.fp.drukuj("wez kurde oprogramuj tego windowsa co?")
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
        self.fp.drukuj("parsowanie_zmiennych")
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
            self.fp.drukuj(lista)
            return lista
        except TypeError as e:
            self.fp.drukuj(str(e))
            traceback.print_exc()
            return None
        except Exception as e:
            self.fp.drukuj(str(e))
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
            self.fp.drukuj(f"response.txt: {response.text}")
            #mogę jeszcze sprawdzać Success
            print(f"response.status_code: {response.status_code}")
            if response.status_code == 200:
                self.fp.drukuj("poprawna odpowiedż serwera")
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
                            self.fp.drukuj(f"Success:{czy_sukces}")
                        dict_zwracany["sukces_zapisu"]=str(f"{czy_sukces}")
                except KeyError as e:
                    self.fp.drukuj(f"Nie ma takiego parametru w odeslanym jsonie z outsystemu {e}")
                    dict_zwracany["sukces_zapisu"]=str(f"{False}")
                #plik_z_danymi=open(self.path_plik_z_krotkami_do_wysylki_file, "w")
                #plik_z_danymi.write("")
                #plik_z_danymi.close()
            else:
                self.fp.drukuj("błędna odpowiedź serwera")
                self.fp.drukuj(f"response.status_code: {response.status_code}")
        except urllib.error.URLError as e:
            self.fp.drukuj(f"Problem z wyslaniem pakietu: {e}")
            traceback.print_exc()
        except Exception as e:
            self.fp.drukuj("zlapałem wyjatek: {e}")
            traceback.print_exc()
        self.fp.drukuj(f"dict_zwracany: {type(dict_zwracany)}")
        return dict_zwracany

    def get_diff(self, now, tzname):
        tz = timezone(tzname)
        utc = timezone('UTC')
        utc.localize(datetime.now())
        delta =  utc.localize(now) - tz.localize(now)
        print(delta)
        delta=str(delta).split(":")[0]
        delta="+"+delta
        print(delta)
        return delta

    def zaczynamy(self):
        self.fp.drukuj("def: zaczynamy")
        try:
            scieszka=f"{self.basic_path_ram}/sort_usr"
            if os.path.isdir(f"{self.basic_path_ram}/sort_usr") == True:
                lista_plikow=os.listdir(f"{self.basic_path_ram}/sort_usr")
                self.fp.drukuj(f"lista_plikow: {lista_plikow}")
                file = open(f"{self.basic_path_ram}/wysylka.log", "a")
                file.write(f"{self.fp.data_i_godzina()}\n")
                lista_plikow=lista_plikow[::-1] #robie rewers na liście żeby wrzucało na outsystem od najstarszego pomiaru
                if len(lista_plikow)>0:
                    for plik in lista_plikow: 
                        self.fp.drukuj(f"nazwa pliku: {plik}")
                        with open(scieszka+"/"+plik, "r") as file:
                            krotki_danych = file.readlines()
                        file.close()
                        lista_pomiarow_z_transmiterow = self.parsowanie_pomiarow(krotki_danych)
                        self.status=self.wylicz_status_platform()
                        json_data = {
                            "wersja_json": self.wersja_json,
                            "sn_platform": self.mac_address_platform,#self.sn_platform,
                            #nie potrzebne#"sn_device_mother": self.mother_serial_number,
                            "status_platform": self.status,
                            "zasieg_platform_wifi": self.zasieg_platform_wifi,
                            "bateria_platform": self.napiecie_baterii_platform,
                            "local_ipv4": self.local_ipv4,
                            "timezone": self.get_diff(datetime.now(), "Europe/Warsaw"),
                            "data": lista_pomiarow_z_transmiterow
                        }
                        #drukuj("dziala")
                        json_object = json.dumps(json_data, indent = 4)
                        #plik będący logiem wysyłanych plików do tomka
                        path_to_json_wysylki_txt=f"{self.basic_path_project}/json_do_wysylki.txt"
                        self.fp.drukuj(f"path_to_json_wysylki_txt: {path_to_json_wysylki_txt}")
                        with open(f"{path_to_json_wysylki_txt}", "a+") as outfile:
                            outfile.write("----------------------------")
                            outfile.write(str(self.fp.data_i_godzina()))
                            outfile.write("\n"+json_object) 
                            #drukuj(json_object)
            
                        slownik_response=self.wyslanie_obiektu_json_z_danymi(json_data)
                        #dopisac ze zalezy od OK=200
                        self.fp.drukuj(f"slownik_response: {slownik_response}")
                        self.fp.drukuj(type(slownik_response['status_code'] ))
                        self.fp.drukuj(type(slownik_response["sukces_zapisu"]))
                        if slownik_response['status_code'] == "200" and slownik_response["sukces_zapisu"] == "True":
                            with open(f"{self.basic_path_ram}/wysylka.log", "a") as logi:
                                logi.write(f"plik: {plik}\n")
                                logi.write(f"status_code:{slownik_response['status_code']}")
                                logi.write(f"sukces_zapisu:{slownik_response['sukces_zapisu']}\n")
                            with open(f"{self.basic_path_ram}/status.log", "a") as status_logi:
                                status_logi.write(f"------------------\n")
                                status_logi.write(f"{self.fp.data_i_godzina()}\n")
                                status_logi.write(f"{self.wylicz_status_platform()}\n")
                        else:
                            self.fp.drukuj("nie udalo się wyslac i poprawnie zapisać pomiarow - wysylac będę probowal ponownie w kolejnej iteracji")
                            with open(f"{self.basic_path_ram}/status.log", "a") as status_logi:
                                status_logi.write(f"------------------\n")
                                status_logi.write(f"{self.fp.data_i_godzina()}\n")
                                status_logi.write(f"{self.wylicz_status_platform()}\n")
                        
                        if os.path.exists(scieszka+"/"+plik):
                            os.remove(scieszka+"/"+plik)
                else:
                    ############ DO ZROBIENIA TUTAJ - STATUS KTORY W CZASIE DZIALANIA PROGRAMU ma problemy
                    self.fp.drukuj("brak posortowanych pomiarow - wysylam san naglowek wiadomosci")
                    self.flaga_pierwszej_wysylki=False
                    self.flaga_brak_danych_z_nadajnikow = True
                    self.status=self.wylicz_status_platform()
                    json_data = {
                        "wersja_json": self.wersja_json,
                        #po uzgodnieniu z tomkiem sn_rpi --> sn_platformy
                        "sn_platform": self.mac_address_platform,#self.sn_platform,
                        "mac_address_platform": self.mac_address_platform,
                        #nie potrzebne#"sn_device_mother": self.mother_serial_number,
                        "status_platform": self.status,
                        "zasieg_platform_wifi": self.zasieg_platform_wifi,
                        "bateria_platform": self.napiecie_baterii_platform,
                        "local_ipv4": self.local_ipv4,
                        "timezone": self.get_diff(datetime.now(), "Europe/Warsaw"),
                        "data": []
                    }
                    json_object = json.dumps(json_data, indent = 4)
                    slownik_response=self.wyslanie_obiektu_json_z_danymi(json_data)
                    path_to_json_wysylki_txt=f"{self.basic_path_project}/json_do_wysylki.txt"
                    self.fp.drukuj(f"path_to_json_wysylki_txt: {path_to_json_wysylki_txt}")
                    with open(f"{path_to_json_wysylki_txt}", "a+") as outfile:
                        outfile.write("----------------------------")
                        outfile.write(str(self.fp.data_i_godzina()))
                        outfile.write("\n"+json_object) 
                        #drukuj(json_object)
                    with open(f"{self.basic_path_ram}/status.log", "a") as status_logi:
                        status_logi.write(f"------------------\n")
                        status_logi.write(f"{self.fp.data_i_godzina()}\n")
                        status_logi.write(f"{self.wylicz_status_platform()}\n")
            else:
                ############ DO ZROBIENIA TUTAJ - STATUS KTORY W CZASIE DZIALANIA PROGRAMU ma problemy
                self.fp.drukuj("wydaje sie to pierwsza wysylka po włączenie platforma")
                self.fp.drukuj("\nbrak plikow do wyslania")
                self.flaga_pierwszej_wysylki = True
                self.flaga_brak_danych_z_nadajnikow = True
                self.status=self.wylicz_status_platform()
                json_data = {
                    "wersja_json": self.wersja_json,
                    #po uzgodnieniu z tomkiem sn_rpi --> sn_platformy
                    "sn_platform": self.mac_address_platform,#self.sn_platform,
                    "mac_address_platform": self.mac_address_platform,
                    #nie potrzebne#"sn_device_mother": self.mother_serial_number,
                    "status_platform": self.status,
                    "zasieg_platform_wifi": self.zasieg_platform_wifi,
                    "bateria_platform": self.napiecie_baterii_platform,
                    "local_ipv4": self.local_ipv4,
                    "timezone": self.get_diff(datetime.now(), "Europe/Warsaw"),
                    "data": []
                }
                json_object = json.dumps(json_data, indent = 4)
                slownik_response = self.wyslanie_obiektu_json_z_danymi(json_data)
                path_to_json_wysylki_txt=f"{self.basic_path_project}/json_do_wysylki.txt"
                self.fp.drukuj(f"path_to_json_wysylki_txt: {path_to_json_wysylki_txt}")
                with open(f"{path_to_json_wysylki_txt}", "a+") as outfile:
                    outfile.write("----------------------------")
                    outfile.write(str(self.fp.data_i_godzina()))
                    outfile.write("\n"+json_object) 
                    #drukuj(json_object)
                with open(f"{self.basic_path_ram}/status.log", "a") as status_logi:
                    status_logi.write(f"------------------\n")
                    status_logi.write(f"{self.fp.data_i_godzina()}\n")
                    status_logi.write(f"{self.wylicz_status_platform()}\n")
        except Exception as e:
            self.fp.drukuj("przy zmiennych został wyłapany bląd "+str(e))
            traceback.print_exc()

def main():
    fp=FunkcjePomocnicze(nazwa_programu())
    basic_path_ram=""
    flara_skryptu=""
    try:
        fp.drukuj(f"------{nazwa_programu()}--------")
        if os.name == "posix":
            fp.drukuj("posix")
            dotenv_path = "../env_programu"
            fp.file_istnienie(dotenv_path, "sprawdz czy plik .env istnieje")
            load_dotenv(dotenv_path)
            basic_path_ram=fp.zmienna_env_folder('basic_path_ram', "env_programu - sprawdz basic_path_ram")

            flara_skryptu=f"{basic_path_ram}/{nazwa_programu()}.flara"
            with open(flara_skryptu, "w") as file:
                file.write(f"{str(os.getpid())}")
            file.close()
            inicjalna=False
            klasawysylka=KlasaWysylka(inicjalna)
        else:
            raise ExceptionWindows
            drukuj("notposix - pewnie windows - wez to czlowieku oprogramuj")
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
