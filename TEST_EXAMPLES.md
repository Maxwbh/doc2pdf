# Exemplos de JSON para Testes - DOC2PDF API

Este arquivo contém exemplos de requisições JSON para todos os endpoints da API.

**Autor:** Maxwell da Silva Oliveira - M&S do Brasil LTDA
**Email:** maxwbh@gmail.com
**Versão:** 1.0.3

---

## 📋 Índice

1. [GET /health](#1-get-health)
2. [GET /](#2-get-)
3. [POST /convert](#3-post-convert)
4. [POST /convert-file](#4-post-convert-file)
5. [POST /process](#5-post-process)

---

## 1. GET /health

**Endpoint:** `GET /health`
**Descrição:** Health check da API
**Body:** Nenhum

**Response Esperada:**
```json
{
    "status": "healthy",
    "service": "doc2pdf-api",
    "version": "1.0.3"
}
```

---

## 2. GET /

**Endpoint:** `GET /`
**Descrição:** Informações da API
**Body:** Nenhum

**Response Esperada:**
```json
{
    "service": "DOC to PDF Converter API",
    "version": "1.0.3",
    "author": "Maxwell da Silva Oliveira - M&S do Brasil LTDA",
    "email": "maxwbh@gmail.com",
    "linkedin": "/maxwbh",
    "endpoints": {
        "/health": "GET - Health check",
        "/convert": "POST - Convert DOC to PDF (Base64)",
        "/convert-file": "POST - Convert DOC to PDF (File)",
        "/process": "POST - Flexible processing"
    }
}
```

---

## 3. POST /convert

**Endpoint:** `POST /convert`
**Descrição:** Converte DOC para PDF retornando Base64
**Content-Type:** `application/json`

### Exemplo 1: Conversão Básica

```json
{
    "document": "UEsDBBQABgAIAAAAIQBi7p1oXgEAAJAEAAATAAgCW0NvbnRlbnRfVHlwZXNdLnhtbCCiBAIooAAC...",
    "replacements": {
        "NOME": "Jose da Silva",
        "CPF": "123.456.789-00",
        "DATA": "27/11/2024"
    }
}
```

### Exemplo 2: Contrato Completo

```json
{
    "document": "BASE64_DO_DOCUMENTO_AQUI",
    "replacements": {
        "NOME_COMPLETO": "João Pedro Santos",
        "CPF": "987.654.321-00",
        "RG": "12.345.678-9",
        "ENDERECO": "Av. Paulista, 1000 - Apto 501",
        "CIDADE": "São Paulo",
        "ESTADO": "SP",
        "CEP": "01310-100",
        "TELEFONE": "(11) 98765-4321",
        "EMAIL": "joao.santos@email.com",
        "DATA_NASCIMENTO": "15/03/1985",
        "VALOR": "R$ 5.000,00",
        "DATA_CONTRATO": "27/11/2024"
    }
}
```

**Response Esperada:**
```json
{
    "success": true,
    "pdf": "JVBERi0xLjQKJeLjz9MKMyAwIG9iago8PC9UeXBlL0...",
    "message": "Documento convertido com sucesso"
}
```

---

## 4. POST /convert-file

**Endpoint:** `POST /convert-file`
**Descrição:** Converte DOC para PDF retornando arquivo
**Content-Type:** `application/json`

### Exemplo 1: Sem nome de arquivo

```json
{
    "document": "BASE64_DO_DOCUMENTO_AQUI",
    "replacements": {
        "NOME": "Maria Silva",
        "CARGO": "Desenvolvedora",
        "SALARIO": "R$ 8.000,00"
    }
}
```

### Exemplo 2: Com nome de arquivo customizado

```json
{
    "document": "BASE64_DO_DOCUMENTO_AQUI",
    "replacements": {
        "EMPRESA": "M&S do Brasil LTDA",
        "CNPJ": "12.345.678/0001-90",
        "REPRESENTANTE": "Maxwell Oliveira",
        "CARGO_REP": "Diretor Técnico"
    },
    "filename": "contrato_empresa_2024.pdf"
}
```

**Response:** Arquivo PDF (binary data)
**Headers:**
- `Content-Type: application/pdf`
- `Content-Disposition: attachment; filename="contrato_empresa_2024.pdf"`

---

## 5. POST /process

**Endpoint:** `POST /process`
**Descrição:** Processamento flexível com múltiplos formatos
**Content-Type:** `application/json`

### Parâmetros:

- **input_type**: `base64` | `doc` (padrão: `base64`)
- **output_type**: `pdf` | `doc` | `base64_pdf` | `base64_doc` (padrão: `pdf`)
- **document**: Documento (Base64 string)
- **replacements**: Objeto com tags e valores
- **filename**: Nome do arquivo (opcional)

---

### Exemplo 1: Base64 → PDF (arquivo)

```json
{
    "input_type": "base64",
    "output_type": "pdf",
    "document": "BASE64_DO_DOCUMENTO_AQUI",
    "replacements": {
        "CLIENTE": "Empresa ABC Ltda",
        "PROJETO": "Sistema de Gestão",
        "VALOR_TOTAL": "R$ 50.000,00",
        "PRAZO": "6 meses"
    },
    "filename": "proposta_comercial"
}
```

**Response:** Arquivo PDF (binary data)

---

### Exemplo 2: Base64 → PDF (Base64)

```json
{
    "input_type": "base64",
    "output_type": "base64_pdf",
    "document": "BASE64_DO_DOCUMENTO_AQUI",
    "replacements": {
        "ALUNO": "Carlos Eduardo",
        "CURSO": "Python Avançado",
        "DATA_CONCLUSAO": "27/11/2024",
        "NOTA": "9.5"
    },
    "filename": "certificado_carlos"
}
```

**Response:**
```json
{
    "success": true,
    "output_type": "base64_pdf",
    "document": "JVBERi0xLjQKJeLjz9MKMyAwIG9...",
    "filename": "certificado_carlos.pdf",
    "size_bytes": 45632,
    "message": "Documento processado com sucesso"
}
```

---

### Exemplo 3: Base64 → DOC (arquivo)

```json
{
    "input_type": "base64",
    "output_type": "doc",
    "document": "BASE64_DO_DOCUMENTO_AQUI",
    "replacements": {
        "TITULO": "Relatório Mensal",
        "MES": "Novembro",
        "ANO": "2024",
        "RESPONSAVEL": "Maxwell Oliveira"
    },
    "filename": "relatorio_novembro_2024"
}
```

**Response:** Arquivo DOCX (binary data)
**Headers:**
- `Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document`
- `Content-Disposition: attachment; filename="relatorio_novembro_2024.docx"`

---

### Exemplo 4: Base64 → DOC (Base64)

```json
{
    "input_type": "base64",
    "output_type": "base64_doc",
    "document": "BASE64_DO_DOCUMENTO_AQUI",
    "replacements": {
        "DEPARTAMENTO": "TI",
        "SOLICITANTE": "João Silva",
        "DESCRICAO": "Upgrade de servidores",
        "PRIORIDADE": "Alta"
    },
    "filename": "ordem_servico_001"
}
```

**Response:**
```json
{
    "success": true,
    "output_type": "base64_doc",
    "document": "UEsDBBQABgAIAAAAIQBi7p1oXgEAA...",
    "filename": "ordem_servico_001.docx",
    "size_bytes": 12456,
    "message": "Documento processado com sucesso"
}
```

---

### Exemplo 5: Casos de Uso Completos

#### Caso 1: Geração de Contrato

```json
{
    "input_type": "base64",
    "output_type": "pdf",
    "document": "BASE64_TEMPLATE_CONTRATO",
    "replacements": {
        "CONTRATANTE_NOME": "Empresa XYZ S.A.",
        "CONTRATANTE_CNPJ": "00.000.000/0001-00",
        "CONTRATANTE_ENDERECO": "Rua A, 123 - São Paulo/SP",
        "CONTRATADO_NOME": "José da Silva",
        "CONTRATADO_CPF": "000.000.000-00",
        "CONTRATADO_ENDERECO": "Rua B, 456 - São Paulo/SP",
        "OBJETO": "Prestação de serviços de consultoria",
        "VALOR_MENSAL": "R$ 10.000,00",
        "DATA_INICIO": "01/12/2024",
        "DATA_FIM": "01/12/2025",
        "DATA_ASSINATURA": "27/11/2024",
        "CIDADE_FORO": "São Paulo"
    },
    "filename": "contrato_jose_silva_2024"
}
```

#### Caso 2: Geração de Certificado

```json
{
    "input_type": "base64",
    "output_type": "base64_pdf",
    "document": "BASE64_TEMPLATE_CERTIFICADO",
    "replacements": {
        "NOME_COMPLETO": "Ana Paula Souza",
        "CPF": "111.222.333-44",
        "CURSO": "Desenvolvimento Full Stack",
        "CARGA_HORARIA": "200 horas",
        "DATA_INICIO": "01/06/2024",
        "DATA_CONCLUSAO": "27/11/2024",
        "NOTA_FINAL": "9.8",
        "CODIGO_CERTIFICADO": "CERT-2024-FS-001234"
    },
    "filename": "certificado_ana_paula"
}
```

#### Caso 3: Geração de Proposta Comercial

```json
{
    "input_type": "base64",
    "output_type": "doc",
    "document": "BASE64_TEMPLATE_PROPOSTA",
    "replacements": {
        "CLIENTE": "Tech Solutions Ltda",
        "PROJETO": "Implementação de ERP",
        "ESCOPO": "Desenvolvimento e implantação de sistema ERP completo",
        "PRAZO_TOTAL": "12 meses",
        "FASE1": "Levantamento de requisitos - 2 meses",
        "FASE2": "Desenvolvimento - 6 meses",
        "FASE3": "Testes e homologação - 2 meses",
        "FASE4": "Implantação e treinamento - 2 meses",
        "VALOR_TOTAL": "R$ 250.000,00",
        "FORMA_PAGAMENTO": "12 parcelas mensais",
        "VALIDADE_PROPOSTA": "30 dias",
        "DATA_PROPOSTA": "27/11/2024"
    },
    "filename": "proposta_tech_solutions_erp"
}
```

---

## 🔒 Exemplos de Erros

### Erro 400: Campo Obrigatório Faltando

**Request:**
```json
{
    "replacements": {
        "NOME": "Teste"
    }
}
```

**Response:**
```json
{
    "error": "Campo \"document\" é obrigatório"
}
```

---

### Erro 400: Tipo Inválido

**Request:**
```json
{
    "input_type": "base64",
    "output_type": "invalid_type",
    "document": "BASE64_AQUI",
    "replacements": {}
}
```

**Response:**
```json
{
    "error": "output_type inválido. Use: pdf, doc, base64_pdf, base64_doc"
}
```

---

### Erro 400: Base64 Inválido

**Request:**
```json
{
    "document": "INVALID_BASE64!!!",
    "replacements": {
        "NOME": "Teste"
    }
}
```

**Response:**
```json
{
    "error": "String Base64 inválida"
}
```

---

## 🎯 Dicas de Uso

### 1. Gerando Base64

```bash
# Linux/Mac
base64 documento.docx

# Windows PowerShell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("documento.docx"))

# Python
import base64
with open('documento.docx', 'rb') as f:
    print(base64.b64encode(f.read()).decode('utf-8'))
```

### 2. Decodificando Resposta Base64

```python
import base64

# De PDF Base64 para arquivo
pdf_base64 = response_json['pdf']
pdf_bytes = base64.b64decode(pdf_base64)
with open('resultado.pdf', 'wb') as f:
    f.write(pdf_bytes)

# De DOC Base64 para arquivo
doc_base64 = response_json['document']
doc_bytes = base64.b64decode(doc_base64)
with open('resultado.docx', 'wb') as f:
    f.write(doc_bytes)
```

### 3. Tags no Documento

No seu documento Word, use tags no formato:
- `%%NOME%%`
- `%%ENDERECO%%`
- `%%DATA_NASCIMENTO%%`
- `%%VALOR%%`

As tags serão substituídas pelos valores fornecidos em `replacements`.

---

## 📊 Tabela Comparativa de Endpoints

| Endpoint | Input | Output | Uso Recomendado |
|----------|-------|--------|-----------------|
| `/convert` | Base64 | Base64 PDF | APIs que trabalham com JSON |
| `/convert-file` | Base64 | Arquivo PDF | Download direto, frontends |
| `/process` (pdf) | Base64 | Arquivo PDF | Mesma finalidade que convert-file |
| `/process` (doc) | Base64 | Arquivo DOC | Retornar documento editável |
| `/process` (base64_pdf) | Base64 | Base64 PDF | Mesma finalidade que convert |
| `/process` (base64_doc) | Base64 | Base64 DOC | APIs que precisam de DOC |

---

**Desenvolvido por Maxwell da Silva Oliveira - M&S do Brasil LTDA**
📧 maxwbh@gmail.com | 💼 [LinkedIn: /maxwbh](https://linkedin.com/in/maxwbh)
