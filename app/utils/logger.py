"""
Configuração de logging para a aplicação

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
"""
import logging
from config.settings import LOG_LEVEL, LOG_FORMAT, LOG_DATE_FORMAT


def setup_logger(name: str = 'doc2pdf') -> logging.Logger:
    """
    Configura e retorna um logger para a aplicação

    Args:
        name: Nome do logger (padrão: 'doc2pdf')

    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Evita duplicação de handlers
    if logger.handlers:
        return logger

    # Handler para console
    handler = logging.StreamHandler()
    handler.setLevel(LOG_LEVEL)

    # Formatter
    formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


# Logger padrão da aplicação
logger = setup_logger()
