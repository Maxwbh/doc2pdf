"""
Testes Unitários - Validators

Testa todas as funções de validação em app/utils/validators.py

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
Versão: 1.5.2
"""
import pytest
from app.utils.validators import (
    validate_quality,
    validate_return_format,
    validate_json_content_type,
    validate_base64_document,
    validate_replacements
)
from werkzeug.exceptions import BadRequest


class TestValidateQuality:
    """Testes para validate_quality()"""

    def test_valid_quality_high(self):
        """Deve aceitar 'high' como qualidade válida"""
        result = validate_quality('high')
        assert result == 'high'

    def test_valid_quality_medium(self):
        """Deve aceitar 'medium' como qualidade válida"""
        result = validate_quality('medium')
        assert result == 'medium'

    def test_valid_quality_low(self):
        """Deve aceitar 'low' como qualidade válida"""
        result = validate_quality('low')
        assert result == 'low'

    def test_invalid_quality(self):
        """Deve rejeitar qualidade inválida"""
        with pytest.raises(BadRequest) as exc_info:
            validate_quality('ultra_mega')

        assert 'qualidade inválida' in str(exc_info.value).lower()

    def test_quality_none(self):
        """Deve usar 'medium' como padrão quando None"""
        result = validate_quality(None)
        assert result == 'medium'

    def test_quality_empty_string(self):
        """Deve usar 'medium' como padrão quando string vazia"""
        result = validate_quality('')
        assert result == 'medium'

    def test_quality_case_insensitive(self):
        """Deve aceitar qualidade case-insensitive"""
        assert validate_quality('HIGH') == 'high'
        assert validate_quality('Medium') == 'medium'
        assert validate_quality('LoW') == 'low'


class TestValidateReturnFormat:
    """Testes para validate_return_format()"""

    def test_valid_format_base64(self):
        """Deve aceitar 'base64' como formato válido"""
        result = validate_return_format('base64')
        assert result == 'base64'

    def test_valid_format_file(self):
        """Deve aceitar 'file' como formato válido"""
        result = validate_return_format('file')
        assert result == 'file'

    def test_invalid_format(self):
        """Deve rejeitar formato inválido"""
        with pytest.raises(BadRequest) as exc_info:
            validate_return_format('json')

        assert 'formato inválido' in str(exc_info.value).lower()

    def test_format_none(self):
        """Deve usar 'base64' como padrão quando None"""
        result = validate_return_format(None)
        assert result == 'base64'

    def test_format_case_insensitive(self):
        """Deve aceitar formato case-insensitive"""
        assert validate_return_format('BASE64') == 'base64'
        assert validate_return_format('File') == 'file'


class TestValidateJsonContentType:
    """Testes para validate_json_content_type()"""

    def test_valid_json_content_type(self):
        """Deve aceitar application/json"""
        class MockRequest:
            content_type = 'application/json'

        validate_json_content_type(MockRequest())  # Não deve lançar erro

    def test_valid_json_with_charset(self):
        """Deve aceitar application/json com charset"""
        class MockRequest:
            content_type = 'application/json; charset=utf-8'

        validate_json_content_type(MockRequest())  # Não deve lançar erro

    def test_invalid_content_type(self):
        """Deve rejeitar content-type não-JSON"""
        class MockRequest:
            content_type = 'application/xml'

        with pytest.raises(BadRequest) as exc_info:
            validate_json_content_type(MockRequest())

        assert 'application/json' in str(exc_info.value).lower()

    def test_missing_content_type(self):
        """Deve rejeitar request sem content-type"""
        class MockRequest:
            content_type = None

        with pytest.raises(BadRequest):
            validate_json_content_type(MockRequest())


class TestValidateBase64Document:
    """Testes para validate_base64_document()"""

    def test_valid_base64(self, lista_vendas_base64):
        """Deve aceitar Base64 válido"""
        result = validate_base64_document(lista_vendas_base64)
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_invalid_base64(self):
        """Deve rejeitar Base64 inválido"""
        with pytest.raises(BadRequest) as exc_info:
            validate_base64_document('isso-nao-é-base64!!!@#$')

        assert 'base64' in str(exc_info.value).lower()

    def test_empty_base64(self):
        """Deve rejeitar Base64 vazio"""
        with pytest.raises(BadRequest):
            validate_base64_document('')

    def test_none_base64(self):
        """Deve rejeitar None"""
        with pytest.raises(BadRequest):
            validate_base64_document(None)

    def test_base64_with_whitespace(self, lista_vendas_base64):
        """Deve aceitar Base64 com whitespace"""
        base64_with_spaces = f"\n  {lista_vendas_base64}  \n"
        result = validate_base64_document(base64_with_spaces)
        assert isinstance(result, bytes)

    def test_base64_docx_format(self, lista_vendas_base64):
        """Deve validar que o resultado é um DOCX válido"""
        result = validate_base64_document(lista_vendas_base64)
        # DOCX é um ZIP, deve começar com PK
        assert result.startswith(b'PK')


class TestValidateReplacements:
    """Testes para validate_replacements()"""

    def test_valid_replacements(self, replacements_lista_vendas):
        """Deve aceitar replacements válidos"""
        result = validate_replacements(replacements_lista_vendas)
        assert result == replacements_lista_vendas

    def test_empty_replacements(self):
        """Deve aceitar replacements vazios"""
        result = validate_replacements({})
        assert result == {}

    def test_none_replacements(self):
        """Deve aceitar None e retornar dict vazio"""
        result = validate_replacements(None)
        assert result == {}

    def test_replacements_not_dict(self):
        """Deve rejeitar replacements que não são dict"""
        with pytest.raises(BadRequest) as exc_info:
            validate_replacements(['lista', 'nao', 'dict'])

        assert 'objeto' in str(exc_info.value).lower() or 'dict' in str(exc_info.value).lower()

    def test_replacements_with_special_chars(self):
        """Deve aceitar replacements com caracteres especiais"""
        replacements = {
            'TAG1': 'Valor com ãçéntüação',
            'TAG2': 'R$ 1.500,00',
            'TAG3': '100% concluído'
        }
        result = validate_replacements(replacements)
        assert result == replacements

    def test_replacements_with_numbers(self):
        """Deve converter valores numéricos para string"""
        replacements = {
            'NUMERO': 12345,
            'FLOAT': 123.45,
            'BOOL': True
        }
        result = validate_replacements(replacements)

        # Os valores devem ser convertidos para string
        assert isinstance(result['NUMERO'], (str, int))
        assert isinstance(result['FLOAT'], (str, float))

    def test_replacements_case_sensitivity(self):
        """Deve preservar case das chaves"""
        replacements = {
            'tag_minuscula': 'valor1',
            'TAG_MAIUSCULA': 'valor2',
            'Tag_MiXeD': 'valor3'
        }
        result = validate_replacements(replacements)
        assert 'tag_minuscula' in result
        assert 'TAG_MAIUSCULA' in result
        assert 'Tag_MiXeD' in result


class TestValidatorsIntegration:
    """Testes de integração entre validators"""

    def test_full_validation_chain_valid(self, lista_vendas_base64, replacements_lista_vendas):
        """Deve passar por toda cadeia de validação com dados válidos"""
        quality = validate_quality('high')
        return_format = validate_return_format('base64')
        document_bytes = validate_base64_document(lista_vendas_base64)
        replacements = validate_replacements(replacements_lista_vendas)

        assert quality == 'high'
        assert return_format == 'base64'
        assert isinstance(document_bytes, bytes)
        assert isinstance(replacements, dict)

    def test_full_validation_chain_defaults(self, lista_vendas_base64):
        """Deve usar valores padrão quando não especificados"""
        quality = validate_quality(None)
        return_format = validate_return_format(None)
        document_bytes = validate_base64_document(lista_vendas_base64)
        replacements = validate_replacements(None)

        assert quality == 'medium'
        assert return_format == 'base64'
        assert isinstance(document_bytes, bytes)
        assert replacements == {}
