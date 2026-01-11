import dateparser
import ftfy
import os
import re
import spacy
import time
import unicodedata
from natsort import natsorted
from pathlib import Path
from PyPDF2 import PdfReader
from spellchecker import SpellChecker


inputpdf = Path("archive")
renamedest = Path("./archive")
renamedest.mkdir(exist_ok=True)
#nlp = spacy.load("es_core_news_sm")


nombres_comunes = set([
    # Common male names
    "JUAN", "MIGUEL", "CARLOS", "FERNANDO", "JOSE", "PEDRO", "LUIS", "DIEGO",
    "JORGE", "FRANCISCO", "ROBERTO", "ALEXANDER", "DANIEL", "RICARDO", "RAUL",
    "ANDRES", "CÉSAR", "MANUEL", "EDUARDO", "DAVID", "PAUL", "VICTOR", "ALBERTO",
    "RAMON", "ANTONIO", "OMAR", "JULIAN", "JAVIER", "SEBASTIAN", "HERNAN", "FELIPE",
    "MARTIN", "GUILLERMO", "EUGENIO", "ESTEBAN", "ADRIAN", "LUISITO", "CARLOS",
    "ANTONIO", "JOSE LUIS", "PEDRO ANTONIO", "JULIO", "MARTIN", "JOSE ANTONIO",
    "ALEXIS", "NICOLAS", "ROGELIO", "CONSUMIDOR",

    # Common female names
    "MARIA", "ANDREA", "ANA", "ROSA", "KARLA", "SOFIA", "VERONICA", "MONICA",
    "MARCELA", "GABRIELA", "CLAUDIA", "LAURA", "DIANA", "CAROLINA", "SANDRA",
    "PATRICIA", "KARINA", "LUZ", "YOLANDA", "MARTHA", "ELENA", "ISABEL", "JULIA",
    "PATRICIA", "BEATRIZ", "TERESA", "ROSA", "MARINA", "NATALIA", "PAOLA", "CARMEN",
    "ARACELI", "VANESSA", "ADRIANA", "CONSTANZA", "SUSANA", "SILVIA", "FRANCINE",
    "VICKY", "NANCY", "LILIANA", "AMELIA", "MAGALY", "MIRIAM", "CARLA", "CELESTE",
    "TERESA", "VERONICA", "GLORIA", "JOBITA", "MARIANA", "MARGARITA", "PAOLA", "NANCY", "ELIZABETH",

    # Common surnames
    "PEREZ", "LOPEZ", "GARCIA", "CUEVA", "MARTINEZ", "GONZALEZ", "RODRIGUEZ", "RUIZ",
    "QUIROZ", "FLORES", "CASTILLO", "HERRERA", "TORRES", "VARGAS", "MENDOZA",
    "ALVARADO", "SANCHEZ", "RAMOS", "SALAZAR", "CHAVEZ", "MORENO", "JIMENEZ",
    "DIAZ", "GOMEZ", "VASQUEZ", "PACHECO", "CARDENAS", "SOTO", "CABRERA", "DOMINGUEZ",
    "NUÑEZ", "TORREALBA", "ESTRADA", "MEDINA", "ALMEIDA", "RODRIGUEZ", "MARTINEZ",
    "SILVA", "FRANCO", "CASTRO", "JUAREZ", "ZAPATA", "AGUIRRE", "YUNDA", "REYES", "TAPIA",
    "MUÑOZ", "PAZ", "CORNEJO", "CARRILLO", "VALVERDE", "AGUINAGA", "GALARZA", "SALGADO",
    "GUERRERO", "SILVA", "ESPINOZA", "BASANTES", "MARIN", "GUAMAN", "POMA", "CALDERON",
    "SAQUISILA", "VARELA", "NALVARADO", "FRANCISCO", "CASTRO", "GALLEGOS", "JARRIN",
    "SAMANIEGO", "BORRERO", "BAQUERO", "ARCOS", "PALACIOS", "ORTEGA", "CARPIO", "MORETA",
    "YUNGA", "PEZANTES", "CONSUMIDOR", "FINAL", "MAYANCELA", "FINAL"
])

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


def clean_ocr_text(text: str) -> str:
    text = ftfy.fix_text(text)
    text = re.sub(r'-\s*\n\s*', '', text)
    text = re.sub(r'\n+', ' ', text)
    #text = unicodedata.normalize('NFC', text)
    text = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode()
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

def safe_filename2(name2):
    name2 = str(name2).strip()
    name2 = name2.replace(" ","_")
    name2 = re.sub(r'[<>:"\\/|?*]','_',name2)
    name2 = re.sub(r'_+','_', name2)
    #name2 = re.sub(r"(\d{2})_(\d{2})_(\d{2})", r"\1-\2-\3", name2)
    return name2



def type_document(raw33):
    # Detect "type" docuemten in base to text
    # Split text in lines
    lines = raw33.split('\n')
    # Selecct only first 25 lines
    raw3 = '\n'.join(lines[:25])

    if "FACTURA" in raw3:
        return "FACTURA"
    elif "NOTA DE VENTA" in raw3 or "NOTA VENTA" in raw3:
        return "NOTA DE VENTA"
    elif "COMPROBANTE DE RETENCION" in raw3 or "RETENCION" in raw3:
        return "COMPROBANTE DE RETENCION"
    elif "LIQUIDACION DE COMPRAS" in raw3 or "LIQUIDACION" in raw3:
        return "LIQUIDACION"
    elif "GUIA DE REMISION" in raw3 or "GUIA REMISION" in raw3 or "GUIA" in raw3:
        return "GUIA DE REMISION"
    elif "NOTA DE CREDITO" in raw3 or "CREDITO" in raw3:
        return "NOTA DE CREDITO"
    elif "NOTA DE DEBITO" in raw3 or "DEBITO" in raw3:
        return "NOTA DE DEBITO"
    elif "COMPROBANTE ELECTRONICO" in raw3:
        return "COMPROBANTE ELECTRONICO"
    elif "PROFORMA" in raw3:
        return "PROFORMA"
    elif "COTIZACION" in raw3:
        return "COTIZACION"
    elif "ORDEN DE COMPRA" in raw3:
        return "ORDEN DE COMPRA"
    elif "ORDEN DE TRABAJO" in raw3:
        return "ORDEN DE TRABAJO"
    elif "ORDEN DE SERVICIO" in raw3:
        return "ORDEN DE SERVICIO"
    elif "CONTRATO" in raw3:
        return "CONTRATO"
    elif "RECIBO" in raw3:
        return "RECIBO"
    elif "VALE DE CAJA" in raw3 or "VALE" in raw3:
        return "VALE DE CAJA"
    elif "VOUCHER" in raw3:
        return "VOUCHER"
    elif "INFORME" in raw3:
        return "INFORME"
    elif "ACTA DE ENTREGA" in raw3 or "ACTA DE ENTREGA-RECEPCION" in raw3:
        return "ACTA DE ENTREGA"
    elif "ACTA DE ACEPTACION" in raw3:
        return "ACTA DE ACEPTACION"
    elif "PRESUPUESTO" in raw3:
        return "PRESUPUESTO"
    elif "LIQUIDACION DE GASTOS" in raw3:
        return "LIQUIDACION DE GASTOS"
    elif "DECLARACION JURAMENTADA" in raw3:
        return "DECLARACION JURAMENTADA"
    elif "DEPOSITO" in raw3:
        return "DEPOSITO"
    elif "TRANSFERENCIA" in raw3:
        return "TRANSFERENCIA"
    elif "ESTADO DE CUENTA" in raw3:
        return "ESTADO DE CUENTA"
    elif "PAGARE" in raw3 or "PAGARÉ" in raw3:
        return "PAGARE"
    elif "LETRA DE CAMBIO" in raw3:
        return "LETRA DE CAMBIO"
    elif "CHEQUE" in raw3:
        return "CHEQUE"
    elif "CDP" in raw3 or "CERTIFICADO DE DEPOSITO" in raw3:
        return "CERTIFICADO DE DEPOSITO"
    elif "COMPROBANTE DE PAGO" in raw3:
        return "COMPROBANTE DE PAGO"
    elif "ROL DE PAGO" in raw3:
        return "ROL DE PAGO"
    elif "CEDULA" in raw3:
        return "CEDULA"
    elif "RUC" in raw3:
        return "RUC"
    elif "PERMISO DE FUNCIONAMIENTO" in raw3:
        return "PERMISO DE FUNCIONAMIENTO"
    elif "LICENCIA DE FUNCIONAMIENTO" in raw3:
        return "LICENCIA DE FUNCIONAMIENTO"
    elif "CERTIFICADO DE CUMPLIMIENTO" in raw3:
        return "CERTIFICADO DE CUMPLIMIENTO"
    elif "TURNO" in raw3:
        return "TURNO"
    elif "COMPROBANTE" in raw3:
        return "COMPROBANTE"
    elif "RESOLUCION" in raw3:
        return "RESOLUCION"
    elif "OFICIO" in raw3:
        return "OFICIO"
    elif "MEMORANDO" in raw3:
        return "MEMORANDO"
    elif "ACTA DE GRADO" in raw3:
        return "ACTA DE GRADO"
    elif "TITULO" in raw3 or "TÍTULO" in raw3:
        return "TITULO"
    elif "CERTIFICADO DE ESTUDIOS" in raw3 or "CERTIFICADO DE MATRICULA" in raw3:
        return "CERTIFICADO DE ESTUDIOS"
    elif "MALLA CURRICULAR" in raw3:
        return "MALLA CURRICULAR"
    elif "KARDEX" in raw3:
        return "KARDEX"
    elif "BOLETA DE CALIFICACIONES" in raw3:
        return "BOLETA DE CALIFICACIONES"
    elif "CONTRATO DE TRABAJO" in raw3:
        return "CONTRATO DE TRABAJO"
    elif "CERTIFICADO LABORAL" in raw3:
        return "CERTIFICADO LABORAL"
    elif "ACTA DE FINIQUITO" in raw3:
        return "ACTA DE FINIQUITO"
    elif "AVISO DE ENTRADA" in raw3 or "AVISO DE SALIDA" in raw3:
        return "AVISO IESS"
    elif "LICENCIA DE CONDUCIR" in raw3:
        return "LICENCIA DE CONDUCIR"
    elif "MATRICULA VEHICULAR" in raw3:
        return "MATRICULA VEHICULAR"
    elif "REVISION TECNICA" in raw3 or "REVISION VEHICULAR" in raw3:
        return "REVISION TECNICA"
    elif "CERTIFICADO DE VOTACION" in raw3:
        return "CERTIFICADO DE VOTACION"
    elif "PARTE POLICIAL" in raw3:
        return "PARTE POLICIAL"
    elif "HOJA DE RUTA" in raw3:
        return "HOJA DE RUTA"
    elif "MANIFIESTO DE CARGA" in raw3:
        return "MANIFIESTO DE CARGA"
    elif "PLANILLA" in raw3:
        return "PLANILLA"
    elif "CERTIFICADO" in raw3:
        return "CERTIFICADO"
    elif "SOLICITUD" in raw3:
        return "SOLICITUD"
    elif "CONSTANCIA" in raw3:
        return "CONSTANCIA"
    elif "ACTA" in raw3:
        return "ACTA"
    elif "RECORD POLICIAL" in raw3:
        return "RECORD POLICIAL"
    elif "RECORD ACADEMICO" in raw3:
        return "RECORD ACADEMICO"
    elif "LATAM" in raw3:
        return "TICKET VUELO"
    else:
        return "notfound"


def name_document(text):
    # Text to Uppercase
    text = text.upper()

    # Split text in lines
    lines = text.splitlines()

    # Search 'NOMBRE', 'NOMBRES', 'CLIENTE' o 'USUARIO' seguido de cualquier texto después de ':'
    pattern = re.compile(r'(?:NOMBRE|NOMBRES|ALUMNO|IDENTIFICACIÓN|IDENTIFICACION|DUEÑO|CLIENTE|REMITENTE|USUARIO)[\s:]+(.*?)(?=\n|$)', re.IGNORECASE | re.DOTALL)

    # Search all matches
    matches = pattern.findall(text)

    # Init filtered_names afuera del loop
    filtered_names = []
    filterName = "nonamefound"

    if matches:
        for match in matches:
            # Deleted space to innecesari to first and final
            words = match.strip().split()  # Split text in words
            first_10_words = " ".join(words[:20])  # Toma las primeras 10 palabras
            first_10_words = first_10_words.split()

            print(first_10_words)  # Mostrar las primeras 10 palabras

            # Filter common names
            filtered_names += [word for word in first_10_words if word in nombres_comunes]
            filterName = " ".join(filtered_names)
            print(filterName)

    # Retunr filtered_names or "nonamefound" if empty
    return filterName if filterName else "nonamefound"



def get_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1

    folder_path = "archive/"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    new_filename = filename
    full_path = os.path.join(folder_path, new_filename)

    while os.path.exists(full_path):
        new_filename = f"{base}_{counter}{ext}"
        full_path = os.path.join(folder_path, new_filename)
        counter += 1

    return new_filename

if __name__ == '__main__':

    for pdf_file in natsorted(inputpdf.glob("*.pdf")):
        raw1 = pdftotext(pdf_file)
        if not raw1:
            continue
        date_text = extract_date(raw1)
        clean_text = clean_ocr_text(raw1)
        type_doc = type_document(clean_text)
        name_doc = name_document(clean_text)
        renamed_file = safe_filename (f"{type_doc} {name_doc} {date_text}.pdf")
        uniq_name = get_unique_filename(renamed_file) # Process to uniq name of document for file
        print (uniq_name)
        print ("Data for renamed file")
        print (date_text)
        print (type_doc)
        print (name_doc)
        print ('############################')
        print (renamed_file)
        destination = renamedest / uniq_name
        os.rename(pdf_file,destination)


