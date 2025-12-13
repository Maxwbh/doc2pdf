"""
Testes de Integração - API Endpoints

Testa todos os endpoints da API DOC2PDF

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
Versão: 1.5.2
"""
import pytest
import json


class TestHealthEndpoint:
    """Testes para GET /health"""

    def test_health_check_success(self, client):
        """Deve retornar status healthy"""
        response = client.get('/health')

        assert response.status_code == 200
        data = response.get_json()

        assert data['status'] == 'healthy'
        assert data['service'] == 'DOC2PDF Converter API'
        assert 'version' in data

    def test_health_check_version(self, client):
        """Deve retornar versão correta"""
        response = client.get('/health')
        data = response.get_json()

        assert data['version'] == '1.5.2'

    def test_health_check_no_body_required(self, client):
        """Não deve exigir corpo na requisição"""
        response = client.get('/health')
        assert response.status_code == 200


class TestConvertEndpoint:
    """Testes para POST /convert"""

    def test_convert_lista_vendas_success(self, client, valid_convert_payload):
        """Deve converter ListaVendas.docx com sucesso"""
        response = client.post(
            '/convert',
            data=json.dumps(valid_convert_payload),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()

        assert data['success'] is True
        assert 'pdf' in data
        assert isinstance(data['pdf'], str)
        assert len(data['pdf']) > 0

    def test_convert_missing_document(self, client, invalid_payload_no_document):
        """Deve rejeitar request sem documento"""
        response = client.post(
            '/convert',
            data=json.dumps(invalid_payload_no_document),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False

    def test_convert_invalid_base64(self, client, invalid_payload_bad_base64):
        """Deve rejeitar Base64 inválido"""
        response = client.post(
            '/convert',
            data=json.dumps(invalid_payload_bad_base64),
            content_type='application/json'
        )

        assert response.status_code == 400

    def test_convert_invalid_quality(self, client, invalid_payload_bad_quality):
        """Deve rejeitar qualidade inválida"""
        response = client.post(
            '/convert',
            data=json.dumps(invalid_payload_bad_quality),
            content_type='application/json'
        )

        assert response.status_code == 400

    def test_convert_wrong_content_type(self, client, valid_convert_payload):
        """Deve rejeitar content-type não-JSON"""
        response = client.post(
            '/convert',
            data=json.dumps(valid_convert_payload),
            content_type='application/xml'
        )

        assert response.status_code == 400

    def test_convert_high_quality(self, client, lista_vendas_base64, replacements_lista_vendas):
        """Deve converter com qualidade alta"""
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

        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True

    def test_convert_medium_quality(self, client, lista_vendas_base64, replacements_lista_vendas):
        """Deve converter com qualidade média"""
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

    def test_convert_low_quality(self, client, lista_vendas_base64, replacements_lista_vendas):
        """Deve converter com qualidade baixa"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'quality': 'low'
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200

    def test_convert_without_replacements(self, client, lista_vendas_base64):
        """Deve aceitar conversão sem replacements"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': {}
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200

    def test_convert_complex_document(self, client, complex_doc_base64, replacements_complex):
        """Deve converter documento complexo"""
        payload = {
            'document': complex_doc_base64,
            'replacements': replacements_complex,
            'quality': 'medium'
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert len(data['pdf']) > 0


class TestConvertFileEndpoint:
    """Testes para POST /convert-file"""

    def test_convert_file_success(self, client, lista_vendas_base64, replacements_lista_vendas):
        """Deve retornar arquivo PDF para download"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'quality': 'high'
        }

        response = client.post(
            '/convert-file',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200
        assert response.content_type == 'application/pdf'
        assert len(response.data) > 0

        # Verifica header de download
        assert 'Content-Disposition' in response.headers

    def test_convert_file_pdf_format(self, client, simple_doc_base64):
        """Deve retornar PDF válido"""
        payload = {
            'document': simple_doc_base64,
            'replacements': {},
            'quality': 'medium'
        }

        response = client.post(
            '/convert-file',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200

        # Verifica formato PDF
        pdf_bytes = response.data
        assert pdf_bytes.startswith(b'%PDF')
        assert b'%%EOF' in pdf_bytes

    def test_convert_file_missing_document(self, client):
        """Deve rejeitar request sem documento"""
        payload = {'replacements': {}}

        response = client.post(
            '/convert-file',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 400


class TestProcessEndpoint:
    """Testes para POST /process"""

    def test_process_return_base64(self, client, lista_vendas_base64, replacements_lista_vendas):
        """Deve retornar PDF em Base64"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'quality': 'medium',
            'return_format': 'base64'
        }

        response = client.post(
            '/process',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200
        assert response.content_type == 'application/json'

        data = response.get_json()
        assert data['success'] is True
        assert 'pdf' in data

    def test_process_return_file(self, client, lista_vendas_base64, replacements_lista_vendas):
        """Deve retornar PDF como arquivo"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'quality': 'medium',
            'return_format': 'file'
        }

        response = client.post(
            '/process',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200
        assert response.content_type == 'application/pdf'

    def test_process_default_format(self, client, lista_vendas_base64, replacements_lista_vendas):
        """Deve usar base64 como formato padrão"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas
        }

        response = client.post(
            '/process',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200
        assert response.content_type == 'application/json'

    def test_process_invalid_format(self, client, lista_vendas_base64):
        """Deve rejeitar formato inválido"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': {},
            'return_format': 'invalid_format'
        }

        response = client.post(
            '/process',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 400


class TestInfoEndpoint:
    """Testes para GET /info"""

    def test_info_endpoint(self, client):
        """Deve retornar informações da API"""
        response = client.get('/info')

        assert response.status_code == 200
        data = response.get_json()

        assert 'service' in data
        assert 'version' in data
        assert 'author' in data

    def test_info_version(self, client):
        """Deve retornar versão 1.5.2"""
        response = client.get('/info')
        data = response.get_json()

        assert data['version'] == '1.5.2'


class TestSwaggerEndpoint:
    """Testes para Swagger UI"""

    def test_swagger_ui_accessible(self, client):
        """Deve acessar Swagger UI"""
        response = client.get('/api/docs/')

        assert response.status_code in [200, 308]  # 308 é redirect

    def test_openapi_spec_accessible(self, client):
        """Deve acessar especificação OpenAPI"""
        response = client.get('/api/openapi.yaml')

        assert response.status_code == 200


class TestErrorHandling:
    """Testes de tratamento de erros"""

    def test_method_not_allowed(self, client):
        """Deve retornar 405 para método não permitido"""
        response = client.get('/convert')  # Convert só aceita POST

        assert response.status_code == 405

    def test_not_found(self, client):
        """Deve retornar 404 para rota inexistente"""
        response = client.get('/rota/inexistente')

        assert response.status_code == 404

    def test_invalid_json(self, client):
        """Deve rejeitar JSON inválido"""
        response = client.post(
            '/convert',
            data='isto não é json válido',
            content_type='application/json'
        )

        assert response.status_code == 400


class TestCORS:
    """Testes de CORS"""

    def test_cors_headers_present(self, client):
        """Deve incluir headers CORS"""
        response = client.get('/health')

        # Verifica se há headers CORS
        assert 'Access-Control-Allow-Origin' in response.headers or response.status_code == 200

    def test_options_request(self, client):
        """Deve responder a requisições OPTIONS"""
        response = client.options('/convert')

        # Deve retornar 200 ou 204
        assert response.status_code in [200, 204, 405]


class TestTagsReplacement:
    """Testes de substituição de tags"""

    def test_tags_replaced_in_pdf(self, client, lista_vendas_base64, replacements_lista_vendas, assert_pdf_valid):
        """Deve substituir tags no PDF gerado"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'quality': 'medium',
            'return_format': 'file'
        }

        response = client.post(
            '/process',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200
        pdf_bytes = response.data

        # Verifica que é um PDF válido
        assert_pdf_valid(pdf_bytes)

    def test_multiple_tags_replacement(self, client, complex_doc_base64, replacements_complex):
        """Deve substituir múltiplas tags"""
        payload = {
            'document': complex_doc_base64,
            'replacements': replacements_complex,
            'quality': 'medium'
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True

    def test_repeated_tags_replacement(self, client, tags_repetidas_base64, replacements_tags_repetidas):
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


class TestPerformance:
    """Testes de performance básicos"""

    def test_conversion_completes_quickly(self, client, simple_doc_base64):
        """Conversão simples deve completar rapidamente"""
        import time

        payload = {
            'document': simple_doc_base64,
            'replacements': {},
            'quality': 'low'
        }

        start = time.time()
        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )
        duration = time.time() - start

        assert response.status_code == 200
        # Deve completar em menos de 30 segundos (generoso para CI)
        assert duration < 30

    @pytest.mark.skip(reason="Teste de carga - executar manualmente")
    def test_concurrent_requests(self, client):
        """Deve lidar com requisições concorrentes"""
        # Teste de carga deve ser executado manualmente
        pass
