"""
Funções de validação

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
"""
from typing import Tuple, Dict, Any
from app.utils.logger import logger
from config.settings import (
    PDF_QUALITY_PROFILES,
    ERROR_MESSAGES,
    MAX_REPLACEMENTS
)


def validate_docx_format(doc_bytes: bytes) -> Tuple[bool, str]:
    """
    Valida se os bytes são de um arquivo DOCX válido

    DOCX files são arquivos ZIP que contêm XML. A assinatura de um arquivo ZIP
    começa com 'PK' (0x50 0x4B). Arquivos .DOC antigos usam formato OLE2 e começam
    com D0 CF 11 E0.

    Args:
        doc_bytes: Bytes do documento

    Returns:
        Tupla (is_valid, error_message)
        - is_valid: True se válido, False caso contrário
        - error_message: Mensagem de erro ou None se válido
    """
    if len(doc_bytes) < 4:
        return False, "Arquivo muito pequeno para ser um DOCX válido"

    # Verifica assinatura ZIP (DOCX files são arquivos ZIP)
    if doc_bytes[0:2] == b'PK':
        logger.info("✓ Formato DOCX detectado (arquivo ZIP)")
        return True, None

    # Verifica assinatura de arquivo DOC antigo (D0 CF 11 E0)
    if doc_bytes[0:4] == b'\xD0\xCF\x11\xE0':
        logger.warning("⚠ Arquivo .DOC (formato antigo) detectado")
        return False, ERROR_MESSAGES['doc_not_supported']

    # Verifica se é texto plano (não binário)
    try:
        if doc_bytes[0:5].decode('utf-8', errors='ignore').isprintable():
            logger.warning("⚠ Arquivo parece ser texto plano, não DOCX")
            return False, "Arquivo parece não ser um documento Word. Certifique-se de enviar um arquivo .DOCX válido em Base64"
    except:
        pass

    # Formato não reconhecido
    logger.error(f"❌ Formato não reconhecido. Primeiros bytes: {doc_bytes[0:8].hex()}")
    return False, "Formato de arquivo não reconhecido. Apenas arquivos .DOCX (Word 2007+) são suportados"


def validate_quality(quality: str) -> str:
    """
    Valida e normaliza o parâmetro de qualidade

    Args:
        quality: String de qualidade ('high', 'medium', 'low')

    Returns:
        String de qualidade validada (sempre em lowercase)
        Se inválida, retorna 'high' como padrão
    """
    if not quality:
        return 'high'

    quality = quality.lower().strip()

    if quality not in PDF_QUALITY_PROFILES:
        logger.warning(f"Qualidade inválida '{quality}', usando 'high' como padrão")
        return 'high'

    return quality


def validate_replacements(replacements: Any) -> Tuple[bool, str]:
    """
    Valida o objeto de substituições

    Args:
        replacements: Objeto com tags e valores

    Returns:
        Tupla (is_valid, error_message)
    """
    # Verifica se é um dicionário
    if not isinstance(replacements, dict):
        return False, ERROR_MESSAGES['invalid_replacements']

    # Verifica se está vazio
    if not replacements:
        logger.warning("⚠ Objeto de substituições está vazio")
        return True, None  # Vazio é válido, mas não fará nada

    # Verifica limite de substituições
    if len(replacements) > MAX_REPLACEMENTS:
        return False, f"Número máximo de substituições excedido (máximo: {MAX_REPLACEMENTS})"

    # Verifica se todas as chaves são strings
    for key in replacements.keys():
        if not isinstance(key, str):
            return False, f"Tag inválida: '{key}' - Todas as tags devem ser strings"

    logger.info(f"✓ {len(replacements)} substituições validadas")
    return True, None


def validate_filename(filename: str, extension: str = '.pdf') -> str:
    """
    Valida e normaliza um nome de arquivo

    Args:
        filename: Nome do arquivo
        extension: Extensão esperada (padrão: '.pdf')

    Returns:
        Nome de arquivo validado com extensão correta
    """
    if not filename:
        return f'documento{extension}'

    # Remove caracteres perigosos
    filename = filename.strip()

    # Garante que termina com a extensão correta
    if not filename.endswith(extension):
        filename += extension

    return filename
