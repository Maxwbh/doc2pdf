"""
Exemplos de uso da API DOC2PDF em Python

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
"""
import requests
import base64
import json

# URL da API (ajuste conforme necessário)
API_URL = "http://localhost:5000"  # ou sua URL do Render


def encode_file_to_base64(file_path: str) -> str:
    """Converte arquivo para Base64"""
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def save_base64_to_file(base64_string: str, output_path: str):
    """Salva Base64 em arquivo"""
    with open(output_path, 'wb') as f:
        f.write(base64.b64decode(base64_string))


# =============================================================================
# EXEMPLO 1: /convert - Retorna PDF em Base64
# =============================================================================
def exemplo_convert():
    """Converte DOCX para PDF e recebe em Base64"""
    print("=" * 60)
    print("EXEMPLO 1: Endpoint /convert (retorna Base64)")
    print("=" * 60)

    # Codifica documento
    doc_base64 = encode_file_to_base64('template.docx')

    # Monta requisição
    payload = {
        "document": doc_base64,
        "replacements": {
            "NOME": "João da Silva",
            "CPF": "123.456.789-00",
            "DATA": "05/12/2025",
            "ENDERECO": "Rua das Flores, 123"
        },
        "quality": "high"  # high, medium ou low
    }

    # Envia requisição
    response = requests.post(f"{API_URL}/convert", json=payload)

    if response.status_code == 200:
        result = response.json()
        print(f"✓ Sucesso!")
        print(f"  Tempo: {result['processing_time']}s")
        print(f"  Qualidade: {result['stats']['quality']}")
        print(f"  Tamanho PDF: {result['stats']['output_size']} bytes")

        # Salva PDF
        save_base64_to_file(result['pdf'], 'output.pdf')
        print(f"✓ PDF salvo em: output.pdf")
    else:
        print(f"✗ Erro: {response.json()}")


# =============================================================================
# EXEMPLO 2: /convert-file - Retorna arquivo PDF
# =============================================================================
def exemplo_convert_file():
    """Converte DOCX para PDF e recebe arquivo direto"""
    print("\n" + "=" * 60)
    print("EXEMPLO 2: Endpoint /convert-file (retorna arquivo)")
    print("=" * 60)

    doc_base64 = encode_file_to_base64('template.docx')

    payload = {
        "document": doc_base64,
        "replacements": {
            "TITULO": "Contrato de Prestação de Serviços",
            "CONTRATANTE": "Empresa ABC LTDA",
            "CONTRATADO": "Fornecedor XYZ",
            "VALOR": "R$ 10.000,00"
        },
        "filename": "contrato.pdf",
        "quality": "medium"
    }

    response = requests.post(f"{API_URL}/convert-file", json=payload)

    if response.status_code == 200:
        # Salva arquivo recebido
        with open('contrato.pdf', 'wb') as f:
            f.write(response.content)
        print(f"✓ PDF salvo em: contrato.pdf")
        print(f"  Tamanho: {len(response.content)} bytes")
    else:
        print(f"✗ Erro: {response.json()}")


# =============================================================================
# EXEMPLO 3: /process - Endpoint flexível
# =============================================================================
def exemplo_process():
    """Usa endpoint flexível /process"""
    print("\n" + "=" * 60)
    print("EXEMPLO 3: Endpoint /process (flexível)")
    print("=" * 60)

    doc_base64 = encode_file_to_base64('template.docx')

    # Exemplo: retorna PDF em Base64
    payload = {
        "document": doc_base64,
        "replacements": {
            "NOME_ALUNO": "Maria Santos",
            "CURSO": "Python Avançado",
            "DATA_CONCLUSAO": "05/12/2025"
        },
        "input_type": "base64",
        "output_type": "base64_pdf",  # pdf, doc, base64_pdf, base64_doc
        "quality": "low"  # Para web/email
    }

    response = requests.post(f"{API_URL}/process", json=payload)

    if response.status_code == 200:
        result = response.json()
        print(f"✓ Sucesso!")
        print(f"  Qualidade: {result['stats']['quality']}")

        save_base64_to_file(result['pdf'], 'certificado.pdf')
        print(f"✓ PDF salvo em: certificado.pdf")
    else:
        print(f"✗ Erro: {response.json()}")


# =============================================================================
# EXEMPLO 4: Processamento em lote
# =============================================================================
def exemplo_lote():
    """Processa múltiplos documentos"""
    print("\n" + "=" * 60)
    print("EXEMPLO 4: Processamento em lote")
    print("=" * 60)

    # Lista de clientes
    clientes = [
        {"NOME": "João Silva", "CPF": "111.111.111-11"},
        {"NOME": "Maria Santos", "CPF": "222.222.222-22"},
        {"NOME": "Pedro Oliveira", "CPF": "333.333.333-33"},
    ]

    doc_base64 = encode_file_to_base64('template.docx')

    for i, cliente in enumerate(clientes, 1):
        payload = {
            "document": doc_base64,
            "replacements": cliente,
            "filename": f"documento_{i}.pdf",
            "quality": "medium"
        }

        response = requests.post(f"{API_URL}/convert-file", json=payload)

        if response.status_code == 200:
            filename = f"documento_{i}.pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✓ {filename} gerado para {cliente['NOME']}")
        else:
            print(f"✗ Erro ao processar {cliente['NOME']}")


# =============================================================================
# EXEMPLO 5: Tratamento de erros
# =============================================================================
def exemplo_erro_handling():
    """Demonstra tratamento de erros"""
    print("\n" + "=" * 60)
    print("EXEMPLO 5: Tratamento de erros")
    print("=" * 60)

    try:
        payload = {
            "document": "INVALIDO_BASE64",  # Base64 inválido
            "replacements": {"TAG": "valor"}
        }

        response = requests.post(f"{API_URL}/convert", json=payload)

        if response.status_code != 200:
            error = response.json()
            print(f"✗ Erro esperado: {error['error']}")
            print(f"  Status code: {response.status_code}")

    except Exception as e:
        print(f"✗ Exceção: {str(e)}")


# =============================================================================
# EXECUÇÃO
# =============================================================================
if __name__ == "__main__":
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║       EXEMPLOS DE USO - API DOC2PDF v1.5.0                ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()

    # Verifica se API está online
    try:
        health = requests.get(f"{API_URL}/health")
        if health.status_code == 200:
            info = health.json()
            print(f"✓ API Online: {info['service']} v{info['version']}")
            print()
        else:
            print("✗ API não está respondendo")
            exit(1)
    except Exception as e:
        print(f"✗ Erro ao conectar: {e}")
        print(f"  Verifique se a API está rodando em {API_URL}")
        exit(1)

    # Executa exemplos (comente os que não quiser executar)
    # exemplo_convert()
    # exemplo_convert_file()
    # exemplo_process()
    # exemplo_lote()
    exemplo_erro_handling()

    print("\n" + "=" * 60)
    print("✓ Exemplos concluídos!")
    print("=" * 60)
