# Guia de Uso - Postman

Este guia explica como usar a coleção do Postman para testar a API DOC to PDF Converter.

**Autor:** Maxwell da Silva Oliveira - M&S do Brasil LTDA
**Email:** maxwbh@gmail.com
**LinkedIn:** /maxwbh

---

## 📥 Importar Coleção no Postman

1. Abra o Postman
2. Clique em **Import** no canto superior esquerdo
3. Selecione o arquivo `DOC2PDF_API.postman_collection.json`
4. A coleção "DOC to PDF Converter API" será importada com todos os endpoints

---

## ⚙️ Configurar Variáveis de Ambiente

A coleção usa variáveis para facilitar o uso:

### Variáveis Disponíveis:

| Variável | Valor Padrão | Descrição |
|----------|--------------|-----------|
| `base_url` | `http://localhost:5000` | URL base da API |
| `document_base64` | `COLE_SEU_DOCUMENTO_BASE64_AQUI` | Documento codificado em Base64 |

### Como Alterar as Variáveis:

1. Clique no ícone de olho (👁️) no canto superior direito
2. Edite os valores conforme necessário:
   - **Local:** Use `http://localhost:5000`
   - **Produção (Render):** Use `https://sua-api.render.com`

---

## 📝 Preparar Documento Base64

Antes de testar os endpoints de conversão, você precisa converter seu documento Word para Base64.

### Opção 1: Python

```python
import base64

with open('seu_documento.docx', 'rb') as f:
    doc_base64 = base64.b64encode(f.read()).decode('utf-8')
    print(doc_base64)
```

### Opção 2: Online

Use serviços como:
- https://base64.guru/converter/encode/file
- https://www.base64encode.org/

### Opção 3: Linha de Comando (Linux/Mac)

```bash
base64 seu_documento.docx
```

### Opção 4: PowerShell (Windows)

```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("seu_documento.docx"))
```

Depois de gerar o Base64:
1. Copie o resultado
2. No Postman, clique no ícone de olho (👁️)
3. Cole o Base64 na variável `document_base64`

---

## 🧪 Testar Endpoints

### 1. Health Check

**Endpoint:** `GET {{base_url}}/health`

**Descrição:** Verifica se a API está funcionando.

**Como usar:**
1. Selecione o request "Health Check"
2. Clique em **Send**
3. Você deve receber:
```json
{
    "status": "healthy",
    "service": "doc2pdf-api",
    "version": "1.0.0"
}
```

---

### 2. API Info

**Endpoint:** `GET {{base_url}}/`

**Descrição:** Retorna informações sobre a API.

**Como usar:**
1. Selecione o request "API Info"
2. Clique em **Send**
3. Você receberá informações sobre todos os endpoints disponíveis

---

### 3. Convert DOC to PDF (Base64)

**Endpoint:** `POST {{base_url}}/convert`

**Descrição:** Converte documento e retorna PDF em Base64.

**Como usar:**

1. **Prepare seu documento Word:**
   - Crie um documento com tags: `%%NOME%%`, `%%ENDERECO%%`, etc.
   - Salve como `.docx`

2. **Converta para Base64:**
   - Use uma das opções acima para gerar Base64
   - Cole na variável `document_base64`

3. **Configure as substituições:**
   - No body do request, ajuste os valores em `replacements`
   ```json
   {
       "document": "{{document_base64}}",
       "replacements": {
           "NOME": "Jose da Silva",
           "ENDERECO": "Rua ABC, 123",
           "DATANASCIMENTO": "01/01/1990",
           "CPF": "123.456.789-00"
       }
   }
   ```

4. **Envie a requisição:**
   - Clique em **Send**
   - O PDF será retornado em Base64 no campo `pdf`

5. **Salve o PDF:**
   - Copie o Base64 do campo `pdf` da resposta
   - Use Python para salvar:
   ```python
   import base64

   pdf_base64 = "COLE_O_BASE64_AQUI"
   pdf_bytes = base64.b64decode(pdf_base64)

   with open('resultado.pdf', 'wb') as f:
       f.write(pdf_bytes)
   ```

**Resposta de Sucesso:**
```json
{
    "success": true,
    "pdf": "JVBERi0xLjQKJeLjz9MKMyAwIG9iago8P...",
    "message": "Documento convertido com sucesso"
}
```

---

### 4. Convert DOC to PDF (File) ⭐ RECOMENDADO

**Endpoint:** `POST {{base_url}}/convert-file`

**Descrição:** Converte documento e retorna arquivo PDF diretamente.

**Como usar:**

1. **Prepare seu documento Word:**
   - Crie um documento com tags: `%%NOME%%`, `%%ENDERECO%%`, etc.
   - Salve como `.docx`

2. **Converta para Base64:**
   - Use uma das opções acima para gerar Base64
   - Cole na variável `document_base64`

3. **Configure as substituições:**
   - No body do request, ajuste os valores
   - Adicione o nome do arquivo de saída (opcional)
   ```json
   {
       "document": "{{document_base64}}",
       "replacements": {
           "NOME": "Jose da Silva",
           "ENDERECO": "Rua ABC, 123",
           "DATANASCIMENTO": "01/01/1990",
           "CPF": "123.456.789-00"
       },
       "filename": "contrato_jose_silva.pdf"
   }
   ```

4. **Envie e salve:**
   - Clique em **Send and Download** (ao lado do botão Send)
   - Escolha onde salvar o PDF
   - O arquivo será baixado automaticamente

**Vantagens:**
- ✅ Salva o PDF diretamente
- ✅ Não precisa decodificar Base64
- ✅ Mais eficiente para arquivos grandes
- ✅ Pode visualizar no navegador

---

## 📋 Exemplos Completos

### Exemplo 1: Contrato Simples

**Documento Word (contrato.docx):**
```
CONTRATO DE PRESTAÇÃO DE SERVIÇOS

Contratante: %%NOME%%
CPF: %%CPF%%
Endereço: %%ENDERECO%%

Data: %%DATA%%
```

**Request no Postman:**
```json
{
    "document": "UEsDBBQABgAIAAAAIQBi7...",
    "replacements": {
        "NOME": "Maria Silva",
        "CPF": "123.456.789-00",
        "ENDERECO": "Rua das Flores, 100",
        "DATA": "27/11/2024"
    },
    "filename": "contrato_maria.pdf"
}
```

### Exemplo 2: Formulário com Múltiplos Campos

**Documento Word:**
```
FICHA DE CADASTRO

Nome Completo: %%NOME%%
Data de Nascimento: %%DATANASCIMENTO%%
CPF: %%CPF%%
RG: %%RG%%
Telefone: %%TELEFONE%%
Email: %%EMAIL%%
Endereço: %%ENDERECO%%
Cidade: %%CIDADE%%
Estado: %%ESTADO%%
CEP: %%CEP%%
```

**Request no Postman:**
```json
{
    "document": "UEsDBBQABgAIAAAAIQBi7...",
    "replacements": {
        "NOME": "João Pedro Santos",
        "DATANASCIMENTO": "15/03/1985",
        "CPF": "987.654.321-00",
        "RG": "12.345.678-9",
        "TELEFONE": "(11) 98765-4321",
        "EMAIL": "joao.santos@email.com",
        "ENDERECO": "Av. Paulista, 1000 - Apto 501",
        "CIDADE": "São Paulo",
        "ESTADO": "SP",
        "CEP": "01310-100"
    },
    "filename": "cadastro_joao.pdf"
}
```

---

## ❌ Tratamento de Erros

### Erro 400: Campo obrigatório faltando
```json
{
    "error": "Campo \"document\" é obrigatório"
}
```
**Solução:** Verifique se incluiu os campos `document` e `replacements`.

### Erro 400: Base64 inválido
```json
{
    "error": "String Base64 inválida"
}
```
**Solução:** Verifique se o Base64 foi copiado corretamente.

### Erro 500: Erro ao processar documento
```json
{
    "error": "Erro ao processar documento: ..."
}
```
**Solução:** Verifique se o documento Word não está corrompido.

---

## 💡 Dicas

1. **Use variáveis de ambiente** para alternar entre ambiente local e produção
2. **Prefira o endpoint `/convert-file`** para facilitar o download
3. **Teste com documento pequeno** primeiro para validar as tags
4. **Use "Send and Download"** para salvar PDFs automaticamente
5. **Verifique os exemplos** na coleção para referência

---

## 🔗 Links Úteis

- **Documentação completa:** Ver `README.md`
- **Exemplos em Python:** Ver `example_usage.py`
- **Deploy no Render:** Instruções no `README.md`

---

## 📞 Suporte

Para dúvidas ou problemas:
- 📧 Email: maxwbh@gmail.com
- 💼 LinkedIn: /maxwbh

---

**Desenvolvido com ❤️ por Maxwell da Silva Oliveira - M&S do Brasil LTDA**
