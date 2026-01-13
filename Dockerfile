# Base image with python
FROM python:3.11-slim

# Install Tesseract and dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    inotify-tools \
    ocrmypdf \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    rsync \
    cron \
    qpdf \
    figlet \
    imagemagick \
    zbar-tools \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define working directory
WORKDIR /ocrapp

# Copy files of project
COPY . .

# Create necessary directories
RUN mkdir -p \
    unify \
    archive \
    pdftopng \
    pdfseparate \
    report/archivo/skip \
    report/consume \
    .original

# Give execution permissions (if needed)
RUN chmod +x entrypoint.sh calhash.sh renamefile-OCR.sh renamefile_spacy.py sep.sh

# Install dependencies of python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Command to be executed when starting the container
ENTRYPOINT ["./entrypoint.sh"]
