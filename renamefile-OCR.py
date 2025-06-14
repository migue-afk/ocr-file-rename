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

def process_name(name)
