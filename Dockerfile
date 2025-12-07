# Dockerfile otimizado para API DOC to PDF
# Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
# Versão: 1.5.2 - Simplificado e robusto para Render

FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Instala LibreOffice essencial + fontes e ferramentas de PDF
# Usa --no-install-recommends para reduzir tamanho
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice-writer-nogui \
    libreoffice-core-nogui \
    # Fontes essenciais para melhor renderização
    fonts-liberation \
    fonts-dejavu-core \
    fonts-liberation2 \
    fonts-noto-core \
    fonts-freefont-ttf \
    # Ferramentas de sistema
    curl \
    # Ghostscript para otimização adicional de PDF
    ghostscript \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

# Copia requirements primeiro (melhor cache)
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia estrutura modular da aplicação
COPY version.py .
COPY config/ ./config/
COPY app/ ./app/
COPY wsgi.py .

# Expõe porta (Render usa PORT environment variable)
EXPOSE 5000

# Define variáveis de ambiente para produção
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # LibreOffice - Otimizações
    SAL_USE_VCLPLUGIN=svp \
    HOME=/tmp \
    # Desabilita screensaver e animações
    DISPLAY= \
    # Melhora performance de conversão
    OOO_DISABLE_RECOVERY=1

# Health check otimizado (9 minutos)
HEALTHCHECK --interval=9m --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:${PORT:-5000}/health || exit 1

# Comando otimizado para iniciar a aplicação
CMD gunicorn --bind 0.0.0.0:$PORT \
    --workers 1 \
    --threads 4 \
    --timeout 120 \
    --worker-class gthread \
    --worker-tmp-dir /dev/shm \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    wsgi:app
