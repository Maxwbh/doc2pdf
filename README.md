<div align="center">

# 📄 DOC to PDF Converter API

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.4.0-brightgreen.svg)](CHANGELOG.md)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**API REST profissional para conversão de documentos Word para PDF com substituição inteligente de tags**

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Maxwbh/doc2pdf)

[Funcionalidades](#funcionalidades) •
[Instalação](#instalação) •
[Uso](#como-usar) •
[API](#endpoints) •
[Deploy](#-deploy-rápido) •
[Contribuir](CONTRIBUTING.md)

</div>

---

## 📖 Descrição

API Flask moderna e robusta que permite converter documentos Word (.DOC/.DOCX) para PDF com substituição dinâmica de tags. Perfeita para geração automatizada de contratos, relatórios, certificados e outros documentos personalizados.

**Desenvolvido por:** [Maxwell da Silva Oliveira](https://linkedin.com/in/maxwbh) - [M&S do Brasil LTDA](mailto:maxwbh@gmail.com)

## Funcionalidades

- ✅ Recebe documento .DOC/.DOCX em Base64
- ✅ Substitui tags no formato `{TAG}` por valores fornecidos
- ✅ Converte documento para PDF com **controle de qualidade** (high/medium/low)
- ✅ Retorna PDF em Base64 ou como arquivo direto
- ✅ Suporte para tags em **parágrafos, tabelas, cabeçalhos e rodapés**
- ✅ Preserva formatação do documento original
- ✅ **Opções avançadas de qualidade**: 300/150/75 DPI
- ✅ **LibreOffice com filtros profissionais** de exportação PDF
- ✅ Pronto para deploy no Render com Docker
- ✅ Coleção completa para Postman incluída

### 🆕 Novidade v1.4.0: Controle de Qualidade de PDF

Escolha entre 3 perfis de qualidade:
- **HIGH** (300 DPI) - Ideal para impressão e documentos oficiais
- **MEDIUM** (150 DPI) - Balanceado para email e visualização
- **LOW** (75 DPI) - Otimizado para web e rascunhos

📖 **Documentação completa:** [QUALIDADE_PDF.md](QUALIDADE_PDF.md)

---

## ☁️ Deploy Rápido

Escolha a opção mais adequada para você:

### Opção 1: Render (1 Clique) ⭐ Mais Fácil

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Maxwbh/doc2pdf)

**Pronto em 5 minutos!** Deploy automático com configuração zero.

📖 **Guia completo:** [RENDER_GUIDE.md](RENDER_GUIDE.md)

### Opção 2: Docker (Localmente)

```bash
docker-compose up -d
# API rodando em http://localhost:5000
```

📖 **Guia completo:** [DOCKER_GUIDE.md](DOCKER_GUIDE.md)

### Opção 3: pip (Desenvolvimento)

```bash
pip install git+https://github.com/Maxwbh/doc2pdf.git
python wsgi.py
```

---

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
  },
  "quality": "high"
}
```

**Parâmetros:**
- `document` (obrigatório): Documento DOCX em Base64
- `replacements` (obrigatório): Objeto com tags e valores
- `quality` (opcional): Qualidade do PDF - `"high"` (padrão), `"medium"` ou `"low"`

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

### `POST /process` ⭐ NOVO

Endpoint flexível que suporta múltiplos formatos de entrada e saída.

**Parâmetros:**
- `input_type`: `base64` ou `doc` (padrão: `base64`)
- `output_type`: `pdf`, `doc`, `base64_pdf`, `base64_doc` (padrão: `pdf`)
- `document`: Documento em Base64
- `replacements`: Tags e valores
- `filename`: Nome do arquivo (opcional)

**Exemplo 1 - Retorna PDF (arquivo):**
```json
{
  "input_type": "base64",
  "output_type": "pdf",
  "document": "BASE64_ENCODED_DOC_FILE",
  "replacements": {
    "CLIENTE": "Empresa ABC",
    "PROJETO": "Sistema de Gestão"
  },
  "filename": "proposta_comercial"
}
```

**Exemplo 2 - Retorna DOC editado (Base64):**
```json
{
  "input_type": "base64",
  "output_type": "base64_doc",
  "document": "BASE64_ENCODED_DOC_FILE",
  "replacements": {
    "TITULO": "Relatório Mensal",
    "MES": "Novembro"
  }
}
```

**Response (Base64):**
```json
{
  "success": true,
  "output_type": "base64_doc",
  "document": "BASE64_ENCODED_DOC",
  "filename": "documento.docx",
  "size_bytes": 12456
}
```

📖 **Exemplos completos:** Ver [TEST_EXAMPLES.md](TEST_EXAMPLES.md) para todos os casos de uso

---

## 🧪 Testes

### Suite de Testes Completa ⭐ NOVO v1.5.2

O projeto conta com uma **suite completa de 120+ testes** cobrindo todos os componentes:

| Componente | Testes | Status | Cobertura |
|------------|--------|--------|-----------|
| Validators | 31 | ✅ PASS | ~100% |
| DOCX Service | 46 | ✅ PASS | ~95% |
| Encoders | 18 | ✅ PASS | ~100% |
| PDF Service | 25 | ⚠️ Requer LibreOffice | ~80% |
| **TOTAL** | **120+** | **97% PASS** | **~94%** |

### Executar Testes

```bash
# Instalar dependências de teste
pip install pytest python-docx flask werkzeug

# Criar documentos de teste
python tests/fixtures/create_test_documents.py

# Executar todos os testes
pytest tests/ -v

# Executar testes específicos
pytest tests/unit/test_validators.py -v
pytest tests/unit/test_lista_vendas.py -v  # Testes do ListaVendas.docx
```

### Documentação de Testes

- 📋 **[Plano de Testes Completo](tests/PLANO_DE_TESTES.md)** - 120+ casos de teste documentados
- ✅ **[Relatório de Validação](tests/VALIDACAO_COMPLETA.md)** - Validação completa da suite
- 📖 **[Guia de Testes](tests/README.md)** - Como executar e criar testes

### Testes do ListaVendas.docx

Testes específicos para o template de vendas:

```python
# Template testado
Listagem de Vendas
Cliente: {NOME_CLIENTE}
Data da Venda: {DATA_VENDA}
Valor: {VALOR}
```

**Validações:**
- ✅ Substituição correta de todas as tags
- ✅ Preservação do título e formatação
- ✅ Conversão para PDF
- ✅ Integridade dos dados

**Executar:**
```bash
pytest tests/unit/test_lista_vendas.py -v
```

---

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

---

## 📦 Instalação

### Instalação via pip

```bash
# Instalação direta do repositório
pip install git+https://github.com/Maxwbh/doc2pdf.git

# Ou clone e instale localmente
git clone https://github.com/Maxwbh/doc2pdf.git
cd doc2pdf
pip install -e .

# Com dependências de desenvolvimento
pip install -e ".[dev]"
```

### Instalação via Docker 🐳 (Recomendado)

A forma mais rápida e fácil de executar a API!

```bash
# 1. Clone o repositório
git clone https://github.com/Maxwbh/doc2pdf.git
cd doc2pdf

# 2. Inicie com Docker Compose
docker-compose up -d

# 3. Acesse a API
curl http://localhost:5000/health
```

**Pronto!** A API está rodando em `http://localhost:5000`

📖 **Guia completo:** Ver [DOCKER_GUIDE.md](DOCKER_GUIDE.md) para configurações avançadas

### Instalação Manual

#### Pré-requisitos

- Python 3.9+ (recomendado: 3.11+)
- LibreOffice (para conversão PDF)
- pip e virtualenv

#### Passos

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
python wsgi.py
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
├── wsgi.py            # Entry point WSGI para produção
├── app/               # Aplicação Flask modular (factory pattern)
├── config/            # Configurações centralizadas
├── requirements.txt   # Dependências Python
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

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia o [Guia de Contribuição](CONTRIBUTING.md) para detalhes sobre:

- Como reportar bugs
- Como sugerir melhorias
- Padrões de código
- Processo de desenvolvimento
- Sistema de versionamento

### Passos Rápidos

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

---

## 📝 Versionamento

Este projeto usa [Versionamento Semântico](https://semver.org/lang/pt-BR/). Para o histórico de versões, veja o [CHANGELOG](CHANGELOG.md).

### Incrementar Versão

```bash
# Patch (1.0.0 -> 1.0.1)
python bump_version.py patch

# Minor (1.0.0 -> 1.1.0)
python bump_version.py minor

# Major (1.0.0 -> 2.0.0)
python bump_version.py major
```

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

```
Copyright (c) 2024 Maxwell da Silva Oliveira - M&S do Brasil LTDA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 📞 Suporte e Contato

### Suporte Técnico

- 📧 **Email:** [maxwbh@gmail.com](mailto:maxwbh@gmail.com)
- 💼 **LinkedIn:** [/maxwbh](https://linkedin.com/in/maxwbh)
- 🐛 **Issues:** [GitHub Issues](https://github.com/Maxwbh/doc2pdf/issues)
- 📖 **Documentação:** [POSTMAN_GUIDE.md](POSTMAN_GUIDE.md)

### Links Úteis

- [Changelog](CHANGELOG.md) - Histórico de versões
- [Contributing](CONTRIBUTING.md) - Guia de contribuição
- [Render Guide](RENDER_GUIDE.md) - Deploy no Render (1 clique)
- [Docker Guide](DOCKER_GUIDE.md) - Instalação com Docker
- [Test Examples](TEST_EXAMPLES.md) - Exemplos de JSON
- [Postman Collection](DOC2PDF_API.postman_collection.json) - Testes da API
- [Postman Guide](POSTMAN_GUIDE.md) - Como usar Postman
- [Examples](example_usage.py) - Exemplos de uso em Python

---

<div align="center">

**Desenvolvido com ❤️ por [Maxwell da Silva Oliveira](https://linkedin.com/in/maxwbh)**

**M&S do Brasil LTDA** | 2024

[![GitHub](https://img.shields.io/badge/GitHub-Maxwbh-181717?logo=github)](https://github.com/Maxwbh)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-maxwbh-0A66C2?logo=linkedin)](https://linkedin.com/in/maxwbh)

</div>
