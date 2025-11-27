# DOC to PDF Converter API

API Flask para conversão de documentos Word (.DOC) para PDF com substituição de tags.

## Autor

**Maxwell da Silva Oliveira**
M&S do Brasil LTDA
📧 maxwbh@gmail.com
💼 [LinkedIn: /maxwbh](https://linkedin.com/in/maxwbh)

## Descrição

Esta API recebe um arquivo Word em Base64, substitui tags personalizadas (ex: `%%NOME%%`, `%%ENDERECO%%`) pelos valores fornecidos e retorna um PDF em Base64.

## Funcionalidades

- ✅ Recebe documento .DOC/.DOCX em Base64
- ✅ Substitui tags no formato `%%TAG%%` por valores fornecidos
- ✅ Converte documento para PDF
- ✅ Retorna PDF em Base64 ou como arquivo direto
- ✅ Suporte para tags em parágrafos e tabelas
- ✅ Preserva formatação do documento original
- ✅ Pronto para deploy no Render com Docker
- ✅ Coleção completa para Postman incluída

## 🚀 Teste Rápido com Postman

Incluímos uma coleção completa do Postman para facilitar os testes:

1. Importe `DOC2PDF_API.postman_collection.json` no Postman
2. Configure a variável `base_url` (ex: `http://localhost:5000`)
3. Adicione seu documento em Base64 na variável `document_base64`
4. Teste todos os endpoints com exemplos prontos

📖 **Guia completo:** Ver `POSTMAN_GUIDE.md` para instruções detalhadas

## Endpoints

### `GET /`
Retorna informações da API e exemplo de uso.

### `GET /health`
Health check da aplicação.

### `POST /convert`
Converte documento Word para PDF com substituição de tags.

**Request:**
```json
{
  "document": "BASE64_ENCODED_DOC_FILE",
  "replacements": {
    "NOME": "Jose da Silva",
    "ENDERECO": "Rua qualquer coisa, Nro1, Bairro das colinas, São Paulo/SP - CEP: 48.4839-877",
    "DATANASCIMENTO": "01/01/1990",
    "CPF": "123.456.789-00"
  }
}
```

**Response:**
```json
{
  "success": true,
  "pdf": "BASE64_ENCODED_PDF_FILE",
  "message": "Documento convertido com sucesso"
}
```

**Response (Erro):**
```json
{
  "error": "Descrição do erro"
}
```

### `POST /convert-file`
Converte documento Word para PDF com substituição de tags e retorna o arquivo PDF diretamente.

**Request:**
```json
{
  "document": "BASE64_ENCODED_DOC_FILE",
  "replacements": {
    "NOME": "Jose da Silva",
    "ENDERECO": "Rua qualquer coisa, Nro1, Bairro das colinas, São Paulo/SP - CEP: 48.4839-877",
    "DATANASCIMENTO": "01/01/1990",
    "CPF": "123.456.789-00"
  },
  "filename": "contrato_jose_silva.pdf"
}
```

**Response:**
- Retorna arquivo PDF diretamente com `Content-Type: application/pdf`
- Pode ser visualizado no navegador ou baixado automaticamente
- Header `Content-Disposition: attachment; filename="contrato_jose_silva.pdf"`

**Response (Erro):**
```json
{
  "error": "Descrição do erro"
}
```

## Como Usar

### 1. Prepare seu Documento Word

Crie um documento Word com tags no formato `%%NOMEDATAG%%`:

```
Contrato de Prestação de Serviços

Nome: %%NOME%%
Endereço: %%ENDERECO%%
Data de Nascimento: %%DATANASCIMENTO%%
CPF: %%CPF%%
```

### 2. Converta o Documento para Base64

```python
import base64

with open('documento.docx', 'rb') as file:
    doc_base64 = base64.b64encode(file.read()).decode('utf-8')
```

### 3. Faça a Requisição à API

#### Opção A: Retorno em Base64 (endpoint `/convert`)

```python
import requests
import json
import base64

# Prepara os dados
data = {
    "document": doc_base64,
    "replacements": {
        "NOME": "Jose da Silva",
        "ENDERECO": "Rua qualquer coisa, Nro1, Bairro das colinas, São Paulo/SP - CEP: 48.4839-877",
        "DATANASCIMENTO": "01/01/1990",
        "CPF": "123.456.789-00"
    }
}

# Faz a requisição
response = requests.post(
    'https://sua-api.render.com/convert',
    json=data,
    headers={'Content-Type': 'application/json'}
)

# Processa a resposta
if response.status_code == 200:
    result = response.json()
    pdf_base64 = result['pdf']

    # Salva o PDF
    pdf_bytes = base64.b64decode(pdf_base64)
    with open('documento_final.pdf', 'wb') as f:
        f.write(pdf_bytes)
    print("PDF gerado com sucesso!")
else:
    print(f"Erro: {response.json()}")
```

#### Opção B: Retorno como Arquivo PDF (endpoint `/convert-file`)

```python
import requests
import base64

# Prepara os dados
data = {
    "document": doc_base64,
    "replacements": {
        "NOME": "Jose da Silva",
        "ENDERECO": "Rua qualquer coisa, Nro1, Bairro das colinas, São Paulo/SP - CEP: 48.4839-877",
        "DATANASCIMENTO": "01/01/1990",
        "CPF": "123.456.789-00"
    },
    "filename": "contrato_jose_silva.pdf"  # Opcional
}

# Faz a requisição
response = requests.post(
    'https://sua-api.render.com/convert-file',
    json=data,
    headers={'Content-Type': 'application/json'}
)

# Processa a resposta
if response.status_code == 200:
    # Salva o PDF diretamente
    with open('documento_final.pdf', 'wb') as f:
        f.write(response.content)
    print("PDF gerado com sucesso!")
else:
    print(f"Erro: {response.json()}")
```

### 4. Exemplo com cURL

#### Retorno em Base64:
```bash
curl -X POST https://sua-api.render.com/convert \
  -H "Content-Type: application/json" \
  -d '{
    "document": "BASE64_STRING_AQUI",
    "replacements": {
      "NOME": "Jose da Silva",
      "ENDERECO": "Rua qualquer coisa, Nro1",
      "DATANASCIMENTO": "01/01/1990"
    }
  }'
```

#### Retorno como Arquivo PDF (salva diretamente):
```bash
curl -X POST https://sua-api.render.com/convert-file \
  -H "Content-Type: application/json" \
  -d '{
    "document": "BASE64_STRING_AQUI",
    "replacements": {
      "NOME": "Jose da Silva",
      "ENDERECO": "Rua qualquer coisa, Nro1",
      "DATANASCIMENTO": "01/01/1990"
    },
    "filename": "contrato.pdf"
  }' \
  --output documento.pdf
```

## Instalação Local

### Pré-requisitos

- Python 3.11+
- LibreOffice (para conversão PDF)

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/maxwbh/doc2pdf.git
cd doc2pdf
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Instale o LibreOffice:
```bash
# Ubuntu/Debian
sudo apt-get install libreoffice libreoffice-writer

# macOS
brew install libreoffice

# Windows
# Baixe e instale de: https://www.libreoffice.org/download/
```

5. Execute a aplicação:
```bash
python app.py
```

A API estará disponível em `http://localhost:5000`

## Deploy no Render

### Usando Docker

1. Faça login no [Render](https://render.com)

2. Crie um novo **Web Service**

3. Conecte seu repositório GitHub

4. Configure o serviço:
   - **Environment**: Docker
   - **Branch**: main (ou sua branch principal)
   - **Instance Type**: Free ou Starter
   - **Port**: 5000 (ou deixe o Render detectar automaticamente)

5. Variáveis de ambiente (opcional):
   - `PORT`: Porta da aplicação (Render define automaticamente)

6. Clique em **Create Web Service**

O Render irá automaticamente:
- Detectar o Dockerfile
- Fazer o build da imagem
- Fazer deploy da aplicação
- Fornecer uma URL pública

### Testando o Deploy

```bash
# Health check
curl https://sua-api.render.com/health

# Informações da API
curl https://sua-api.render.com/
```

## Estrutura do Projeto

```
doc2pdf/
├── app.py              # Aplicação Flask principal
├── requirements.txt    # Dependências Python
├── Dockerfile         # Configuração Docker
├── .dockerignore      # Arquivos ignorados pelo Docker
└── README.md          # Esta documentação
```

## Tecnologias Utilizadas

- **Flask**: Framework web
- **python-docx**: Manipulação de arquivos Word
- **LibreOffice**: Conversão de DOCX para PDF
- **Gunicorn**: Servidor WSGI para produção
- **Docker**: Containerização

## Notas Importantes

- Tags devem estar no formato `%%NOMEDATAG%%` (maiúsculas recomendadas)
- A API suporta documentos .DOC e .DOCX
- Tamanho máximo do documento: limitado pela configuração do servidor
- Timeout de conversão: 30 segundos
- A conversão preserva a formatação original do documento

## Limitações

- Conversão de imagens complexas pode aumentar o tempo de processamento
- Documentos muito grandes podem exceder o timeout
- Tags dentro de cabeçalhos e rodapés podem não ser substituídas

## Resolução de Problemas

### Erro: "Erro na conversão para PDF"
- Verifique se o LibreOffice está instalado corretamente
- Confirme que o documento Word não está corrompido

### Erro: "String Base64 inválida"
- Verifique se o documento foi corretamente codificado em Base64
- Certifique-se de usar UTF-8 ao decodificar

### Timeout na conversão
- Reduza o tamanho do documento
- Simplifique imagens e formatação complexa

## Suporte

Para questões ou suporte, entre em contato:
- 📧 Email: maxwbh@gmail.com
- 💼 LinkedIn: [/maxwbh](https://linkedin.com/in/maxwbh)

## Licença

Este projeto foi desenvolvido por Maxwell da Silva Oliveira - M&S do Brasil LTDA.

---

**Desenvolvido com ❤️ por Maxwell da Silva Oliveira**
