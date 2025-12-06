# 📊 Opções de Qualidade de PDF - v1.4.0

## 🎯 Visão Geral

A partir da versão 1.4.0, a API DOC2PDF oferece controle avançado sobre a qualidade dos PDFs gerados através do parâmetro `quality`.

## 🔧 Como Usar

Adicione o parâmetro `quality` no JSON de requisição em qualquer endpoint:

```json
{
  "document": "base64_do_documento",
  "replacements": {
    "NOME": "João Silva",
    "DATA": "05/12/2025"
  },
  "quality": "high"
}
```

## 📐 Perfis de Qualidade

### 🏆 HIGH - Alta Qualidade (Padrão)

**Ideal para:** Impressão, documentos oficiais, contratos, certificados

**Características:**
- ✅ **Resolução:** 300 DPI (máxima qualidade)
- ✅ **Compressão JPEG:** 95% (mínima perda)
- ✅ **Redução de resolução:** Desabilitada
- ✅ **Tamanho do arquivo:** Maior (~2-5 MB típico)
- ✅ **Qualidade de imagem:** Excelente
- ✅ **Texto:** Extremamente nítido

**Quando usar:**
- 📄 Contratos e documentos legais
- 🎓 Certificados e diplomas
- 📋 Propostas comerciais formais
- 🖨️ Documentos para impressão em alta qualidade

**Exemplo:**
```json
{
  "document": "JVBERi0xLjQK...",
  "replacements": {"CONTRATO": "2025-001"},
  "quality": "high"
}
```

---

### ⚖️ MEDIUM - Qualidade Média (Balanceado)

**Ideal para:** Uso geral, arquivamento digital, compartilhamento por email

**Características:**
- ✅ **Resolução:** 150 DPI (boa qualidade)
- ✅ **Compressão JPEG:** 85% (leve perda)
- ✅ **Redução de resolução:** Ativada
- ✅ **Tamanho do arquivo:** Médio (~500 KB - 2 MB típico)
- ✅ **Qualidade de imagem:** Boa
- ✅ **Texto:** Muito legível

**Quando usar:**
- 📧 Documentos para envio por email
- 💾 Arquivamento digital
- 👀 Visualização em tela
- 🔄 Compartilhamento rápido

**Exemplo:**
```json
{
  "document": "JVBERi0xLjQK...",
  "replacements": {"CLIENTE": "Maria Santos"},
  "quality": "medium"
}
```

---

### 📉 LOW - Qualidade Baixa (Compacto)

**Ideal para:** Rascunhos, prévia rápida, documentos para web com limitação de banda

**Características:**
- ✅ **Resolução:** 75 DPI (qualidade básica)
- ✅ **Compressão JPEG:** 70% (compressão alta)
- ✅ **Redução de resolução:** Ativada (máxima)
- ✅ **Tamanho do arquivo:** Pequeno (~100-500 KB típico)
- ⚠️ **Qualidade de imagem:** Básica
- ⚠️ **Texto:** Legível (pode ter leve pixelização)

**Quando usar:**
- 🚀 Prévia rápida de documentos
- 📱 Envio para dispositivos móveis
- 🌐 Upload em conexões lentas
- 📝 Rascunhos e versões preliminares

**Exemplo:**
```json
{
  "document": "JVBERi0xLjQK...",
  "replacements": {"VERSAO": "Rascunho"},
  "quality": "low"
}
```

---

## 🔄 Compatibilidade com Endpoints

O parâmetro `quality` está disponível em **TODOS** os endpoints:

### 1️⃣ `/convert` - Retorna PDF em Base64
```json
POST /convert
{
  "document": "base64_docx",
  "replacements": {"TAG": "valor"},
  "quality": "high"
}
```

### 2️⃣ `/convert-file` - Retorna arquivo PDF para download
```json
POST /convert-file
{
  "document": "base64_docx",
  "replacements": {"TAG": "valor"},
  "filename": "contrato.pdf",
  "quality": "medium"
}
```

### 3️⃣ `/process` - Endpoint flexível
```json
POST /process
{
  "document": "base64_docx",
  "replacements": {"TAG": "valor"},
  "input_type": "base64",
  "output_type": "pdf",
  "quality": "low"
}
```

---

## ⚙️ Configurações Técnicas do LibreOffice

### Parâmetros Aplicados Internamente

Todas as conversões usam filtros avançados do LibreOffice:

```
writer_pdf_Export:{
  SelectPdfVersion=1              # PDF 1.4 (compatibilidade universal)
  UseTaggedPDF=true               # PDF acessível com estrutura
  ExportBookmarks=true            # Preserva marcadores e índice
  ExportNotes=false               # Remove comentários
  Quality=[70-95]                 # Varia por perfil
  ReduceImageResolution=[true/false]
  MaxImageResolution=[75-300]     # DPI por perfil
  ExportFormFields=true           # Preserva campos de formulário
  EmbedStandardFonts=false        # Reduz tamanho do arquivo
}
```

### Opções de Linha de Comando

```bash
libreoffice \
  --headless \
  --invisible \
  --nocrashreport \
  --nodefault \
  --nofirststartwizard \
  --nolockcheck \
  --nologo \
  --norestore \
  --convert-to "pdf:writer_pdf_Export:{...}"
```

---

## 📊 Comparação de Tamanhos

**Exemplo:** Documento DOCX de 1 MB com 10 páginas e 5 imagens

| Qualidade | Tamanho PDF | Tempo | Uso Ideal |
|-----------|-------------|-------|-----------|
| **high**   | ~3.5 MB     | ~8s   | 🖨️ Impressão |
| **medium** | ~1.2 MB     | ~6s   | 📧 Email |
| **low**    | ~400 KB     | ~5s   | 🌐 Web |

*Tempos medidos em servidor com 1 CPU e 512MB RAM (Render free tier)*

---

## 🚀 Melhorias de Performance

### Docker Otimizado

O Dockerfile v1.4.0 inclui:

```dockerfile
# Fontes melhoradas para renderização
fonts-liberation
fonts-dejavu-core
fonts-liberation2
fonts-noto-core
fonts-freefont-ttf

# Ghostscript para otimização adicional
ghostscript

# Variáveis de ambiente otimizadas
SAL_USE_VCLPLUGIN=svp
OOO_DISABLE_RECOVERY=1
HOME=/tmp
```

---

## 💡 Dicas e Boas Práticas

### ✅ Recomendações

1. **Use `high` para documentos oficiais** que serão impressos ou arquivados permanentemente
2. **Use `medium` para 90% dos casos** - oferece excelente equilíbrio entre qualidade e tamanho
3. **Use `low` para prévias rápidas** ou quando o tamanho do arquivo é crítico
4. **Documente sempre não enviam o parâmetro**, o padrão é `high`

### ⚠️ Avisos

1. **Imagens originais de baixa qualidade** - Qualidade `high` não pode melhorar imagens ruins no DOCX original
2. **Fontes não instaladas** - Se o DOCX usar fontes não disponíveis, haverá substituição automática
3. **Timeout** - Documentos muito grandes (>50 páginas) podem exceder o timeout de 60s

### 🎯 Casos de Uso Específicos

#### Contratos e Documentos Legais
```json
{
  "quality": "high",
  "replacements": {
    "CONTRATANTE": "Empresa X",
    "CONTRATADO": "Fornecedor Y",
    "DATA": "05/12/2025",
    "VALOR": "R$ 50.000,00"
  }
}
```

#### Boletos e Faturas
```json
{
  "quality": "medium",  // Suficiente para impressão em casa
  "replacements": {
    "CODIGO_BARRAS": "34191.79001 01043.510047 91020.150008 1 96610000014500",
    "VENCIMENTO": "15/12/2025"
  }
}
```

#### Newsletters e Marketing
```json
{
  "quality": "low",  // Otimizado para web
  "replacements": {
    "NOME_CLIENTE": "João",
    "OFERTA_ESPECIAL": "30% OFF"
  }
}
```

---

## 📈 Monitoramento nos Logs

Ao usar diferentes qualidades, os logs mostram:

```
Iniciando conversão PDF com qualidade: high
Perfil selecionado: Alta qualidade - ideal para impressão
Resolução máxima: 300 DPI
Qualidade JPEG: 95%
Executando LibreOffice com filtro customizado...
PDF gerado com sucesso: 3584.23 KB
```

---

## 🔄 Migração da v1.3.x para v1.4.0

### ✅ Compatibilidade Total

A v1.4.0 é **100% compatível** com requisições antigas:

```json
// v1.3.x - Funcionará normalmente (usará quality=high)
{
  "document": "base64...",
  "replacements": {"TAG": "valor"}
}

// v1.4.0 - Novo parâmetro opcional
{
  "document": "base64...",
  "replacements": {"TAG": "valor"},
  "quality": "medium"  // NOVO!
}
```

### 🚀 Sem Breaking Changes

- ✅ Todos os endpoints continuam funcionando
- ✅ Parâmetro `quality` é opcional
- ✅ Padrão é `high` (mesma qualidade anterior)
- ✅ Validação automática de valores inválidos

---

## 📞 Suporte

**Desenvolvido por:** Maxwell da Silva Oliveira
**Empresa:** M&S do Brasil LTDA
**Email:** maxwbh@gmail.com
**LinkedIn:** linkedin.com/in/maxwbh
**Versão:** 1.4.0

---

## 🎉 Agradecimentos

Esta funcionalidade foi desenvolvida para oferecer mais controle e flexibilidade na geração de PDFs, atendendo diferentes casos de uso sem comprometer a qualidade.

**Boas conversões!** 🚀📄
