import re
import ftfy
import unicodedata
import os
import dateparser
from spellchecker import SpellChecker
from pathlib import Path
from PyPDF2 import PdfReader
from natsort import natsorted
import ollama

MODEL_NAME = 'llama3.1:8b'
inputpdf = Path("archive")
renamedest = Path("./archive")
renamedest.mkdir(exist_ok=True)

def pdftotext(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        raw = " "
        for page in reader.pages:
            raw += page.extract_text() + "\n"
        return raw
    except Exception as excep:
        print(f"Error read {pdf_path.name}: {excep}")
    return ""

def clean_ocr_text(text):
    text = ftfy.fix_text(text)
    text = re.sub(r'-\s*\n\s*', '', text)
    text = re.sub(r'\n+', ' ', text)
    text = unicodedata.normalize('NFC', text)
    text = re.sub(r'[^\x09\x0A\x0D\x20-\x7EÁÉÍÓÚ;ÜÑáéíóúüñ¿¡]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_date(raw2):
    date_pattern = re.findall(
        r'(\d{1,2}\s+de\s+\w+\s+\d{4}'
        r'|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}'
        r'|\d{4}-\d{2}-\d{2}'
        r'|[A-Za-z]+\s+\d{1,2},\s+\d{4}'
        r'|\d{1,2}\s+[A-Za-z]+\s+\d{4})',
        raw2,
        flags=re.IGNORECASE
    )
    if not date_pattern:
        raw2 = 'datenotfound2'
        return raw2
    for date_str in date_pattern:
        date_obj = dateparser.parse(date_str)
        if date_obj:
            raw2 = date_obj.strftime('%d-%m-%Y')
            break
        else:
            raw2 = 'datenotfound'
    return raw2

def safe_filename(name):
    name = name.replace(" ","_")
    name = re.sub(r'[<>:"\\/|?*]','_',name)
    name = re.sub(r'_+','_', name)
    name = re.sub(r"(\d{2})_(\d{2})_(\d{2})", r"\1-\2-\3", name)
    return name

def type_document(raw3):
    # Insert all type document; for example: BILL
    raw3 = raw3.upper()
    if "BILL" in raw3:
        return "BILL"
    elif "TICKET" in raw3:
        return "TICKET"
    elif "CERTIFICATE" in raw3:
        return "CERTIFICATE"
    else:
        return "notfound"

def ollama_document(raw4):
    if not raw4.strip():
        return "Error: empy text"

    try:
        prompt = f"""Task: Extract 1 first and last name from the TEXT

You are given OCR text from a document. Extract the name and last name (ignore companies).
OUTPUT RULES:
- Return ONLY ONE LINE, IN UPPERCASE, with FIRST and LAST NAME (max 4 words).
- If no personal name is present, return: UNKNOWN
- No explanations. No extra characters.


TEXT:
{raw4}
"""
        response = ollama.chat(
                model = MODEL_NAME,
                messages = [{'role': 'user', 'content': prompt}]
                )
        return response['message']['content']
    except Exception as e:
        #return f"Error in the model: {str(e)}"
        return f"Error in the model"

if __name__ == '__main__':

    for pdf_file in natsorted(inputpdf.glob("*.pdf")):
        raw1 = pdftotext(pdf_file)
        if not raw1:
            continue
        clean_text = clean_ocr_text(raw1) 
        date_text = extract_date(clean_text)
        type_doc = type_document(clean_text)
        name_doc = ollama_document(clean_text)
        renamed_file = safe_filename (f"{type_doc} {name_doc} {date_text}.pdf")
        print (clean_text)
        print (date_text)
        print (type_doc)
        print (name_doc)
        print (renamed_file)
        print ('############################')
        destination = renamedest / renamed_file
        os.rename(pdf_file,destination)




















