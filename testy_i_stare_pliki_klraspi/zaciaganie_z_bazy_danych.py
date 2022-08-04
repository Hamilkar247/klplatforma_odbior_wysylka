#!/usr/bin/python3
# - *- coding: utf-8 - *-

import sqlite3
from sqlite3 import Error
import math
import time
import datetime
import sys
import traceback
import os

def nazwa_programu():
    return "zaciaganie_z_bazy_danych.py"

def data_i_godzina():
    teraz = datetime.datetime.now()
    current_time = teraz.strftime("%d/%m/%y %H:%M:%S")
    return current_time

def drukuj(obiekt_do_wydruku):
    try:
        print(data_i_godzina()+" "+nazwa_programu()+" "+str(obiekt_do_wydruku))
    except Exception as e:
        print(e)
        print(traceback.print_exc())

def przerwij_i_wyswietl_czas():
    czas_teraz = datetime.datetime.now()
    current_time = czas_teraz.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    sys.exit()

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_all_tables(conn):
    """Zwraca liste tablic w bazie danych"""
    cur = conn.cursor()

    #table_list = list()
    cur.execute("SELECT tbl_name FROM sqlite_master WHERE type='table';")
    #table_list.append(str(row[0]))
    rows = cur.fetchall()

    for row in rows:
        print(row)

#08/06/22 13:45:00
def unixTime_toHumanTime(unixtime):
    date_for_human=datetime.datetime.fromtimestamp(unixtime).strftime('%d/%m/%y %H:%M:%S')
    return date_for_human

def zasieg_w_procentach(zasieg_w_procentach):
    range=None
    if zasieg_w_procentach is not None:
        range=str(math.floor(zasieg_w_procentach))
    return range

def fahr_to_celsius(degree_fahrenheit):
    cels=None
    if degree_fahrenheit is not None:
        cels="{:.1f}".format(round((int(degree_fahrenheit)-32)*(5/9), 1))
    return cels

def humidity_transfer(humidity):
    hum=None
    if humidity is not None:
        hum="{:}".format(round(humidity))
    return hum

def bateria_status(battery):
    status_baterii=None
    if battery is not None:
        status_baterii="{:}".format(round(battery))
    return status_baterii

def interval_time(interval):
    return str(interval)

#podaj poczatek i koniec jako string w formacie - dzien miesiac rok - #08/06/22 13:45:00
def select_dateTime(conn, poczatek):
    #drukuj(poczatek)
    try:
        drukuj(poczatek)
        poczatek=time.mktime(datetime.datetime.strptime(str(poczatek), "%d/%m/%y %H:%M:%S").timetuple())
        #koniec=time.mktime(datetime.datetime.strptime(koniec, "%d/%m/%y %H:%M:%S").timetuple()) 
        cur = conn.cursor()
        sql_query="""
SELECT dateTime, interval, rxCheckPercent,
temp0, temp1, temp2, temp3, temp4, 
temp5, temp6, temp7, temp8,
humidity0, humidity1, humidity2, humidity3, humidity4, 
humidity5, humidity6, humidity7, humidity8,
batteryStatus0, batteryStatus1, batteryStatus2, batteryStatus3, batteryStatus4, 
batteryStatus5, batteryStatus6, batteryStatus7, batteryStatus8
FROM archive
WHERE dateTime > {}
LIMIT {};
""".format(str(poczatek), str(100000))
        cur.execute(sql_query)
        rekordy=cur.fetchall()
        file_line_records=open("/home/weewx/wk_skrypty/plik_z_krotkami.txt", "a")
        lista_rekordow=[]
        #logi
        logi_krotek_z_bazy_danej=open("/home/weewx/wk_skrypty/plik_z_krotkami_logi.json", "a")
        for rekord in rekordy:
            krotka=[]
            #czas
            krotka.append(unixTime_toHumanTime(rekord[0]))
            #interval pomiaru
            krotka.append(interval_time(rekord[1]))
            #zasieg - jest już domyslnie w procentach
            krotka.append(zasieg_w_procentach(rekord[2]))
            #temperatura
            krotka.append(fahr_to_celsius(rekord[3]))
            krotka.append(fahr_to_celsius(rekord[4]))
            krotka.append(fahr_to_celsius(rekord[5]))
            krotka.append(fahr_to_celsius(rekord[6]))
                                                     
            krotka.append(fahr_to_celsius(rekord[7]))
                                                     
            krotka.append(fahr_to_celsius(rekord[8]))
            krotka.append(fahr_to_celsius(rekord[9]))
            krotka.append(fahr_to_celsius(rekord[10]))
            krotka.append(fahr_to_celsius(rekord[11]))
            #wilgotnosc                                
            krotka.append(humidity_transfer(rekord[12]))
            krotka.append(humidity_transfer(rekord[13]))
            krotka.append(humidity_transfer(rekord[14]))
            krotka.append(humidity_transfer(rekord[15]))
                                                    
            krotka.append(humidity_transfer(rekord[16]))
                                                       
            krotka.append(humidity_transfer(rekord[17]))
            krotka.append(humidity_transfer(rekord[18]))
            krotka.append(humidity_transfer(rekord[19]))
            krotka.append(humidity_transfer(rekord[20]))
            #baterie
            krotka.append(bateria_status(rekord[21]))
            krotka.append(bateria_status(rekord[22]))
            krotka.append(bateria_status(rekord[23]))
            krotka.append(bateria_status(rekord[24]))

            krotka.append(bateria_status(rekord[25]))
            
            krotka.append(bateria_status(rekord[26]))
            krotka.append(bateria_status(rekord[27]))
            krotka.append(bateria_status(rekord[28]))
            krotka.append(bateria_status(rekord[29]))
            
            lista_rekordow.append(krotka)
        drukuj(f"liczba wciągnietych rekordów: {len(lista_rekordow)}")
        liczba_iteracji=0
        flaga_zmiany_daty_ostatniego_pomiaru=False
        while True:
            if os.path.exists(r"/tmp/krotki_z_danymi_delete.txt") == False:
                file = open(r"/tmp/krotki_z_danymi_add.txt", "w")
                file.write("trwa dzialanie na krotkach")
                #logi
                if len(lista_rekordow) > 0:
                    logi_krotek_z_bazy_danej.write(f"data wpisywania krotek {data_i_godzina()}\n")
                for krotka in lista_rekordow:
                    for wartosc in krotka:
                        file_line_records.write(str(wartosc)+";")
                        #logi
                        logi_krotek_z_bazy_danej.write((str(wartosc)+";"))
                    file_line_records.write("\n")
                    #logi
                    logi_krotek_z_bazy_danej.write("\n")
                # PO TESTACH I NA PRODUKCJI ODKOMENTUJ!
                if len(lista_rekordow) > 0:
                     drukuj(f"ostatni rekord to {lista_rekordow[-1][0]}")
                #    flaga_zmiany_daty_ostatniego_pomiaru=True
                #    with open("/home/weewx/wk_skrypty/czas_ostatniego_pomiaru.txt", "w") as plik_z_czasem_ostatniego_pomiaru:
                #       plik_z_czasem_ostatniego_pomiaru.write(str(lista_rekordow[-1][0]))
                #    drukuj(f"zaktualizowano datę pomiaru na {lista_rekordow[-1][0]}")
                else:
                    drukuj("nie pobrano żadnych krotek danych")
                os.remove(r"/tmp/krotki_z_danymi_add.txt")
                break
            else:
                liczba_iteracji=liczba_iteracji+1
                time.sleep(10)
                if liczba_iteracji == 10:
                    print("proces miał problem wstrzelić się z modyfikacją pliku - koncze dzialanie procesu")
                    print("kolejny proces będzie się zachowywał jak gdyby ten nie pobrał żadnych danych z bazy")
                    sys.exit()
    except ValueError as e:
        drukuj(f"{str(e)} PS: sprawdź czy ci jakiś znak biały się nie zaplatal")
        traceback.print_exc()
    except TypeError as e:
        drukuj(f"{str(e)}")
        traceback.print_exc()
    except AttributeError as e:
        drukuj("brakuje wartości dla zmiennej "+str(e))
        traceback.print_exc()
    except Exception as e:
        drukuj("przy zmiennych został wyłapany bląd "+str(e))
        traceback.print_exc()

#do testów
def dodanie_miesiaca_do_daty_poczatkowej(poczatek_string_data):
    date_time_object = datetime.datetime.strptime(poczatek_string_data, "%d/%m/%y %H:%M:%S")
    date_time_object = date_time_object + datetime.timedelta(days=30)
    koniec_string_data = date_time_object.strftime("%d/%m/%y %H:%M:%S")
    return koniec_string_data

def main(poczatek):
    database = r"/var/lib/weewx/weewx-kl.sdb"
    # połączenie do bazy danych create a database connection
    if poczatek is not None:
        conn = create_connection(database)
        with conn:
            select_dateTime(conn, poczatek)
    else:
        drukuj("brak podanego czasu")

def pobieranie_danych_od_poczatku():
    plik=open("czas_ostatniego_pomiaru.txt", "w")   
    plik.write("01/01/00 01:01:01")
    plik.close()
    plik=open("plik_z_krotkami.txt", "w")
    plik.write("")
    plik.close()

if __name__ == "__main__":
    pobierz_dane_od_poczatku=False
    if pobierz_dane_od_poczatku:
        pobieranie_danych_od_poczatku()
    poczatek=None
    drukuj("------------------")
    with open("/home/weewx/wk_skrypty/czas_ostatniego_pomiaru.txt", "r") as plik_z_czasem:
        poczatek=plik_z_czasem.readlines()[0].strip() 
    drukuj("poczatek:"+poczatek)
    main(poczatek)