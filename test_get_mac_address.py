import uuid
from datetime import datetime
import sys
import traceback
import fcntl, socket, struct
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

#Podejśćie pierwsze - błędne https://stackoverflow.com/questions/159137/getting-mac-address
# w komentarzch tłumaczą że jśli libka nie da rady znaleźć numeru mac address - to zwraca
##def main():
##    mac_address_int = uuid.getnode()
##    print(mac_address_int)
##    mac_address_hex = hex(mac_address_int)
##    print(mac_address_hex)
##    mac_address_hex_bez_zeroiks=str(mac_address_hex).split("x")[1]
##    print(f"MAC address: {mac_address_hex_bez_zeroiks}")

#https://stackoverflow.com/questions/159137/getting-mac-address

def main2():
    nics = psutil.net_if_addrs()['enp1s0']
    for interface in nics:
        if interface.family == 17:
            print(interface.address)

if __name__ == "__main__":
    #main()
    main2()