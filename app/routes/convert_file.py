"""
Rota /convert-file - Converte DOCX para PDF e retorna arquivo

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
"""
import os
import time
import tempfile
from flask import Blueprint, request, jsonify, send_file
from app.utils.logger import logger
from app.utils.encoders import decode_base64_file
from app.utils.validators import validate_replacements, validate_quality, validate_filename
from app.services.docx_service import DocxService
from app.services.pdf_service import PdfService
from config.settings import ERROR_MESSAGES

convert_file_bp = Blueprint('convert_file', __name__)


@convert_file_bp.route('/convert-file', methods=['POST'])
def convert_file():
    """
    Converte DOCX para PDF e retorna arquivo para download

    Request JSON:
        {
            "document": "BASE64_ENCODED_DOCX",
            "replacements": {"TAG": "valor"},
            "filename": "documento.pdf" (opcional),
            "quality": "high" (opcional)
        }

    Response: Arquivo PDF para download
    """
    temp_dir = None
    try:
        if not request.is_json:
            return jsonify({'error': ERROR_MESSAGES['invalid_json']}), 400

        data = request.get_json()

        if 'document' not in data:
            return jsonify({'error': ERROR_MESSAGES['missing_document']}), 400

        if 'replacements' not in data:
            return jsonify({'error': ERROR_MESSAGES['missing_replacements']}), 400

        document_base64 = data['document']
        replacements = data['replacements']
        filename = validate_filename(data.get('filename', 'documento.pdf'))
        quality = validate_quality(data.get('quality', 'high'))

        is_valid, error_msg = validate_replacements(replacements)
        if not is_valid:
            return jsonify({'error': error_msg}), 400

        logger.info(f"✓ Validação OK - {len(replacements)} substituições")
        logger.info(f"Arquivo de saída: {filename}")
        logger.info(f"Qualidade: {quality}")

        # Processa documento
        logger.info("Etapa 1/4: Decodificando documento...")
        doc_bytes = decode_base64_file(document_base64)

        logger.info("Etapa 2/4: Substituindo tags...")
        modified_doc = DocxService.replace_tags_in_doc(doc_bytes, replacements)

        temp_dir = tempfile.mkdtemp()
        docx_path = os.path.join(temp_dir, 'document.docx')
        pdf_path = os.path.join(temp_dir, 'document.pdf')

        logger.info("Etapa 3/4: Salvando DOCX...")
        modified_doc.save(docx_path)

        logger.info("Etapa 4/4: Convertendo para PDF...")
        PdfService.convert_docx_to_pdf(docx_path, pdf_path, quality=quality)

        if not os.path.exists(pdf_path):
            raise Exception(ERROR_MESSAGES['pdf_not_generated'])

        pdf_size = os.path.getsize(pdf_path)
        logger.info(f"✅ PDF gerado: {pdf_size / 1024:.2f} KB")

        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro: {str(e)}")
        return jsonify({'error': f'Erro ao processar: {str(e)}'}), 500
    finally:
        # Cleanup é feito pelo send_file após envio
        pass
