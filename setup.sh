#!/bin/bash

while :
do

clear

banner(){
echo

echo -e "\033[32m   ___ ___                 __      _________                      \033[0m"
echo -e "\033[32m  /   |   \  ____  _______/  |_   /   _____/ ____ _____    ____   \033[0m"
echo -e "\033[32m /    ~    \/  _ \/  ___/\   __\  \_____  \_/ ___\__   \  /    \  \033[0m"
echo -e "\033[32m \    Y    (  <_> )___ \  |  |    /        \  \___ / __ \|   |  \ \033[0m"
echo -e "\033[32m  \___|_  / \____/____  > |__|   /_______  /\___  >____  /___|  / \033[0m"
echo -e "\033[32m        \/            \/                 \/     \/     \/     \/  \033[0m"

}

banner

int_handler (){
    clear
    echo
    echo -e "\033[1m [+] Adios \033[0m"
    kill $PPID
    exit 1
}

trap 'int_handler' INT

   echo
   echo -e "   \033[1m [1] Instalar en Kali Linux y Parrot OS \033[0m"
   echo -e "   \033[1m [2] Instalar en Termux \033[0m"
   echo -e "   \033[1m [3] Salir \033[0m"
   echo

   read -p $'\033[1m [+] Seleccione una opción: \033[0m' opcion

   case $opcion in

           1) echo
           sudo apt-get update && sudo apt install -y python3-pip xclip lolcat figlet && python3 -m pip install --upgrade colorama;;

           2) echo
           apt-get update
           pip install xclip 
           pip install lolcat 
           pip install figlet
           pip install colorama
           sleep 1.5;;

           3) echo
           clear
           echo -e "\033[1m [+] Adios\033[0m"
           exit;;

esac

done