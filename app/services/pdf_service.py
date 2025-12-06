"""
Serviço de conversão para PDF

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
"""
import os
import subprocess
from typing import Literal
from app.utils.logger import logger
from app.utils.validators import validate_quality
from config.settings import (
    CONVERSION_TIMEOUT,
    PDF_QUALITY_PROFILES,
    LIBREOFFICE_COMMAND,
    LIBREOFFICE_OPTIONS,
    ERROR_MESSAGES
)


class PdfService:
    """Serviço para conversão de documentos para PDF"""

    @staticmethod
    def convert_docx_to_pdf(
        docx_path: str,
        pdf_path: str,
        quality: Literal['high', 'medium', 'low'] = 'high'
    ) -> None:
        """
        Converte documento DOCX para PDF usando LibreOffice com opções avançadas de qualidade

        Args:
            docx_path: Caminho do arquivo DOCX
            pdf_path: Caminho onde salvar o PDF
            quality: Qualidade do PDF ('high', 'medium', 'low')
                - high: 300 DPI, sem compressão de imagem, ideal para impressão
                - medium: 150 DPI, compressão moderada, balanceado (padrão)
                - low: 75 DPI, alta compressão, menor tamanho de arquivo

        Raises:
            Exception: Se houver erro na conversão
        """
        try:
            # Valida e normaliza qualidade
            quality = validate_quality(quality)

            logger.info(f"Iniciando conversão PDF com qualidade: {quality}")

            # Obtém configurações do perfil selecionado
            settings = PDF_QUALITY_PROFILES[quality]
            logger.info(f"Perfil selecionado: {settings['description']}")
            logger.info(f"Resolução máxima: {settings['MaxImageResolution']} DPI")
            logger.info(f"Qualidade JPEG: {settings['Quality']}%")

            # Monta filtro avançado para LibreOffice
            # Formato: writer_pdf_Export:{opcao1:valor1,opcao2:valor2}
            pdf_filter_options = [
                f"SelectPdfVersion=1",  # PDF 1.4 (compatível)
                f"UseTaggedPDF=true",   # PDF acessível com tags
                f"ExportBookmarks=true",  # Exporta marcadores/índice
                f"ExportNotes=false",   # Não exporta comentários
                f"Quality={settings['Quality']}",  # Qualidade de compressão JPEG
                f"ReduceImageResolution={str(settings['ReduceImageResolution']).lower()}",
                f"MaxImageResolution={settings['MaxImageResolution']}",
                f"ExportFormFields=true",  # Exporta campos de formulário
                f"FormsType=0",  # FDF format
                f"EmbedStandardFonts=false",  # Não embute fontes padrão (reduz tamanho)
            ]

            # Junta todas as opções em uma string
            filter_data = ":".join(pdf_filter_options)
            convert_format = f"pdf:writer_pdf_Export:{{{filter_data}}}"

            logger.info(f"Executando LibreOffice com filtro customizado...")

            # Comando LibreOffice com opções avançadas
            cmd = [LIBREOFFICE_COMMAND] + LIBREOFFICE_OPTIONS + [
                '--convert-to', convert_format,
                '--outdir', os.path.dirname(pdf_path),
                docx_path
            ]

            # Executa conversão
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=CONVERSION_TIMEOUT,
                env={**os.environ, 'HOME': '/tmp'}  # Define HOME temporário
            )

            if result.returncode != 0:
                logger.error(f"Erro LibreOffice (código {result.returncode})")
                logger.error(f"STDOUT: {result.stdout}")
                logger.error(f"STDERR: {result.stderr}")
                raise Exception(f"Erro na conversão para PDF: {result.stderr}")

            logger.info(f"LibreOffice output: {result.stdout}")

            # LibreOffice salva com o mesmo nome base do arquivo de entrada
            generated_pdf = os.path.join(
                os.path.dirname(pdf_path),
                os.path.splitext(os.path.basename(docx_path))[0] + '.pdf'
            )

            # Verifica se PDF foi gerado
            if not os.path.exists(generated_pdf):
                raise Exception(f"PDF não foi gerado. Arquivo esperado: {generated_pdf}")

            # Obtém tamanho do PDF gerado
            pdf_size = os.path.getsize(generated_pdf)
            logger.info(f"PDF gerado com sucesso: {pdf_size / 1024:.2f} KB")

            # Renomeia se necessário
            if generated_pdf != pdf_path:
                os.rename(generated_pdf, pdf_path)
                logger.info(f"PDF renomeado para: {os.path.basename(pdf_path)}")

        except subprocess.TimeoutExpired:
            logger.error(f"Timeout na conversão do documento (limite: {CONVERSION_TIMEOUT}s)")
            raise Exception(ERROR_MESSAGES['conversion_timeout'])
        except Exception as e:
            logger.error(f"Erro na conversão: {str(e)}")
            raise
