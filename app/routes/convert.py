"""
Rota /convert - Converte DOCX para PDF e retorna em Base64

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
"""
import os
import time
import tempfile
from flask import Blueprint, request, jsonify
from app.utils.logger import logger
from app.utils.encoders import decode_base64_file, encode_base64_file
from app.utils.validators import validate_replacements, validate_quality
from app.services.docx_service import DocxService
from app.services.pdf_service import PdfService
from config.settings import ERROR_MESSAGES

# Cria blueprint
convert_bp = Blueprint('convert', __name__)


@convert_bp.route('/convert', methods=['POST'])
def convert():
    """
    Converte documento DOCX para PDF com substituição de tags

    Request JSON:
        {
            "document": "BASE64_ENCODED_DOCX",
            "replacements": {"TAG": "valor"},
            "quality": "high" (opcional: high|medium|low)
        }

    Response JSON:
        {
            "success": true,
            "pdf": "BASE64_ENCODED_PDF",
            "message": "Documento convertido com sucesso",
            "processing_time": 5.234,
            "stats": {
                "input_size": 12345,
                "output_size": 54321,
                "quality": "high"
            }
        }
    """
    try:
        # Valida requisição
        if not request.is_json:
            return jsonify({'error': ERROR_MESSAGES['invalid_json']}), 400

        data = request.get_json()

        # Valida campos obrigatórios
        if 'document' not in data:
            return jsonify({'error': ERROR_MESSAGES['missing_document']}), 400

        if 'replacements' not in data:
            return jsonify({'error': ERROR_MESSAGES['missing_replacements']}), 400

        document_base64 = data['document']
        replacements = data['replacements']
        quality = validate_quality(data.get('quality', 'high'))

        # Valida replacements
        is_valid, error_msg = validate_replacements(replacements)
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        logger.info(f"✓ Validação OK - {len(replacements)} substituições encontradas")
        logger.info(f"Tags a substituir: {list(replacements.keys())}")
        logger.info(f"Qualidade do PDF: {quality}")

        # Decodifica o documento
        logger.info("Etapa 1/4: Decodificando documento Base64...")
        start_decode = time.time()
        doc_bytes = decode_base64_file(document_base64)
        logger.info(f"✓ Documento decodificado ({len(doc_bytes)} bytes) em {time.time() - start_decode:.3f}s")

        # Substitui as tags no documento
        logger.info("Etapa 2/4: Substituindo tags no documento...")
        start_replace = time.time()
        modified_doc = DocxService.replace_tags_in_doc(doc_bytes, replacements)
        logger.info(f"✓ Tags substituídas em {time.time() - start_replace:.3f}s")

        # Cria arquivos temporários
        with tempfile.TemporaryDirectory() as temp_dir:
            logger.info(f"Diretório temporário: {temp_dir}")
            docx_path = os.path.join(temp_dir, 'document.docx')
            pdf_path = os.path.join(temp_dir, 'document.pdf')

            # Salva o documento modificado
            logger.info("Etapa 3/4: Salvando documento DOCX...")
            start_save = time.time()
            modified_doc.save(docx_path)
            doc_size = os.path.getsize(docx_path)
            logger.info(f"✓ DOCX salvo ({doc_size} bytes) em {time.time() - start_save:.3f}s")

            # Converte para PDF
            logger.info("Etapa 4/4: Convertendo DOCX para PDF...")
            start_convert = time.time()
            PdfService.convert_docx_to_pdf(docx_path, pdf_path, quality=quality)

            # Verifica se o PDF foi gerado
            if not os.path.exists(pdf_path):
                logger.error("ERRO: PDF não foi gerado pelo LibreOffice")
                raise Exception(ERROR_MESSAGES['pdf_not_generated'])

            pdf_size = os.path.getsize(pdf_path)
            logger.info(f"✓ PDF gerado ({pdf_size} bytes) em {time.time() - start_convert:.3f}s")

            # Lê o PDF e converte para Base64
            logger.info("Codificando PDF para Base64...")
            start_encode = time.time()
            with open(pdf_path, 'rb') as pdf_file:
                pdf_bytes = pdf_file.read()
                pdf_base64 = encode_base64_file(pdf_bytes)
            logger.info(f"✓ PDF codificado em Base64 ({len(pdf_base64)} chars) em {time.time() - start_encode:.3f}s")

        # Calcula tempo total
        total_time = time.time() - request.start_time if hasattr(request, 'start_time') else 0
        logger.info(f"✅ CONVERSÃO CONCLUÍDA COM SUCESSO")
        logger.info(f"Resumo: DOCX ({doc_size}b) -> PDF ({pdf_size}b) -> Base64 ({len(pdf_base64)} chars)")
        logger.info(f"Tempo total de conversão: {total_time:.3f}s")

        return jsonify({
            'success': True,
            'pdf': pdf_base64,
            'message': 'Documento convertido com sucesso',
            'processing_time': round(total_time, 3),
            'stats': {
                'input_size': doc_size,
                'output_size': pdf_size,
                'quality': quality,
                'replacements_count': len(replacements)
            }
        }), 200

    except ValueError as e:
        logger.error(f"Erro de validação: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro interno: {str(e)}")
        return jsonify({'error': f'Erro ao processar documento: {str(e)}'}), 500
