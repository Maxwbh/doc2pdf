# 🧪 Testes DOC2PDF API

Esta pasta contém todos os testes do projeto.

## 📂 Estrutura

```
tests/
├── unit/          # Testes unitários (isolados)
├── integration/   # Testes de integração (com dependências)
└── fixtures/      # Dados de teste (documentos, mocks)
```

---

## 📋 Tipos de Testes

### 🔬 Unit Tests (`tests/unit/`)

Testes isolados de componentes individuais:

**Planejados:**
- `test_validators.py` - Testa funções de validação
- `test_encoders.py` - Testa Base64 encode/decode
- `test_docx_service.py` - Testa substituição de tags
- `test_pdf_service.py` - Testa conversão PDF

**Como rodar:**
```bash
pytest tests/unit/
```

---

### 🔗 Integration Tests (`tests/integration/`)

Testes end-to-end com todas as dependências:

**Planejados:**
- `test_api_endpoints.py` - Testa endpoints da API
- `test_full_conversion.py` - Testa fluxo completo
- `test_error_handling.py` - Testa tratamento de erros

**Como rodar:**
```bash
pytest tests/integration/
```

---

### 📦 Fixtures (`tests/fixtures/`)

Dados de teste reutilizáveis:

**Estrutura:**
```
fixtures/
├── documents/       # Documentos DOCX de teste
│   ├── simple.docx
│   ├── with_tags.docx
│   └── complex.docx
├── pdfs/           # PDFs esperados
└── mocks/          # Mocks e stubs
```

---

## 🚀 Como Rodar Testes

### Instalação de Dependências

```bash
pip install pytest pytest-cov pytest-mock
```

### Rodar Todos os Testes

```bash
pytest tests/
```

### Rodar com Cobertura

```bash
pytest --cov=app --cov-report=html tests/
```

### Rodar Testes Específicos

```bash
# Apenas unit tests
pytest tests/unit/

# Apenas integration tests
pytest tests/integration/

# Arquivo específico
pytest tests/unit/test_validators.py

# Teste específico
pytest tests/unit/test_validators.py::test_validate_docx_format
```

---

## ✅ Testes Atuais

### Postman Collection

Enquanto os testes Python estão sendo desenvolvidos, use a collection Postman:

```bash
newman run docs/postman/DOC2PDF_v1.5.0_Tests.postman_collection.json
```

**Cobertura Atual (Postman):**
- ✅ Health checks
- ✅ Validações de erro
- ✅ Conversão com qualidades diferentes
- ✅ Todos os endpoints

---

## 📊 Cobertura Alvo

| Módulo | Cobertura Alvo | Status |
|--------|----------------|--------|
| `app/utils/validators.py` | 90% | ⏳ Pendente |
| `app/utils/encoders.py` | 95% | ⏳ Pendente |
| `app/services/docx_service.py` | 85% | ⏳ Pendente |
| `app/services/pdf_service.py` | 80% | ⏳ Pendente |
| `app/routes/*` | 75% | ✅ Postman |

---

## 🎯 Próximos Passos

1. [ ] Criar testes unitários para validators
2. [ ] Criar testes unitários para encoders
3. [ ] Criar fixtures DOCX de teste
4. [ ] Criar testes de integração para API
5. [ ] Configurar CI/CD com GitHub Actions
6. [ ] Alcançar 80%+ de cobertura

---

## 📚 Referências

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [Testing Flask Applications](https://flask.palletsprojects.com/en/latest/testing/)

---

**Autor:** Maxwell da Silva Oliveira - M&S do Brasil LTDA
**Versão:** 1.5.2
