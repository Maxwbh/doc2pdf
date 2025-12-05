# Dockerfile para API DOC to PDF
# Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA

FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Instala LibreOffice e dependências necessárias
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    fonts-liberation \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia código da aplicação
COPY app.py .
COPY version.py .

# Expõe porta (Render usa PORT environment variable)
EXPOSE 5000

# Define variável de ambiente para produção
ENV PYTHONUNBUFFERED=1

# Comando para iniciar a aplicação
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 app:app
