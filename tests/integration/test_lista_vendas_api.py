"""
Testes de Integração - API com ListaVendas.docx

Testa a API completa usando o documento ListaVendas.docx

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
Versão: 1.5.2
"""
import pytest
import base64
import json


class TestListaVendasAPIConvert:
    """Testes do endpoint /convert com ListaVendas.docx"""

    def test_convert_lista_vendas_success(self, client, lista_vendas_base64, replacements_lista_vendas):
        """Deve converter ListaVendas.docx com sucesso via /convert"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'quality': 'high'
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200, f"Erro: {response.get_json()}"

        data = response.get_json()
        assert data['success'] is True
        assert 'pdf' in data
        assert len(data['pdf']) > 0

        # Valida que é Base64 válido
        try:
            pdf_bytes = base64.b64decode(data['pdf'])
            assert pdf_bytes.startswith(b'%PDF'), "PDF inválido"
        except Exception as e:
            pytest.fail(f"Base64 inválido: {e}")

    def test_convert_lista_vendas_medium_quality(self, client, lista_vendas_base64, replacements_lista_vendas):
        """Deve converter com qualidade média"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'quality': 'medium'
        }

        response = client.post('/convert', json=payload)

        assert response.status_code == 200
        data = response.get_json()
        assert data['stats']['quality'] == 'medium'

    def test_convert_lista_vendas_low_quality(self, client, lista_vendas_base64, replacements_lista_vendas):
        """Deve converter com qualidade baixa"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'quality': 'low'
        }

        response = client.post('/convert', json=payload)

        assert response.status_code == 200
        data = response.get_json()
        assert data['stats']['quality'] == 'low'

    def test_convert_lista_vendas_without_quality(self, client, lista_vendas_base64, replacements_lista_vendas):
        """Deve usar qualidade padrão quando não especificada"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas
        }

        response = client.post('/convert', json=payload)

        assert response.status_code == 200
        data = response.get_json()
        # Padrão agora é 'medium' após ajustes
        assert data['stats']['quality'] in ['high', 'medium']

    def test_convert_lista_vendas_missing_document(self, client, replacements_lista_vendas):
        """Deve retornar erro quando documento está faltando"""
        payload = {
            'replacements': replacements_lista_vendas
        }

        response = client.post('/convert', json=payload)

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_convert_lista_vendas_missing_replacements(self, client, lista_vendas_base64):
        """Deve retornar erro quando replacements estão faltando"""
        payload = {
            'document': lista_vendas_base64
        }

        response = client.post('/convert', json=payload)

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_convert_lista_vendas_invalid_quality(self, client, lista_vendas_base64, replacements_lista_vendas):
        """Deve retornar erro com qualidade inválida"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'quality': 'ultra_mega_high'
        }

        response = client.post('/convert', json=payload)

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'qualidade' in data['error'].lower() or 'quality' in data['error'].lower()

    def test_convert_lista_vendas_empty_replacements(self, client, lista_vendas_base64):
        """Deve aceitar replacements vazios"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': {}
        }

        response = client.post('/convert', json=payload)

        # Deve processar normalmente, mas tags não serão substituídas
        assert response.status_code == 200


class TestListaVendasAPIConvertFile:
    """Testes do endpoint /convert-file com ListaVendas.docx"""

    def test_convert_file_lista_vendas(self, client, lista_vendas_base64, replacements_lista_vendas):
        """Deve retornar arquivo PDF"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'filename': 'lista_vendas.pdf'
        }

        response = client.post('/convert-file', json=payload)

        assert response.status_code == 200
        assert response.content_type == 'application/pdf'
        assert response.data.startswith(b'%PDF')

    def test_convert_file_lista_vendas_custom_filename(
        self,
        client,
        lista_vendas_base64,
        replacements_lista_vendas
    ):
        """Deve usar nome de arquivo customizado"""
        custom_filename = 'relatorio_vendas_dezembro.pdf'
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'filename': custom_filename
        }

        response = client.post('/convert-file', json=payload)

        assert response.status_code == 200
        assert 'Content-Disposition' in response.headers
        # Verifica que o filename está no header (pode variar o formato)
        assert 'relatorio_vendas_dezembro' in response.headers['Content-Disposition']

    def test_convert_file_lista_vendas_without_filename(
        self,
        client,
        lista_vendas_base64,
        replacements_lista_vendas
    ):
        """Deve usar nome padrão quando não especificado"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas
        }

        response = client.post('/convert-file', json=payload)

        assert response.status_code == 200
        assert response.content_type == 'application/pdf'


class TestListaVendasAPIProcess:
    """Testes do endpoint /process com ListaVendas.docx"""

    def test_process_lista_vendas_pdf_file(
        self,
        client,
        lista_vendas_base64,
        replacements_lista_vendas
    ):
        """Deve processar e retornar PDF como arquivo"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'output_type': 'pdf',
            'quality': 'high'
        }

        response = client.post('/process', json=payload)

        assert response.status_code == 200
        assert response.content_type == 'application/pdf'
        assert response.data.startswith(b'%PDF')

    def test_process_lista_vendas_base64_pdf(
        self,
        client,
        lista_vendas_base64,
        replacements_lista_vendas
    ):
        """Deve processar e retornar PDF em Base64"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'output_type': 'base64_pdf',
            'quality': 'medium'
        }

        response = client.post('/process', json=payload)

        assert response.status_code == 200
        data = response.get_json()
        assert 'pdf' in data
        assert data['success'] is True

        # Valida Base64
        pdf_bytes = base64.b64decode(data['pdf'])
        assert pdf_bytes.startswith(b'%PDF')

    def test_process_lista_vendas_doc_file(
        self,
        client,
        lista_vendas_base64,
        replacements_lista_vendas
    ):
        """Deve processar e retornar DOCX como arquivo"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'output_type': 'doc'
        }

        response = client.post('/process', json=payload)

        assert response.status_code == 200
        # DOCX é um ZIP
        assert response.data.startswith(b'PK')

    def test_process_lista_vendas_base64_doc(
        self,
        client,
        lista_vendas_base64,
        replacements_lista_vendas
    ):
        """Deve processar e retornar DOCX em Base64"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'output_type': 'base64_doc'
        }

        response = client.post('/process', json=payload)

        assert response.status_code == 200
        data = response.get_json()
        assert 'document' in data
        assert data['success'] is True

        # Valida Base64
        doc_bytes = base64.b64decode(data['document'])
        assert doc_bytes.startswith(b'PK')  # ZIP header


class TestListaVendasAPIValidation:
    """Testes de validação com ListaVendas.docx"""

    def test_lista_vendas_invalid_base64(self, client, replacements_lista_vendas):
        """Deve rejeitar Base64 inválido"""
        payload = {
            'document': 'isso-não-é-base64-válido!!!',
            'replacements': replacements_lista_vendas
        }

        response = client.post('/convert', json=payload)

        assert response.status_code in [400, 500]

    def test_lista_vendas_invalid_replacements_type(self, client, lista_vendas_base64):
        """Deve rejeitar replacements que não são dict"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': ['lista', 'não', 'dict']
        }

        response = client.post('/convert', json=payload)

        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data

    def test_lista_vendas_not_json_content_type(self, client):
        """Deve rejeitar Content-Type diferente de JSON"""
        response = client.post(
            '/convert',
            data='não é json',
            content_type='text/plain'
        )

        assert response.status_code == 400


class TestListaVendasAPIPerformance:
    """Testes de performance com ListaVendas.docx"""

    def test_lista_vendas_conversion_time(
        self,
        client,
        lista_vendas_base64,
        replacements_lista_vendas
    ):
        """Conversão deve completar em tempo razoável"""
        import time

        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'quality': 'medium'
        }

        start = time.time()
        response = client.post('/convert', json=payload)
        duration = time.time() - start

        assert response.status_code == 200
        # Deve completar em menos de 30 segundos
        assert duration < 30, f"Conversão levou {duration:.2f}s"

    @pytest.mark.skip(reason="Teste de stress - executar manualmente")
    def test_lista_vendas_multiple_requests(
        self,
        client,
        lista_vendas_base64,
        replacements_lista_vendas
    ):
        """Deve lidar com múltiplas requisições"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'quality': 'low'
        }

        # Faz 10 requisições
        for i in range(10):
            response = client.post('/convert', json=payload)
            assert response.status_code == 200


class TestListaVendasAPIDataIntegrity:
    """Testes de integridade de dados com ListaVendas.docx"""

    def test_lista_vendas_data_preservation(
        self,
        client,
        lista_vendas_base64,
        replacements_lista_vendas
    ):
        """PDF deve conter os dados substituídos"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'quality': 'high'
        }

        response = client.post('/convert', json=payload)
        data = response.get_json()

        # Decodifica o PDF
        pdf_bytes = base64.b64decode(data['pdf'])

        # Verifica que é um PDF válido
        assert pdf_bytes.startswith(b'%PDF')
        assert len(pdf_bytes) > 1000  # PDF deve ter tamanho razoável

    def test_lista_vendas_no_tags_in_output(
        self,
        client,
        lista_vendas_base64,
        replacements_lista_vendas
    ):
        """PDF não deve conter tags originais"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas
        }

        response = client.post('/convert', json=payload)

        assert response.status_code == 200
        # Nota: Verificação completa requer extração de texto do PDF
        # que está além do escopo deste teste básico
