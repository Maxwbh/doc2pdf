"""
Inicialização da aplicação Flask DOC2PDF

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
"""
import time
from flask import Flask, request
from flask_cors import CORS
from app.utils.logger import logger
from config.settings import (
    API_NAME,
    CORS_ORIGINS,
    SECURITY_HEADERS,
    HEALTH_CHECK_PATH,
    FILTER_HEALTH_LOGS
)
from version import __version__, __author__, __company__


def create_app():
    """
    Factory para criar e configurar a aplicação Flask

    Returns:
        Aplicação Flask configurada
    """
    app = Flask(__name__)

    # Configuração CORS
    CORS(app, origins=CORS_ORIGINS)

    # Banner de inicialização
    logger.info("="*60)
    logger.info(f"{API_NAME} v{__version__}")
    logger.info(f"Desenvolvido por: {__author__} - {__company__}")
    logger.info("="*60)

    # Middleware para logging de requisições (otimizado para Render)
    @app.before_request
    def log_request():
        """Log detalhado de cada requisição (filtra health checks)"""
        request.start_time = time.time()

        # Ignora logs detalhados de health checks para reduzir ruído no Render
        if FILTER_HEALTH_LOGS and request.path == HEALTH_CHECK_PATH:
            return  # Não loga health checks

        logger.info(f">>> NOVA REQUISIÇÃO")
        logger.info(f"Método: {request.method}")
        logger.info(f"Endpoint: {request.path}")
        logger.info(f"IP Cliente: {request.remote_addr}")
        logger.info(f"User-Agent: {request.headers.get('User-Agent', 'N/A')[:100]}")

        if request.method in ['POST', 'PUT', 'PATCH']:
            content_length = request.headers.get('Content-Length', 0)
            logger.info(f"Tamanho do payload: {content_length} bytes")

    @app.after_request
    def log_response(response):
        """Log da resposta e tempo de processamento (filtra health checks)"""
        # Ignora logs detalhados de health checks
        if FILTER_HEALTH_LOGS and request.path == HEALTH_CHECK_PATH:
            return response

        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(f"<<< RESPOSTA ENVIADA")
            logger.info(f"Status: {response.status_code}")
            logger.info(f"Tempo de processamento: {duration:.3f}s")
            logger.info(f"Tamanho da resposta: {response.content_length or 0} bytes")
            logger.info(f"-"*60)
        return response

    # Headers de segurança
    @app.after_request
    def add_security_headers(response):
        """Adiciona headers de segurança em todas as respostas"""
        for header, value in SECURITY_HEADERS.items():
            response.headers[header] = value
        return response

    # Registra blueprints (rotas)
    from app.routes.health import health_bp
    from app.routes.convert import convert_bp
    from app.routes.convert_file import convert_file_bp
    from app.routes.process import process_bp

    app.register_blueprint(health_bp)
    app.register_blueprint(convert_bp)
    app.register_blueprint(convert_file_bp)
    app.register_blueprint(process_bp)

    logger.info("✓ Blueprints registrados: health, convert, convert_file, process")
    logger.info("✓ Aplicação pronta para receber requisições")

    return app
