"""
API Flask para conversão de documentos DOC para PDF com substituição de tags

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
Email: maxwbh@gmail.com
LinkedIn: /maxwbh
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import base64
import io
import os
import tempfile
from docx import Document
import subprocess
from werkzeug.exceptions import BadRequest
import logging

app = Flask(__name__)
CORS(app)

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def decode_base64_file(base64_string):
    """Decodifica string Base64 para bytes"""
    try:
        return base64.b64decode(base64_string)
    except Exception as e:
        logger.error(f"Erro ao decodificar Base64: {str(e)}")
        raise ValueError("String Base64 inválida")


def replace_tags_in_doc(doc_bytes, replacements):
    """
    Substitui tags no documento Word pelos valores fornecidos

    Args:
        doc_bytes: Bytes do documento Word
        replacements: Dicionário com as substituições {tag: valor}

    Returns:
        Document: Documento modificado
    """
    try:
        # Abre o documento a partir dos bytes
        doc = Document(io.BytesIO(doc_bytes))

        # Substitui tags nos parágrafos
        for paragraph in doc.paragraphs:
            for tag, value in replacements.items():
                # Formata a tag com %%
                tag_formatted = f"%%{tag.upper()}%%"
                if tag_formatted in paragraph.text:
                    # Substitui em cada run para preservar formatação
                    for run in paragraph.runs:
                        if tag_formatted in run.text:
                            run.text = run.text.replace(tag_formatted, str(value))

        # Substitui tags nas tabelas
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for tag, value in replacements.items():
                        tag_formatted = f"%%{tag.upper()}%%"
                        if tag_formatted in cell.text:
                            for paragraph in cell.paragraphs:
                                for run in paragraph.runs:
                                    if tag_formatted in run.text:
                                        run.text = run.text.replace(tag_formatted, str(value))

        return doc
    except Exception as e:
        logger.error(f"Erro ao processar documento: {str(e)}")
        raise ValueError(f"Erro ao processar documento Word: {str(e)}")


def convert_docx_to_pdf(docx_path, pdf_path):
    """
    Converte documento DOCX para PDF usando LibreOffice

    Args:
        docx_path: Caminho do arquivo DOCX
        pdf_path: Caminho onde salvar o PDF
    """
    try:
        # Usa LibreOffice para conversão (disponível no Docker)
        result = subprocess.run(
            [
                'libreoffice',
                '--headless',
                '--convert-to',
                'pdf',
                '--outdir',
                os.path.dirname(pdf_path),
                docx_path
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            logger.error(f"Erro LibreOffice: {result.stderr}")
            raise Exception(f"Erro na conversão para PDF: {result.stderr}")

        # LibreOffice salva com o mesmo nome base do arquivo de entrada
        generated_pdf = os.path.join(
            os.path.dirname(pdf_path),
            os.path.splitext(os.path.basename(docx_path))[0] + '.pdf'
        )

        # Renomeia se necessário
        if generated_pdf != pdf_path and os.path.exists(generated_pdf):
            os.rename(generated_pdf, pdf_path)

    except subprocess.TimeoutExpired:
        raise Exception("Timeout na conversão do documento")
    except Exception as e:
        logger.error(f"Erro na conversão: {str(e)}")
        raise


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificação de saúde da API"""
    return jsonify({
        'status': 'healthy',
        'service': 'doc2pdf-api',
        'version': '1.0.0'
    }), 200


@app.route('/convert', methods=['POST'])
def convert_document():
    """
    Endpoint principal para conversão de documentos

    Espera JSON com:
    - document: string Base64 do arquivo .DOC
    - replacements: objeto com as substituições {tag: valor}

    Retorna:
    - pdf: string Base64 do PDF gerado
    """
    try:
        # Valida requisição
        if not request.is_json:
            return jsonify({'error': 'Content-Type deve ser application/json'}), 400

        data = request.get_json()

        # Valida campos obrigatórios
        if 'document' not in data:
            return jsonify({'error': 'Campo "document" é obrigatório'}), 400

        if 'replacements' not in data:
            return jsonify({'error': 'Campo "replacements" é obrigatório'}), 400

        document_base64 = data['document']
        replacements = data['replacements']

        # Valida que replacements é um dicionário
        if not isinstance(replacements, dict):
            return jsonify({'error': 'Campo "replacements" deve ser um objeto JSON'}), 400

        logger.info(f"Processando documento com {len(replacements)} substituições")

        # Decodifica o documento
        doc_bytes = decode_base64_file(document_base64)

        # Substitui as tags no documento
        modified_doc = replace_tags_in_doc(doc_bytes, replacements)

        # Cria arquivos temporários
        with tempfile.TemporaryDirectory() as temp_dir:
            docx_path = os.path.join(temp_dir, 'document.docx')
            pdf_path = os.path.join(temp_dir, 'document.pdf')

            # Salva o documento modificado
            modified_doc.save(docx_path)

            # Converte para PDF
            convert_docx_to_pdf(docx_path, pdf_path)

            # Verifica se o PDF foi gerado
            if not os.path.exists(pdf_path):
                raise Exception("PDF não foi gerado")

            # Lê o PDF e converte para Base64
            with open(pdf_path, 'rb') as pdf_file:
                pdf_bytes = pdf_file.read()
                pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

        logger.info("Documento convertido com sucesso")

        return jsonify({
            'success': True,
            'pdf': pdf_base64,
            'message': 'Documento convertido com sucesso'
        }), 200

    except ValueError as e:
        logger.error(f"Erro de validação: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro interno: {str(e)}")
        return jsonify({'error': f'Erro ao processar documento: {str(e)}'}), 500


@app.route('/convert-file', methods=['POST'])
def convert_document_file():
    """
    Endpoint para conversão de documentos retornando arquivo PDF

    Espera JSON com:
    - document: string Base64 do arquivo .DOC
    - replacements: objeto com as substituições {tag: valor}
    - filename (opcional): nome do arquivo PDF a ser gerado

    Retorna:
    - Arquivo PDF para download/visualização
    """
    temp_dir = None
    try:
        # Valida requisição
        if not request.is_json:
            return jsonify({'error': 'Content-Type deve ser application/json'}), 400

        data = request.get_json()

        # Valida campos obrigatórios
        if 'document' not in data:
            return jsonify({'error': 'Campo "document" é obrigatório'}), 400

        if 'replacements' not in data:
            return jsonify({'error': 'Campo "replacements" é obrigatório'}), 400

        document_base64 = data['document']
        replacements = data['replacements']
        filename = data.get('filename', 'documento.pdf')

        # Garante que o filename termina com .pdf
        if not filename.endswith('.pdf'):
            filename += '.pdf'

        # Valida que replacements é um dicionário
        if not isinstance(replacements, dict):
            return jsonify({'error': 'Campo "replacements" deve ser um objeto JSON'}), 400

        logger.info(f"Processando documento com {len(replacements)} substituições para arquivo")

        # Decodifica o documento
        doc_bytes = decode_base64_file(document_base64)

        # Substitui as tags no documento
        modified_doc = replace_tags_in_doc(doc_bytes, replacements)

        # Cria diretório temporário
        temp_dir = tempfile.mkdtemp()
        docx_path = os.path.join(temp_dir, 'document.docx')
        pdf_path = os.path.join(temp_dir, 'document.pdf')

        # Salva o documento modificado
        modified_doc.save(docx_path)

        # Converte para PDF
        convert_docx_to_pdf(docx_path, pdf_path)

        # Verifica se o PDF foi gerado
        if not os.path.exists(pdf_path):
            raise Exception("PDF não foi gerado")

        logger.info(f"Documento convertido com sucesso: {filename}")

        # Retorna o arquivo PDF
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )

    except ValueError as e:
        logger.error(f"Erro de validação: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro interno: {str(e)}")
        return jsonify({'error': f'Erro ao processar documento: {str(e)}'}), 500
    finally:
        # Limpa arquivos temporários após o envio
        if temp_dir and os.path.exists(temp_dir):
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except Exception as e:
                logger.warning(f"Não foi possível remover diretório temporário: {str(e)}")


@app.route('/', methods=['GET'])
def index():
    """Endpoint raiz com informações da API"""
    return jsonify({
        'service': 'DOC to PDF Converter API',
        'version': '1.0.0',
        'author': 'Maxwell da Silva Oliveira - M&S do Brasil LTDA',
        'email': 'maxwbh@gmail.com',
        'linkedin': '/maxwbh',
        'endpoints': {
            '/health': 'GET - Health check',
            '/convert': 'POST - Convert DOC to PDF with tag replacement (returns Base64)',
            '/convert-file': 'POST - Convert DOC to PDF with tag replacement (returns PDF file)'
        },
        'usage': {
            'method': 'POST',
            'endpoint': '/convert',
            'content_type': 'application/json',
            'body': {
                'document': 'Base64 encoded .DOC file',
                'replacements': {
                    'NOME': 'Jose da Silva',
                    'ENDERECO': 'Rua qualquer coisa, Nro1, Bairro das colinas, São Paulo/SP - CEP: 48.4839-877',
                    'DATANASCIMENTO': '01/01/1990'
                }
            },
            'response': {
                'success': True,
                'pdf': 'Base64 encoded PDF file',
                'message': 'Documento convertido com sucesso'
            }
        }
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
