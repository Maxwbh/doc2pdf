"""
Testes Específicos - ListaVendas.docx

Testes dedicados ao documento ListaVendas.docx conforme especificado
no planejamento de testes.

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
Versão: 1.5.2
"""
import pytest
import os
from docx import Document
from app.services.docx_service import DocxService
from app.services.pdf_service import PdfService


class TestListaVendasDocument:
    """Testes específicos para o documento ListaVendas.docx"""

    def test_lista_vendas_exists(self, lista_vendas_path):
        """Deve encontrar o documento ListaVendas.docx"""
        assert lista_vendas_path.exists(), "Arquivo ListaVendas.docx não encontrado"
        assert lista_vendas_path.suffix == '.docx', "Arquivo deve ter extensão .docx"

    def test_lista_vendas_is_valid_docx(self, lista_vendas_bytes):
        """Deve ser um arquivo DOCX válido"""
        # DOCX é um ZIP que começa com PK
        assert lista_vendas_bytes.startswith(b'PK'), "Arquivo não é um DOCX válido"
        assert len(lista_vendas_bytes) > 0, "Arquivo está vazio"

    def test_lista_vendas_contains_tags(self, lista_vendas_bytes):
        """Deve conter as tags especificadas"""
        doc = Document(io.BytesIO(lista_vendas_bytes))
        text = '\n'.join([p.text for p in doc.paragraphs])

        # Verifica que as tags estão presentes no documento original
        assert '{NOME_CLIENTE}' in text, "Tag NOME_CLIENTE não encontrada"
        assert '{DATA_VENDA}' in text, "Tag DATA_VENDA não encontrada"
        assert '{VALOR}' in text, "Tag VALOR não encontrada"

    def test_lista_vendas_has_title(self, lista_vendas_bytes):
        """Deve conter o título 'Listagem de Vendas'"""
        doc = Document(io.BytesIO(lista_vendas_bytes))
        text = '\n'.join([p.text for p in doc.paragraphs])

        assert 'Listagem de Vendas' in text, "Título não encontrado no documento"


class TestListaVendasReplacement:
    """Testes de substituição de tags no ListaVendas.docx"""

    def test_replace_nome_cliente(self, lista_vendas_bytes):
        """Deve substituir tag NOME_CLIENTE corretamente"""
        replacements = {'NOME_CLIENTE': 'João Silva'}

        result_doc = DocxService.replace_tags_in_doc(lista_vendas_bytes, replacements)
        text = '\n'.join([p.text for p in result_doc.paragraphs])

        assert 'João Silva' in text, "NOME_CLIENTE não foi substituído"
        assert '{NOME_CLIENTE}' not in text, "Tag NOME_CLIENTE ainda presente"

    def test_replace_data_venda(self, lista_vendas_bytes):
        """Deve substituir tag DATA_VENDA corretamente"""
        replacements = {'DATA_VENDA': '06/12/2025'}

        result_doc = DocxService.replace_tags_in_doc(lista_vendas_bytes, replacements)
        text = '\n'.join([p.text for p in result_doc.paragraphs])

        assert '06/12/2025' in text, "DATA_VENDA não foi substituído"
        assert '{DATA_VENDA}' not in text, "Tag DATA_VENDA ainda presente"

    def test_replace_valor(self, lista_vendas_bytes):
        """Deve substituir tag VALOR corretamente"""
        replacements = {'VALOR': 'R$ 1.500,00'}

        result_doc = DocxService.replace_tags_in_doc(lista_vendas_bytes, replacements)
        text = '\n'.join([p.text for p in result_doc.paragraphs])

        assert 'R$ 1.500,00' in text, "VALOR não foi substituído"
        assert '{VALOR}' not in text, "Tag VALOR ainda presente"

    def test_replace_all_tags_lista_vendas(self, lista_vendas_bytes, replacements_lista_vendas):
        """Deve substituir todas as tags do ListaVendas.docx"""
        result_doc = DocxService.replace_tags_in_doc(
            lista_vendas_bytes,
            replacements_lista_vendas
        )

        text = '\n'.join([p.text for p in result_doc.paragraphs])

        # Verifica que todos os valores foram inseridos
        assert 'João Silva' in text
        assert '06/12/2025' in text
        assert 'R$ 1.500,00' in text

        # Verifica que nenhuma tag permanece
        assert '{NOME_CLIENTE}' not in text
        assert '{DATA_VENDA}' not in text
        assert '{VALOR}' not in text

    def test_lista_vendas_preserves_title(self, lista_vendas_bytes, replacements_lista_vendas):
        """Deve preservar o título após substituições"""
        result_doc = DocxService.replace_tags_in_doc(
            lista_vendas_bytes,
            replacements_lista_vendas
        )

        text = '\n'.join([p.text for p in result_doc.paragraphs])
        assert 'Listagem de Vendas' in text, "Título foi alterado ou removido"


class TestListaVendasConversion:
    """Testes de conversão PDF do ListaVendas.docx"""

    def test_convert_lista_vendas_to_pdf_high(self, lista_vendas_path, temp_dir):
        """Deve converter ListaVendas.docx para PDF (alta qualidade)"""
        pdf_path = temp_dir / 'lista_vendas_high.pdf'

        PdfService.convert_docx_to_pdf(
            str(lista_vendas_path),
            str(pdf_path),
            quality='high'
        )

        assert pdf_path.exists(), "PDF não foi gerado"
        assert pdf_path.stat().st_size > 0, "PDF está vazio"

        # Valida formato PDF
        with open(pdf_path, 'rb') as f:
            content = f.read()
            assert content.startswith(b'%PDF'), "Arquivo não é um PDF válido"
            assert b'%%EOF' in content, "PDF não tem marcador de fim"

    def test_convert_lista_vendas_to_pdf_medium(self, lista_vendas_path, temp_dir):
        """Deve converter ListaVendas.docx para PDF (média qualidade)"""
        pdf_path = temp_dir / 'lista_vendas_medium.pdf'

        PdfService.convert_docx_to_pdf(
            str(lista_vendas_path),
            str(pdf_path),
            quality='medium'
        )

        assert pdf_path.exists()
        assert pdf_path.stat().st_size > 0

    def test_convert_lista_vendas_to_pdf_low(self, lista_vendas_path, temp_dir):
        """Deve converter ListaVendas.docx para PDF (baixa qualidade)"""
        pdf_path = temp_dir / 'lista_vendas_low.pdf'

        PdfService.convert_docx_to_pdf(
            str(lista_vendas_path),
            str(pdf_path),
            quality='low'
        )

        assert pdf_path.exists()
        assert pdf_path.stat().st_size > 0


class TestListaVendasFullWorkflow:
    """Testes do fluxo completo com ListaVendas.docx"""

    def test_full_workflow_replace_and_convert(
        self,
        lista_vendas_bytes,
        replacements_lista_vendas,
        temp_dir
    ):
        """Testa fluxo completo: substituir tags → converter para PDF"""
        # Passo 1: Substituir tags
        modified_doc = DocxService.replace_tags_in_doc(
            lista_vendas_bytes,
            replacements_lista_vendas
        )

        # Passo 2: Salvar DOCX modificado
        docx_path = temp_dir / 'lista_vendas_modified.docx'
        modified_doc.save(str(docx_path))

        assert docx_path.exists(), "DOCX modificado não foi salvo"

        # Passo 3: Converter para PDF
        pdf_path = temp_dir / 'lista_vendas_final.pdf'
        PdfService.convert_docx_to_pdf(
            str(docx_path),
            str(pdf_path),
            quality='high'
        )

        assert pdf_path.exists(), "PDF final não foi gerado"
        assert pdf_path.stat().st_size > 500, "PDF muito pequeno"

        # Validação do PDF
        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()
            assert pdf_content.startswith(b'%PDF')
            assert b'%%EOF' in pdf_content

    def test_workflow_preserves_data(
        self,
        lista_vendas_bytes,
        replacements_lista_vendas,
        temp_dir
    ):
        """Verifica que os dados são preservados no workflow completo"""
        # Substituir
        modified_doc = DocxService.replace_tags_in_doc(
            lista_vendas_bytes,
            replacements_lista_vendas
        )

        # Salvar e reabrir
        docx_path = temp_dir / 'test.docx'
        modified_doc.save(str(docx_path))

        reopened_doc = Document(str(docx_path))
        text = '\n'.join([p.text for p in reopened_doc.paragraphs])

        # Dados devem estar presentes
        assert 'João Silva' in text
        assert '06/12/2025' in text
        assert 'R$ 1.500,00' in text

        # Tags não devem estar presentes
        assert '{NOME_CLIENTE}' not in text
        assert '{DATA_VENDA}' not in text
        assert '{VALOR}' not in text

    def test_workflow_completes_in_reasonable_time(
        self,
        lista_vendas_bytes,
        replacements_lista_vendas,
        temp_dir
    ):
        """Workflow completo deve ser executado em tempo razoável"""
        import time

        start = time.time()

        # Substituir tags
        modified_doc = DocxService.replace_tags_in_doc(
            lista_vendas_bytes,
            replacements_lista_vendas
        )

        # Salvar
        docx_path = temp_dir / 'timed.docx'
        modified_doc.save(str(docx_path))

        # Converter
        pdf_path = temp_dir / 'timed.pdf'
        PdfService.convert_docx_to_pdf(
            str(docx_path),
            str(pdf_path),
            quality='medium'
        )

        duration = time.time() - start

        # Deve completar em menos de 30 segundos
        assert duration < 30, f"Workflow levou {duration:.2f}s (máximo: 30s)"


class TestListaVendasEdgeCases:
    """Testes de casos extremos com ListaVendas.docx"""

    def test_lista_vendas_empty_replacements(self, lista_vendas_bytes):
        """Deve lidar com replacements vazios"""
        result_doc = DocxService.replace_tags_in_doc(lista_vendas_bytes, {})

        text = '\n'.join([p.text for p in result_doc.paragraphs])

        # Tags originais devem permanecer
        assert '{NOME_CLIENTE}' in text
        assert '{DATA_VENDA}' in text
        assert '{VALOR}' in text

    def test_lista_vendas_partial_replacement(self, lista_vendas_bytes):
        """Deve substituir apenas tags especificadas"""
        replacements = {
            'NOME_CLIENTE': 'Maria Santos'
            # Não inclui DATA_VENDA nem VALOR
        }

        result_doc = DocxService.replace_tags_in_doc(lista_vendas_bytes, replacements)
        text = '\n'.join([p.text for p in result_doc.paragraphs])

        # Substituída
        assert 'Maria Santos' in text
        assert '{NOME_CLIENTE}' not in text

        # Não substituídas (devem permanecer)
        assert '{DATA_VENDA}' in text
        assert '{VALOR}' in text

    def test_lista_vendas_with_special_characters(self, lista_vendas_bytes):
        """Deve aceitar valores com caracteres especiais"""
        replacements = {
            'NOME_CLIENTE': 'José María Öztürk',
            'DATA_VENDA': '25/12/2025',
            'VALOR': 'R$ 1.234.567,89'
        }

        result_doc = DocxService.replace_tags_in_doc(lista_vendas_bytes, replacements)
        text = '\n'.join([p.text for p in result_doc.paragraphs])

        assert 'José María Öztürk' in text
        assert 'R$ 1.234.567,89' in text

    def test_lista_vendas_with_very_long_values(self, lista_vendas_bytes):
        """Deve lidar com valores muito longos"""
        long_name = 'X' * 500
        replacements = {
            'NOME_CLIENTE': long_name,
            'DATA_VENDA': '06/12/2025',
            'VALOR': 'R$ 1.500,00'
        }

        result_doc = DocxService.replace_tags_in_doc(lista_vendas_bytes, replacements)
        text = '\n'.join([p.text for p in result_doc.paragraphs])

        assert long_name in text

    def test_lista_vendas_with_numeric_values(self, lista_vendas_bytes):
        """Deve converter valores numéricos para string"""
        replacements = {
            'NOME_CLIENTE': 'Cliente 123',
            'DATA_VENDA': 20251206,  # Número
            'VALOR': 1500.50  # Float
        }

        result_doc = DocxService.replace_tags_in_doc(lista_vendas_bytes, replacements)
        text = '\n'.join([p.text for p in result_doc.paragraphs])

        # Valores devem ser convertidos para string
        assert '20251206' in text or '2025' in text
        assert '1500' in text


# Fixture necessária para alguns testes
import io
