# Exemplo: Tags Repetidas no Documento

**Versão:** 1.3.0
**Autor:** Maxwell da Silva Oliveira - M&S do Brasil LTDA

---

## ✅ Tags Repetidas São Totalmente Suportadas!

A API **substitui TODAS as ocorrências** de cada tag no documento, não importa quantas vezes ela apareça.

---

## 📄 Exemplo Prático: Contrato com Tags Repetidas

### **Documento Word (Template):**

```
═══════════════════════════════════════════════
              CABEÇALHO (Header)
═══════════════════════════════════════════════
CONTRATO - {CONTRATANTE} - {DATA}
═══════════════════════════════════════════════


CONTRATO DE PRESTAÇÃO DE SERVIÇOS

Entre {CONTRATANTE}, doravante denominada CONTRATANTE,
e {CONTRATADO}, doravante denominado CONTRATADO,
celebram o presente contrato em {DATA}.

CLÁUSULA 1 - DO OBJETO
{CONTRATANTE} contrata {CONTRATADO} para prestação de serviços.

CLÁUSULA 2 - DO VALOR
{CONTRATADO} receberá de {CONTRATANTE} o valor de {VALOR}.

CLÁUSULA 3 - DO PRAZO
Este contrato tem validade a partir de {DATA} por {PRAZO}.

CLÁUSULA 4 - DAS OBRIGAÇÕES
{CONTRATADO} se compromete a:
- Prestar serviços conforme acordado
- Respeitar prazos estabelecidos

{CONTRATANTE} se compromete a:
- Efetuar pagamento de {VALOR}
- Fornecer recursos necessários

CLÁUSULA 5 - DA ASSINATURA
Assinado em {DATA}.

_______________________________
{CONTRATANTE}
CNPJ: {CNPJ}

_______________________________
{CONTRATADO}
CPF: {CPF}


═══════════════════════════════════════════════
              RODAPÉ (Footer)
═══════════════════════════════════════════════
{CONTRATANTE} - {CONTRATADO} - {DATA} - Página {PAGINA}
═══════════════════════════════════════════════
```

### **Análise de Repetições:**

| Tag | Ocorrências | Locais |
|-----|-------------|---------|
| `{CONTRATANTE}` | **8 vezes** | Cabeçalho (1x), Parágrafo principal (1x), Cláusula 1 (1x), Cláusula 2 (1x), Cláusula 4 (1x), Assinatura (1x), Rodapé (1x) |
| `{CONTRATADO}` | **7 vezes** | Parágrafo principal (1x), Cláusula 1 (1x), Cláusula 2 (2x), Cláusula 4 (1x), Assinatura (1x), Rodapé (1x) |
| `{DATA}` | **5 vezes** | Cabeçalho (1x), Parágrafo principal (1x), Cláusula 3 (1x), Cláusula 5 (1x), Rodapé (1x) |
| `{VALOR}` | **2 vezes** | Cláusula 2 (1x), Cláusula 4 (1x) |
| `{PRAZO}` | **1 vez** | Cláusula 3 (1x) |
| `{CNPJ}` | **1 vez** | Assinatura (1x) |
| `{CPF}` | **1 vez** | Assinatura (1x) |
| `{PAGINA}` | **1 vez** | Rodapé (1x) |

**Total:** 26 substituições de 8 tags diferentes

---

## 📨 Request JSON

```json
POST /convert-file
Content-Type: application/json

{
  "document": "UEsDBBQAAAAIAOWB0lZm7L5jLwEAAIsDAAATAAAAW0NvbnRlbnRfVHlwZXNdLnhtbK2S...",
  "replacements": {
    "CONTRATANTE": "Tech Solutions LTDA",
    "CONTRATADO": "João da Silva",
    "DATA": "05/12/2025",
    "VALOR": "R$ 50.000,00",
    "PRAZO": "12 meses",
    "CNPJ": "12.345.678/0001-90",
    "CPF": "123.456.789-00",
    "PAGINA": "1"
  },
  "filename": "contrato_tech_joao_2025.pdf"
}
```

---

## 📊 Resultado da Substituição

### **Documento Processado:**

```
═══════════════════════════════════════════════
              CABEÇALHO (Header)
═══════════════════════════════════════════════
CONTRATO - Tech Solutions LTDA - 05/12/2025
═══════════════════════════════════════════════


CONTRATO DE PRESTAÇÃO DE SERVIÇOS

Entre Tech Solutions LTDA, doravante denominada CONTRATANTE,
e João da Silva, doravante denominado CONTRATADO,
celebram o presente contrato em 05/12/2025.

CLÁUSULA 1 - DO OBJETO
Tech Solutions LTDA contrata João da Silva para prestação de serviços.

CLÁUSULA 2 - DO VALOR
João da Silva receberá de Tech Solutions LTDA o valor de R$ 50.000,00.

CLÁUSULA 3 - DO PRAZO
Este contrato tem validade a partir de 05/12/2025 por 12 meses.

CLÁUSULA 4 - DAS OBRIGAÇÕES
João da Silva se compromete a:
- Prestar serviços conforme acordado
- Respeitar prazos estabelecidos

Tech Solutions LTDA se compromete a:
- Efetuar pagamento de R$ 50.000,00
- Fornecer recursos necessários

CLÁUSULA 5 - DA ASSINATURA
Assinado em 05/12/2025.

_______________________________
Tech Solutions LTDA
CNPJ: 12.345.678/0001-90

_______________________________
João da Silva
CPF: 123.456.789-00


═══════════════════════════════════════════════
              RODAPÉ (Footer)
═══════════════════════════════════════════════
Tech Solutions LTDA - João da Silva - 05/12/2025 - Página 1
═══════════════════════════════════════════════
```

---

## 🔍 Logs da API (Exemplo)

```
>>> NOVA REQUISIÇÃO
Método: POST
Endpoint: /convert-file
✓ Validação OK - 8 substituições encontradas
Tags a substituir: ['CONTRATANTE', 'CONTRATADO', 'DATA', 'VALOR', 'PRAZO', 'CNPJ', 'CPF', 'PAGINA']

Etapa 2/4: Substituindo tags no documento...
✓ Formato DOCX detectado (arquivo ZIP)
Substituindo tags nos parágrafos...
Substituindo tags nas tabelas...
Substituindo tags nos cabeçalhos...
  ✓ Tag {CONTRATANTE} substituída no cabeçalho
  ✓ Tag {DATA} substituída no cabeçalho
Substituindo tags nos rodapés...
  ✓ Tag {CONTRATANTE} substituída no rodapé
  ✓ Tag {CONTRATADO} substituída no rodapé
  ✓ Tag {DATA} substituída no rodapé
  ✓ Tag {PAGINA} substituída no rodapé
Total de tags substituídas: 26

✓ Tags substituídas em 0.156s
✅ CONVERSÃO CONCLUÍDA COM SUCESSO
```

**Observe:** Total de 26 substituições de apenas 8 tags únicas!

---

## 🎯 Casos de Uso com Tags Repetidas

### **1. Nome do Cliente Repetido**
```
Caro {CLIENTE},

Agradecemos sua preferência, {CLIENTE}.

Att,
Equipe de Atendimento

P.S.: {CLIENTE}, não esqueça de...
```

**JSON:**
```json
{
  "CLIENTE": "Maria Santos"
}
```

**Resultado:** `{CLIENTE}` substituído 3 vezes por "Maria Santos"

---

### **2. Data em Múltiplos Locais**
```
Cabeçalho: Relatório - {DATA}
Parágrafo 1: Em {DATA}, iniciamos...
Parágrafo 2: Até {DATA}, observamos...
Rodapé: Gerado em {DATA}
```

**JSON:**
```json
{
  "DATA": "05/12/2025"
}
```

**Resultado:** `{DATA}` substituído 4 vezes por "05/12/2025"

---

### **3. Valor Monetário Repetido**
```
Valor do contrato: {VALOR}
Pagamento: {VALOR} em 12 parcelas
Total a pagar: {VALOR}
```

**JSON:**
```json
{
  "VALOR": "R$ 120.000,00"
}
```

**Resultado:** `{VALOR}` substituído 3 vezes

---

## ✅ Vantagens de Tags Repetidas

| Vantagem | Descrição |
|----------|-----------|
| **Consistência** | Mesmo valor em todo o documento |
| **Manutenção** | Alterar 1 valor no JSON atualiza todas as ocorrências |
| **Flexibilidade** | Use a mesma tag quantas vezes precisar |
| **Simplicidade** | Não precisa criar tags diferentes para o mesmo dado |

---

## 🚨 Importante

### ✅ **Funciona Perfeitamente:**
```json
{
  "NOME": "João Silva",
  "EMPRESA": "Tech Corp"
}
```

Documento:
```
{NOME} trabalha na {EMPRESA}.
Contato de {NOME}: email@example.com
{EMPRESA} agradece a {NOME}.
```

**Resultado:**
```
João Silva trabalha na Tech Corp.
Contato de João Silva: email@example.com
Tech Corp agradece a João Silva.
```

### ❌ **NÃO Funciona (case-sensitive):**
```json
{
  "nome": "João Silva"  // Minúscula ❌
}
```

Documento com `{NOME}` (maiúscula) → **NÃO será substituído**

**Solução:** Sempre use **MAIÚSCULAS** nas tags do documento e nas chaves do JSON.

---

## 🧪 Teste Você Mesmo

### **Template para Teste:**

Crie um documento Word com:

```
Olá {NOME}!

Prezado(a) {NOME}, tudo bem?

Este é um teste para verificar se {NOME}
será substituído em todos os lugares.

Atenciosamente,
Equipe {EMPRESA}

P.S.: {NOME}, entre em contato com {EMPRESA}!

Cabeçalho: {EMPRESA} - {NOME}
Rodapé: {NOME} © {EMPRESA} 2025
```

### **JSON de Teste:**

```json
{
  "document": "[BASE64_DO_TEMPLATE]",
  "replacements": {
    "NOME": "João da Silva",
    "EMPRESA": "M&S do Brasil LTDA"
  },
  "filename": "teste_tags_repetidas.pdf"
}
```

### **Resultado Esperado:**

- `{NOME}` substituído **7 vezes**
- `{EMPRESA}` substituído **4 vezes**
- **Total: 11 substituições** de 2 tags

---

## 📚 Recursos

- [Exemplo Postman v1.3.0](./EXEMPLO_POSTMAN_v1.3.0.md)
- [Testes Completos](./TESTES_COMPLETOS.md)
- [API Documentation](./README.md)

---

**Desenvolvido por Maxwell da Silva Oliveira - M&S do Brasil LTDA**
**Email:** maxwbh@gmail.com
**Versão:** 1.3.0 - Suporte completo a tags repetidas! ✅
