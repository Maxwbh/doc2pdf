"""
Configurações da aplicação DOC2PDF API

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
"""
import os
from typing import Literal

# Informações da API
API_NAME = "DOC2PDF Converter API"
API_DESCRIPTION = "API REST profissional para conversão de documentos Word para PDF com substituição inteligente de tags"

# Configurações de conversão
CONVERSION_TIMEOUT = 60  # segundos
DEFAULT_PDF_QUALITY: Literal['high', 'medium', 'low'] = 'high'

# Perfis de qualidade de PDF
PDF_QUALITY_PROFILES = {
    'high': {
        'MaxImageResolution': 300,
        'Quality': 95,
        'ReduceImageResolution': False,
        'description': 'Alta qualidade - ideal para impressão'
    },
    'medium': {
        'MaxImageResolution': 150,
        'Quality': 85,
        'ReduceImageResolution': True,
        'description': 'Qualidade média - balanceado'
    },
    'low': {
        'MaxImageResolution': 75,
        'Quality': 70,
        'ReduceImageResolution': True,
        'description': 'Baixa qualidade - menor tamanho'
    }
}

# Configurações do LibreOffice
LIBREOFFICE_COMMAND = 'libreoffice'
LIBREOFFICE_OPTIONS = [
    '--headless',           # Modo sem interface
    '--invisible',          # Completamente invisível
    '--nocrashreport',      # Não envia crash reports
    '--nodefault',          # Não carrega documento padrão
    '--nofirststartwizard', # Pula wizard de primeira execução
    '--nolockcheck',        # Não verifica locks de arquivo
    '--nologo',             # Não mostra logo
    '--norestore',          # Não restaura sessão anterior
]

# Formatos suportados
SUPPORTED_INPUT_FORMATS = ['docx']  # .DOC (antigo) não é suportado
SUPPORTED_OUTPUT_FORMATS = ['pdf']

# Validação de tags
TAG_FORMAT = r'\{[A-Z0-9_]+\}'  # Regex para formato {TAG}
TAG_OPEN = '{'
TAG_CLOSE = '}'

# Limites de tamanho
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_REPLACEMENTS = 1000  # Máximo de substituições por documento

# Configurações de logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s] - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# CORS
CORS_ORIGINS = '*'  # Em produção, especifique domínios permitidos

# Health check
HEALTH_CHECK_PATH = '/health'
FILTER_HEALTH_LOGS = True  # Não loga health checks para reduzir ruído

# Configurações de segurança (headers)
SECURITY_HEADERS = {
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
}

# Mensagens de erro padrão
ERROR_MESSAGES = {
    'invalid_json': 'Content-Type deve ser application/json',
    'missing_document': 'Campo "document" é obrigatório',
    'missing_replacements': 'Campo "replacements" é obrigatório',
    'invalid_replacements': 'Campo "replacements" deve ser um objeto JSON',
    'invalid_quality': 'Campo "quality" deve ser "high", "medium" ou "low"',
    'invalid_base64': 'String Base64 inválida',
    'invalid_docx': 'Arquivo DOCX inválido',
    'doc_not_supported': 'Formato .DOC (Word 97-2003) não suportado. Por favor, converta para .DOCX primeiro',
    'conversion_timeout': 'Timeout na conversão do documento. O documento pode ser muito grande ou complexo.',
    'pdf_not_generated': 'PDF não foi gerado pelo LibreOffice',
}
