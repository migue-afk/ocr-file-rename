#!/bin/bash
#Colours
greenColour="\e[0;32m\033[1m"
endColour="\033[0m\e[0m"
redColour="\e[0;31m\033[1m"
blueColour="\e[0;34m\033[1m"
yellowColour="\e[0;33m\033[1m"
purpleColour="\e[0;35m\033[1m"
turquoiseColour="\e[0;36m\033[1m"
grayColour="\e[0;37m\033[1m"

function ctrl_c (){
        echo -e "${yellowColour}\n[!]${endColour} ${redColour}Ended process\n${endColour} "
        exit 1
}
trap ctrl_c INT

#------------------------------------------------------------------------------------------

DIRECTORY="./archive"
DIRECTORYORG="./original"

if [[ ! -d "$DIRECTORYORG" ]];then
        echo "[-] Error: The directory '$DIRECTORYORG' does not exist or is not a directory"
        echo "[-] Try again"
        exit 1
else
        if [ ! -n "$(ls -A $DIRECTORYORG)" ];then
                echo "The directory '$DIRECTORYORG' is empty"
                exit 1
        fi
fi

