import re
import ftfy
import unicodedata
import ollama
import os
import dateparser
from spellchecker import SpellChecker
from pathlib import Path
from PyPDF2 import PdfReader
from natsort import natsorted

MODEL_NAME = 'llama3.2:3b'
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

def extarct_date(raw2)

    date_pattern = re.findall(  r'(\d{1,2}\s+de\s+\w+\s+\d{4}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}-\d{2}-\d{2})',raw2,flags = re.IGNORECASE)

    if not date_pattern:
        raw2 = 'datenotfound'
        return raw2
    
    for date_str in date_pattern:
        date_obj = dateparser.parse(date_str)
        if date_obj:
            raw2 = date.obj.strftime('%d-%m-%Y') #date format ISO
            break   # Show only the first result
        else:
            raw2 = 'datenotfound'
    return raw2
 
if __name__ == '__main__':

    for pdf_file in natsorted(inputpdf.glob("*.pdf")):
        raw1 = pdftotext(pdf_file)
        if not raw1:
            continue
    clean_text = clean_ocr_text(raw1) 
    date_text = extract_date(clean_text)

