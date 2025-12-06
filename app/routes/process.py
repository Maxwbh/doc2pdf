"""
Rota /process - Endpoint flexível com múltiplas opções

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
"""
import os
import time
import tempfile
from flask import Blueprint, request, jsonify, send_file
from app.utils.logger import logger
from app.utils.encoders import decode_base64_file, encode_base64_file
from app.utils.validators import validate_replacements, validate_quality, validate_filename
from app.services.docx_service import DocxService
from app.services.pdf_service import PdfService
from config.settings import ERROR_MESSAGES

process_bp = Blueprint('process', __name__)


@process_bp.route('/process', methods=['POST'])
def process():
    """
    Endpoint flexível para processamento de documentos

    Request JSON:
        {
            "document": "BASE64_ENCODED_DOCX",
            "replacements": {"TAG": "valor"},
            "input_type": "base64" (opcional: base64|doc),
            "output_type": "pdf" (opcional: pdf|doc|base64_pdf|base64_doc),
            "filename": "documento" (opcional),
            "quality": "high" (opcional)
        }

    Response: Varia conforme output_type
    """
    temp_dir = None
    try:
        if not request.is_json:
            return jsonify({'error': ERROR_MESSAGES['invalid_json']}), 400

        data = request.get_json()

        if 'document' not in data or 'replacements' not in data:
            return jsonify({'error': 'Campos "document" e "replacements" são obrigatórios'}), 400

        # Parâmetros
        input_type = data.get('input_type', 'base64').lower()
        output_type = data.get('output_type', 'pdf').lower()
        document_data = data['document']
        replacements = data['replacements']
        filename = data.get('filename', 'documento')
        quality = validate_quality(data.get('quality', 'high'))

        # Valida tipos
        valid_input_types = ['base64', 'doc']
        valid_output_types = ['pdf', 'doc', 'base64_pdf', 'base64_doc']

        if input_type not in valid_input_types:
            return jsonify({'error': f'input_type inválido. Use: {", ".join(valid_input_types)}'}), 400

        if output_type not in valid_output_types:
            return jsonify({'error': f'output_type inválido. Use: {", ".join(valid_output_types)}'}), 400

        is_valid, error_msg = validate_replacements(replacements)
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        logger.info(f"✓ Configuração: input={input_type}, output={output_type}, quality={quality}")

        # Processa entrada
        logger.info(f"Etapa 1/4: Processando entrada ({input_type})...")
        if input_type == 'base64':
            doc_bytes = decode_base64_file(document_data)
        else:
            doc_bytes = document_data.encode() if isinstance(document_data, str) else document_data

        # Substitui tags
        logger.info("Etapa 2/4: Substituindo tags...")
        modified_doc = DocxService.replace_tags_in_doc(doc_bytes, replacements)

        # Cria diretório temporário
        temp_dir = tempfile.mkdtemp()
        docx_path = os.path.join(temp_dir, 'document.docx')

        logger.info("Etapa 3/4: Salvando DOCX...")
        modified_doc.save(docx_path)
        doc_size = os.path.getsize(docx_path)

        # Processa saída baseado no tipo
        if output_type == 'pdf':
            logger.info("Etapa 4/4: Convertendo para PDF (arquivo)...")
            pdf_path = os.path.join(temp_dir, 'document.pdf')
            PdfService.convert_docx_to_pdf(docx_path, pdf_path, quality=quality)

            if not os.path.exists(pdf_path):
                raise Exception(ERROR_MESSAGES['pdf_not_generated'])

            output_filename = validate_filename(filename, '.pdf')
            return send_file(pdf_path, mimetype='application/pdf', as_attachment=True, download_name=output_filename)

        elif output_type == 'doc':
            logger.info("Etapa 4/4: Retornando DOCX...")
            output_filename = validate_filename(filename, '.docx')
            return send_file(
                docx_path,
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                as_attachment=True,
                download_name=output_filename
            )

        elif output_type == 'base64_pdf':
            logger.info("Etapa 4/4: Convertendo para PDF (Base64)...")
            pdf_path = os.path.join(temp_dir, 'document.pdf')
            PdfService.convert_docx_to_pdf(docx_path, pdf_path, quality=quality)

            if not os.path.exists(pdf_path):
                raise Exception(ERROR_MESSAGES['pdf_not_generated'])

            with open(pdf_path, 'rb') as f:
                pdf_base64 = encode_base64_file(f.read())

            return jsonify({
                'success': True,
                'pdf': pdf_base64,
                'message': 'PDF gerado em Base64',
                'stats': {'output_size': os.path.getsize(pdf_path), 'quality': quality}
            }), 200

        elif output_type == 'base64_doc':
            logger.info("Etapa 4/4: Retornando DOCX em Base64...")
            with open(docx_path, 'rb') as f:
                doc_base64 = encode_base64_file(f.read())

            return jsonify({
                'success': True,
                'document': doc_base64,
                'message': 'DOCX gerado em Base64',
                'stats': {'output_size': doc_size}
            }), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro: {str(e)}")
        return jsonify({'error': f'Erro ao processar: {str(e)}'}), 500
    finally:
        pass
