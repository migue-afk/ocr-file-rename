This repository can be used to rename documents en masse from GNU/Linux, and can also determine the hash values ​​of each file to ensure its integrity.
### Step 1. Scan file OCR and order
Place the scanned file in the ./original directory, run ./renamefile-OCR.sh to perform OCR recognition, and rename the file from examplescanpdf.pdf to 0001.pdf, 000x.pdf.
### Step 2. Rename file
Execute "python renamefile.py" for extract type and date for rename the file type_date.pdf.
Execute "python renamefile_spacy.py" for extract type, name and date for rename the file type_name_date.pdf.

