"""
Script de exemplo para usar a API DOC to PDF
Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
"""

import requests
import base64
import json
from pathlib import Path


def convert_doc_to_pdf(api_url, doc_path, replacements):
    """
    Converte um documento Word para PDF usando a API (retorna Base64)

    Args:
        api_url: URL da API (ex: http://localhost:5000 ou https://sua-api.render.com)
        doc_path: Caminho para o arquivo .DOC/.DOCX
        replacements: Dicionário com as substituições {TAG: valor}

    Returns:
        bytes: Conteúdo do PDF gerado
    """

    # Lê e codifica o documento em Base64
    with open(doc_path, 'rb') as file:
        doc_base64 = base64.b64encode(file.read()).decode('utf-8')

    # Prepara o payload
    payload = {
        "document": doc_base64,
        "replacements": replacements
    }

    # Faz a requisição
    print(f"Enviando documento para {api_url}/convert...")
    response = requests.post(
        f"{api_url}/convert",
        json=payload,
        headers={'Content-Type': 'application/json'}
    )

    # Verifica a resposta
    if response.status_code == 200:
        result = response.json()
        print("✅ Conversão realizada com sucesso!")

        # Decodifica o PDF
        pdf_bytes = base64.b64decode(result['pdf'])
        return pdf_bytes
    else:
        print(f"❌ Erro: {response.status_code}")
        print(response.json())
        return None


def convert_doc_to_pdf_file(api_url, doc_path, replacements, output_filename="documento.pdf"):
    """
    Converte um documento Word para PDF usando a API (retorna arquivo PDF diretamente)

    Args:
        api_url: URL da API (ex: http://localhost:5000 ou https://sua-api.render.com)
        doc_path: Caminho para o arquivo .DOC/.DOCX
        replacements: Dicionário com as substituições {TAG: valor}
        output_filename: Nome do arquivo PDF de saída

    Returns:
        bytes: Conteúdo do PDF gerado ou None em caso de erro
    """

    # Lê e codifica o documento em Base64
    with open(doc_path, 'rb') as file:
        doc_base64 = base64.b64encode(file.read()).decode('utf-8')

    # Prepara o payload
    payload = {
        "document": doc_base64,
        "replacements": replacements,
        "filename": output_filename
    }

    # Faz a requisição
    print(f"Enviando documento para {api_url}/convert-file...")
    response = requests.post(
        f"{api_url}/convert-file",
        json=payload,
        headers={'Content-Type': 'application/json'}
    )

    # Verifica a resposta
    if response.status_code == 200:
        print("✅ Conversão realizada com sucesso!")
        return response.content
    else:
        print(f"❌ Erro: {response.status_code}")
        try:
            print(response.json())
        except:
            print(response.text)
        return None


def main():
    """Exemplo de uso da API - Método 1: Retorno em Base64"""

    # Configuração
    API_URL = "http://localhost:5000"  # Altere para a URL do Render em produção
    DOC_PATH = "exemplo.docx"  # Coloque o caminho do seu documento
    OUTPUT_PATH = "resultado_base64.pdf"

    # Dados para substituição
    replacements = {
        "NOME": "Jose da Silva",
        "ENDERECO": "Rua qualquer coisa, Nro1, Bairro das colinas, São Paulo/SP - CEP: 48.4839-877",
        "DATANASCIMENTO": "01/01/1990",
        "CPF": "123.456.789-00",
        "TELEFONE": "(11) 98765-4321",
        "EMAIL": "jose.silva@email.com"
    }

    # Verifica se o arquivo existe
    if not Path(DOC_PATH).exists():
        print(f"❌ Arquivo não encontrado: {DOC_PATH}")
        print("\nPara usar este exemplo:")
        print("1. Crie um documento Word com tags como %%NOME%%, %%ENDERECO%%, etc.")
        print(f"2. Salve como '{DOC_PATH}' no mesmo diretório deste script")
        print("3. Execute novamente este script")
        return

    # Converte o documento usando endpoint /convert (Base64)
    pdf_bytes = convert_doc_to_pdf(API_URL, DOC_PATH, replacements)

    if pdf_bytes:
        # Salva o PDF
        with open(OUTPUT_PATH, 'wb') as f:
            f.write(pdf_bytes)
        print(f"✅ PDF salvo em: {OUTPUT_PATH}")
        print(f"📄 Tamanho: {len(pdf_bytes) / 1024:.2f} KB")


def main_file():
    """Exemplo de uso da API - Método 2: Retorno como arquivo PDF"""

    # Configuração
    API_URL = "http://localhost:5000"  # Altere para a URL do Render em produção
    DOC_PATH = "exemplo.docx"  # Coloque o caminho do seu documento
    OUTPUT_PATH = "resultado_file.pdf"

    # Dados para substituição
    replacements = {
        "NOME": "Jose da Silva",
        "ENDERECO": "Rua qualquer coisa, Nro1, Bairro das colinas, São Paulo/SP - CEP: 48.4839-877",
        "DATANASCIMENTO": "01/01/1990",
        "CPF": "123.456.789-00",
        "TELEFONE": "(11) 98765-4321",
        "EMAIL": "jose.silva@email.com"
    }

    # Verifica se o arquivo existe
    if not Path(DOC_PATH).exists():
        print(f"❌ Arquivo não encontrado: {DOC_PATH}")
        print("\nPara usar este exemplo:")
        print("1. Crie um documento Word com tags como %%NOME%%, %%ENDERECO%%, etc.")
        print(f"2. Salve como '{DOC_PATH}' no mesmo diretório deste script")
        print("3. Execute novamente este script")
        return

    # Converte o documento usando endpoint /convert-file (retorna arquivo)
    pdf_bytes = convert_doc_to_pdf_file(
        API_URL,
        DOC_PATH,
        replacements,
        output_filename="contrato_jose_silva.pdf"
    )

    if pdf_bytes:
        # Salva o PDF
        with open(OUTPUT_PATH, 'wb') as f:
            f.write(pdf_bytes)
        print(f"✅ PDF salvo em: {OUTPUT_PATH}")
        print(f"📄 Tamanho: {len(pdf_bytes) / 1024:.2f} KB")


def test_health_check():
    """Testa o endpoint de health check"""
    API_URL = "http://localhost:5000"

    print("Testando health check...")
    response = requests.get(f"{API_URL}/health")

    if response.status_code == 200:
        print("✅ API está funcionando!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Erro: {response.status_code}")


if __name__ == "__main__":
    print("=" * 60)
    print("DOC to PDF Converter - Exemplo de Uso")
    print("Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA")
    print("=" * 60)
    print()

    # Primeiro testa o health check
    test_health_check()
    print()

    # Menu de opções
    print("Escolha o método de conversão:")
    print("1. Endpoint /convert (retorna Base64)")
    print("2. Endpoint /convert-file (retorna arquivo PDF)")
    print("3. Testar ambos")
    print()

    choice = input("Digite sua escolha (1, 2 ou 3): ").strip()
    print()

    if choice == "1":
        print("🔄 Testando endpoint /convert (Base64)...")
        print()
        main()
    elif choice == "2":
        print("🔄 Testando endpoint /convert-file (Arquivo PDF)...")
        print()
        main_file()
    elif choice == "3":
        print("🔄 Testando endpoint /convert (Base64)...")
        print()
        main()
        print()
        print("-" * 60)
        print()
        print("🔄 Testando endpoint /convert-file (Arquivo PDF)...")
        print()
        main_file()
    else:
        print("❌ Opção inválida. Use 1, 2 ou 3.")
