#!/bin/bash
flara_skryptu="/run/user/1000/skrypt_rtl_433.sh.txt"
touch $flara_skryptu #flara skryptu
MAXSIZE=4
timedatectl | grep "Local time"
echo "skrypt_rtl_433.sh"
FILE="/run/user/1000/pomiary.txt"
#if [ -f $FILE ]; then #czy istnieje taki plik sprawdza
#    FILESIZE=$(stat -c%s "$FILE")
#    if (( $FILESIZE < $MAXSIZE )); then #czy ten plik jest pusty
#        rm $FILE
#    else
#        echo "file $FILE nadal istnieje i nie jest pusty"
#    fi
#fi
#if [ -f $FILE ]; then
#    echo ""
#else
echo "rozpoczynam nasluch"
timeout 55 rtl_433 -s 2.5e6 -f 868.5e6 -H 30 -R 75 -R 150 -F json > $FILE 2>"/home/klraspi/skrypty_klraspi/problemy_rtl_433.log"
FILESIZE=$(ls -lh $FILE | awk '{print  $5}')
echo "FILESIZE: $FILESIZE"
echo "MAXSIZE: $MAXSIZE"
if [ "$FILESIZE" != "0" ]; then #czy ten plik jest pusty
  cp /run/user/1000/pomiary.txt /run/user/1000/pomiary.txt.old
  echo "kopiuje"
else
  echo "nie kopiuje - jest rowne zero"
  cat /run/user/1000/pomiary.txt > /run/user/1000/brak_danych.txt
  timedatectl | grep "Local time" >> /run/user/1000/brak_danych.txt
fi
echo "rozlaczam sie"
if [ -f $flara_skryptu ]; then
  echo "usuwam flare"
  rm $flara_skryptu
fi
