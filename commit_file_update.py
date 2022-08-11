# - *- coding: utf-8 - *-

import os
import sys
import traceback
from datetime import datetime
import json
import requests
import urllib
from funkcje_pomocnicze import FunkcjePomocnicze, ExceptionEnvProjektu, ExceptionNotExistFolder, ExceptionWindows

############################

def nazwa_programu():
    return "commit_file_update.py"

def funkcje_pomocnicze_inicjalizacja():
    fp=FunkcjePomocnicze(nazwa_programu())
    return fp

#############################

class CommitFileUpdate():

    def __init__(self):
        self.fp=funkcje_pomocnicze_inicjalizacja()

    def aktualizacja_na_outsystem_wersji_programu(self, value):
        link="https://personal-5ndvfcym.outsystemscloud.com/KlimaLog_core/rest/V1/ProgramSettingsPost"
        #shutil.copy2(self.path_plik_z_krotkami_do_wysylki_file, self.path_plik_z_krotkami_do_wysylki_file+".work")
        #print(json_object)
        dict_zwracany={"status_code":"0", "sukces_zapisu":"False", "error_text":"brak"}
        nazwa_settingu="obecna_wersja_czasowa_oprogramowania_na_produkcji"
        data_settingu={
          "Name": nazwa_settingu,
          "Value": value
        }
        tab_settings=[data_settingu]
        #kusy_json=json.dumps(tab_kusy)
        self.fp.drukuj(tab_settings)
        try:
            docelowy_url_dla_post=link
            response = requests.post(
                docelowy_url_dla_post,
                json=tab_settings,
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

def main():
    fp=FunkcjePomocnicze(nazwa_programu())
    data_wersji=fp.data_i_godzina()
    a=open("commit.txt", "w")
    a.write(data_wersji)
    a.close()
    cfu=CommitFileUpdate()
    cfu.aktualizacja_na_outsystem_wersji_programu(data_wersji)

if __name__ == "__main__":
    main()