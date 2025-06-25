This repository can be used to rename documents en masse from GNU/Linux, and can also determine the hash values ​​of each file to ensure its integrity.
### Step 1. Scan file OCR and order
Place the scanned file in the ./original directory, run ./renamefile.sh to perform OCR recognition, and rename the file from examplescanpdf.pdf to 0001.pdf, 000x.pdf.
### Step 2. Rename file
Execute "python renamefile-OCR.py" for extract name, type, date for rename the file name_type_date.pdf.
