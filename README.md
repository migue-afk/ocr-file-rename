This repository can be used to perform OCR recognition and rename documents based on content, for example, name_date.pdf, and it also determines the hash values of each file to ensure its integrity. 
This tool is intended for use on Linux systems only.



### Step 1. Create Python Virtual Environment

Create virtual environment, access and install requirements
```bash
$ python3 -m venv .env
$ source .env/bin/activate
(.env) $ pip install -r requirements.txt
(.env) $ python -m spacy download en_core_web_sm
```

### Step 2. Scan file OCR and order
Place the scanned file into ./original directory, run ./renamefile-OCR.sh to perform OCR recognition, the script sequence will rename the original file from examplescanpdf.pdf to 0001.pdf, 000x.pdf, the new filewill be saved in ./archive.
### Step 3. Rename file
- Execute "python renamefile.py" for extract type and date for rename the file type_date.pdf.
- Execute "python renamefile_spacy.py" for extract type, name and date for rename the file type_name_date.pdf.
- Execute "python renamefile_ollama.py" for extarct type, name and date for rename the file type_name_date.pdf, using llama3.1:8b.

## Dockerfile

In directory execute `docker build`

```bash
sudo docker build -t ocr_rename .
```

After installation, `run` Docker to perform OCR recognition and set the identifier in the `archive` directory.

```bash
sudo docker run --rm -v "$(pwd)/original":/ocrapp/original -v "$(pwd)/archive":/ocrapp/archive ocr_rename renamefile-OCR.sh
```

Now we can execute other scripts for rename

```bash
sudo docker run --rm -v "$(pwd)/original":/ocrapp/original -v "$(pwd)/archive":/ocrapp/archive ocr_rename renamefile.py
```

```bash
sudo docker run --rm -v "$(pwd)/original":/ocrapp/original -v "$(pwd)/archive":/ocrapp/archive ocr_rename renamefile_spacy.py
```

```bash
sudo docker run --rm --network=host -v "$(pwd)/original":/ocrapp/original -v "$(pwd)/archive":/ocrapp/archive ocr_rename renamefile_ollama.py
```

For Docker Dessktop `network=host` does not work, use `ollama_host = "http://host.docker.internal:11434` in **renamefile_ollama.py**


Don't forget to install ollama and the llama3.1:8b model or another as a client on your host or remote client, in that case define the IP in ollama_host

**Run the container in the background with a shell**
```bash
sudo docker run -dit --name ocr_rename_con -v "$(pwd)/original":/ocrapp/original -v "$(pwd)/archive":/ocrapp/archive ocr_rename /bin/bash
```

**Enter the container**
```bash
sudo docker exec -it ocr_rename_con /bin/bash
```


