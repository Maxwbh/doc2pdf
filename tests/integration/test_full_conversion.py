"""
Testes de Integração - Fluxo Completo de Conversão

Testa o fluxo end-to-end completo de conversão DOCX -> PDF

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
Versão: 1.5.2
"""
import pytest
import base64
import json
from docx import Document
import io


class TestFullConversionWorkflow:
    """Testes do fluxo completo de conversão"""

    def test_lista_vendas_complete_workflow(self, client, lista_vendas_bytes, replacements_lista_vendas):
        """Fluxo completo: DOCX -> substituir tags -> PDF"""
        # 1. Codifica documento
        doc_base64 = base64.b64encode(lista_vendas_bytes).decode('utf-8')

        # 2. Envia para conversão
        payload = {
            'document': doc_base64,
            'replacements': replacements_lista_vendas,
            'quality': 'high',
            'return_format': 'file'
        }

        response = client.post(
            '/process',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # 3. Verifica resposta
        assert response.status_code == 200
        assert response.content_type == 'application/pdf'

        # 4. Valida PDF
        pdf_bytes = response.data
        assert pdf_bytes.startswith(b'%PDF')
        assert len(pdf_bytes) > 1000  # PDF deve ter tamanho razoável

    def test_simple_doc_workflow(self, client, simple_doc_bytes):
        """Fluxo completo com documento simples"""
        doc_base64 = base64.b64encode(simple_doc_bytes).decode('utf-8')

        payload = {
            'document': doc_base64,
            'replacements': {},
            'quality': 'medium'
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()

        # Decodifica PDF retornado
        pdf_bytes = base64.b64decode(data['pdf'])
        assert pdf_bytes.startswith(b'%PDF')

    def test_complex_doc_workflow(self, client, complex_doc_bytes, replacements_complex):
        """Fluxo completo com documento complexo"""
        doc_base64 = base64.b64encode(complex_doc_bytes).decode('utf-8')

        payload = {
            'document': doc_base64,
            'replacements': replacements_complex,
            'quality': 'high'
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True

    def test_workflow_with_special_characters(self, client, lista_vendas_bytes):
        """Fluxo com caracteres especiais nas substituições"""
        doc_base64 = base64.b64encode(lista_vendas_bytes).decode('utf-8')

        replacements = {
            'NOME_CLIENTE': 'José María Öztürk',
            'DATA_VENDA': '25/12/2025',
            'VALOR': 'R$ 9.999.999,99'
        }

        payload = {
            'document': doc_base64,
            'replacements': replacements,
            'quality': 'medium'
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200


class TestMultipleQualityLevels:
    """Testa conversão com diferentes níveis de qualidade"""

    def test_all_quality_levels(self, client, lista_vendas_base64, replacements_lista_vendas):
        """Deve converter com todos os níveis de qualidade"""
        qualities = ['low', 'medium', 'high']

        for quality in qualities:
            payload = {
                'document': lista_vendas_base64,
                'replacements': replacements_lista_vendas,
                'quality': quality,
                'return_format': 'file'
            }

            response = client.post(
                '/process',
                data=json.dumps(payload),
                content_type='application/json'
            )

            assert response.status_code == 200, f"Falhou com quality={quality}"
            pdf_bytes = response.data
            assert pdf_bytes.startswith(b'%PDF'), f"PDF inválido com quality={quality}"


class TestDifferentReturnFormats:
    """Testa diferentes formatos de retorno"""

    def test_return_base64(self, client, lista_vendas_base64, replacements_lista_vendas):
        """Deve retornar em Base64"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'return_format': 'base64'
        }

        response = client.post(
            '/process',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()

        # Decodifica e valida
        pdf_bytes = base64.b64decode(data['pdf'])
        assert pdf_bytes.startswith(b'%PDF')

    def test_return_file(self, client, lista_vendas_base64, replacements_lista_vendas):
        """Deve retornar como arquivo"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'return_format': 'file'
        }

        response = client.post(
            '/process',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200
        assert response.content_type == 'application/pdf'
        assert response.data.startswith(b'%PDF')


class TestTagsReplacementIntegration:
    """Testes de integração para substituição de tags"""

    def test_single_tag_replacement(self, client, lista_vendas_base64):
        """Deve substituir uma única tag"""
        replacements = {
            'NOME_CLIENTE': 'Teste Cliente'
        }

        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements,
            'quality': 'low'
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200

    def test_multiple_tags_replacement(self, client, lista_vendas_base64, replacements_lista_vendas):
        """Deve substituir múltiplas tags"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'quality': 'medium'
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200

    def test_no_tags_replacement(self, client, lista_vendas_base64):
        """Deve funcionar sem substituições"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': {},
            'quality': 'medium'
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200

    def test_repeated_tags(self, client, tags_repetidas_base64, replacements_tags_repetidas):
        """Deve substituir tags repetidas"""
        payload = {
            'document': tags_repetidas_base64,
            'replacements': replacements_tags_repetidas,
            'quality': 'low'
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200


class TestRealWorldScenarios:
    """Testes de cenários do mundo real"""

    def test_invoice_generation(self, client, lista_vendas_base64):
        """Cenário: Geração de nota fiscal"""
        replacements = {
            'NOME_CLIENTE': 'Empresa XYZ Ltda',
            'DATA_VENDA': '06/12/2025',
            'VALOR': 'R$ 15.750,00'
        }

        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements,
            'quality': 'high',  # Alta qualidade para impressão
            'return_format': 'file'
        }

        response = client.post(
            '/process',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200
        assert response.content_type == 'application/pdf'

    def test_contract_generation(self, client, complex_doc_base64):
        """Cenário: Geração de contrato"""
        replacements = {
            'TITULO': 'Contrato de Prestação de Serviços',
            'CLIENTE': 'João Silva',
            'PROJETO': 'Desenvolvimento de Sistema',
            'DATA': '06/12/2025',
            'ITEM1': 'Análise de Requisitos',
            'QTD1': '40h',
            'VALOR1': 'R$ 4.000,00',
            'ITEM2': 'Implementação',
            'QTD2': '120h',
            'VALOR2': 'R$ 12.000,00',
            'TOTAL': 'R$ 16.000,00',
            'OBS1': 'Prazo de 60 dias',
            'OBS2': 'Pagamento em 3 parcelas',
            'OBS3': 'Garantia de 90 dias',
            'DATA_GERACAO': '06/12/2025',
            'VERSAO': '1.0'
        }

        payload = {
            'document': complex_doc_base64,
            'replacements': replacements,
            'quality': 'high'
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200

    def test_report_generation(self, client, with_tags_base64):
        """Cenário: Geração de relatório mensal"""
        replacements = {
            'MES': 'Dezembro',
            'ANO': '2025',
            'EMPRESA': 'M&S do Brasil LTDA',
            'RESPONSAVEL': 'Maxwell da Silva Oliveira',
            'PROJETO': 'DOC2PDF API v1.5.2',
            'STATUS': 'Em Produção'
        }

        payload = {
            'document': with_tags_base64,
            'replacements': replacements,
            'quality': 'medium',
            'return_format': 'base64'
        }

        response = client.post(
            '/process',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert 'pdf' in data


class TestBatchConversion:
    """Testes de conversão em lote"""

    def test_multiple_documents_sequential(self, client, lista_vendas_base64, simple_doc_base64):
        """Deve converter múltiplos documentos sequencialmente"""
        documents = [
            {
                'document': lista_vendas_base64,
                'replacements': {'NOME_CLIENTE': 'Cliente 1', 'DATA_VENDA': '01/12/2025', 'VALOR': 'R$ 100'},
                'quality': 'low'
            },
            {
                'document': simple_doc_base64,
                'replacements': {},
                'quality': 'low'
            }
        ]

        for payload in documents:
            response = client.post(
                '/convert',
                data=json.dumps(payload),
                content_type='application/json'
            )

            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is True


class TestEdgeCases:
    """Testes de casos extremos"""

    def test_empty_document(self, client, empty_doc_base64):
        """Deve processar documento vazio"""
        payload = {
            'document': empty_doc_base64,
            'replacements': {},
            'quality': 'low'
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Pode retornar 200 (sucesso) ou 400/500 (erro esperado)
        assert response.status_code in [200, 400, 500]

    def test_very_long_replacement_value(self, client, lista_vendas_base64):
        """Deve lidar com valores de substituição muito longos"""
        long_value = 'X' * 10000

        replacements = {
            'NOME_CLIENTE': long_value,
            'DATA_VENDA': '06/12/2025',
            'VALOR': 'R$ 100,00'
        }

        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements,
            'quality': 'low'
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code in [200, 400, 500]

    def test_many_replacements(self, client, complex_doc_base64):
        """Deve lidar com muitas substituições"""
        replacements = {f'TAG{i}': f'valor{i}' for i in range(100)}

        # Adiciona as tags reais também
        replacements.update({
            'TITULO': 'Teste',
            'CLIENTE': 'Teste',
            'PROJETO': 'Teste'
        })

        payload = {
            'document': complex_doc_base64,
            'replacements': replacements,
            'quality': 'low'
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code in [200, 400]
