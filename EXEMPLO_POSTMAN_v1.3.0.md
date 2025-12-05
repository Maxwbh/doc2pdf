# Exemplo Postman - DOC2PDF API v1.3.0

**Autor:** Maxwell da Silva Oliveira - M&S do Brasil LTDA
**Versão:** 1.3.0
**Formato de Tags:** `{TAG}` (colchetes)

---

## 📋 Pré-requisitos

### 1. **Criar Documento DOCX com Tags**

Crie um documento Word (.DOCX) com o seguinte conteúdo:

```
═══════════════════════════════════════════════
              CABEÇALHO (Header)
═══════════════════════════════════════════════
CONTRATO DE PRESTAÇÃO DE SERVIÇOS
Data: {DATA}
═══════════════════════════════════════════════


CONTRATO N°: {NUMERO_CONTRATO}

CONTRATANTE:
Nome: {CONTRATANTE}
CNPJ: {CNPJ_CONTRATANTE}
Endereço: {ENDERECO_CONTRATANTE}

CONTRATADO:
Nome: {CONTRATADO}
CPF: {CPF_CONTRATADO}
Endereço: {ENDERECO_CONTRATADO}

OBJETO DO CONTRATO:
Prestação de serviços de {SERVICO} pelo período de {PERIODO}.

VALOR:
R$ {VALOR}

CLÁUSULAS:
1. O contratado {CONTRATADO} compromete-se a...
2. O contratante {CONTRATANTE} pagará...


═══════════════════════════════════════════════
              RODAPÉ (Footer)
═══════════════════════════════════════════════
Contrato {NUMERO_CONTRATO} - {CONTRATANTE} - Página {PAGINA}
═══════════════════════════════════════════════
```

### 2. **Converter DOCX para Base64**

**Python:**
```python
import base64

with open('contrato_template.docx', 'rb') as f:
    docx_base64 = base64.b64encode(f.read()).decode('utf-8')
    print(docx_base64)
```

**Bash/Linux:**
```bash
base64 -w 0 contrato_template.docx > contrato_base64.txt
cat contrato_base64.txt
```

**PowerShell (Windows):**
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("contrato_template.docx")) | Out-File contrato_base64.txt
```

**Node.js:**
```javascript
const fs = require('fs');
const buffer = fs.readFileSync('contrato_template.docx');
const base64 = buffer.toString('base64');
console.log(base64);
```

---

## 🚀 Exemplo 1: `/convert` - Retorna PDF em Base64

### **Request**

```json
POST {{base_url}}/convert
Content-Type: application/json

{
  "document": "UEsDBBQAAAAIAOWB0lZm7L5jLwEAAIsDAAATAAAAW0NvbnRlbnRfVHlwZXNdLnhtbK2S...",
  "replacements": {
    "DATA": "05/12/2025",
    "NUMERO_CONTRATO": "2025/001",
    "CONTRATANTE": "Tech Solutions LTDA",
    "CNPJ_CONTRATANTE": "12.345.678/0001-90",
    "ENDERECO_CONTRATANTE": "Av. Paulista, 1000, São Paulo/SP - CEP: 01310-100",
    "CONTRATADO": "João da Silva",
    "CPF_CONTRATADO": "123.456.789-00",
    "ENDERECO_CONTRATADO": "Rua das Flores, 123, São Paulo/SP - CEP: 04567-890",
    "SERVICO": "Desenvolvimento de Software",
    "PERIODO": "12 meses",
    "VALOR": "120.000,00",
    "PAGINA": "1"
  }
}
```

### **Response (200 OK)**

```json
{
  "success": true,
  "pdf": "JVBERi0xLjQKJeLjz9MKMSAwIG9iago8PC9UeXBlL0NhdGFsb2cvUGFnZXMgMiAwIFI+PgplbmRvYmoKMiAwIG9iago8PC9UeXBlL1BhZ2VzL0tpZHNbMyAwIFJdL0NvdW50IDE+PgplbmRvYmoKMyAwIG9iago8PC9UeXBlL1BhZ2UvTWVkaWFCb3hbMCA...",
  "message": "Documento convertido com sucesso"
}
```

### **Logs Esperados**

```
>>> NOVA REQUISIÇÃO
Método: POST
Endpoint: /convert
✓ Validação OK - 11 substituições encontradas
Tags a substituir: ['DATA', 'NUMERO_CONTRATO', 'CONTRATANTE', ...]
Etapa 1/4: Decodificando documento Base64...
✓ Documento decodificado (12345 bytes) em 0.005s
Etapa 2/4: Substituindo tags no documento...
✓ Formato DOCX detectado (arquivo ZIP)
Substituindo tags nos parágrafos...
Substituindo tags nas tabelas...
Substituindo tags nos cabeçalhos...
  ✓ Tag {DATA} substituída no cabeçalho
  ✓ Tag {NUMERO_CONTRATO} substituída no cabeçalho
Substituindo tags nos rodapés...
  ✓ Tag {NUMERO_CONTRATO} substituída no rodapé
  ✓ Tag {CONTRATANTE} substituída no rodapé
  ✓ Tag {PAGINA} substituída no rodapé
Total de tags substituídas: 25
✓ Tags substituídas em 0.125s
Etapa 3/4: Salvando documento DOCX...
✓ DOCX salvo (12567 bytes) em 0.012s
Etapa 4/4: Convertendo DOCX para PDF...
✓ PDF gerado (23456 bytes) em 1.845s
✅ CONVERSÃO CONCLUÍDA COM SUCESSO
Resumo: DOCX (12567b) -> PDF (23456b) -> Base64 (31275 chars)
Tempo total de conversão: 2.156s
<<< RESPOSTA ENVIADA
Status: 200
```

---

## 📄 Exemplo 2: `/convert-file` - Retorna PDF como Arquivo

### **Request**

```json
POST {{base_url}}/convert-file
Content-Type: application/json

{
  "document": "UEsDBBQAAAAIAOWB0lZm7L5jLwEAAIsDAAATAAAAW0NvbnRlbnRfVHlwZXNdLnhtbK2S...",
  "replacements": {
    "DATA": "05/12/2025",
    "NUMERO_CONTRATO": "2025/001",
    "CONTRATANTE": "Tech Solutions LTDA",
    "CNPJ_CONTRATANTE": "12.345.678/0001-90",
    "ENDERECO_CONTRATANTE": "Av. Paulista, 1000, São Paulo/SP",
    "CONTRATADO": "João da Silva",
    "CPF_CONTRATADO": "123.456.789-00",
    "ENDERECO_CONTRATADO": "Rua das Flores, 123, São Paulo/SP",
    "SERVICO": "Desenvolvimento de Software",
    "PERIODO": "12 meses",
    "VALOR": "120.000,00",
    "PAGINA": "1"
  },
  "filename": "contrato_tech_solutions_2025_001.pdf"
}
```

### **Response (200 OK)**

```
Content-Type: application/pdf
Content-Disposition: attachment; filename="contrato_tech_solutions_2025_001.pdf"

[Arquivo PDF binário para download]
```

---

## 🔄 Exemplo 3: `/process` - Múltiplos Formatos de Saída

### **3A. Saída: PDF (arquivo)**

```json
POST {{base_url}}/process
Content-Type: application/json

{
  "input_type": "base64",
  "document": "UEsDBBQAAAAIAOWB0lZm7L5jLwEAAIsDAAATAAAAW0NvbnRlbnRfVHlwZXNdLnhtbK2S...",
  "output_type": "pdf",
  "replacements": {
    "NOME": "Maria Santos",
    "CPF": "987.654.321-00",
    "DATA": "05/12/2025"
  },
  "filename": "certificado_maria_santos"
}
```

**Response:** Arquivo PDF (download)

---

### **3B. Saída: Base64_PDF (JSON)**

```json
POST {{base_url}}/process
Content-Type: application/json

{
  "input_type": "base64",
  "document": "UEsDBBQAAAAIAOWB0lZm7L5jLwEAAIsDAAATAAAAW0NvbnRlbnRfVHlwZXNdLnhtbK2S...",
  "output_type": "base64_pdf",
  "replacements": {
    "NOME": "Pedro Oliveira",
    "EMAIL": "pedro@example.com",
    "TELEFONE": "(11) 98765-4321"
  },
  "filename": "proposta_pedro"
}
```

**Response:**
```json
{
  "success": true,
  "output_type": "base64_pdf",
  "document": "JVBERi0xLjQKJeLjz9MKMSAwIG9iago8PC9UeXBlL0Nh...",
  "filename": "proposta_pedro.pdf",
  "size_bytes": 18765,
  "message": "Documento processado com sucesso"
}
```

---

## 🧪 Testando no Postman

### **Passo 1: Configurar Variáveis**

Em **Environment** ou **Collection Variables**, adicione:

```
base_url: http://localhost:5000
```

Ou para produção no Render:

```
base_url: https://sua-api.onrender.com
```

### **Passo 2: Criar Request**

1. **Method:** POST
2. **URL:** `{{base_url}}/convert-file`
3. **Headers:**
   ```
   Content-Type: application/json
   ```
4. **Body (raw JSON):**
   ```json
   {
     "document": "[SEU_BASE64_AQUI]",
     "replacements": {
       "NOME": "João da Silva",
       "CPF": "123.456.789-00",
       "DATA": "05/12/2025"
     },
     "filename": "teste.pdf"
   }
   ```

### **Passo 3: Enviar e Visualizar**

- Clique em **Send**
- Para `/convert-file` e `/process` (output=pdf): O PDF será baixado automaticamente
- Para `/convert` e `/process` (output=base64_pdf): Copie o campo `pdf` ou `document` e decodifique

### **Decodificar Base64 para PDF:**

**Python:**
```python
import base64

pdf_base64 = "JVBERi0xLjQKJe..."  # Do response
with open('documento.pdf', 'wb') as f:
    f.write(base64.b64decode(pdf_base64))
```

**Node.js:**
```javascript
const fs = require('fs');
const pdfBase64 = "JVBERi0xLjQKJe...";
fs.writeFileSync('documento.pdf', Buffer.from(pdfBase64, 'base64'));
```

---

## 📊 Exemplos de Tags Comuns

### **Contrato**
```json
{
  "CONTRATANTE": "Empresa XYZ",
  "CONTRATADO": "João Silva",
  "DATA": "05/12/2025",
  "VALOR": "R$ 50.000,00",
  "PRAZO": "12 meses"
}
```

### **Certificado**
```json
{
  "NOME": "Maria Santos",
  "CURSO": "Python Avançado",
  "CARGA_HORARIA": "40 horas",
  "DATA_CONCLUSAO": "05/12/2025",
  "INSTRUTOR": "Prof. Carlos Silva"
}
```

### **Proposta Comercial**
```json
{
  "CLIENTE": "Tech Company LTDA",
  "PROJETO": "Sistema ERP",
  "VALOR_TOTAL": "R$ 250.000,00",
  "PRAZO_ENTREGA": "6 meses",
  "DATA_PROPOSTA": "05/12/2025"
}
```

### **Nota Fiscal**
```json
{
  "NUMERO_NF": "001234",
  "CLIENTE": "ABC Comércio",
  "VALOR": "R$ 10.500,00",
  "DATA_EMISSAO": "05/12/2025",
  "VENCIMENTO": "20/12/2025"
}
```

---

## 🎯 Dicas Importantes

### ✅ **DO's (Faça)**
- Use tags em **MAIÚSCULAS**: `{NOME}` ✅
- Coloque tags onde precisar: parágrafos, tabelas, headers, footers
- Use nomes descritivos: `{NOME_COMPLETO}`, `{CPF_FORMATADO}`
- Teste com documento simples primeiro

### ❌ **DON'Ts (Não Faça)**
- ~~Usar minúsculas~~: `{nome}` ❌ (não funcionará)
- ~~Usar formato antigo~~: `%%NOME%%` ❌ (versão antiga)
- ~~Espaços nas tags~~: `{NOME COMPLETO}` ❌
- ~~Caracteres especiais~~: `{NOME@EMPRESA}` ❌

### 💡 **Boas Práticas**
1. Mantenha tags simples: `{NOME}`, `{DATA}`, `{VALOR}`
2. Use underscores para separar: `{DATA_NASCIMENTO}`
3. Documente suas tags em cada template
4. Teste substituição antes de usar em produção

---

## 📚 Recursos Adicionais

- [Coleção Postman Completa](./DOC2PDF_API_COMPLETE.postman_collection.json)
- [Testes Completos](./TESTES_COMPLETOS.md)
- [Documentação da API](./README.md)
- [Changelog v1.3.0](./CHANGELOG.md)

---

**Desenvolvido por Maxwell da Silva Oliveira - M&S do Brasil LTDA**
**Email:** maxwbh@gmail.com
**LinkedIn:** /maxwbh
**Versão:** 1.3.0
