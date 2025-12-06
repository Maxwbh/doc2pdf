# 📚 Documentação DOC2PDF API

Esta pasta contém toda a documentação do projeto organizada por categoria.

## 📂 Estrutura

```
docs/
├── api/               # 🔌 Especificações da API
├── architecture/      # 🏗️ Decisões de arquitetura
├── examples/          # 💡 Exemplos de uso
├── guides/            # 📖 Guias e tutoriais
└── postman/           # 📬 Collections Postman
```

---

## 🔌 API (`docs/api/`)

**openapi.yaml** - Especificação OpenAPI 3.0 completa

- Todos os endpoints documentados
- Schemas de request/response
- Exemplos de uso
- Acesse interativamente em: `/api/docs`

---

## 🏗️ Arquitetura (`docs/architecture/`)

**ARQUITETURAS_COMPARACAO.md** - Análise comparativa de stacks

- Comparação de 5 frameworks/linguagens
- Métricas de performance
- Análise de custos
- Recomendações por cenário
- Planos de migração

---

## 💡 Exemplos (`docs/examples/`)

Exemplos práticos de uso da API:

- **python_example.py** - Exemplos completos em Python
- **curl_examples.sh** - Scripts cURL prontos
- **javascript_example.js** - Exemplos Node.js/JavaScript

---

## 📖 Guias (`docs/guides/`)

**QUALIDADE_PDF.md** - Guia completo de qualidade de PDF

- 3 perfis de qualidade (high/medium/low)
- Comparação de DPI e tamanhos
- Casos de uso específicos
- Melhores práticas

---

## 📬 Postman (`docs/postman/`)

**DOC2PDF_v1.5.0_Tests.postman_collection.json** - Testes automatizados

- 15+ testes automatizados
- Cobertura completa de endpoints
- Validações de erro
- Testes de qualidade
- Pronto para CI/CD

### Como usar:
```bash
# Newman (CLI)
newman run docs/postman/DOC2PDF_v1.5.0_Tests.postman_collection.json

# Ou importe no Postman Desktop/Web
```

---

## 🚀 Quick Start

### 1. Ver documentação interativa
```bash
python app.py
# Acesse: http://localhost:5000/api/docs
```

### 2. Testar com Postman
```bash
# Importe a collection
docs/postman/DOC2PDF_v1.5.0_Tests.postman_collection.json
```

### 3. Rodar exemplos
```bash
# Python
python docs/examples/python_example.py

# cURL
bash docs/examples/curl_examples.sh

# Node.js
node docs/examples/javascript_example.js
```

---

**Autor:** Maxwell da Silva Oliveira - M&S do Brasil LTDA
**Versão:** 1.5.2
