"""
Funções de codificação e decodificação

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
"""
import base64
from typing import Union
from app.utils.logger import logger
from config.settings import ERROR_MESSAGES


def decode_base64_file(base64_string: str) -> bytes:
    """
    Decodifica string Base64 para bytes

    Args:
        base64_string: String em Base64

    Returns:
        Bytes decodificados

    Raises:
        ValueError: Se a string Base64 for inválida
    """
    try:
        # Remove possíveis espaços em branco
        base64_string = base64_string.strip()
        return base64.b64decode(base64_string)
    except Exception as e:
        logger.error(f"Erro ao decodificar Base64: {str(e)}")
        raise ValueError(ERROR_MESSAGES['invalid_base64'])


def encode_base64_file(file_bytes: bytes) -> str:
    """
    Codifica bytes para string Base64

    Args:
        file_bytes: Bytes do arquivo

    Returns:
        String Base64
    """
    try:
        return base64.b64encode(file_bytes).decode('utf-8')
    except Exception as e:
        logger.error(f"Erro ao codificar Base64: {str(e)}")
        raise ValueError(f"Erro ao codificar arquivo em Base64: {str(e)}")


def is_valid_base64(s: str) -> bool:
    """
    Verifica se uma string é um Base64 válido

    Args:
        s: String para verificar

    Returns:
        True se válido, False caso contrário
    """
    try:
        if not s:
            return False
        base64.b64decode(s, validate=True)
        return True
    except Exception:
        return False
