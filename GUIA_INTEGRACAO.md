# 🔌 Guia de Integração - API DOC2PDF

**URL de Produção:** https://doc2pdf-api.onrender.com
**Versão:** 1.6.0
**Autor:** Maxwell da Silva Oliveira - M&S do Brasil LTDA

---

## 🚀 Início Rápido

### Instalação

```bash
# Instalar requests (única dependência necessária)
pip install requests
```

### Exemplo Mínimo

```python
import requests
import base64

# 1. Carrega documento
with open('documento.docx', 'rb') as f:
    doc_base64 = base64.b64encode(f.read()).decode('utf-8')

# 2. Envia para API
response = requests.post(
    'https://doc2pdf-api.onrender.com/convert',
    json={
        'document': doc_base64,
        'replacements': {
            'NOME': 'João Silva',
            'DATA': '06/12/2025'
        },
        'quality': 'medium'
    },
    timeout=60
)

# 3. Salva PDF
pdf_bytes = base64.b64decode(response.json()['pdf'])
with open('saida.pdf', 'wb') as f:
    f.write(pdf_bytes)
```

---

## 📖 Cliente Python

### Uso da Classe DOC2PDFClient

```python
from examples.integracao_api import DOC2PDFClient

# Inicializa cliente
client = DOC2PDFClient()

# Converte documento
pdf_path = client.convert_to_pdf_file(
    'template.docx',
    {'NOME': 'Maria Santos', 'CPF': '123.456.789-00'},
    output_path='resultado.pdf',
    quality='high'
)
```

### Métodos Disponíveis

| Método | Descrição | Retorno |
|--------|-----------|---------|
| `health_check()` | Verifica status da API | dict |
| `convert_to_pdf_base64()` | Converte e retorna Base64 | dict |
| `convert_to_pdf_file()` | Converte e salva arquivo | str (caminho) |

---

## 🌐 Endpoints da API

### Base URL
```
https://doc2pdf-api.onrender.com
```

### 1. Health Check

**Endpoint:** `GET /health`

**Exemplo:**
```bash
curl https://doc2pdf-api.onrender.com/health
```

**Resposta:**
```json
{
  "service": "DOC2PDF Converter API",
  "status": "healthy",
  "version": "1.6.0"
}
```

### 2. Conversão com Base64

**Endpoint:** `POST /convert`

**Request:**
```json
{
  "document": "BASE64_ENCODED_DOCX",
  "replacements": {"TAG": "valor"},
  "quality": "medium"
}
```

**Response:**
```json
{
  "success": true,
  "pdf": "BASE64_ENCODED_PDF",
  "message": "Documento convertido com sucesso"
}
```

### 3. Conversão com Arquivo

**Endpoint:** `POST /convert-file`

**Request:**
```json
{
  "document": "BASE64_ENCODED_DOCX",
  "replacements": {"NOME": "João"},
  "filename": "contrato.pdf"
}
```

**Response:** Arquivo PDF direto

---

## 💡 Exemplos Práticos

### Exemplo 1: Listagem de Vendas

```python
from examples.integracao_api import DOC2PDFClient

client = DOC2PDFClient()

pdf_path = client.convert_to_pdf_file(
    'templates/ListaVendas.docx',
    {
        'NOME_CLIENTE': 'João Silva',
        'DATA_VENDA': '06/12/2025',
        'VALOR': 'R$ 1.500,00'
    },
    output_path='vendas/joao_silva.pdf',
    quality='high'
)
```

### Exemplo 2: Lote de Documentos

```python
contratos = [
    {'NOME': 'Maria Santos', 'VALOR': 'R$ 15.000,00'},
    {'NOME': 'Pedro Costa', 'VALOR': 'R$ 20.000,00'},
]

for i, dados in enumerate(contratos, 1):
    client.convert_to_pdf_file(
        'template.docx',
        dados,
        output_path=f'contrato_{i}.pdf'
    )
```

---

## 🎨 Qualidades de PDF

| Qualidade | DPI | Uso Recomendado |
|-----------|-----|-----------------|
| **high** | 300 | Impressão, documentos oficiais |
| **medium** | 150 | Email, visualização geral |
| **low** | 75 | Web, rascunhos |

---

## 🔐 Tratamento de Erros

```python
import requests

try:
    result = client.convert_to_pdf_file('template.docx', {'NOME': 'João'})

except FileNotFoundError:
    print("❌ Arquivo não encontrado")

except requests.exceptions.Timeout:
    print("❌ Timeout na requisição")

except requests.exceptions.HTTPError as e:
    print(f"❌ Erro HTTP: {e.response.status_code}")
```

---

## 🧪 Testes

```bash
# Executar exemplos
python examples/integracao_api.py

# Exemplo simples
python examples/exemplo_simples.py
```

---

## 📞 Suporte

**Desenvolvedor:** Maxwell da Silva Oliveira
**Email:** maxwbh@gmail.com
**LinkedIn:** /maxwbh
**API:** https://doc2pdf-api.onrender.com

---

<div align="center">

**🔌 Guia de Integração - API DOC2PDF v1.6.0**

Criado por **Maxwell da Silva Oliveira**

**M&S do Brasil LTDA | 2025**

</div>
