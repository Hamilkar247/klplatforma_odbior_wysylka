#!/bin/bash
timedatectl | grep "Local time"
echo "ubijanie_rtl_433.sh"
FILE="/home/klraspi/skrypty_klraspi/problemy_rtl_433.log"
if [ -f "$FILE" ]; then
  echo "plik problemy_rtl_433.log istnieje"
  numb_pid=$(pidof rtl_433)
  echo "numer procesu pid to: $var"
  #kill -9 $var
  numb_error=$(tail $FILE -n 15 | grep -o "LIBUSB_ERROR_NOT_FOUND" | wc -l)
  if (( $numb_error > 0 )); then
    kill -9 $numb_pid
    /home/klraspi/skrypty_klraspi/reset_portu_usb.py
    rm $FILE/run/user/1000/problemy_rtl_433.log
    echo "ubilem zapetlony problem"
  else
    numb_error=$(tail $FILE -n 15 | grep -o "usb_claim_interface error -6" | wc -l)
    if (( $numb_error > 0)); then
      echo "usb_claim_interface error -6 wystapilo: $numb_error"
      /home/klraspi/skrypty_klraspi/reset_portu_usb.py
    #rm /run/user/1000/problemy_rtl_433.log
    fi
    #timedatectl | grep "Local time" >> /home/klraspi/skrypty_klraspi/reboot.log
    #sudo reboot
  fi 
fi
echo "koniec ubijanie_rtl_433.sh"
