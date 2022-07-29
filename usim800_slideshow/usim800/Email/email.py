#!/usr/bin/python3
# - *- coding: utf-8 - *-

from usim800_slideshow.usim800.Communicate_slideshow import communicate_slideshow
import traceback

from datetime import datetime
def nazwa_programu():
    return "email.py"

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


#Do przeorania
class email(communicate_slideshow):
    def __init__(self, *args, **kwargs):
        drukuj("email __init__")
        super().__init__(*args, **kwargs)
    
    def init(self, *args, **kwargs):
        drukuj("email init")
        super().__init__(*args, **kwargs)

    def send(self, number, sms):
        cmd = "AT"
        self._send_cmd(cmd, return_data=True, t=1)
        cmd = "AT+CMGF=1"
        # Sets the GSM Module in Text Mode
        self._send_cmd(cmd, return_data=True, t=1)
        cmd = 'AT+CMGS="{}"'.format(number)
        self._send_cmd(cmd)
        SMS = sms
        self._send_cmd(SMS,t=0.5)
        cmd = "\x1A"
        self._send_cmd(cmd,t=0.1)
        cmd = "AT+SAPBR=0,1"
        data = self._send_cmd(cmd,return_data=True,t=0.5)
        try:
            stats = (data.decode().split()[-1])
            if "OK" in stats:
                stats = True
        except:
            stats = False
        return stats

    def readAll(self,index=None):
        cmd = "AT"
        self._send_cmd(cmd)
        cmd = "AT+CMGF=1"
        # Sets the GSM Module in Text Mode
        self._send_cmd(cmd)
        cmd = 'AT+CMGL="ALL"'
        # Sets the GSM Module in Text Mode
        self._send_cmd(cmd,read=False)
        data = self._readtill("OK")
        print(data)