#!/bin/bash

COPYARCHIVE="./report/archivo"
DIRARCHIVE="./archive"

echo "Filename, SHA256" > $DIRARCHIVE/hashes.csv  # Head of file CSV

for file in $DIRARCHIVE/*.pdf; do
    # Calculate the hash SHA-256 of file
    hash=$(sha256sum "$file" | awk '{ print $1 }')
    # Added the name of file and hash to CSV
    echo "$file, $hash" >> $DIRARCHIVE/hashes.csv
done
