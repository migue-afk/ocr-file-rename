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

function ctrl_c () {
        echo -e "${yellowColour}\n[!]${endColour} ${redColour}Ended process\n${endColour} "
        exit 1
}
trap ctrl_c INT

#----------------------------------------------------------------------------
# Directory Created
CONSUME="./report/consume"
DIRECTORYSEP="./pdfseparate"
DIRECTORYPNG="./pdftopng"
DIRECTORYORG="./.original"
DIRECTDUPLI="./.original/duplicate"
DIRECTUNIFY="./unify"
DIRARCHIVE="./archive"
COPYARCHIVE="./report/archivo"

#----------------------------------------------------------------------------
# Define global variables
PAG_SEP=()

#----------------------------------------------------------------------------
#find consume/ -type f -exec touch {} \; # --> command for relaunch "alert" in consume dicrectory
#----------------------------------------------------------------------------
# Clean Directories
echo "Clean Separate and PNG directory"
rm "$DIRECTORYSEP"/*
rm "$DIRECTORYPNG"/*

#----------------------------------------------------------------------------
# Event trigger
wait_until_stable() {
    local file="$1"
    local oldsize=-1
    local newsize=$(stat -c%s "$file" 2>/dev/null || echo 0)
    while [ "$newsize" -ne "$oldsize" ]; do
    echo "wait for '$file'"
        oldsize=$newsize
        sleep 0.2
        newsize=$(stat -c%s "$file" 2>/dev/null || echo 0)
    done
}

#----------------------------------------------------------------------------
# Enable inotify for consume directory
#-e moved_to -e moved_from
inotifywait -m -e close_write -e moved_to --format "%w %e %f" "$CONSUME" | while read dir action filepdf; do
existfile=0 # Variable for detect duplicated files
#%w print directory
#%e print action or event
#%f print file name
sleep 1  # one second to wait for evate the race condition
echo "[$(date '+%H:%M:%S')] Start Monitoring"
path="$dir$filepdf"
#path="${dir%/}/$filepdf"
wait_until_stable "$path"
echo "[$(date '+%H:%M:%S')] File OK: $path"

#----------------------------------------------------------------------------
# Calc hashes for comparate files duplicated
hashcomp=$(md5sum "$path" | awk '{print $1}')
echo "Hash MD5 '$hashcomp'"

for fileor in "$DIRECTORYORG"/*; do
    [ -f "$fileor" ] || continue
    hashor=$(md5sum "$fileor" | awk '{print $1}')
    if [ "$hashcomp" == "$hashor" ]; then
        echo "Exist File"
        existfile=1
    fi
done

if [ $existfile -eq 1 ]; then
    mv "$path" "$DIRECTDUPLI"
    continue
fi

#----------------------------------------------------------------------------
# Number pages of file
NUM_PAGE=$(qpdf --show-npages "$path")
echo "Number Pages '$NUM_PAGE'"
basename_file=$(basename "$path" .pdf)

# Split pages in #N pdf files
#for i in $(seq 1 $NUM_PAGE);do
#    qpdf "$path" --pages . $i -- "${DIRECTORYSEP}/${basename_file}-$i.pdf"
#done

define=0
i=1

# Loop for detect QR code
while [ $i -le $NUM_PAGE ]; do
    # Convert page "i" to PNG
    magick -density 300 "$path"[$((i-1))] "$DIRECTORYPNG/${basename_file}-$i.png"

    # Detect QR code
    if zbarimg "$DIRECTORYPNG/${basename_file}-$i.png" 2>/dev/null | grep -q "stopscan123456V9"; then
        PAG_SEP+=($i)
        define=1
        echo "[+] Find QRcode in: '$DIRECTORYPNG/${basename_file}-$i.png'"

        if [ ${#PAG_SEP[@]} -eq 4 ]; then
            echo "Total QR Code finished"
            define=0
            echo "Separated in: ${PAG_SEP[@]}"

            # Process page ranges into separated
            for (( j=0; j < ${#PAG_SEP[@]}-2; j+=2 )); do
                START_PAG=$(( PAG_SEP[j] + 2 ))
                END_PAG=$(( PAG_SEP[j+2] - 1 ))
                echo "START $START_PAG"
                echo "END $END_PAG"

                # Save segmented PDF
                qpdf "$path" --pages . $START_PAG-$END_PAG -- "$DIRECTUNIFY/${basename_file}-segment-$((i+1)).pdf"
            done
            echo "define PAG_SEP to ZERO"
            PAG_SEP=()
        fi

    else
        # If define=0, unit normal pages
        if [ $define -eq 0 ]; then
            qpdf "$path" --pages . $i-$((i + 1)) -- "$DIRECTUNIFY/${basename_file}-$i.pdf"
            (( i += 1))
        fi
    fi
    # Increment i (ever)
    ((i += 1))
done

#----------------------------------------------------------------------------
# Cleaned varibles and directories
echo "Clean PAG_SEP"
PAG_SEP=()

echo "Cleaned separate"
rm "$DIRECTORYSEP"/*

echo "Cleaned PDFtoPNG directory"
rm "$DIRECTORYPNG"/*


#----------------------------------------------------------------------------
# Init process to OCR
echo "INIT PROCESS OCR"
./renamefile-OCR.sh

#----------------------------------------------------------------------------
# Init process to rename file
echo "Rename file to PDF"
python renamefile_spacy.py

#----------------------------------------------------------------------------
# Cleaned directory used for inotify "consume"
echo "File in consume 'DELETE'"
mv "$path" "$DIRECTORYORG"

#----------------------------------------------------------------------------
# Calculated HASH and save in CSV
./calhash.sh

#----------------------------------------------------------------------------
# Move all files of archive to report/archivo
echo "Move files to /report/archivo"
DIR_NAME="batch_$(date +'%Y%m%d_%H%M%S')"
rsync -av --backup --suffix='.bak' "$DIRARCHIVE/" "$COPYARCHIVE/$DIR_NAME/"

#----------------------------------------------------------------------------
echo "Cleaned directory archive and unify"
rm "$DIRARCHIVE"/*
rm "$DIRECTUNIFY"/*

#----------------------------------------------------------------------------
# Ended process
figlet -f "smslant" "Wait files"
done #done --> inotifywait

