"""
Testes de Validação - API em Produção (Render)

Este script testa a API em produção usando o documento ListaVendas.docx

URL de Produção: https://doc2pdf-api.onrender.com

Autor: Maxwell da Silva Oliveira - M&S do Brasil LTDA
Versão: 1.5.2
"""
import requests
import base64
import json
from pathlib import Path


# Configuração
PROD_URL = "https://doc2pdf-api.onrender.com"
FIXTURES_DIR = Path(__file__).parent / "fixtures" / "documents"
LISTA_VENDAS_PATH = FIXTURES_DIR / "ListaVendas.docx"


def load_document_base64(file_path):
    """Carrega documento e converte para Base64"""
    with open(file_path, 'rb') as f:
        doc_bytes = f.read()
        return base64.b64encode(doc_bytes).decode('utf-8')


def test_health_check():
    """Testa health check da API"""
    print("\n" + "="*60)
    print("🔍 Testando Health Check...")
    print("="*60)

    try:
        response = requests.get(f"{PROD_URL}/health", timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")

        assert response.status_code == 200, f"Health check falhou: {response.status_code}"
        print("✅ Health check passou!")
        return True
    except Exception as e:
        print(f"❌ Health check falhou: {str(e)}")
        return False


def test_convert_lista_vendas():
    """Testa conversão do ListaVendas.docx"""
    print("\n" + "="*60)
    print("🔍 Testando Conversão - ListaVendas.docx")
    print("="*60)

    try:
        # Carrega documento
        print("📄 Carregando ListaVendas.docx...")
        if not LISTA_VENDAS_PATH.exists():
            print(f"⚠️  Documento não encontrado em: {LISTA_VENDAS_PATH}")
            print("💡 Execute: python tests/fixtures/create_test_documents.py")
            return False

        doc_base64 = load_document_base64(LISTA_VENDAS_PATH)
        print(f"✅ Documento carregado ({len(doc_base64)} chars)")

        # Prepara dados
        data = {
            "document": doc_base64,
            "replacements": {
                "NOME_CLIENTE": "João Silva - Teste Produção",
                "DATA_VENDA": "06/12/2025",
                "VALOR": "R$ 1.500,00"
            },
            "quality": "medium"  # Medium para teste mais rápido
        }

        # Faz requisição
        print(f"🚀 Enviando requisição para {PROD_URL}/convert...")
        response = requests.post(
            f"{PROD_URL}/convert",
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=60  # 60s timeout para conversão
        )

        print(f"📊 Status Code: {response.status_code}")

        if response.status_code != 200:
            print(f"❌ Erro na conversão:")
            print(json.dumps(response.json(), indent=2))
            return False

        # Valida resposta
        result = response.json()
        print(f"✅ Resposta recebida:")
        print(f"   - success: {result.get('success')}")
        print(f"   - message: {result.get('message')}")

        if 'pdf' in result:
            pdf_size = len(result['pdf'])
            print(f"   - PDF Base64: {pdf_size} chars")

            # Valida que é Base64 válido
            try:
                pdf_bytes = base64.b64decode(result['pdf'])
                print(f"   - PDF Bytes: {len(pdf_bytes)} bytes")

                # Valida que é PDF válido
                if pdf_bytes.startswith(b'%PDF'):
                    print(f"   ✅ PDF válido gerado!")

                    # Salva PDF para inspeção (opcional)
                    output_path = Path(__file__).parent / "output_production_test.pdf"
                    with open(output_path, 'wb') as f:
                        f.write(pdf_bytes)
                    print(f"   💾 PDF salvo em: {output_path}")
                    return True
                else:
                    print(f"   ❌ PDF inválido (não começa com %PDF)")
                    return False

            except Exception as e:
                print(f"   ❌ Erro ao decodificar Base64: {str(e)}")
                return False
        else:
            print(f"   ❌ Campo 'pdf' não encontrado na resposta")
            return False

    except requests.exceptions.Timeout:
        print("❌ Timeout na requisição (>60s)")
        return False
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_convert_file_lista_vendas():
    """Testa endpoint /convert-file"""
    print("\n" + "="*60)
    print("🔍 Testando /convert-file - ListaVendas.docx")
    print("="*60)

    try:
        if not LISTA_VENDAS_PATH.exists():
            print(f"⚠️  Documento não encontrado")
            return False

        doc_base64 = load_document_base64(LISTA_VENDAS_PATH)

        data = {
            "document": doc_base64,
            "replacements": {
                "NOME_CLIENTE": "Maria Santos - Teste File",
                "DATA_VENDA": "06/12/2025",
                "VALOR": "R$ 2.500,00"
            },
            "filename": "lista_vendas_teste.pdf",
            "quality": "low"  # Low para teste mais rápido
        }

        print(f"🚀 Enviando requisição...")
        response = requests.post(
            f"{PROD_URL}/convert-file",
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )

        print(f"📊 Status Code: {response.status_code}")

        if response.status_code != 200:
            print(f"❌ Erro:")
            print(response.text)
            return False

        # Valida que recebeu PDF
        if response.headers.get('Content-Type') == 'application/pdf':
            pdf_size = len(response.content)
            print(f"✅ PDF recebido: {pdf_size} bytes")

            if response.content.startswith(b'%PDF'):
                print(f"✅ PDF válido!")

                # Salva PDF
                output_path = Path(__file__).parent / "output_convert_file_test.pdf"
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                print(f"💾 PDF salvo em: {output_path}")
                return True
            else:
                print(f"❌ Conteúdo não é PDF válido")
                return False
        else:
            print(f"❌ Content-Type incorreto: {response.headers.get('Content-Type')}")
            return False

    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        return False


def test_error_handling():
    """Testa tratamento de erros"""
    print("\n" + "="*60)
    print("🔍 Testando Tratamento de Erros")
    print("="*60)

    tests_passed = 0
    tests_total = 3

    # Teste 1: Sem documento
    print("\n📝 Teste 1: Requisição sem documento...")
    try:
        response = requests.post(
            f"{PROD_URL}/convert",
            json={"replacements": {}},
            timeout=10
        )
        if response.status_code == 400:
            print("✅ Retornou 400 corretamente")
            tests_passed += 1
        else:
            print(f"❌ Status incorreto: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

    # Teste 2: Sem replacements
    print("\n📝 Teste 2: Requisição sem replacements...")
    try:
        response = requests.post(
            f"{PROD_URL}/convert",
            json={"document": "AAAA"},
            timeout=10
        )
        if response.status_code == 400:
            print("✅ Retornou 400 corretamente")
            tests_passed += 1
        else:
            print(f"❌ Status incorreto: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

    # Teste 3: Base64 inválido
    print("\n📝 Teste 3: Base64 inválido...")
    try:
        response = requests.post(
            f"{PROD_URL}/convert",
            json={
                "document": "isso-nao-e-base64!!!",
                "replacements": {"TAG": "valor"}
            },
            timeout=10
        )
        if response.status_code in [400, 500]:
            print("✅ Retornou erro corretamente")
            tests_passed += 1
        else:
            print(f"❌ Status incorreto: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

    print(f"\n📊 Testes de erro: {tests_passed}/{tests_total} passaram")
    return tests_passed == tests_total


def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("🧪 TESTES DE VALIDAÇÃO - API EM PRODUÇÃO")
    print(f"🌐 URL: {PROD_URL}")
    print("="*60)

    results = {}

    # Health Check
    results['health'] = test_health_check()

    # Conversão ListaVendas
    results['convert_lista_vendas'] = test_convert_lista_vendas()

    # Convert File
    results['convert_file'] = test_convert_file_lista_vendas()

    # Tratamento de Erros
    results['error_handling'] = test_error_handling()

    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:30} {status}")

    total = len(results)
    passed = sum(1 for v in results.values() if v)

    print("\n" + "="*60)
    print(f"Total: {passed}/{total} testes passaram")

    if passed == total:
        print("✅ TODOS OS TESTES PASSARAM!")
    else:
        print(f"⚠️  {total - passed} testes falharam")

    print("="*60)

    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
