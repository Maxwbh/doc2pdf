"""
Funções de validação

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
"""
from typing import Tuple, Dict, Any
import base64
from werkzeug.exceptions import BadRequest
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

    Raises:
        BadRequest: Se qualidade for inválida
    """
    if not quality or quality == '':
        return 'medium'  # Padrão é medium

    quality = quality.lower().strip()

    if quality not in PDF_QUALITY_PROFILES:
        logger.error(f"Qualidade inválida '{quality}'")
        raise BadRequest(f"Qualidade inválida: '{quality}'. Use 'high', 'medium' ou 'low'")

    return quality


def validate_replacements(replacements: Any) -> Dict[str, Any]:
    """
    Valida o objeto de substituições

    Args:
        replacements: Objeto com tags e valores

    Returns:
        Dicionário validado de substituições

    Raises:
        BadRequest: Se replacements for inválido
    """
    # Permite None e retorna dict vazio
    if replacements is None:
        return {}

    # Verifica se é um dicionário
    if not isinstance(replacements, dict):
        logger.error("Replacements não é um dicionário")
        raise BadRequest(ERROR_MESSAGES['invalid_replacements'])

    # Verifica se está vazio
    if not replacements:
        logger.warning("⚠ Objeto de substituições está vazio")
        return {}  # Vazio é válido, mas não fará nada

    # Verifica limite de substituições
    if len(replacements) > MAX_REPLACEMENTS:
        logger.error(f"Número de substituições excede o máximo ({MAX_REPLACEMENTS})")
        raise BadRequest(f"Número máximo de substituições excedido (máximo: {MAX_REPLACEMENTS})")

    # Verifica se todas as chaves são strings
    for key in replacements.keys():
        if not isinstance(key, str):
            logger.error(f"Tag inválida: '{key}'")
            raise BadRequest(f"Tag inválida: '{key}' - Todas as tags devem ser strings")

    logger.info(f"✓ {len(replacements)} substituições validadas")
    return replacements


def validate_return_format(return_format: str) -> str:
    """
    Valida e normaliza o formato de retorno

    Args:
        return_format: Formato de retorno ('base64' ou 'file')

    Returns:
        Formato validado (sempre lowercase)

    Raises:
        BadRequest: Se formato for inválido
    """
    if not return_format or return_format == '':
        return 'base64'  # Padrão

    return_format = return_format.lower().strip()

    valid_formats = ['base64', 'file']
    if return_format not in valid_formats:
        logger.error(f"Formato inválido '{return_format}'")
        raise BadRequest(f"Formato inválido: '{return_format}'. Use 'base64' ou 'file'")

    return return_format


def validate_json_content_type(request) -> None:
    """
    Valida se a requisição tem Content-Type application/json

    Args:
        request: Objeto request do Flask

    Raises:
        BadRequest: Se Content-Type não for application/json
    """
    content_type = request.content_type

    if not content_type or 'application/json' not in content_type.lower():
        logger.error(f"Content-Type inválido: {content_type}")
        raise BadRequest("Content-Type deve ser 'application/json'")


def validate_base64_document(document_base64: str) -> bytes:
    """
    Valida e decodifica documento em Base64

    Args:
        document_base64: String Base64 do documento

    Returns:
        Bytes do documento decodificado

    Raises:
        BadRequest: Se Base64 for inválido ou vazio
    """
    if not document_base64:
        logger.error("Documento Base64 vazio ou None")
        raise BadRequest("Documento Base64 não pode estar vazio")

    try:
        # Remove whitespace
        document_base64 = document_base64.strip()

        # Tenta decodificar
        doc_bytes = base64.b64decode(document_base64)

        if len(doc_bytes) == 0:
            raise BadRequest("Documento decodificado está vazio")

        return doc_bytes

    except Exception as e:
        logger.error(f"Erro ao decodificar Base64: {str(e)}")
        raise BadRequest(f"String Base64 inválida: {str(e)}")


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
