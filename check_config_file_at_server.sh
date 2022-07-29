#!/bin/bash

#Uwaga jq libka bez parametru -r zczytuje zmienne z json plików razem z ... cudzysłowiami
#https://github.com/stedolan/jq/issues/250

#function replace_wifi_wpa_applicant
# {
#  sleep 1
#  echo "replace_wifi_wpa_applicant"
#  wifi_nazwa_sieci="$(jq '.wifi_nazwa_sieci' config.json)"
#  wifi_haslo_sieci="$(jq '.wifi_haslo_sieci' config.json)"
#  echo "$wifi_nazwa_sieci"
#  echo "$wifi_haslo_sieci"
#}

function check_internet
{
  wget -q --tries=10 --timeout=20 --spider http://google.com
  if [[ $? -eq 0 ]]; then
          return "Online"
  else
          return "Offline"
  fi
}

function replace_wifi_wpa_applicant
{
  sleep 5
  echo "replace_wifi_wpa_applicant"
  wifi_nazwa_sieci="$(jq '.wifi_nazwa_sieci' config.json)"
  wifi_haslo_sieci="$(jq '.wifi_haslo_sieci' config.json)"
  if [ -z "$wifi_nazwa_sieci" ]
    then
      #python -c 'import createWpaSupplicantScript; createWpaSupplicantScript.dane_sieci(ssid='"$wifi_nazwa_sieci"', psk='"$")'
      echo "nazwa do wifi jest puste! Prawdopodobnie wystapil blad config.json"
      wifi_nazwa_sieci="$(jq '.wifi_nazwa_sieci' config.json.old)"
      wifi_haslo_sieci="$(jq '.wifi_haslo_sieci' config.json.old)"
  elif [ -z "$wifi_haslo_sieci" ]
    then
      echo "haslo do wifi jest puste! Prawdopodobnie wystąpił błąd config.json"
      wifi_nazwa_sieci="$(jq '.wifi_nazwa_sieci' config.json.old.)"
      wifi_haslo_sieci="$(jq '.wifi_haslo_sieci' config.json.old)"
  fi
  begin_folder="$(pwd)"
  #cd "/etc/wpa_supplicant/" || returns
  etc_wpa_supplicant="/etc/wpa_supplicant"
  if [ -f $etc_wpa_supplicant"/wpa_supplicant-wlan0.conf" ]
    then
      cat $etc_wpa_supplicant"/wpa_supplicant-wlan0.conf"
      echo "podmiana danych w pliku wpa_supplicant-wlan0.conf"
      #dla sprawdzenia czy sekcja "network w wpa_supplicant.conf nie znikła
      network_exist=$(cat $etc_wpa_supplicant"/wpa_supplicant-wlan0.conf" | grep -c "network={")
      if [ "$network_exist" -ne 1 ]; then
          if [ -f $etc_wpa_supplicant"/wpa_supplicant-wlan0.conf.bkp" ]; then
              cp $etc_wpa_supplicant"/wpa_supplicant-wlan0.conf.bkp" $etc_wpa_supplicant"/wpa_supplicant-wlan0.conf"
          fi
      fi
      cp $etc_wpa_supplicant"/wpa_supplicant-wlan0.conf" $etc_wpa_supplicant"/wpa_supplicant-wlan0.conf.bkp"
      pwd

      # z zmiennych usuwam zbedne cudzyslowia 
      python /home/weewx/wk_skrypty/create_wpa_supplicant_script.py ${wifi_nazwa_sieci:1:-1} ${wifi_haslo_sieci:1:-1} > $etc_wpa_supplicant"/wpa_supplicant-wlan0.conf" #$komenda_do_wykonania
      echo "po skrypcie create_wpa_supplicant_script.py"
      #komenda_do_wykonania="python -c 'import create_wpa_supplicant_script; create_wpa_supplicant_script.dane_sieci(ssid=$wifi_nazwa_sieci, psk=$wifi_haslo_sieci )' "
      #echo "$komenda_do_wykonania"
      #eval $komenda_do_wykonania > $etc_wpa_supplicant"/wpa_supplicant.conf"
      
      ##każe wziąć pod uwagę zmieniony plik wpa_supplicant.conf
      wpa_cli -i wlan0 reconfigure #w przyszłości pomyśleć nazwe interfejsu zaciągać z config.json
      ###po przedniej komendzie prawdopodobnie dhcpcd oszalał - dlatego ją uruchomiamy
      dhcpcd -d
      cat $etc_wpa_supplicant"/wpa_supplicant-wlan0.conf"
  else
    echo "nie istnienie pliku wpa_supplicant-wlan0.conf"
  fi
  #cd "$begin_folder" || returns
}

status_internet=check_internet
if [[ status_internet == "Offline" ]] 
  then
    curr_dirr=$(pwd)
    cd "/home/weewx/config"
    replace_wifi_wpa_applicant
    cd $curr_dirr
else
    echo "jest połączenie z internetem"
fi

