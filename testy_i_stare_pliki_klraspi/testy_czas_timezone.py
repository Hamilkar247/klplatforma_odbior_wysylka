# - *- coding: utf-8 - *-

from datetime import datetime
import traceback
import sys
from datetime import datetime
from pytz import timezone

def nazwa_programu():
    return "zasieg_wifi_test.py"

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

def get_diff(now, tzname):
    #print(now.hour)
    tz = timezone(tzname)
    utc = timezone('UTC')
    utc.localize(datetime.now())
    delta =  utc.localize(now) - tz.localize(now)
    print(delta)
    print(str(delta).split(":")[0])
    #delta_hour =  utc.localize(now).hour - tz.localize(now).hour
    #print(delta_hour)
    przerwij_i_wyswietl_czas()
    return delta

def main():
    now = datetime.utcnow()
    print(now)
    tzname = 'Europe/Warsaw'
    delta = get_diff(now, tzname)
    print(delta)
    #now_in_stockholm = now + delta
    #drukuj(now_in_stockholm)

if __name__ == "__main__":
    main()