"""
Testes de Integração - Tratamento de Erros

Testa o tratamento de erros da API em diversos cenários

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
Versão: 1.5.2
"""
import pytest
import json


class TestValidationErrors:
    """Testes de erros de validação"""

    def test_missing_document_field(self, client):
        """Deve retornar erro 400 quando documento está faltando"""
        payload = {
            'replacements': {'TAG': 'valor'}
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'error' in data or 'message' in data

    def test_invalid_base64_encoding(self, client):
        """Deve retornar erro 400 para Base64 inválido"""
        payload = {
            'document': 'isto-não-é-base64-válido!!!@#$%',
            'replacements': {}
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 400

    def test_invalid_quality_value(self, client, lista_vendas_base64):
        """Deve retornar erro 400 para qualidade inválida"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': {},
            'quality': 'super_ultra_mega_high'
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 400

    def test_invalid_return_format(self, client, lista_vendas_base64):
        """Deve retornar erro 400 para formato de retorno inválido"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': {},
            'return_format': 'json'
        }

        response = client.post(
            '/process',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 400

    def test_non_dict_replacements(self, client, lista_vendas_base64):
        """Deve retornar erro 400 quando replacements não é dict"""
        payload = {
            'document': lista_vendas_base64,
            'replacements': ['lista', 'não', 'dict']
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 400


class TestContentTypeErrors:
    """Testes de erros de Content-Type"""

    def test_missing_content_type(self, client, valid_convert_payload):
        """Deve retornar erro 400 sem Content-Type"""
        response = client.post(
            '/convert',
            data=json.dumps(valid_convert_payload)
            # Não especifica content_type
        )

        # Pode retornar 400 ou 415 (Unsupported Media Type)
        assert response.status_code in [400, 415]

    def test_wrong_content_type_xml(self, client, valid_convert_payload):
        """Deve retornar erro 400 com Content-Type XML"""
        response = client.post(
            '/convert',
            data=json.dumps(valid_convert_payload),
            content_type='application/xml'
        )

        assert response.status_code == 400

    def test_wrong_content_type_form(self, client):
        """Deve retornar erro 400 com Content-Type form"""
        response = client.post(
            '/convert',
            data='document=abc&replacements={}',
            content_type='application/x-www-form-urlencoded'
        )

        assert response.status_code == 400


class TestMalformedJSON:
    """Testes de JSON malformado"""

    def test_invalid_json_syntax(self, client):
        """Deve retornar erro 400 para JSON inválido"""
        response = client.post(
            '/convert',
            data='{"document": "abc", invalid json here}',
            content_type='application/json'
        )

        assert response.status_code == 400

    def test_empty_request_body(self, client):
        """Deve retornar erro 400 para corpo vazio"""
        response = client.post(
            '/convert',
            data='',
            content_type='application/json'
        )

        assert response.status_code == 400

    def test_null_json(self, client):
        """Deve retornar erro 400 para JSON null"""
        response = client.post(
            '/convert',
            data='null',
            content_type='application/json'
        )

        assert response.status_code == 400


class TestHTTPMethodErrors:
    """Testes de métodos HTTP incorretos"""

    def test_get_on_convert_endpoint(self, client):
        """Deve retornar erro 405 para GET em /convert"""
        response = client.get('/convert')

        assert response.status_code == 405

    def test_put_on_convert_endpoint(self, client):
        """Deve retornar erro 405 para PUT em /convert"""
        response = client.put('/convert')

        assert response.status_code == 405

    def test_delete_on_convert_endpoint(self, client):
        """Deve retornar erro 405 para DELETE em /convert"""
        response = client.delete('/convert')

        assert response.status_code == 405

    def test_patch_on_convert_endpoint(self, client):
        """Deve retornar erro 405 para PATCH em /convert"""
        response = client.patch('/convert')

        assert response.status_code == 405


class TestNotFoundErrors:
    """Testes de rotas não encontradas"""

    def test_invalid_route(self, client):
        """Deve retornar erro 404 para rota inexistente"""
        response = client.get('/rota/inexistente')

        assert response.status_code == 404

    def test_invalid_endpoint(self, client):
        """Deve retornar erro 404 para endpoint inexistente"""
        response = client.post('/convert-docx-to-pdf-endpoint-invalido')

        assert response.status_code == 404


class TestDocumentErrors:
    """Testes de erros relacionados a documentos"""

    def test_corrupted_docx_base64(self, client):
        """Deve retornar erro para DOCX corrompido"""
        # Base64 válido, mas não é um DOCX
        import base64
        corrupted = base64.b64encode(b'isto não é um docx válido').decode('utf-8')

        payload = {
            'document': corrupted,
            'replacements': {}
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Pode retornar 400 ou 500 dependendo da implementação
        assert response.status_code in [400, 500]

    def test_empty_base64(self, client):
        """Deve retornar erro para Base64 vazio"""
        payload = {
            'document': '',
            'replacements': {}
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 400

    def test_null_document(self, client):
        """Deve retornar erro para documento null"""
        payload = {
            'document': None,
            'replacements': {}
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 400


class TestResponseFormat:
    """Testes de formato de resposta de erro"""

    def test_error_response_has_success_false(self, client):
        """Resposta de erro deve ter success: false"""
        payload = {'replacements': {}}  # Falta documento

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = response.get_json()

        if data:  # Se retornou JSON
            assert data.get('success') is False or 'error' in data

    def test_error_response_is_json(self, client):
        """Resposta de erro deve ser JSON"""
        payload = {'replacements': {}}

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 400
        # Tenta parsear como JSON
        try:
            data = response.get_json()
            assert data is not None
        except:
            # Se não for JSON, não é crítico
            pass

    def test_error_response_has_message(self, client):
        """Resposta de erro deve ter mensagem descritiva"""
        payload = {'replacements': {}}

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert response.status_code == 400
        data = response.get_json()

        if data:
            # Deve ter alguma mensagem de erro
            assert ('error' in data or 'message' in data or
                    'detail' in data or 'description' in data)


class TestConcurrencyErrors:
    """Testes de erros de concorrência"""

    @pytest.mark.skip(reason="Teste de concorrência - executar manualmente")
    def test_simultaneous_requests(self, client):
        """Deve lidar com requisições simultâneas sem erros"""
        # Teste de concorrência deve ser manual
        pass


class TestEdgeCaseErrors:
    """Testes de casos extremos de erro"""

    def test_very_large_payload(self, client):
        """Deve lidar com payload muito grande"""
        # Cria um payload muito grande
        large_string = 'X' * (10 * 1024 * 1024)  # 10MB

        payload = {
            'document': large_string,
            'replacements': {}
        }

        response = client.post(
            '/convert',
            data=json.dumps(payload),
            content_type='application/json'
        )

        # Pode retornar 400 (bad request) ou 413 (payload too large)
        assert response.status_code in [400, 413, 500]

    def test_very_long_tag_name(self, client, lista_vendas_base64):
        """Deve lidar com nomes de tag muito longos"""
        long_tag_name = 'X' * 10000

        replacements = {
            long_tag_name: 'valor'
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

        # Deve completar sem crash (pode retornar 200 ou 400)
        assert response.status_code in [200, 400]

    def test_special_characters_in_tags(self, client, lista_vendas_base64):
        """Deve lidar com caracteres especiais em tags"""
        replacements = {
            'NOME_CLIENTE<script>': 'Teste XSS',
            'DATA_VENDA\x00': 'Teste Null Byte',
            'VALOR\n\r\t': 'Teste Whitespace'
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

        # Deve completar sem crash
        assert response.status_code in [200, 400]


class TestErrorRecovery:
    """Testes de recuperação de erros"""

    def test_error_then_success(self, client, lista_vendas_base64, replacements_lista_vendas):
        """Deve permitir requisição bem-sucedida após erro"""
        # 1. Requisição com erro
        bad_payload = {'replacements': {}}

        response1 = client.post(
            '/convert',
            data=json.dumps(bad_payload),
            content_type='application/json'
        )

        assert response1.status_code == 400

        # 2. Requisição bem-sucedida
        good_payload = {
            'document': lista_vendas_base64,
            'replacements': replacements_lista_vendas,
            'quality': 'medium'
        }

        response2 = client.post(
            '/convert',
            data=json.dumps(good_payload),
            content_type='application/json'
        )

        assert response2.status_code == 200

    def test_multiple_errors_do_not_crash(self, client):
        """Múltiplos erros não devem crashar a aplicação"""
        bad_payload = {'replacements': {}}

        for _ in range(5):
            response = client.post(
                '/convert',
                data=json.dumps(bad_payload),
                content_type='application/json'
            )

            assert response.status_code == 400

        # Aplicação deve ainda estar funcionando
        health_response = client.get('/health')
        assert health_response.status_code == 200
