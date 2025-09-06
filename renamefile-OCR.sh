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

#Cleaned .txt
echo " " > /tmp/hashfile.txt
echo " " > /tmp/hashfile2.txt
echo " " > original/hashes.txt

#------------------------------------------------------------------------------------------

DIRECTORY="./archive"		#Destination directory
DIRECTORYORG="./original"	#Insert files for OCR processing and file renaming

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

if [[ ! -d "$DIRECTORY" ]]; then
        echo "Error : The directory '$DIRECTORY' does not exist or is not a directory"
        echo "Creating the directory ---> Try again"
        mkdir archive
        exit 1
else
        if [ -n "$(ls -A $DIRECTORY)" ];then
                echo "Directory '$DIRECTORY' has content; possible overwrite"
                exit 1
        else
                echo "🔂 → Starting OCR"
		#Convert all files .jpg to .pdf
		p=20
		find "$DIRECTORYORG" -type f -name "*.jpg" -newer marcador.tmp | sort | while IFS= read -r filereadjpg; do
    		img2pdf "$filereadjpg" -o "$DIRECTORYORG/${p}.pdf"
		#echo "convert $filereadjpg"
    		p=$((p + 1))
		done
		# Init OCR and create hashes for all file
                find "$DIRECTORYORG" -type f -name "*.pdf" -newer marcador.tmp -exec ls -tr {} + | while read filereada; do
                echo "File Original $(md5sum $filereada)" >> /tmp/hashfile.txt
                namebase=$(basename $filereada .pdf)
                ocrmypdf -l spa --force-ocr --output-type pdfa --optimize 3 --deskew --rotate-pages --jobs 4 --tesseract-timeout=300 $filereada $DIRECTORY/$namebase.pdf
        done
        fi
fi

#Process substitution no subshell

while IFS= read -r fileread; do
        i=$((i+1))
        printf -v newname "%04d.pdf" "$i"
        destiny="$DIRECTORY/$newname"
        if [[ -e "$destiny" ]]; then
                echo "Error: destiny '$destiny' exist"
                exit 1
        fi

        mv -- "$fileread" "$destiny"

        echo "🟢 Rename: '$(basename "$fileread")' → '$(basename "$destiny")'"

done < <(find "$DIRECTORY" -maxdepth 1 -type f -name "*.pdf" -newer marcador.tmp -exec ls -tr {} +)

echo "Rename succefully. $(printf "%d" "$i")"

find "$DIRECTORY" -type f -name "*.pdf" -newer marcador.tmp -exec ls -tr {} + | while read filereada; do
	echo "→ File rename "$DIRECTORY"/$(basename "$filereada") $(date)" >> /tmp/hashfile2.txt
done

paste /tmp/hashfile.txt /tmp/hashfile2.txt > original/hashes.txt



