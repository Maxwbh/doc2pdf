"""
Rota para documentação Swagger/OpenAPI

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
"""
from flask import Blueprint, send_from_directory, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import os

# Blueprint para servir arquivos estáticos do Swagger
swagger_bp = Blueprint('swagger', __name__)

# Configuração do Swagger UI
SWAGGER_URL = '/api/docs'  # URL para acessar a documentação
API_URL = '/api/openapi.yaml'  # URL do arquivo OpenAPI spec

# Cria blueprint do Swagger UI
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "DOC2PDF Converter API",
        'docExpansion': 'list',
        'defaultModelsExpandDepth': 3,
        'displayRequestDuration': True,
    }
)


@swagger_bp.route('/api/openapi.yaml')
def serve_openapi_spec():
    """Serve o arquivo OpenAPI YAML"""
    # Obtém o diretório raiz do projeto
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    return send_from_directory(root_dir, 'docs', 'api', 'openapi.yaml')


@swagger_bp.route('/api/openapi.json')
def serve_openapi_json():
    """Serve o OpenAPI spec em formato JSON (alternativa)"""
    import yaml
    import json

    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    yaml_path = os.path.join(root_dir, 'docs', 'api', 'openapi.yaml')

    with open(yaml_path, 'r', encoding='utf-8') as f:
        spec = yaml.safe_load(f)

    return jsonify(spec)
