"""
Testes Unitários - Encoders

Testa todas as funções de encoding/decoding em app/utils/encoders.py

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
Versão: 1.5.2
"""
import pytest
import base64
from app.utils.encoders import encode_file_to_base64, decode_base64_file
from werkzeug.exceptions import BadRequest


class TestEncodeFileToBase64:
    """Testes para encode_file_to_base64()"""

    def test_encode_docx_file(self, lista_vendas_bytes):
        """Deve codificar bytes DOCX para Base64"""
        result = encode_file_to_base64(lista_vendas_bytes)

        assert isinstance(result, str)
        assert len(result) > 0
        # Deve ser Base64 válido
        decoded = base64.b64decode(result)
        assert decoded == lista_vendas_bytes

    def test_encode_empty_bytes(self):
        """Deve codificar bytes vazios"""
        result = encode_file_to_base64(b'')
        assert result == ''

    def test_encode_small_bytes(self):
        """Deve codificar bytes pequenos"""
        test_bytes = b'Hello World'
        result = encode_file_to_base64(test_bytes)

        # Decodifica e verifica
        decoded = base64.b64decode(result)
        assert decoded == test_bytes

    def test_encode_binary_data(self):
        """Deve codificar dados binários"""
        binary_data = bytes([0, 1, 2, 3, 255, 254, 253])
        result = encode_file_to_base64(binary_data)

        decoded = base64.b64decode(result)
        assert decoded == binary_data

    def test_encode_large_file(self, complex_doc_bytes):
        """Deve codificar arquivos grandes"""
        result = encode_file_to_base64(complex_doc_bytes)

        assert isinstance(result, str)
        decoded = base64.b64decode(result)
        assert decoded == complex_doc_bytes

    def test_encode_returns_string(self, lista_vendas_bytes):
        """Deve retornar string, não bytes"""
        result = encode_file_to_base64(lista_vendas_bytes)
        assert isinstance(result, str)
        assert not isinstance(result, bytes)


class TestDecodeBase64File:
    """Testes para decode_base64_file()"""

    def test_decode_valid_base64(self, lista_vendas_base64, lista_vendas_bytes):
        """Deve decodificar Base64 válido"""
        result = decode_base64_file(lista_vendas_base64)

        assert isinstance(result, bytes)
        assert result == lista_vendas_bytes

    def test_decode_empty_string(self):
        """Deve rejeitar string vazia"""
        with pytest.raises(BadRequest) as exc_info:
            decode_base64_file('')

        assert 'base64' in str(exc_info.value).lower()

    def test_decode_invalid_base64(self):
        """Deve rejeitar Base64 inválido"""
        with pytest.raises(BadRequest) as exc_info:
            decode_base64_file('isso-não-é-base64!!!@#$%')

        assert 'base64' in str(exc_info.value).lower()

    def test_decode_none(self):
        """Deve rejeitar None"""
        with pytest.raises(BadRequest):
            decode_base64_file(None)

    def test_decode_with_whitespace(self, lista_vendas_base64, lista_vendas_bytes):
        """Deve decodificar Base64 com whitespace"""
        base64_with_spaces = f"\n  {lista_vendas_base64}  \n"
        result = decode_base64_file(base64_with_spaces)

        assert result == lista_vendas_bytes

    def test_decode_multiline_base64(self, lista_vendas_base64, lista_vendas_bytes):
        """Deve decodificar Base64 com quebras de linha"""
        # Adiciona quebras de linha a cada 76 caracteres (padrão RFC)
        multiline = '\n'.join([lista_vendas_base64[i:i+76]
                              for i in range(0, len(lista_vendas_base64), 76)])

        result = decode_base64_file(multiline)
        assert result == lista_vendas_bytes

    def test_decode_returns_bytes(self, lista_vendas_base64):
        """Deve retornar bytes, não string"""
        result = decode_base64_file(lista_vendas_base64)
        assert isinstance(result, bytes)
        assert not isinstance(result, str)

    def test_decode_malformed_base64(self):
        """Deve rejeitar Base64 malformado"""
        malformed = "SGVsbG8gV29ybGQ="  # válido
        malformed += "INVALID!!!"         # inválido

        with pytest.raises(BadRequest):
            decode_base64_file(malformed)


class TestEncodersRoundTrip:
    """Testes de ida e volta (encode -> decode)"""

    def test_roundtrip_lista_vendas(self, lista_vendas_bytes):
        """Deve fazer roundtrip completo com ListaVendas.docx"""
        encoded = encode_file_to_base64(lista_vendas_bytes)
        decoded = decode_base64_file(encoded)

        assert decoded == lista_vendas_bytes

    def test_roundtrip_simple_doc(self, simple_doc_bytes):
        """Deve fazer roundtrip completo com simple.docx"""
        encoded = encode_file_to_base64(simple_doc_bytes)
        decoded = decode_base64_file(encoded)

        assert decoded == simple_doc_bytes

    def test_roundtrip_complex_doc(self, complex_doc_bytes):
        """Deve fazer roundtrip completo com complex.docx"""
        encoded = encode_file_to_base64(complex_doc_bytes)
        decoded = decode_base64_file(encoded)

        assert decoded == complex_doc_bytes

    def test_roundtrip_empty(self):
        """Deve fazer roundtrip com bytes vazios"""
        empty_bytes = b''
        encoded = encode_file_to_base64(empty_bytes)
        decoded = decode_base64_file(encoded) if encoded else b''

        assert decoded == empty_bytes

    def test_roundtrip_binary_data(self):
        """Deve fazer roundtrip com dados binários"""
        binary_data = bytes(range(256))
        encoded = encode_file_to_base64(binary_data)
        decoded = decode_base64_file(encoded)

        assert decoded == binary_data

    def test_roundtrip_preserves_docx_structure(self, lista_vendas_bytes):
        """Deve preservar estrutura DOCX após roundtrip"""
        # DOCX é um ZIP, deve começar com PK
        assert lista_vendas_bytes.startswith(b'PK')

        encoded = encode_file_to_base64(lista_vendas_bytes)
        decoded = decode_base64_file(encoded)

        # Deve preservar o header ZIP
        assert decoded.startswith(b'PK')
        assert decoded == lista_vendas_bytes


class TestEncodersEdgeCases:
    """Testes de casos extremos"""

    def test_encode_large_file(self):
        """Deve codificar arquivo grande (> 1MB)"""
        large_bytes = b'X' * (1024 * 1024)  # 1MB
        result = encode_file_to_base64(large_bytes)

        assert isinstance(result, str)
        assert len(result) > 0

    def test_decode_very_long_base64(self):
        """Deve decodificar Base64 muito longo"""
        large_bytes = b'Y' * (1024 * 1024)  # 1MB
        encoded = base64.b64encode(large_bytes).decode('utf-8')
        result = decode_base64_file(encoded)

        assert result == large_bytes

    def test_encode_unicode_not_supported(self):
        """Deve rejeitar string Unicode (deve receber bytes)"""
        with pytest.raises((TypeError, AttributeError)):
            encode_file_to_base64("string unicode não bytes")

    def test_decode_non_ascii_characters(self):
        """Deve lidar com caracteres não-ASCII em Base64"""
        # Base64 deve conter apenas caracteres ASCII
        text = "Olá Mundo ãçéntúação"
        text_bytes = text.encode('utf-8')
        encoded = base64.b64encode(text_bytes).decode('utf-8')

        result = decode_base64_file(encoded)
        assert result == text_bytes
        assert result.decode('utf-8') == text


class TestEncodersConsistency:
    """Testes de consistência entre encoders"""

    def test_encode_decode_idempotent(self, lista_vendas_bytes):
        """Encode/decode deve ser idempotente"""
        encoded1 = encode_file_to_base64(lista_vendas_bytes)
        decoded1 = decode_base64_file(encoded1)
        encoded2 = encode_file_to_base64(decoded1)
        decoded2 = decode_base64_file(encoded2)

        assert encoded1 == encoded2
        assert decoded1 == decoded2
        assert decoded1 == lista_vendas_bytes

    def test_multiple_files_same_encoding(self, lista_vendas_bytes, simple_doc_bytes):
        """Diferentes arquivos devem ter encodings diferentes"""
        encoded1 = encode_file_to_base64(lista_vendas_bytes)
        encoded2 = encode_file_to_base64(simple_doc_bytes)

        # Devem ser diferentes
        assert encoded1 != encoded2

        # Mas devem decodificar corretamente
        assert decode_base64_file(encoded1) == lista_vendas_bytes
        assert decode_base64_file(encoded2) == simple_doc_bytes
