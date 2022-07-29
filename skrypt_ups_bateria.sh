#!/bin/bash
flara_skryptu="/run/user/1000/skrypt_ups_bateria.sh"
touch $flara_skryptu
timedatectl | grep "Local time"
echo "skrypt_ups_bateria.sh"
timeout 6 /home/klraspi/skrypty_klraspi/UPS_HAT_B/INA219.py
rm $flara_skryptu
