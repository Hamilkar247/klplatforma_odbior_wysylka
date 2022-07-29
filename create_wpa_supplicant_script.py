#!/usr/bin/python3
# - *- coding: utf-8 - *-
import sys 

def create_wpa_supplicant(uzupelnienie):
    template_wpa_supplicant_conf="""country=PL
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

{uzupelnienie}

network={{
    ssid="czujniki"
    scan_ssid=1
    psk="czujniki"
    priority=1
}}
    """.format(uzupelnienie=uzupelnienie)
    print(template_wpa_supplicant_conf)


def dane_sieci(ssid, psk=""):
    #print("dane_sieci"+ssid+" "+psk)
    if psk != "":
        uzupelnienie="""network={{
    ssid="{ssid}"
    psk="{psk}"
    priority=2
    scan_ssid=1
}}
""".format(ssid=ssid, psk=psk)
    else:
        uzupelnienie = """network={{
    ssid="{ssid}"
    key_mgmt=NONE
    priority=2
    scan_ssid=1
}}""".format(ssid=ssid)
    create_wpa_supplicant(uzupelnienie)

if __name__ == "__main__":
    #print("echxd")
    #create_wpa_supplicant("uzupelnienie")
    if len (sys.argv ) > 1:# and len (sys.argv < 3):
        ssid = str(sys.argv[1])
        if str(sys.argv[2]) == "hasla_brak":
            psk = ""
        else:
            psk = str(sys.argv[2])
    else:
        print("nie podano nazwy sieci")
        sys.exit()

    dane_sieci(ssid, psk)
