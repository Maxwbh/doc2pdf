"""
Exemplos de Integração - API DOC2PDF em Produção

Este script demonstra como integrar a API DOC2PDF em produção
para converter documentos Word em PDF com substituição de tags.

URL da API: https://doc2pdf-api.onrender.com

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
Versão: 1.6.0
"""
import requests
import base64
import json
from pathlib import Path
from typing import Dict, Optional


# Configuração da API
API_URL = "https://doc2pdf-api.onrender.com"
TIMEOUT = 60  # 60 segundos


class DOC2PDFClient:
    """Cliente Python para a API DOC2PDF"""

    def __init__(self, base_url: str = API_URL, timeout: int = TIMEOUT):
        """
        Inicializa o cliente da API

        Args:
            base_url: URL base da API (padrão: produção)
            timeout: Timeout em segundos (padrão: 60s)
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json'
        })

    def health_check(self) -> Dict:
        """
        Verifica se a API está funcionando

        Returns:
            dict: Status da API

        Example:
            >>> client = DOC2PDFClient()
            >>> status = client.health_check()
            >>> print(status)
            {'service': 'DOC2PDF Converter API', 'status': 'healthy', 'version': '1.6.0'}
        """
        response = self.session.get(
            f"{self.base_url}/health",
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def convert_to_pdf_base64(
        self,
        document_path: str,
        replacements: Dict[str, str],
        quality: str = 'medium'
    ) -> Dict:
        """
        Converte documento Word para PDF e retorna em Base64

        Args:
            document_path: Caminho do arquivo DOCX
            replacements: Dicionário com tags e valores
            quality: Qualidade do PDF ('high', 'medium', 'low')

        Returns:
            dict: Resposta da API com PDF em Base64

        Example:
            >>> client = DOC2PDFClient()
            >>> result = client.convert_to_pdf_base64(
            ...     'contrato.docx',
            ...     {'NOME': 'João Silva', 'CPF': '123.456.789-00'},
            ...     quality='high'
            ... )
            >>> pdf_base64 = result['pdf']
        """
        # Carrega e codifica documento
        with open(document_path, 'rb') as f:
            doc_base64 = base64.b64encode(f.read()).decode('utf-8')

        # Prepara payload
        payload = {
            'document': doc_base64,
            'replacements': replacements,
            'quality': quality
        }

        # Envia requisição
        response = self.session.post(
            f"{self.base_url}/convert",
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()

        return response.json()

    def convert_to_pdf_file(
        self,
        document_path: str,
        replacements: Dict[str, str],
        output_path: Optional[str] = None,
        quality: str = 'medium'
    ) -> str:
        """
        Converte documento Word para PDF e salva em arquivo

        Args:
            document_path: Caminho do arquivo DOCX
            replacements: Dicionário com tags e valores
            output_path: Caminho para salvar o PDF (opcional)
            quality: Qualidade do PDF ('high', 'medium', 'low')

        Returns:
            str: Caminho do arquivo PDF salvo

        Example:
            >>> client = DOC2PDFClient()
            >>> pdf_path = client.convert_to_pdf_file(
            ...     'contrato.docx',
            ...     {'NOME': 'Maria Santos', 'DATA': '06/12/2025'},
            ...     output_path='contrato_final.pdf',
            ...     quality='high'
            ... )
            >>> print(f"PDF salvo em: {pdf_path}")
        """
        # Carrega e codifica documento
        with open(document_path, 'rb') as f:
            doc_base64 = base64.b64encode(f.read()).decode('utf-8')

        # Define nome do arquivo de saída
        if output_path is None:
            output_path = Path(document_path).with_suffix('.pdf')
        else:
            output_path = Path(output_path)

        # Prepara payload
        payload = {
            'document': doc_base64,
            'replacements': replacements,
            'filename': output_path.name,
            'quality': quality
        }

        # Envia requisição
        response = self.session.post(
            f"{self.base_url}/convert-file",
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()

        # Salva PDF
        with open(output_path, 'wb') as f:
            f.write(response.content)

        return str(output_path)


# =============================================================================
# EXEMPLOS DE USO
# =============================================================================

def exemplo_1_listagem_vendas():
    """
    Exemplo 1: Gerar listagem de vendas

    Usa o template ListaVendas.docx para gerar PDF de vendas
    """
    print("\n" + "="*60)
    print("EXEMPLO 1: Listagem de Vendas")
    print("="*60)

    # Inicializa cliente
    client = DOC2PDFClient()

    # Verifica se API está online
    print("🔍 Verificando API...")
    status = client.health_check()
    print(f"✅ API Status: {status['status']}")

    # Dados de venda
    dados_venda = {
        'NOME_CLIENTE': 'João Silva',
        'DATA_VENDA': '06/12/2025',
        'VALOR': 'R$ 1.500,00'
    }

    try:
        # Converte e salva PDF
        print("\n📄 Gerando PDF de vendas...")
        pdf_path = client.convert_to_pdf_file(
            document_path='tests/fixtures/documents/ListaVendas.docx',
            replacements=dados_venda,
            output_path='exemplo_listagem_vendas.pdf',
            quality='high'
        )

        print(f"✅ PDF gerado com sucesso!")
        print(f"📁 Arquivo salvo em: {pdf_path}")

    except FileNotFoundError:
        print("⚠️  Template não encontrado.")
        print("💡 Execute: python tests/fixtures/create_test_documents.py")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")


def exemplo_2_lote_vendas():
    """
    Exemplo 2: Gerar relatórios em lote

    Gera múltiplos relatórios de vendas
    """
    print("\n" + "="*60)
    print("EXEMPLO 2: Relatórios em Lote")
    print("="*60)

    client = DOC2PDFClient()

    # Lista de vendas para processar
    vendas = [
        {'NOME_CLIENTE': 'Cliente A', 'DATA_VENDA': '01/12/2025', 'VALOR': 'R$ 1.000,00'},
        {'NOME_CLIENTE': 'Cliente B', 'DATA_VENDA': '02/12/2025', 'VALOR': 'R$ 2.500,00'},
        {'NOME_CLIENTE': 'Cliente C', 'DATA_VENDA': '03/12/2025', 'VALOR': 'R$ 3.200,00'},
    ]

    print(f"\n📊 Gerando {len(vendas)} relatórios...")

    try:
        for i, venda in enumerate(vendas, 1):
            print(f"\n📄 Relatório {i}/{len(vendas)}: {venda['NOME_CLIENTE']}")

            pdf_path = client.convert_to_pdf_file(
                document_path='tests/fixtures/documents/ListaVendas.docx',
                replacements=venda,
                output_path=f'relatorio_{i}.pdf',
                quality='medium'
            )

            print(f"   ✅ Salvo em: {pdf_path}")

        print(f"\n✅ {len(vendas)} relatórios gerados com sucesso!")

    except FileNotFoundError:
        print("⚠️  Template não encontrado.")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")


def exemplo_3_base64_response():
    """
    Exemplo 3: Trabalhar com resposta em Base64

    Útil para integração com outras APIs ou bancos de dados
    """
    print("\n" + "="*60)
    print("EXEMPLO 3: Resposta em Base64")
    print("="*60)

    client = DOC2PDFClient()

    dados = {
        'NOME_CLIENTE': 'Empresa XYZ',
        'DATA_VENDA': '06/12/2025',
        'VALOR': 'R$ 50.000,00'
    }

    try:
        print("\n📄 Convertendo e obtendo Base64...")

        result = client.convert_to_pdf_base64(
            document_path='tests/fixtures/documents/ListaVendas.docx',
            replacements=dados,
            quality='medium'
        )

        pdf_base64 = result['pdf']
        print(f"✅ PDF convertido!")
        print(f"📊 Base64 size: {len(pdf_base64)} chars")

        # Decodifica e salva (opcional)
        pdf_bytes = base64.b64decode(pdf_base64)
        print(f"📊 PDF size: {len(pdf_bytes)} bytes")

        # Salvar em arquivo
        with open('exemplo_from_base64.pdf', 'wb') as f:
            f.write(pdf_bytes)
        print("💾 PDF salvo: exemplo_from_base64.pdf")

    except FileNotFoundError:
        print("⚠️  Template não encontrado.")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")


def main():
    """Executa todos os exemplos"""
    print("\n" + "="*60)
    print("🚀 EXEMPLOS DE INTEGRAÇÃO - API DOC2PDF")
    print("="*60)
    print(f"🌐 API: {API_URL}")
    print("="*60)

    # Menu de exemplos
    exemplos = [
        ("Listagem de Vendas", exemplo_1_listagem_vendas),
        ("Relatórios em Lote", exemplo_2_lote_vendas),
        ("Resposta em Base64", exemplo_3_base64_response),
    ]

    print("\nEscolha um exemplo para executar:")
    for i, (nome, _) in enumerate(exemplos, 1):
        print(f"  {i}. {nome}")
    print(f"  {len(exemplos) + 1}. Executar todos")

    try:
        escolha = input("\nOpção (1-4): ").strip()

        if escolha == str(len(exemplos) + 1):
            # Executar todos
            for nome, func in exemplos:
                func()
        elif escolha.isdigit() and 1 <= int(escolha) <= len(exemplos):
            # Executar exemplo selecionado
            exemplos[int(escolha) - 1][1]()
        else:
            print("Opção inválida!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")

    print("\n" + "="*60)
    print("✅ Exemplos concluídos!")
    print("="*60)


if __name__ == "__main__":
    main()
