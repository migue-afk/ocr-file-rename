This repository can be used to perform OCR recognition and rename documents based on content, for example, name_date.pdf, and it also determines the hash values of each file to ensure its integrity. 
This tool is intended for use on Linux systems only.



### Step 1. Create Python Virtual Environment

Create virtual environment, access and install requirements
```bash
$ pyhton3 -m venv .env
$ source .env/bin/activate
(.env) $ pip install -r requirements.txt
```

### Step 2. Scan file OCR and order
Place the scanned file into ./original directory, run ./renamefile-OCR.sh to perform OCR recognition, the script sequence will rename the original file from examplescanpdf.pdf to 0001.pdf, 000x.pdf, the new filewill be saved in ./archive.
### Step 3. Rename file
- Execute "python renamefile.py" for extract type and date for rename the file type_date.pdf.
- Execute "python renamefile_spacy.py" for extract type, name and date for rename the file type_name_date.pdf.

