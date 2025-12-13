"""
Configuração de fixtures compartilhadas para testes

Este arquivo contém fixtures pytest que são compartilhadas entre
testes unitários e de integração.

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
Versão: 1.5.2
"""
import pytest
import os
import base64
import tempfile
from pathlib import Path
from app import create_app


# =============================================================================
# Fixtures de Aplicação
# =============================================================================

@pytest.fixture
def app():
    """Cria instância da aplicação Flask para testes"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Cliente de teste Flask"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """CLI runner para testes de comandos"""
    return app.test_cli_runner()


# =============================================================================
# Fixtures de Diretórios
# =============================================================================

@pytest.fixture
def fixtures_dir():
    """Retorna o diretório de fixtures"""
    return Path(__file__).parent / 'fixtures'


@pytest.fixture
def documents_dir(fixtures_dir):
    """Retorna o diretório de documentos de teste"""
    return fixtures_dir / 'documents'


@pytest.fixture
def temp_dir():
    """Cria e retorna diretório temporário para testes"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


# =============================================================================
# Fixtures de Documentos
# =============================================================================

@pytest.fixture
def lista_vendas_path(documents_dir):
    """Retorna o caminho para ListaVendas.docx"""
    return documents_dir / 'ListaVendas.docx'


@pytest.fixture
def lista_vendas_bytes(lista_vendas_path):
    """Retorna o conteúdo binário de ListaVendas.docx"""
    with open(lista_vendas_path, 'rb') as f:
        return f.read()


@pytest.fixture
def lista_vendas_base64(lista_vendas_bytes):
    """Retorna ListaVendas.docx codificado em Base64"""
    return base64.b64encode(lista_vendas_bytes).decode('utf-8')


@pytest.fixture
def simple_doc_path(documents_dir):
    """Retorna o caminho para simple.docx"""
    return documents_dir / 'simple.docx'


@pytest.fixture
def simple_doc_bytes(simple_doc_path):
    """Retorna o conteúdo binário de simple.docx"""
    with open(simple_doc_path, 'rb') as f:
        return f.read()


@pytest.fixture
def simple_doc_base64(simple_doc_bytes):
    """Retorna simple.docx codificado em Base64"""
    return base64.b64encode(simple_doc_bytes).decode('utf-8')


@pytest.fixture
def with_tags_path(documents_dir):
    """Retorna o caminho para with_tags.docx"""
    return documents_dir / 'with_tags.docx'


@pytest.fixture
def with_tags_bytes(with_tags_path):
    """Retorna o conteúdo binário de with_tags.docx"""
    with open(with_tags_path, 'rb') as f:
        return f.read()


@pytest.fixture
def with_tags_base64(with_tags_bytes):
    """Retorna with_tags.docx codificado em Base64"""
    return base64.b64encode(with_tags_bytes).decode('utf-8')


@pytest.fixture
def complex_doc_path(documents_dir):
    """Retorna o caminho para complex.docx"""
    return documents_dir / 'complex.docx'


@pytest.fixture
def complex_doc_bytes(complex_doc_path):
    """Retorna o conteúdo binário de complex.docx"""
    with open(complex_doc_path, 'rb') as f:
        return f.read()


@pytest.fixture
def complex_doc_base64(complex_doc_bytes):
    """Retorna complex.docx codificado em Base64"""
    return base64.b64encode(complex_doc_bytes).decode('utf-8')


@pytest.fixture
def empty_doc_path(documents_dir):
    """Retorna o caminho para empty.docx"""
    return documents_dir / 'empty.docx'


@pytest.fixture
def empty_doc_bytes(empty_doc_path):
    """Retorna o conteúdo binário de empty.docx"""
    with open(empty_doc_path, 'rb') as f:
        return f.read()


@pytest.fixture
def empty_doc_base64(empty_doc_bytes):
    """Retorna empty.docx codificado em Base64"""
    return base64.b64encode(empty_doc_bytes).decode('utf-8')


@pytest.fixture
def tags_repetidas_path(documents_dir):
    """Retorna o caminho para tags_repetidas.docx"""
    return documents_dir / 'tags_repetidas.docx'


@pytest.fixture
def tags_repetidas_bytes(tags_repetidas_path):
    """Retorna o conteúdo binário de tags_repetidas.docx"""
    with open(tags_repetidas_path, 'rb') as f:
        return f.read()


@pytest.fixture
def tags_repetidas_base64(tags_repetidas_bytes):
    """Retorna tags_repetidas.docx codificado em Base64"""
    return base64.b64encode(tags_repetidas_bytes).decode('utf-8')


# =============================================================================
# Fixtures de Dados de Teste
# =============================================================================

@pytest.fixture
def replacements_lista_vendas():
    """Retorna substituições para ListaVendas.docx"""
    return {
        'NOME_CLIENTE': 'João Silva',
        'DATA_VENDA': '06/12/2025',
        'VALOR': 'R$ 1.500,00'
    }


@pytest.fixture
def replacements_with_tags():
    """Retorna substituições para with_tags.docx"""
    return {
        'MES': 'Dezembro',
        'ANO': '2025',
        'EMPRESA': 'M&S do Brasil LTDA',
        'RESPONSAVEL': 'Maxwell da Silva Oliveira',
        'PROJETO': 'DOC2PDF API',
        'STATUS': 'Concluído'
    }


@pytest.fixture
def replacements_complex():
    """Retorna substituições para complex.docx"""
    return {
        'TITULO': 'Relatório Financeiro Q4 2025',
        'CLIENTE': 'Empresa XYZ',
        'PROJETO': 'Implementação API',
        'DATA': '06/12/2025',
        'ITEM1': 'Desenvolvimento',
        'QTD1': '160h',
        'VALOR1': 'R$ 16.000,00',
        'ITEM2': 'Testes',
        'QTD2': '40h',
        'VALOR2': 'R$ 4.000,00',
        'TOTAL': 'R$ 20.000,00',
        'OBS1': 'Projeto concluído no prazo',
        'OBS2': 'Todos os testes passaram',
        'OBS3': 'Cliente satisfeito',
        'DATA_GERACAO': '06/12/2025 14:30',
        'VERSAO': '1.5.2'
    }


@pytest.fixture
def replacements_tags_repetidas():
    """Retorna substituições para tags_repetidas.docx"""
    return {
        'TAG_REPETIDA': 'VALOR_SUBSTITUIDO'
    }


# =============================================================================
# Fixtures de Payloads API
# =============================================================================

@pytest.fixture
def valid_convert_payload(lista_vendas_base64, replacements_lista_vendas):
    """Retorna payload válido para /convert"""
    return {
        'document': lista_vendas_base64,
        'replacements': replacements_lista_vendas,
        'quality': 'high'
    }


@pytest.fixture
def valid_process_payload(lista_vendas_base64, replacements_lista_vendas):
    """Retorna payload válido para /process"""
    return {
        'document': lista_vendas_base64,
        'replacements': replacements_lista_vendas,
        'quality': 'medium',
        'return_format': 'base64'
    }


@pytest.fixture
def invalid_payload_no_document():
    """Retorna payload inválido sem documento"""
    return {
        'replacements': {'TAG': 'valor'}
    }


@pytest.fixture
def invalid_payload_no_replacements(lista_vendas_base64):
    """Retorna payload inválido sem replacements"""
    return {
        'document': lista_vendas_base64
    }


@pytest.fixture
def invalid_payload_bad_base64():
    """Retorna payload com Base64 inválido"""
    return {
        'document': 'isso-nao-e-base64-valido!!!',
        'replacements': {'TAG': 'valor'}
    }


@pytest.fixture
def invalid_payload_bad_quality(lista_vendas_base64):
    """Retorna payload com qualidade inválida"""
    return {
        'document': lista_vendas_base64,
        'replacements': {'TAG': 'valor'},
        'quality': 'super_ultra_mega_high'
    }


# =============================================================================
# Fixtures de Helpers
# =============================================================================

@pytest.fixture
def assert_pdf_valid():
    """Helper para validar se bytes são um PDF válido"""
    def _assert(pdf_bytes):
        assert pdf_bytes is not None, "PDF bytes não podem ser None"
        assert len(pdf_bytes) > 0, "PDF bytes não podem estar vazios"
        assert pdf_bytes.startswith(b'%PDF'), "Bytes não começam com %PDF"
        assert b'%%EOF' in pdf_bytes, "PDF não contém %%EOF"
        return True
    return _assert


@pytest.fixture
def assert_docx_valid():
    """Helper para validar se bytes são um DOCX válido"""
    def _assert(docx_bytes):
        assert docx_bytes is not None, "DOCX bytes não podem ser None"
        assert len(docx_bytes) > 0, "DOCX bytes não podem estar vazios"
        # DOCX é um ZIP, deve começar com PK
        assert docx_bytes.startswith(b'PK'), "DOCX não é um arquivo ZIP válido"
        return True
    return _assert


@pytest.fixture
def assert_json_response():
    """Helper para validar resposta JSON da API"""
    def _assert(response, status_code=200, has_keys=None):
        assert response.status_code == status_code, \
            f"Status code esperado {status_code}, recebido {response.status_code}"

        data = response.get_json()
        assert data is not None, "Resposta não contém JSON válido"

        if has_keys:
            for key in has_keys:
                assert key in data, f"Chave '{key}' não encontrada na resposta"

        return data
    return _assert
