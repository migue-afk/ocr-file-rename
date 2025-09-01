# Base image with python
FROM python:3.11-slim

# Install Tesseract and dependencies
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

# Define working directory
WORKDIR /ocrapp

# Copy files of proyect
COPY . .

# Give execution permissions
RUN chmod +x entrypoint.sh

# Install dependencies of python
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Command to be executed when starting the container
ENTRYPOINT ["./entrypoint.sh"]
