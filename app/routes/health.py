"""
Rotas de health check e informações da API

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
"""
from flask import Blueprint, jsonify
from version import __version__, __author__, __email__, __company__, __linkedin__
from config.settings import API_NAME, API_DESCRIPTION

# Cria blueprint
health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificação de saúde da API"""
    return jsonify({
        'status': 'healthy',
        'service': API_NAME,
        'version': __version__
    }), 200


@health_bp.route('/', methods=['GET'])
def index():
    """Endpoint raiz com informações da API"""
    return jsonify({
        'name': API_NAME,
        'description': API_DESCRIPTION,
        'version': __version__,
        'author': __author__,
        'email': __email__,
        'company': __company__,
        'linkedin': f"https://linkedin.com/in{__linkedin__}",
        'endpoints': {
            'health': {
                'path': '/health',
                'method': 'GET',
                'description': 'Verificação de saúde'
            },
            'convert': {
                'path': '/convert',
                'method': 'POST',
                'description': 'Converte DOCX para PDF (retorna Base64)'
            },
            'convert_file': {
                'path': '/convert-file',
                'method': 'POST',
                'description': 'Converte DOCX para PDF (retorna arquivo)'
            },
            'process': {
                'path': '/process',
                'method': 'POST',
                'description': 'Processamento flexível com múltiplas opções de entrada/saída'
            }
        },
        'documentation': {
            'postman': 'DOC2PDF_API_COMPLETE.postman_collection.json',
            'quality_guide': 'QUALIDADE_PDF.md',
            'changelog': 'CHANGELOG.md'
        },
        'quality_profiles': ['high', 'medium', 'low'],
        'tag_format': '{TAG}',
        'supported_formats': {
            'input': ['DOCX (Base64)'],
            'output': ['PDF (Base64)', 'PDF (file)']
        }
    }), 200
