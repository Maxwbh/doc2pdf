"""
Exemplo Simples - Integração com API DOC2PDF

Script minimalista para uso rápido da API em produção

URL: https://doc2pdf-api.onrender.com

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
Versão: 1.6.0
"""
import requests
import base64


def converter_docx_para_pdf(
    arquivo_docx: str,
    substituicoes: dict,
    arquivo_pdf: str = 'saida.pdf',
    qualidade: str = 'medium'
):
    """
    Converte DOCX para PDF usando a API DOC2PDF

    Args:
        arquivo_docx: Caminho do arquivo .docx
        substituicoes: Dict com tags e valores {'TAG': 'valor'}
        arquivo_pdf: Caminho para salvar o PDF
        qualidade: 'high', 'medium' ou 'low'

    Example:
        >>> converter_docx_para_pdf(
        ...     'contrato.docx',
        ...     {'NOME': 'João Silva', 'DATA': '06/12/2025'},
        ...     'contrato_final.pdf',
        ...     'high'
        ... )
    """
    # 1. Carrega o documento e converte para Base64
    with open(arquivo_docx, 'rb') as f:
        doc_base64 = base64.b64encode(f.read()).decode('utf-8')

    # 2. Prepara os dados
    dados = {
        'document': doc_base64,
        'replacements': substituicoes,
        'quality': qualidade
    }

    # 3. Envia para API
    print(f"📤 Enviando documento para conversão...")
    response = requests.post(
        'https://doc2pdf-api.onrender.com/convert',
        json=dados,
        headers={'Content-Type': 'application/json'},
        timeout=60
    )

    # 4. Verifica resposta
    if response.status_code != 200:
        raise Exception(f"Erro na API: {response.json()}")

    # 5. Decodifica e salva o PDF
    resultado = response.json()
    pdf_bytes = base64.b64decode(resultado['pdf'])

    with open(arquivo_pdf, 'wb') as f:
        f.write(pdf_bytes)

    print(f"✅ PDF gerado: {arquivo_pdf}")
    print(f"📊 Tamanho: {len(pdf_bytes)} bytes")


# =============================================================================
# EXEMPLOS DE USO
# =============================================================================

if __name__ == "__main__":
    print("\n🚀 API DOC2PDF - Exemplo Simples\n")

    # Exemplo 1: Listagem de Vendas
    print("=" * 50)
    print("EXEMPLO 1: Listagem de Vendas")
    print("=" * 50)

    try:
        converter_docx_para_pdf(
            arquivo_docx='tests/fixtures/documents/ListaVendas.docx',
            substituicoes={
                'NOME_CLIENTE': 'João Silva',
                'DATA_VENDA': '06/12/2025',
                'VALOR': 'R$ 1.500,00'
            },
            arquivo_pdf='vendas_joao_silva.pdf',
            qualidade='high'
        )
        print("✅ Sucesso!\n")

    except FileNotFoundError:
        print("⚠️  Arquivo não encontrado")
        print("💡 Certifique-se de que o template existe\n")

    except Exception as e:
        print(f"❌ Erro: {str(e)}\n")

    # Exemplo 2: Múltiplas vendas
    print("=" * 50)
    print("EXEMPLO 2: Múltiplas Vendas")
    print("=" * 50)

    vendas = [
        {'nome': 'Maria Santos', 'valor': 'R$ 2.500,00'},
        {'nome': 'Pedro Oliveira', 'valor': 'R$ 3.200,00'},
        {'nome': 'Ana Costa', 'valor': 'R$ 1.800,00'},
    ]

    for i, venda in enumerate(vendas, 1):
        try:
            converter_docx_para_pdf(
                arquivo_docx='tests/fixtures/documents/ListaVendas.docx',
                substituicoes={
                    'NOME_CLIENTE': venda['nome'],
                    'DATA_VENDA': '06/12/2025',
                    'VALOR': venda['valor']
                },
                arquivo_pdf=f'venda_{i}.pdf',
                qualidade='medium'
            )
        except FileNotFoundError:
            print(f"⚠️  Template não encontrado (venda {i})")
            break
        except Exception as e:
            print(f"❌ Erro na venda {i}: {str(e)}")

    print("\n✅ Processo concluído!")
