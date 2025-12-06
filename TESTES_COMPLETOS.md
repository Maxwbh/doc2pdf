# Testes Completos - DOC2PDF API v1.1.2

**Autor:** Maxwell da Silva Oliveira - M&S do Brasil LTDA
**Email:** maxwbh@gmail.com
**LinkedIn:** /maxwbh
**Versão:** 1.1.2

## 📋 Índice

1. [Tipos de Entrada Suportados](#tipos-de-entrada)
2. [Tipos de Saída Suportados](#tipos-de-saída)
3. [Matriz de Testes Completa](#matriz-de-testes)
4. [Exemplos JSON por Endpoint](#exemplos-json)
5. [Casos de Uso Específicos](#casos-de-uso)

---

## 🔹 Tipos de Entrada Suportados

### 1. **Base64_DOCX** (Padrão)
```json
{
  "document": "UEsDBBQAAAAIAOWB0lZm7L5j...",  // DOCX codificado em Base64
  "input_type": "base64"  // Opcional, padrão é "base64"
}
```

**Formatos aceitos:**
- `.doc` (Word 97-2003) em Base64
- `.docx` (Word 2007+) em Base64

**Como gerar:**
```python
import base64
with open('documento.docx', 'rb') as f:
    base64_doc = base64.b64encode(f.read()).decode('utf-8')
```

### 2. **DOC_Bytes**
```json
{
  "document": "bytes_do_documento",
  "input_type": "doc"
}
```

**Uso:** Menos comum, para integração com sistemas que trabalham diretamente com bytes

---

## 🔹 Tipos de Saída Suportados

| Tipo | Formato | Retorno | Uso |
|------|---------|---------|-----|
| **`pdf`** | Arquivo | Download direto | Visualização/download imediato |
| **`doc`** | Arquivo | Download DOCX | Edição posterior do documento |
| **`base64_pdf`** | JSON | PDF em Base64 | Integração com APIs/bancos |
| **`base64_doc`** | JSON | DOCX em Base64 | Armazenamento/transferência |

---

## 📊 Matriz de Testes Completa

### **Endpoint: `/convert`**
| # | Entrada | Saída | Status | Descrição |
|---|---------|-------|--------|-----------|
| 1 | Base64_DOCX | Base64_PDF | ✅ | Padrão - conversão completa |

**Características:**
- ✅ Entrada: Sempre Base64
- ✅ Saída: Sempre Base64_PDF
- ✅ Retorno: JSON com campo `pdf`

---

### **Endpoint: `/convert-file`**
| # | Entrada | Saída | Status | Descrição |
|---|---------|-------|--------|-----------|
| 2 | Base64_DOCX | PDF File | ✅ | Retorna arquivo para download |

**Características:**
- ✅ Entrada: Sempre Base64
- ✅ Saída: Sempre PDF (arquivo)
- ✅ Retorno: Arquivo binário
- ✅ Permite especificar `filename`

---

### **Endpoint: `/process` (Flexível)**

#### **Saída: PDF (Arquivo)**
| # | Entrada | Output Type | Status | Descrição |
|---|---------|-------------|--------|-----------|
| 3 | Base64_DOCX | `pdf` | ✅ | Base64 → PDF file |
| 4 | DOC_Bytes | `pdf` | ✅ | Bytes → PDF file |

#### **Saída: DOCX (Arquivo)**
| # | Entrada | Output Type | Status | Descrição |
|---|---------|-------------|--------|-----------|
| 5 | Base64_DOCX | `doc` | ✅ | Base64 → DOCX file |
| 6 | DOC_Bytes | `doc` | ✅ | Bytes → DOCX file |

#### **Saída: Base64_PDF (JSON)**
| # | Entrada | Output Type | Status | Descrição |
|---|---------|-------------|--------|-----------|
| 7 | Base64_DOCX | `base64_pdf` | ✅ | Base64 → Base64_PDF |
| 8 | DOC_Bytes | `base64_pdf` | ✅ | Bytes → Base64_PDF |

#### **Saída: Base64_DOC (JSON)**
| # | Entrada | Output Type | Status | Descrição |
|---|---------|-------------|--------|-----------|
| 9 | Base64_DOCX | `base64_doc` | ✅ | Base64 → Base64_DOCX |
| 10 | DOC_Bytes | `base64_doc` | ✅ | Bytes → Base64_DOCX |

**TOTAL: 10 combinações diferentes de entrada/saída**

---

## 📝 Exemplos JSON por Endpoint

### **1. `/convert` - Base64 → Base64_PDF**

```json
{
  "document": "UEsDBBQAAAAIAOWB0lZm7L5j...",
  "replacements": {
    "NOME": "João da Silva",
    "CPF": "123.456.789-00",
    "DATA": "05/12/2025"
  }
}
```

**Resposta:**
```json
{
  "success": true,
  "pdf": "JVBERi0xLjQKJeLjz9MKMSAwIG9iago8PC9UeXBlL0Nh...",
  "message": "Documento convertido com sucesso"
}
```

---

### **2. `/convert-file` - Base64 → PDF File**

```json
{
  "document": "UEsDBBQAAAAIAOWB0lZm7L5j...",
  "replacements": {
    "CLIENTE": "Tech Solutions LTDA",
    "VALOR": "R$ 15.000,00"
  },
  "filename": "proposta_tech_solutions.pdf"
}
```

**Resposta:** Arquivo PDF (binário)

---

### **3. `/process` - Base64_DOCX → PDF File**

```json
{
  "input_type": "base64",
  "document": "UEsDBBQAAAAIAOWB0lZm7L5j...",
  "output_type": "pdf",
  "replacements": {
    "EMPRESA": "M&S do Brasil LTDA",
    "PROJETO": "Sistema ERP"
  },
  "filename": "contrato_erp"
}
```

**Resposta:** Arquivo PDF (binário)

---

### **4. `/process` - DOC_Bytes → PDF File**

```json
{
  "input_type": "doc",
  "document": "PK\u0003\u0004\u0014\u0000\u0000...",
  "output_type": "pdf",
  "replacements": {
    "CARGO": "Desenvolvedor Senior",
    "SALARIO": "R$ 12.000,00"
  },
  "filename": "oferta_emprego"
}
```

**Resposta:** Arquivo PDF (binário)

---

### **5. `/process` - Base64_DOCX → DOCX File**

```json
{
  "input_type": "base64",
  "document": "UEsDBBQAAAAIAOWB0lZm7L5j...",
  "output_type": "doc",
  "replacements": {
    "VERSAO": "2.0",
    "DATA_RELEASE": "01/01/2026"
  },
  "filename": "release_notes_v2"
}
```

**Resposta:** Arquivo DOCX (binário)

---

### **6. `/process` - DOC_Bytes → DOCX File**

```json
{
  "input_type": "doc",
  "document": "PK\u0003\u0004\u0014\u0000\u0000...",
  "output_type": "doc",
  "replacements": {
    "AUTOR": "Maxwell Oliveira",
    "REVISAO": "3"
  },
  "filename": "documento_revisado"
}
```

**Resposta:** Arquivo DOCX (binário)

---

### **7. `/process` - Base64_DOCX → Base64_PDF**

```json
{
  "input_type": "base64",
  "document": "UEsDBBQAAAAIAOWB0lZm7L5j...",
  "output_type": "base64_pdf",
  "replacements": {
    "NUMERO_NF": "001234",
    "VALOR_NF": "R$ 10.500,00"
  },
  "filename": "nota_fiscal_001234"
}
```

**Resposta:**
```json
{
  "success": true,
  "output_type": "base64_pdf",
  "document": "JVBERi0xLjQKJeLjz9MKMSAwIG9iago8PC9UeXBlL0Nh...",
  "filename": "nota_fiscal_001234.pdf",
  "size_bytes": 12345,
  "message": "Documento processado com sucesso"
}
```

---

### **8. `/process` - DOC_Bytes → Base64_PDF**

```json
{
  "input_type": "doc",
  "document": "PK\u0003\u0004\u0014\u0000\u0000...",
  "output_type": "base64_pdf",
  "replacements": {
    "PRODUTO": "Licença Software",
    "TOTAL": "R$ 5.000,00"
  },
  "filename": "orcamento"
}
```

**Resposta:**
```json
{
  "success": true,
  "output_type": "base64_pdf",
  "document": "JVBERi0xLjQKJeLjz9MKMSAwIG9iago8PC9UeXBlL0Nh...",
  "filename": "orcamento.pdf",
  "size_bytes": 8765,
  "message": "Documento processado com sucesso"
}
```

---

### **9. `/process` - Base64_DOCX → Base64_DOCX**

```json
{
  "input_type": "base64",
  "document": "UEsDBBQAAAAIAOWB0lZm7L5j...",
  "output_type": "base64_doc",
  "replacements": {
    "ANO": "2025",
    "TRIMESTRE": "Q4"
  },
  "filename": "relatorio_q4_2025"
}
```

**Resposta:**
```json
{
  "success": true,
  "output_type": "base64_doc",
  "document": "UEsDBBQAAAAIAOWB0lZm7L5j...",
  "filename": "relatorio_q4_2025.docx",
  "size_bytes": 6543,
  "message": "Documento processado com sucesso"
}
```

---

### **10. `/process` - DOC_Bytes → Base64_DOCX**

```json
{
  "input_type": "doc",
  "document": "PK\u0003\u0004\u0014\u0000\u0000...",
  "output_type": "base64_doc",
  "replacements": {
    "EVENTO": "Workshop Python",
    "DATA_EVENTO": "15/01/2026"
  },
  "filename": "convite_workshop"
}
```

**Resposta:**
```json
{
  "success": true,
  "output_type": "base64_doc",
  "document": "UEsDBBQAAAAIAOWB0lZm7L5j...",
  "filename": "convite_workshop.docx",
  "size_bytes": 5432,
  "message": "Documento processado com sucesso"
}
```

---

## 🎯 Casos de Uso Específicos

### **Caso 1: Contrato com Múltiplas Tags (15+)**

```json
{
  "input_type": "base64",
  "document": "{{base64_contrato}}",
  "output_type": "pdf",
  "replacements": {
    "CONTRATANTE": "Tech Innovations LTDA",
    "CNPJ_CONTRATANTE": "45.123.789/0001-55",
    "ENDERECO_CONTRATANTE": "Av. Paulista, 1000, São Paulo/SP",
    "CONTRATADO": "Lucas Fernandes",
    "CPF_CONTRATADO": "456.789.123-00",
    "RG_CONTRATADO": "12.345.678-9",
    "ENDERECO_CONTRATADO": "Rua das Flores, 50, Rio/RJ",
    "CARGO": "Desenvolvedor Full Stack Senior",
    "SALARIO": "R$ 15.000,00",
    "DATA_INICIO": "01/02/2026",
    "DATA_FIM": "31/01/2027",
    "CARGA_HORARIA": "40 horas semanais",
    "BENEFICIOS": "VT, VR, Plano de Saúde",
    "DATA_ASSINATURA": "05/12/2025"
  },
  "filename": "contrato_lucas_fernandes_2026"
}
```

---

### **Caso 2: Caracteres Especiais e Acentuação**

```json
{
  "input_type": "base64",
  "document": "{{base64_doc}}",
  "output_type": "base64_pdf",
  "replacements": {
    "NOME": "José Antônio Côrrea",
    "DESCRICAO": "Análise & Desenvolvimento de Software",
    "OBSERVACAO": "100% remoto - Ótimas condições!",
    "VALOR": "R$ 8.500,00 (oito mil e quinhentos reais)"
  },
  "filename": "proposta_jose_antonio"
}
```

---

### **Caso 3: Documento com Tabelas Complexas**

```json
{
  "input_type": "base64",
  "document": "{{base64_tabelas}}",
  "output_type": "pdf",
  "replacements": {
    "MES_REF": "Dezembro/2025",
    "TOTAL_VENDAS": "R$ 250.000,00",
    "TOTAL_DESPESAS": "R$ 180.000,00",
    "LUCRO_LIQUIDO": "R$ 70.000,00",
    "MARGEM": "28%"
  },
  "filename": "relatorio_financeiro_dez_2025"
}
```

---

## 🧪 Como Testar

### **1. Importar Coleção Postman**
```bash
# Importar no Postman:
DOC2PDF_API_COMPLETE.postman_collection.json
```

### **2. Configurar Variáveis**
```
base_url: http://localhost:5000 (local) ou https://sua-api.onrender.com (Render)
base64_docx: [seu documento Base64]
```

### **3. Executar Testes**
- Teste cada endpoint individualmente
- Verifique logs estruturados na resposta
- Confirme tamanhos de arquivo
- Valide conteúdo do PDF/DOCX gerado

---

## 📊 Performance Esperada

| Endpoint | Entrada | Tempo Médio | Observações |
|----------|---------|-------------|-------------|
| `/convert` | Base64 (50KB) | ~1.5s | Inclui conversão PDF |
| `/convert-file` | Base64 (50KB) | ~1.5s | Retorno de arquivo |
| `/process` (PDF) | Base64 (50KB) | ~1.5s | Conversão completa |
| `/process` (DOC) | Base64 (50KB) | ~0.5s | Sem conversão PDF |
| `/process` (Base64_PDF) | Base64 (50KB) | ~1.5s | Com encoding |
| `/process` (Base64_DOC) | Base64 (50KB) | ~0.5s | Apenas encoding |

**Fatores que afetam performance:**
- ✅ Tamanho do documento
- ✅ Número de tags a substituir
- ✅ Complexidade do documento (tabelas, imagens)
- ✅ Recursos do servidor (CPU, memória)

---

## 📚 Referências

- [Postman Collection Completa](./DOC2PDF_API_COMPLETE.postman_collection.json)
- [Documentação da API](./README.md)
- [Guia Docker](./DOCKER_GUIDE.md)
- [Guia Render](./RENDER_GUIDE.md)

---

**Desenvolvido por Maxwell da Silva Oliveira - M&S do Brasil LTDA**
**Todos os direitos reservados © 2025**
