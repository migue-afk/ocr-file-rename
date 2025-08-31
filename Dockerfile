# Imagen base con Python
FROM python:3.11-slim

# Instala Tesseract y dependencias necesarias
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    ocrmypdf \
    tesseract-ocr-spa \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Da permisos al script .sh
RUN chmod +x entrypoint.sh

# Instala dependencias de Python si existen
RUN pip install --no-cache-dir -r requirements.txt

# Comando que se ejecutará al iniciar el contenedor
ENTRYPOINT ["./entrypoint.sh"]
