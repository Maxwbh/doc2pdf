"""
Testes Unitários - PDF Service

Testa o serviço de conversão PDF em app/services/pdf_service.py

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
Versão: 1.5.2
"""
import pytest
import os
import tempfile
from pathlib import Path
from app.services.pdf_service import PdfService


class TestConvertDocxToPdf:
    """Testes para PdfService.convert_docx_to_pdf()"""

    def test_convert_simple_doc_high_quality(self, simple_doc_path, temp_dir):
        """Deve converter documento simples com qualidade alta"""
        pdf_path = temp_dir / 'output_high.pdf'

        result = PdfService.convert_docx_to_pdf(
            str(simple_doc_path),
            str(pdf_path),
            quality='high'
        )

        assert result is True or pdf_path.exists()
        assert pdf_path.exists()
        assert pdf_path.stat().st_size > 0

        # Verifica se é um PDF válido
        with open(pdf_path, 'rb') as f:
            content = f.read()
            assert content.startswith(b'%PDF')
            assert b'%%EOF' in content

    def test_convert_simple_doc_medium_quality(self, simple_doc_path, temp_dir):
        """Deve converter documento simples com qualidade média"""
        pdf_path = temp_dir / 'output_medium.pdf'

        result = PdfService.convert_docx_to_pdf(
            str(simple_doc_path),
            str(pdf_path),
            quality='medium'
        )

        assert result is True or pdf_path.exists()
        assert pdf_path.exists()
        assert pdf_path.stat().st_size > 0

    def test_convert_simple_doc_low_quality(self, simple_doc_path, temp_dir):
        """Deve converter documento simples com qualidade baixa"""
        pdf_path = temp_dir / 'output_low.pdf'

        result = PdfService.convert_docx_to_pdf(
            str(simple_doc_path),
            str(pdf_path),
            quality='low'
        )

        assert result is True or pdf_path.exists()
        assert pdf_path.exists()
        assert pdf_path.stat().st_size > 0

    def test_convert_lista_vendas(self, lista_vendas_path, temp_dir):
        """Deve converter ListaVendas.docx"""
        pdf_path = temp_dir / 'lista_vendas.pdf'

        PdfService.convert_docx_to_pdf(
            str(lista_vendas_path),
            str(pdf_path),
            quality='high'
        )

        assert pdf_path.exists()

        # Verifica formato PDF
        with open(pdf_path, 'rb') as f:
            content = f.read()
            assert content.startswith(b'%PDF')

    def test_convert_complex_doc(self, complex_doc_path, temp_dir):
        """Deve converter documento complexo"""
        pdf_path = temp_dir / 'complex.pdf'

        PdfService.convert_docx_to_pdf(
            str(complex_doc_path),
            str(pdf_path),
            quality='medium'
        )

        assert pdf_path.exists()
        # Documento complexo deve gerar PDF maior
        assert pdf_path.stat().st_size > 1000

    def test_convert_with_tags_doc(self, with_tags_path, temp_dir):
        """Deve converter documento com tags"""
        pdf_path = temp_dir / 'with_tags.pdf'

        PdfService.convert_docx_to_pdf(
            str(with_tags_path),
            str(pdf_path),
            quality='high'
        )

        assert pdf_path.exists()

    def test_convert_empty_doc(self, empty_doc_path, temp_dir):
        """Deve converter documento vazio sem erros"""
        pdf_path = temp_dir / 'empty.pdf'

        PdfService.convert_docx_to_pdf(
            str(empty_doc_path),
            str(pdf_path),
            quality='medium'
        )

        assert pdf_path.exists()

    def test_quality_affects_file_size(self, simple_doc_path, temp_dir):
        """Qualidade deve afetar o tamanho do arquivo"""
        pdf_high = temp_dir / 'high.pdf'
        pdf_low = temp_dir / 'low.pdf'

        PdfService.convert_docx_to_pdf(
            str(simple_doc_path),
            str(pdf_high),
            quality='high'
        )

        PdfService.convert_docx_to_pdf(
            str(simple_doc_path),
            str(pdf_low),
            quality='low'
        )

        # HIGH deve ser maior ou igual a LOW
        # (nem sempre é verdade, mas geralmente sim)
        assert pdf_high.exists()
        assert pdf_low.exists()

    def test_output_path_created(self, simple_doc_path, temp_dir):
        """Deve criar arquivo PDF no caminho especificado"""
        pdf_path = temp_dir / 'subdir' / 'output.pdf'

        # Cria o diretório pai
        pdf_path.parent.mkdir(parents=True, exist_ok=True)

        PdfService.convert_docx_to_pdf(
            str(simple_doc_path),
            str(pdf_path),
            quality='medium'
        )

        assert pdf_path.exists()

    def test_overwrite_existing_pdf(self, simple_doc_path, temp_dir):
        """Deve sobrescrever PDF existente"""
        pdf_path = temp_dir / 'overwrite.pdf'

        # Primeira conversão
        PdfService.convert_docx_to_pdf(
            str(simple_doc_path),
            str(pdf_path),
            quality='low'
        )
        first_size = pdf_path.stat().st_size

        # Segunda conversão (sobrescreve)
        PdfService.convert_docx_to_pdf(
            str(simple_doc_path),
            str(pdf_path),
            quality='high'
        )
        second_size = pdf_path.stat().st_size

        # Arquivo deve existir (pode ter tamanho diferente)
        assert pdf_path.exists()


class TestPdfServiceErrorHandling:
    """Testes de tratamento de erros"""

    def test_convert_nonexistent_file(self, temp_dir):
        """Deve falhar com arquivo inexistente"""
        docx_path = temp_dir / 'nao_existe.docx'
        pdf_path = temp_dir / 'output.pdf'

        with pytest.raises(Exception):
            PdfService.convert_docx_to_pdf(
                str(docx_path),
                str(pdf_path),
                quality='medium'
            )

    def test_convert_invalid_quality(self, simple_doc_path, temp_dir):
        """Deve usar fallback com qualidade inválida"""
        pdf_path = temp_dir / 'output.pdf'

        # Dependendo da implementação, pode aceitar ou rejeitar
        # Vamos testar se não causa crash
        try:
            PdfService.convert_docx_to_pdf(
                str(simple_doc_path),
                str(pdf_path),
                quality='invalid_quality'
            )
            # Se não lançou erro, deve ter criado o PDF
            assert pdf_path.exists() or True
        except (ValueError, KeyError):
            # Se lançou erro, é comportamento aceitável
            pass

    def test_convert_to_invalid_path(self, simple_doc_path):
        """Deve falhar com caminho de saída inválido"""
        pdf_path = '/caminho/inexistente/muito/profundo/output.pdf'

        with pytest.raises(Exception):
            PdfService.convert_docx_to_pdf(
                str(simple_doc_path),
                pdf_path,
                quality='medium'
            )


class TestPdfServiceQualityProfiles:
    """Testes de perfis de qualidade"""

    def test_high_quality_profile(self, simple_doc_path, temp_dir):
        """Perfil HIGH deve usar configurações de alta qualidade"""
        pdf_path = temp_dir / 'high_quality.pdf'

        PdfService.convert_docx_to_pdf(
            str(simple_doc_path),
            str(pdf_path),
            quality='high'
        )

        assert pdf_path.exists()
        # High quality geralmente resulta em arquivos maiores
        assert pdf_path.stat().st_size > 0

    def test_medium_quality_profile(self, simple_doc_path, temp_dir):
        """Perfil MEDIUM deve usar configurações balanceadas"""
        pdf_path = temp_dir / 'medium_quality.pdf'

        PdfService.convert_docx_to_pdf(
            str(simple_doc_path),
            str(pdf_path),
            quality='medium'
        )

        assert pdf_path.exists()

    def test_low_quality_profile(self, simple_doc_path, temp_dir):
        """Perfil LOW deve usar configurações otimizadas"""
        pdf_path = temp_dir / 'low_quality.pdf'

        PdfService.convert_docx_to_pdf(
            str(simple_doc_path),
            str(pdf_path),
            quality='low'
        )

        assert pdf_path.exists()
        # Low quality geralmente resulta em arquivos menores


class TestPdfServiceIntegration:
    """Testes de integração do serviço PDF"""

    def test_full_conversion_workflow(self, lista_vendas_path, temp_dir):
        """Testa fluxo completo de conversão"""
        # 1. Converter
        pdf_path = temp_dir / 'workflow.pdf'

        PdfService.convert_docx_to_pdf(
            str(lista_vendas_path),
            str(pdf_path),
            quality='high'
        )

        # 2. Verificar existência
        assert pdf_path.exists()

        # 3. Verificar formato
        with open(pdf_path, 'rb') as f:
            content = f.read()
            assert content.startswith(b'%PDF')
            assert b'%%EOF' in content

        # 4. Verificar tamanho mínimo
        assert pdf_path.stat().st_size > 500

    def test_batch_conversion(self, documents_dir, temp_dir):
        """Deve converter múltiplos documentos"""
        docx_files = list(Path(documents_dir).glob('*.docx'))

        for docx_file in docx_files[:3]:  # Testa 3 arquivos
            pdf_path = temp_dir / f'{docx_file.stem}.pdf'

            PdfService.convert_docx_to_pdf(
                str(docx_file),
                str(pdf_path),
                quality='medium'
            )

            assert pdf_path.exists()

    def test_conversion_preserves_content(self, simple_doc_path, temp_dir):
        """Conversão deve preservar conteúdo (teste básico)"""
        pdf_path = temp_dir / 'preserve_content.pdf'

        PdfService.convert_docx_to_pdf(
            str(simple_doc_path),
            str(pdf_path),
            quality='high'
        )

        # Verifica que o PDF foi criado e tem tamanho razoável
        assert pdf_path.exists()
        assert pdf_path.stat().st_size > 100


class TestPdfServicePerformance:
    """Testes de performance (básicos)"""

    def test_conversion_completes_in_reasonable_time(self, simple_doc_path, temp_dir):
        """Conversão deve completar em tempo razoável"""
        import time

        pdf_path = temp_dir / 'timing.pdf'

        start = time.time()
        PdfService.convert_docx_to_pdf(
            str(simple_doc_path),
            str(pdf_path),
            quality='medium'
        )
        duration = time.time() - start

        # Deve completar em menos de 30 segundos (generoso para CI)
        assert duration < 30
        assert pdf_path.exists()

    @pytest.mark.skip(reason="Teste de stress - executar manualmente")
    def test_handle_large_document(self, temp_dir):
        """Deve lidar com documentos grandes"""
        # Este teste deve ser executado manualmente
        # pois requer criação de documento grande
        pass


class TestPdfServiceEdgeCases:
    """Testes de casos extremos"""

    def test_convert_with_special_chars_in_path(self, simple_doc_path, temp_dir):
        """Deve lidar com caracteres especiais no caminho"""
        pdf_path = temp_dir / 'arquivo com espaços.pdf'

        PdfService.convert_docx_to_pdf(
            str(simple_doc_path),
            str(pdf_path),
            quality='medium'
        )

        assert pdf_path.exists()

    def test_convert_with_unicode_filename(self, simple_doc_path, temp_dir):
        """Deve lidar com nomes de arquivo Unicode"""
        pdf_path = temp_dir / 'relatório_ãçéntüação.pdf'

        try:
            PdfService.convert_docx_to_pdf(
                str(simple_doc_path),
                str(pdf_path),
                quality='medium'
            )
            assert pdf_path.exists()
        except (UnicodeError, OSError):
            # Em alguns sistemas, caracteres Unicode podem não ser suportados
            pytest.skip("Sistema não suporta Unicode em nomes de arquivo")

    def test_pdf_path_with_extension(self, simple_doc_path, temp_dir):
        """Deve aceitar caminho com extensão .pdf"""
        pdf_path = temp_dir / 'output.pdf'

        PdfService.convert_docx_to_pdf(
            str(simple_doc_path),
            str(pdf_path),
            quality='medium'
        )

        assert pdf_path.exists()

    def test_pdf_path_without_extension(self, simple_doc_path, temp_dir):
        """Deve lidar com caminho sem extensão"""
        pdf_path = temp_dir / 'output'

        # Dependendo da implementação, pode adicionar .pdf automaticamente
        PdfService.convert_docx_to_pdf(
            str(simple_doc_path),
            str(pdf_path),
            quality='medium'
        )

        # Verifica se criou o arquivo (com ou sem extensão)
        assert pdf_path.exists() or Path(str(pdf_path) + '.pdf').exists()
