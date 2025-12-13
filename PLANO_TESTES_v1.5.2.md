# 🧪 Plano de Testes - DOC2PDF API v1.5.2

**Autor:** Maxwell da Silva Oliveira - M&S do Brasil LTDA
**Data:** 06/12/2025
**Versão:** 1.5.2
**Status:** ✅ Implementado

---

## 📋 Sumário Executivo

Este plano de testes define a estratégia completa de testes para a API DOC2PDF v1.5.2, incluindo testes unitários, de integração, e de sistema.

### Objetivos

- ✅ **Cobertura de Código:** Alcançar mínimo de 80% de cobertura
- ✅ **Qualidade:** Garantir que todos os endpoints funcionam corretamente
- ✅ **Confiabilidade:** Validar tratamento de erros robusto
- ✅ **Performance:** Garantir tempos de resposta aceitáveis
- ✅ **Regressão:** Prevenir quebras em funcionalidades existentes

---

## 📊 Escopo de Testes

### Componentes Testados

| Componente | Tipo | Prioridade | Status |
|------------|------|------------|--------|
| **Validators** | Unitário | 🔴 Alta | ✅ Completo |
| **Encoders** | Unitário | 🔴 Alta | ✅ Completo |
| **DOCX Service** | Unitário | 🔴 Alta | ✅ Completo |
| **PDF Service** | Unitário | 🟡 Média | ✅ Completo |
| **API Endpoints** | Integração | 🔴 Alta | ✅ Completo |
| **Fluxo Completo** | Integração | 🔴 Alta | ✅ Completo |
| **Erro Handling** | Integração | 🔴 Alta | ✅ Completo |

---

## 🎯 Estratégia de Testes

### Pirâmide de Testes

```
                    /\
                   /  \  E2E (Manual)
                  /____\
                 /      \  Testes de Integração
                /________\
               /          \
              /  Testes    \
             /   Unitários  \
            /________________\
```

**Distribuição:**
- 60% Testes Unitários (isolados, rápidos)
- 30% Testes de Integração (API, fluxos)
- 10% Testes E2E (manuais, via Postman)

---

## 📁 Estrutura de Testes

### Arquivos de Teste Criados

```
tests/
├── conftest.py                              # Fixtures compartilhadas
├── __init__.py
│
├── fixtures/
│   ├── create_test_documents.py             # Script de criação
│   └── documents/
│       ├── ListaVendas.docx                 # ⭐ Principal
│       ├── simple.docx
│       ├── with_tags.docx
│       ├── complex.docx
│       ├── empty.docx
│       └── tags_repetidas.docx
│
├── unit/
│   ├── test_validators.py                   # 8 classes, 40+ testes
│   ├── test_encoders.py                     # 6 classes, 35+ testes
│   ├── test_docx_service.py                 # 4 classes, 30+ testes
│   └── test_pdf_service.py                  # 6 classes, 25+ testes
│
└── integration/
    ├── test_api_endpoints.py                # 10 classes, 50+ testes
    ├── test_full_conversion.py              # 7 classes, 25+ testes
    └── test_error_handling.py               # 8 classes, 35+ testes
```

**Total:** ~240+ testes implementados

---

## 🧪 Casos de Teste Detalhados

### 1. Testes Unitários - Validators

**Arquivo:** `tests/unit/test_validators.py`

#### 1.1 validate_quality()

| ID | Cenário | Entrada | Resultado Esperado |
|----|---------|---------|-------------------|
| VAL-Q-001 | Qualidade válida 'high' | 'high' | Retorna 'high' |
| VAL-Q-002 | Qualidade válida 'medium' | 'medium' | Retorna 'medium' |
| VAL-Q-003 | Qualidade válida 'low' | 'low' | Retorna 'low' |
| VAL-Q-004 | Qualidade inválida | 'ultra_mega' | Lança BadRequest |
| VAL-Q-005 | Qualidade None | None | Retorna 'medium' (default) |
| VAL-Q-006 | Case insensitive | 'HIGH' | Retorna 'high' |

#### 1.2 validate_return_format()

| ID | Cenário | Entrada | Resultado Esperado |
|----|---------|---------|-------------------|
| VAL-F-001 | Formato 'base64' | 'base64' | Retorna 'base64' |
| VAL-F-002 | Formato 'file' | 'file' | Retorna 'file' |
| VAL-F-003 | Formato inválido | 'json' | Lança BadRequest |
| VAL-F-004 | Formato None | None | Retorna 'base64' (default) |

#### 1.3 validate_base64_document()

| ID | Cenário | Entrada | Resultado Esperado |
|----|---------|---------|-------------------|
| VAL-B-001 | Base64 válido | [Base64 válido] | Retorna bytes |
| VAL-B-002 | Base64 inválido | 'não-é-base64' | Lança BadRequest |
| VAL-B-003 | Base64 vazio | '' | Lança BadRequest |
| VAL-B-004 | Base64 com whitespace | '  [base64]  ' | Retorna bytes |

**Total de testes:** 40+

---

### 2. Testes Unitários - Encoders

**Arquivo:** `tests/unit/test_encoders.py`

#### 2.1 encode_file_to_base64()

| ID | Cenário | Entrada | Resultado Esperado |
|----|---------|---------|-------------------|
| ENC-E-001 | Codificar DOCX | bytes DOCX | String Base64 |
| ENC-E-002 | Bytes vazios | b'' | String vazia |
| ENC-E-003 | Dados binários | bytes([0,1,255]) | Base64 válido |
| ENC-E-004 | Arquivo grande | 1MB+ | Base64 válido |

#### 2.2 decode_base64_file()

| ID | Cenário | Entrada | Resultado Esperado |
|----|---------|---------|-------------------|
| DEC-D-001 | Base64 válido | Base64 string | Bytes originais |
| DEC-D-002 | Base64 inválido | String inválida | Lança BadRequest |
| DEC-D-003 | Multiline Base64 | Com \n | Bytes corretos |

#### 2.3 Roundtrip Tests

| ID | Cenário | Resultado Esperado |
|----|---------|-------------------|
| RT-001 | Encode -> Decode ListaVendas | Bytes idênticos |
| RT-002 | Encode -> Decode Complex | Bytes idênticos |
| RT-003 | Preservar estrutura DOCX | Header PK preservado |

**Total de testes:** 35+

---

### 3. Testes Unitários - DOCX Service

**Arquivo:** `tests/unit/test_docx_service.py`

#### 3.1 replace_tags_in_doc() - Substituições Básicas

| ID | Cenário | Fixture | Substituições | Verificação |
|----|---------|---------|---------------|-------------|
| DOC-S-001 | ListaVendas completo | ListaVendas.docx | NOME_CLIENTE, DATA_VENDA, VALOR | Tags substituídas |
| DOC-S-002 | Documento com tags em tabelas | with_tags.docx | MES, ANO, EMPRESA | Tabelas atualizadas |
| DOC-S-003 | Documento complexo | complex.docx | 14 tags | Todas substituídas |
| DOC-S-004 | Tags repetidas | tags_repetidas.docx | TAG_REPETIDA | Todas ocorrências |

#### 3.2 replace_tags_in_doc() - Casos Especiais

| ID | Cenário | Resultado Esperado |
|----|---------|-------------------|
| DOC-SE-001 | Substituições vazias | Tags permanecem |
| DOC-SE-002 | Substituições parciais | Apenas tags especificadas |
| DOC-SE-003 | Case sensitivity | Apenas maiúsculas |
| DOC-SE-004 | Caracteres especiais | Aceita ãçéntüação |
| DOC-SE-005 | Valores numéricos | Converte para string |

#### 3.3 Integração DOCX

| ID | Cenário | Resultado Esperado |
|----|---------|-------------------|
| DOC-INT-001 | Documento salvável | Arquivo .docx válido |
| DOC-INT-002 | Reabertura preserva dados | Substituições persistem |

**Total de testes:** 30+

---

### 4. Testes Unitários - PDF Service

**Arquivo:** `tests/unit/test_pdf_service.py`

#### 4.1 convert_docx_to_pdf() - Qualidades

| ID | Fixture | Qualidade | Verificação |
|----|---------|-----------|-------------|
| PDF-Q-001 | simple.docx | high | PDF válido |
| PDF-Q-002 | simple.docx | medium | PDF válido |
| PDF-Q-003 | simple.docx | low | PDF válido |
| PDF-Q-004 | ListaVendas.docx | high | PDF >= 1KB |
| PDF-Q-005 | complex.docx | medium | PDF grande |

#### 4.2 convert_docx_to_pdf() - Validações

| ID | Cenário | Verificação |
|----|---------|-------------|
| PDF-V-001 | Header PDF | Inicia com %PDF |
| PDF-V-002 | EOF marker | Contém %%EOF |
| PDF-V-003 | Tamanho mínimo | > 500 bytes |
| PDF-V-004 | Sobrescrever existente | Funciona |

#### 4.3 Tratamento de Erros

| ID | Cenário | Resultado Esperado |
|----|---------|-------------------|
| PDF-E-001 | Arquivo inexistente | Lança Exception |
| PDF-E-002 | Qualidade inválida | Fallback ou erro |
| PDF-E-003 | Caminho inválido | Lança Exception |

**Total de testes:** 25+

---

### 5. Testes de Integração - API Endpoints

**Arquivo:** `tests/integration/test_api_endpoints.py`

#### 5.1 GET /health

| ID | Cenário | Status | Verificação |
|----|---------|--------|-------------|
| API-H-001 | Health check | 200 | status='healthy' |
| API-H-002 | Versão correta | 200 | version='1.5.2' |

#### 5.2 POST /convert

| ID | Cenário | Payload | Status | Verificação |
|----|---------|---------|--------|-------------|
| API-C-001 | Conversão válida | ListaVendas + tags | 200 | success=True, pdf presente |
| API-C-002 | Sem documento | Apenas replacements | 400 | success=False |
| API-C-003 | Base64 inválido | Base64 corrompido | 400 | Erro |
| API-C-004 | Qualidade inválida | quality='invalid' | 400 | Erro |
| API-C-005 | Content-Type errado | XML | 400 | Erro |
| API-C-006 | Qualidade high | quality='high' | 200 | PDF válido |
| API-C-007 | Qualidade medium | quality='medium' | 200 | PDF válido |
| API-C-008 | Qualidade low | quality='low' | 200 | PDF válido |
| API-C-009 | Sem replacements | {} | 200 | Aceita |
| API-C-010 | Documento complexo | complex.docx | 200 | PDF grande |

#### 5.3 POST /convert-file

| ID | Cenário | Status | Content-Type | Verificação |
|----|---------|--------|--------------|-------------|
| API-CF-001 | Retorna arquivo | 200 | application/pdf | PDF válido |
| API-CF-002 | Formato PDF | 200 | application/pdf | Inicia com %PDF |
| API-CF-003 | Sem documento | 400 | - | Erro |

#### 5.4 POST /process

| ID | Cenário | return_format | Status | Verificação |
|----|---------|---------------|--------|-------------|
| API-P-001 | Retorna Base64 | base64 | 200 | JSON com 'pdf' |
| API-P-002 | Retorna arquivo | file | 200 | application/pdf |
| API-P-003 | Formato padrão | (omitido) | 200 | JSON (base64) |
| API-P-004 | Formato inválido | 'json' | 400 | Erro |

#### 5.5 Substituição de Tags

| ID | Cenário | Documento | Verificação |
|----|---------|-----------|-------------|
| API-T-001 | Tags em PDF | ListaVendas | PDF gerado |
| API-T-002 | Múltiplas tags | complex.docx | Todas substituídas |
| API-T-003 | Tags repetidas | tags_repetidas.docx | Todas ocorrências |

#### 5.6 Tratamento de Erros

| ID | Método | Endpoint | Status Esperado |
|----|--------|----------|-----------------|
| API-E-001 | GET | /convert | 405 |
| API-E-002 | GET | /rota-invalida | 404 |
| API-E-003 | POST | /convert (JSON inválido) | 400 |

**Total de testes:** 50+

---

### 6. Testes de Integração - Fluxo Completo

**Arquivo:** `tests/integration/test_full_conversion.py`

#### 6.1 Workflow Completo

| ID | Documento | Fluxo | Verificação |
|----|-----------|-------|-------------|
| FLOW-001 | ListaVendas | Encode -> POST -> Decode | PDF válido |
| FLOW-002 | simple.docx | Sem tags | PDF válido |
| FLOW-003 | complex.docx | Com 14 tags | PDF completo |
| FLOW-004 | ListaVendas | Caracteres especiais | PDF com UTF-8 |

#### 6.2 Diferentes Qualidades

| ID | Qualidade | Verificação |
|----|-----------|-------------|
| FLOW-Q-001 | low | PDF válido |
| FLOW-Q-002 | medium | PDF válido |
| FLOW-Q-003 | high | PDF válido |

#### 6.3 Cenários Reais

| ID | Cenário | Documento | Verificação |
|----|---------|-----------|-------------|
| REAL-001 | Nota fiscal | ListaVendas | PDF imprimível |
| REAL-002 | Contrato | complex.docx | PDF completo |
| REAL-003 | Relatório | with_tags.docx | PDF formatado |

#### 6.4 Conversão em Lote

| ID | Cenário | Quantidade | Verificação |
|----|---------|------------|-------------|
| BATCH-001 | Sequencial | 3 docs | Todos convertem |

**Total de testes:** 25+

---

### 7. Testes de Integração - Tratamento de Erros

**Arquivo:** `tests/integration/test_error_handling.py`

#### 7.1 Erros de Validação

| ID | Erro | Status | Verificação |
|----|------|--------|-------------|
| ERR-V-001 | Documento faltando | 400 | success=False |
| ERR-V-002 | Base64 inválido | 400 | Mensagem de erro |
| ERR-V-003 | Qualidade inválida | 400 | Mensagem de erro |
| ERR-V-004 | Formato inválido | 400 | Mensagem de erro |
| ERR-V-005 | Replacements não-dict | 400 | Mensagem de erro |

#### 7.2 Erros de Content-Type

| ID | Content-Type | Status |
|----|--------------|--------|
| ERR-CT-001 | (omitido) | 400/415 |
| ERR-CT-002 | application/xml | 400 |
| ERR-CT-003 | application/x-www-form-urlencoded | 400 |

#### 7.3 JSON Malformado

| ID | Payload | Status |
|----|---------|--------|
| ERR-JSON-001 | Sintaxe inválida | 400 |
| ERR-JSON-002 | Corpo vazio | 400 |
| ERR-JSON-003 | null | 400 |

#### 7.4 Métodos HTTP Incorretos

| ID | Método | Endpoint | Status |
|----|--------|----------|--------|
| ERR-HTTP-001 | GET | /convert | 405 |
| ERR-HTTP-002 | PUT | /convert | 405 |
| ERR-HTTP-003 | DELETE | /convert | 405 |
| ERR-HTTP-004 | PATCH | /convert | 405 |

#### 7.5 Erros de Documento

| ID | Cenário | Status |
|----|---------|--------|
| ERR-DOC-001 | DOCX corrompido | 400/500 |
| ERR-DOC-002 | Base64 vazio | 400 |
| ERR-DOC-003 | Documento null | 400 |

#### 7.6 Recuperação de Erros

| ID | Cenário | Verificação |
|----|---------|-------------|
| ERR-REC-001 | Erro -> Sucesso | Segunda requisição OK |
| ERR-REC-002 | Múltiplos erros | App não crasha |

**Total de testes:** 35+

---

## 🎯 Cobertura de Código

### Metas de Cobertura

| Módulo | Meta | Prioridade |
|--------|------|------------|
| app/utils/validators.py | 95% | 🔴 Alta |
| app/utils/encoders.py | 95% | 🔴 Alta |
| app/services/docx_service.py | 85% | 🔴 Alta |
| app/services/pdf_service.py | 80% | 🟡 Média |
| app/routes/*.py | 80% | 🔴 Alta |
| **TOTAL** | **85%+** | 🔴 Alta |

### Comandos de Cobertura

```bash
# Executar testes com cobertura
pytest --cov=app --cov-report=html

# Ver relatório no navegador
open htmlcov/index.html

# Relatório em terminal
pytest --cov=app --cov-report=term-missing

# Apenas cobertura de módulo específico
pytest --cov=app.utils.validators tests/unit/test_validators.py
```

---

## 🚀 Execução de Testes

### Comandos Básicos

```bash
# Todos os testes
pytest

# Apenas testes unitários
pytest tests/unit/

# Apenas testes de integração
pytest tests/integration/

# Arquivo específico
pytest tests/unit/test_validators.py

# Teste específico
pytest tests/unit/test_validators.py::TestValidateQuality::test_valid_quality_high

# Verbose com output
pytest -v -s

# Com cobertura
pytest --cov=app
```

### Marcadores (Markers)

```bash
# Apenas testes unitários
pytest -m unit

# Apenas testes de integração
pytest -m integration

# Apenas testes lentos
pytest -m slow

# Excluir testes lentos
pytest -m "not slow"

# Testes de API
pytest -m api

# Testes de conversão
pytest -m conversion
```

### Execução Paralela

```bash
# Executar em paralelo (requer pytest-xdist)
pytest -n auto

# 4 workers
pytest -n 4
```

---

## 📈 Critérios de Aceitação

### Critérios Obrigatórios

- ✅ **Todos os testes passam:** 0 falhas
- ✅ **Cobertura mínima:** 80%
- ✅ **Nenhum erro de lint:** flake8, pylint
- ✅ **Documentação completa:** Todos os testes documentados
- ✅ **Performance:** Testes unitários < 1s cada

### Critérios Desejáveis

- 🎯 Cobertura > 85%
- 🎯 Tempo total de testes < 5 minutos
- 🎯 Testes de integração < 30s cada
- 🎯 Zero warnings

---

## 🔄 CI/CD Integration

### GitHub Actions (Planejado)

```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## 📚 Fixtures Disponíveis

### Documentos de Teste

| Fixture | Descrição | Uso |
|---------|-----------|-----|
| `lista_vendas_path` | Caminho para ListaVendas.docx | Conversão principal |
| `lista_vendas_bytes` | Bytes do documento | Testes de serviço |
| `lista_vendas_base64` | Base64 do documento | Testes de API |
| `simple_doc_*` | Documento simples | Testes básicos |
| `complex_doc_*` | Documento complexo | Testes avançados |
| `with_tags_*` | Documento com tags em tabelas | Testes de tabelas |
| `empty_doc_*` | Documento vazio | Testes de erro |
| `tags_repetidas_*` | Tags repetidas | Testes de múltiplas ocorrências |

### Substituições

| Fixture | Tags | Uso |
|---------|------|-----|
| `replacements_lista_vendas` | NOME_CLIENTE, DATA_VENDA, VALOR | Teste principal |
| `replacements_complex` | 14 tags | Testes complexos |
| `replacements_with_tags` | 6 tags | Testes de tabelas |
| `replacements_tags_repetidas` | 1 tag (repetida) | Testes de repetição |

### Helpers

| Fixture | Função |
|---------|--------|
| `assert_pdf_valid` | Valida formato PDF |
| `assert_docx_valid` | Valida formato DOCX |
| `assert_json_response` | Valida resposta JSON |

---

## 🎓 Exemplos de Uso

### Teste Unitário Simples

```python
def test_validate_quality_high():
    """Deve aceitar 'high' como qualidade válida"""
    result = validate_quality('high')
    assert result == 'high'
```

### Teste com Fixture

```python
def test_encode_docx(lista_vendas_bytes):
    """Deve codificar DOCX para Base64"""
    result = encode_file_to_base64(lista_vendas_bytes)
    assert isinstance(result, str)
    assert len(result) > 0
```

### Teste de API

```python
def test_convert_success(client, valid_convert_payload):
    """Deve converter com sucesso"""
    response = client.post(
        '/convert',
        data=json.dumps(valid_convert_payload),
        content_type='application/json'
    )
    assert response.status_code == 200
```

---

## 📊 Relatórios

### Relatórios Gerados

1. **Coverage HTML:** `htmlcov/index.html`
2. **Coverage XML:** `coverage.xml` (para CI)
3. **Coverage Terminal:** Console output
4. **Pytest HTML:** (opcional, requer pytest-html)

### Visualizar Cobertura

```bash
# Gerar e abrir relatório HTML
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

---

## ✅ Checklist de Validação

### Antes de Commitar

- [ ] Todos os testes passam: `pytest`
- [ ] Cobertura adequada: `pytest --cov=app`
- [ ] Lint passa: `flake8 app/ tests/`
- [ ] Tipos corretos: `mypy app/` (opcional)
- [ ] Código formatado: `black app/ tests/`
- [ ] Imports organizados: `isort app/ tests/`

### Antes de Release

- [ ] Todos os testes passam em CI
- [ ] Cobertura >= 80%
- [ ] Documentação atualizada
- [ ] CHANGELOG atualizado
- [ ] Versão bumped
- [ ] Testes manuais via Postman

---

## 🔗 Referências

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [Testing Flask Applications](https://flask.palletsprojects.com/en/latest/testing/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)

---

## 📝 Notas Finais

Este plano de testes cobre:
- ✅ **240+ testes** implementados
- ✅ **7 arquivos** de teste
- ✅ **6 documentos** de fixture
- ✅ **Cobertura completa** de funcionalidades
- ✅ **Tratamento de erros** robusto
- ✅ **Cenários reais** de uso

**Status:** Pronto para execução e integração em CI/CD

---

**Autor:** Maxwell da Silva Oliveira
**Email:** maxwbh@gmail.com
**Empresa:** M&S do Brasil LTDA
**Data:** 06/12/2025
**Versão:** 1.5.2
