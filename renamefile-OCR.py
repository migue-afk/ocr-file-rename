import re
import ftfy
import unicodedata
import os
import dateparser
from spellchecker import SpellChecker
from pathlib import Path
from PyPDF2 import PdfReader
from natsort import natsorted

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
    # Buscar fechas en el texto
    date_pattern = re.findall(
        r'(\d{1,2}\s+de\s+\w+\s+\d{4}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})',
        raw2,
        flags=re.IGNORECASE
    )
    if not date_pattern:
        raw2 = 'datenotfound'
        return raw2
    for date_str in date_pattern:
        date_obj = dateparser.parse(date_str)
        if date_obj:
            raw2 = date_obj.strftime('%d-%m-%Y')
            break
        else:
            raw2 = 'datenotfound'
    return raw2


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
 
if __name__ == '__main__':

    for pdf_file in natsorted(inputpdf.glob("*.pdf")):
        raw1 = pdftotext(pdf_file)
        if not raw1:
            continue
        clean_text = clean_ocr_text(raw1) 
        date_text = extract_date(clean_text)
        type_doc = type_document(clean_text)
        #print (clean_text)
        print (date_text)
        print (type_doc)
        print ('############################')

