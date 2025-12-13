# 📋 Plano de Testes Completo - DOC2PDF API

**Versão:** 1.5.2
**Data:** 06/12/2025
**Autor:** Maxwell da Silva Oliveira - M&S do Brasil LTDA
**Email:** maxwbh@gmail.com
**LinkedIn:** /maxwbh

---

## 📖 Índice

1. [Objetivo](#objetivo)
2. [Escopo](#escopo)
3. [Estratégia de Testes](#estratégia-de-testes)
4. [Ambiente de Testes](#ambiente-de-testes)
5. [Casos de Teste](#casos-de-teste)
6. [Documentos de Teste](#documentos-de-teste)
7. [Execução](#execução)
8. [Critérios de Sucesso](#critérios-de-sucesso)

---

## 🎯 Objetivo

Este plano de testes tem como objetivo validar completamente a API DOC2PDF, garantindo que:

- ✅ Todos os componentes funcionem corretamente
- ✅ A substituição de tags seja precisa e confiável
- ✅ A conversão para PDF mantenha qualidade e formatação
- ✅ Erros sejam tratados adequadamente
- ✅ A API seja robusta e resiliente

---

## 🔍 Escopo

### Componentes Testados

1. **Validators** (`app/utils/validators.py`)
   - Validação de qualidade
   - Validação de replacements
   - Validação de formato de retorno
   - Validação de Content-Type
   - Validação de Base64
   - Validação de nomes de arquivo

2. **DOCX Service** (`app/services/docx_service.py`)
   - Substituição de tags em parágrafos
   - Substituição de tags em tabelas
   - Substituição de tags em cabeçalhos
   - Substituição de tags em rodapés
   - Tratamento de tags repetidas
   - Preservação de formatação

3. **PDF Service** (`app/services/pdf_service.py`)
   - Conversão DOCX → PDF
   - Perfis de qualidade (high, medium, low)
   - Preservação de conteúdo
   - Tratamento de erros

4. **API Endpoints**
   - `/convert` - Conversão com retorno Base64
   - `/convert-file` - Conversão com retorno de arquivo
   - `/process` - Endpoint flexível
   - `/health` - Health check

5. **Encoders** (`app/utils/encoders.py`)
   - Codificação/decodificação Base64
   - Tratamento de erros

---

## 🧪 Estratégia de Testes

### Tipos de Testes

#### 1. Testes Unitários
- **Objetivo:** Testar componentes isoladamente
- **Localização:** `tests/unit/`
- **Arquivos:**
  - `test_validators.py` - Testes de validação
  - `test_docx_service.py` - Testes de manipulação DOCX
  - `test_pdf_service.py` - Testes de conversão PDF
  - `test_encoders.py` - Testes de codificação

#### 2. Testes de Integração
- **Objetivo:** Testar fluxo completo da API
- **Localização:** `tests/integration/`
- **Arquivos:**
  - `test_api_endpoints.py` - Testes de endpoints
  - `test_full_conversion.py` - Testes de conversão completa
  - `test_error_handling.py` - Testes de tratamento de erros

#### 3. Testes de Caso de Uso Específico
- **Objetivo:** Validar ListaVendas.docx conforme especificado
- **Cobertura:**
  - Substituição de `{NOME_CLIENTE}`
  - Substituição de `{DATA_VENDA}`
  - Substituição de `{VALOR}`
  - Conversão para PDF
  - Validação de resultado

---

## 🌍 Ambiente de Testes

### Requisitos

- Python 3.9+
- pytest 9.0+
- python-docx 1.2.0+
- Flask 3.0+
- LibreOffice 7.0+ (para conversão PDF)

### Configuração

```bash
# Instalar dependências
pip install -r requirements.txt

# Criar documentos de teste
python tests/fixtures/create_test_documents.py

# Executar testes
pytest tests/ -v
```

### Fixtures e Documentos

Os testes utilizam fixtures centralizadas em `tests/conftest.py` que fornecem:

- **Documentos de teste** (em `tests/fixtures/documents/`)
- **Dados de teste** (replacements, payloads)
- **Helpers de validação**
- **Cliente Flask para testes**

---

## 📝 Casos de Teste

### 1. Validators (`test_validators.py`)

#### 1.1 Validação de Qualidade (`validate_quality`)

| ID | Caso de Teste | Entrada | Resultado Esperado |
|----|---------------|---------|-------------------|
| VQ-01 | Qualidade válida 'high' | `'high'` | Retorna `'high'` |
| VQ-02 | Qualidade válida 'medium' | `'medium'` | Retorna `'medium'` |
| VQ-03 | Qualidade válida 'low' | `'low'` | Retorna `'low'` |
| VQ-04 | Qualidade inválida | `'ultra_mega'` | Lança `BadRequest` |
| VQ-05 | Qualidade None | `None` | Retorna `'medium'` (padrão) |
| VQ-06 | Qualidade vazia | `''` | Retorna `'medium'` (padrão) |
| VQ-07 | Case insensitive | `'HIGH'`, `'Medium'` | Normaliza para lowercase |

#### 1.2 Validação de Formato de Retorno (`validate_return_format`)

| ID | Caso de Teste | Entrada | Resultado Esperado |
|----|---------------|---------|-------------------|
| VRF-01 | Formato 'base64' | `'base64'` | Retorna `'base64'` |
| VRF-02 | Formato 'file' | `'file'` | Retorna `'file'` |
| VRF-03 | Formato inválido | `'json'` | Lança `BadRequest` |
| VRF-04 | Formato None | `None` | Retorna `'base64'` (padrão) |
| VRF-05 | Case insensitive | `'BASE64'`, `'File'` | Normaliza para lowercase |

#### 1.3 Validação de Content-Type (`validate_json_content_type`)

| ID | Caso de Teste | Content-Type | Resultado Esperado |
|----|---------------|--------------|-------------------|
| VCT-01 | application/json | `'application/json'` | Passa sem erro |
| VCT-02 | JSON com charset | `'application/json; charset=utf-8'` | Passa sem erro |
| VCT-03 | Content-type inválido | `'application/xml'` | Lança `BadRequest` |
| VCT-04 | Content-type ausente | `None` | Lança `BadRequest` |

#### 1.4 Validação de Base64 (`validate_base64_document`)

| ID | Caso de Teste | Entrada | Resultado Esperado |
|----|---------------|---------|-------------------|
| VB64-01 | Base64 válido | DOCX em Base64 válido | Retorna bytes |
| VB64-02 | Base64 inválido | `'isso-não-é-base64'` | Lança `BadRequest` |
| VB64-03 | Base64 vazio | `''` | Lança `BadRequest` |
| VB64-04 | None | `None` | Lança `BadRequest` |
| VB64-05 | Base64 com whitespace | Base64 com `\n` e espaços | Remove whitespace e valida |
| VB64-06 | Valida formato DOCX | Base64 de DOCX | Bytes começam com `b'PK'` |

#### 1.5 Validação de Replacements (`validate_replacements`)

| ID | Caso de Teste | Entrada | Resultado Esperado |
|----|---------------|---------|-------------------|
| VR-01 | Replacements válidos | `{'TAG': 'valor'}` | Retorna dict validado |
| VR-02 | Replacements vazios | `{}` | Retorna `{}` |
| VR-03 | None | `None` | Retorna `{}` |
| VR-04 | Não é dict | `['lista']` | Lança `BadRequest` |
| VR-05 | Com caracteres especiais | `{'TAG': 'ãçéñt'}` | Aceita e retorna |
| VR-06 | Com números | `{'TAG': 12345}` | Converte para string |
| VR-07 | Case sensitivity | Preserva case das chaves | Mantém case original |

---

### 2. DOCX Service (`test_docx_service.py`)

#### 2.1 Substituição de Tags - ListaVendas.docx

| ID | Caso de Teste | Tags | Valores | Validação |
|----|---------------|------|---------|-----------|
| DS-LV-01 | Substituir NOME_CLIENTE | `{NOME_CLIENTE}` | `'João Silva'` | Texto contém 'João Silva' |
| DS-LV-02 | Substituir DATA_VENDA | `{DATA_VENDA}` | `'06/12/2025'` | Texto contém '06/12/2025' |
| DS-LV-03 | Substituir VALOR | `{VALOR}` | `'R$ 1.500,00'` | Texto contém 'R$ 1.500,00' |
| DS-LV-04 | Todas as tags | Todas as 3 tags | Valores correspondentes | Tags removidas, valores inseridos |
| DS-LV-05 | Sem tags no texto | - | - | Tags `{...}` não aparecem no resultado |

#### 2.2 Substituição em Documentos Complexos

| ID | Caso de Teste | Documento | Validação |
|----|---------------|-----------|-----------|
| DS-WT-01 | with_tags.docx | Tags em tabelas e parágrafos | Substitui corretamente |
| DS-CX-01 | complex.docx | Tags em múltiplos elementos | Substitui em tabelas e rodapé |
| DS-TR-01 | tags_repetidas.docx | Mesma tag 3+ vezes | Substitui todas as ocorrências |
| DS-EM-01 | empty.docx | Documento vazio | Não gera erro |

#### 2.3 Casos Extremos

| ID | Caso de Teste | Cenário | Resultado Esperado |
|----|---------------|---------|-------------------|
| DS-E-01 | Replacements vazios | `{}` | Documento inalterado |
| DS-E-02 | Substituição parcial | Apenas 1 de 3 tags | Substitui apenas a especificada |
| DS-E-03 | Case sensitivity | Tags maiúsculas vs minúsculas | Respeita case (maiúsculas) |
| DS-E-04 | Caracteres especiais | `'José María Öztürk'` | Aceita e substitui |
| DS-E-05 | Valores numéricos | `1500.50` | Converte para string |
| DS-E-06 | Tag inexistente | Tag não presente no doc | Ignora sem erro |
| DS-E-07 | Valor muito longo | String de 10.000 chars | Substitui corretamente |
| DS-E-08 | Valor vazio | `''` | Remove tag (substitui por vazio) |

#### 2.4 Integração

| ID | Caso de Teste | Fluxo | Validação |
|----|---------------|-------|-----------|
| DS-I-01 | Workflow completo | Abrir → Substituir → Salvar → Reabrir | Substituições persistem |
| DS-I-02 | Múltiplas substituições | Substituir 2 vezes sequencialmente | Ambas aplicadas |
| DS-I-03 | Documento salvável | Resultado é salvável | Arquivo criado e válido |

---

### 3. PDF Service (`test_pdf_service.py`)

#### 3.1 Conversão Básica

| ID | Caso de Teste | Documento | Qualidade | Validação |
|----|---------------|-----------|-----------|-----------|
| PS-C-01 | Simple doc - high | simple.docx | `high` | PDF criado e válido |
| PS-C-02 | Simple doc - medium | simple.docx | `medium` | PDF criado e válido |
| PS-C-03 | Simple doc - low | simple.docx | `low` | PDF criado e válido |
| PS-C-04 | ListaVendas | ListaVendas.docx | `high` | PDF criado |
| PS-C-05 | Complex doc | complex.docx | `medium` | PDF > 1KB |
| PS-C-06 | With tags | with_tags.docx | `high` | PDF criado |
| PS-C-07 | Empty doc | empty.docx | `medium` | PDF criado sem erro |

#### 3.2 Qualidade de PDF

| ID | Caso de Teste | Cenário | Validação |
|----|---------------|---------|-----------|
| PS-Q-01 | Perfil HIGH | Qualidade `high` | PDF criado, configurações DPI corretas |
| PS-Q-02 | Perfil MEDIUM | Qualidade `medium` | PDF criado, balanceado |
| PS-Q-03 | Perfil LOW | Qualidade `low` | PDF criado, menor tamanho |
| PS-Q-04 | Comparação tamanhos | high vs low | HIGH ≥ LOW (geralmente) |

#### 3.3 Validação de Formato

| ID | Caso de Teste | Validação | Critério |
|----|---------------|-----------|----------|
| PS-V-01 | Header PDF | Bytes iniciais | Começam com `b'%PDF'` |
| PS-V-02 | Footer PDF | Bytes finais | Contém `b'%%EOF'` |
| PS-V-03 | Tamanho mínimo | PDF não vazio | Tamanho > 0 bytes |

#### 3.4 Tratamento de Erros

| ID | Caso de Teste | Cenário | Resultado Esperado |
|----|---------------|---------|-------------------|
| PS-E-01 | Arquivo inexistente | DOCX não existe | Lança Exception |
| PS-E-02 | Qualidade inválida | `'invalid_quality'` | Usa fallback ou lança erro |
| PS-E-03 | Caminho inválido | Path não existe | Lança Exception |

#### 3.5 Casos Especiais

| ID | Caso de Teste | Cenário | Validação |
|----|---------------|---------|-----------|
| PS-S-01 | Caminho com espaços | `'arquivo com espaços.pdf'` | PDF criado |
| PS-S-02 | Nome Unicode | `'relatório_ãçéntüação.pdf'` | PDF criado ou skip |
| PS-S-03 | Sobrescrever PDF | Converter 2 vezes no mesmo path | Segunda sobrescreve |

---

### 4. API Endpoints (`test_api_endpoints.py`)

#### 4.1 Endpoint `/convert`

| ID | Caso de Teste | Request | Status | Response |
|----|---------------|---------|--------|----------|
| API-C-01 | Conversão válida | Payload completo | 200 | JSON com `pdf` em Base64 |
| API-C-02 | Sem documento | `{'replacements': {}}` | 400 | Erro: campo obrigatório |
| API-C-03 | Sem replacements | `{'document': '...'}` | 400 | Erro: campo obrigatório |
| API-C-04 | Base64 inválido | Base64 malformado | 400 | Erro: Base64 inválido |
| API-C-05 | Qualidade inválida | `quality: 'super_high'` | 400 | Erro: qualidade inválida |
| API-C-06 | Content-Type errado | `text/plain` | 400 | Erro: deve ser JSON |

#### 4.2 Endpoint `/convert-file`

| ID | Caso de Teste | Request | Status | Response |
|----|---------------|---------|--------|----------|
| API-CF-01 | Retorna arquivo PDF | Payload válido | 200 | Content-Type: application/pdf |
| API-CF-02 | Nome customizado | `filename: 'relatorio.pdf'` | 200 | Download com nome correto |
| API-CF-03 | Sem filename | Não especifica filename | 200 | Nome padrão 'documento.pdf' |

#### 4.3 Endpoint `/process`

| ID | Caso de Teste | Request | Output Type | Validação |
|----|---------------|---------|-------------|-----------|
| API-P-01 | output_type: pdf | - | `pdf` | Retorna arquivo PDF |
| API-P-02 | output_type: doc | - | `doc` | Retorna arquivo DOCX |
| API-P-03 | output_type: base64_pdf | - | `base64_pdf` | JSON com PDF em Base64 |
| API-P-04 | output_type: base64_doc | - | `base64_doc` | JSON com DOCX em Base64 |

#### 4.4 Endpoint `/health`

| ID | Caso de Teste | Request | Status | Response |
|----|---------------|---------|--------|----------|
| API-H-01 | Health check | GET `/health` | 200 | JSON com status OK |

---

### 5. Encoders (`test_encoders.py`)

| ID | Caso de Teste | Função | Entrada | Resultado |
|----|---------------|--------|---------|-----------|
| ENC-01 | Encode Base64 | `encode_base64_file` | bytes | String Base64 válida |
| ENC-02 | Decode Base64 | `decode_base64_file` | String Base64 | bytes originais |
| ENC-03 | Round-trip | Encode → Decode | bytes | Bytes iguais aos originais |
| ENC-04 | Erro decode | String inválida | - | Lança exceção |

---

## 📁 Documentos de Teste

### Documentos Criados

Todos os documentos estão em `tests/fixtures/documents/`:

| Arquivo | Descrição | Tags | Uso |
|---------|-----------|------|-----|
| **ListaVendas.docx** | Template de listagem de vendas | `{NOME_CLIENTE}`, `{DATA_VENDA}`, `{VALOR}` | Teste principal especificado |
| **simple.docx** | Documento simples sem tags | Nenhuma | Testes de conversão básica |
| **with_tags.docx** | Tags em parágrafos e tabelas | `{MES}`, `{ANO}`, `{EMPRESA}`, etc. | Testes de substituição em tabelas |
| **complex.docx** | Documento complexo com rodapé | 15+ tags | Testes de documentos complexos |
| **empty.docx** | Documento vazio | Nenhuma | Testes de edge cases |
| **tags_repetidas.docx** | Mesma tag repetida 5+ vezes | `{TAG_REPETIDA}` | Testes de tags duplicadas |

### Geração de Documentos

```bash
# Criar todos os documentos de teste
python tests/fixtures/create_test_documents.py
```

---

## 🚀 Execução

### Executar Todos os Testes

```bash
# Todos os testes
pytest tests/ -v

# Com cobertura
pytest tests/ -v --cov=app --cov-report=html

# Apenas unitários
pytest tests/unit/ -v

# Apenas integração
pytest tests/integration/ -v

# Teste específico
pytest tests/unit/test_validators.py::TestValidateQuality -v
```

### Executar Teste do ListaVendas.docx

```bash
# Teste específico do documento ListaVendas
pytest tests/unit/test_docx_service.py::TestReplaceTagsInDoc::test_replace_tags_lista_vendas -v

# Integração completa com ListaVendas
pytest tests/integration/test_full_conversion.py -k lista_vendas -v
```

### Verificar LibreOffice

```bash
# Verificar se LibreOffice está disponível
libreoffice --version

# Testar conversão manual
libreoffice --headless --convert-to pdf tests/fixtures/documents/ListaVendas.docx
```

---

## ✅ Critérios de Sucesso

### Critérios Mínimos

- ✅ **100% dos testes unitários** devem passar
- ✅ **100% dos testes de integração** devem passar
- ✅ **Cobertura de código ≥ 90%**
- ✅ **Documento ListaVendas.docx** deve ser processado corretamente
- ✅ **LibreOffice** deve estar disponível e funcional
- ✅ **Zero falhas críticas**

### Validações Específicas - ListaVendas.docx

Para o documento especificado `ListaVendas.docx`:

1. ✅ Substituir `{NOME_CLIENTE}` → Valor fornecido
2. ✅ Substituir `{DATA_VENDA}` → Valor fornecido
3. ✅ Substituir `{VALOR}` → Valor fornecido
4. ✅ Gerar PDF válido
5. ✅ PDF contém os valores substituídos
6. ✅ PDF não contém as tags originais
7. ✅ Formatação preservada
8. ✅ Processo completo em < 30 segundos

### Métricas de Qualidade

| Métrica | Meta | Atual |
|---------|------|-------|
| Testes Passando | 100% | A validar |
| Cobertura de Código | ≥ 90% | A validar |
| Tempo de Execução | < 2 min | A validar |
| Falhas Críticas | 0 | A validar |

---

## 🐛 Problemas Conhecidos e Soluções

### 1. Validators retornam tuplas ao invés de BadRequest
**Status:** ✅ Resolvido
**Solução:** Atualizado para lançar `BadRequest` do Werkzeug

### 2. Documentos de teste não criados
**Status:** ✅ Resolvido
**Solução:** Executado `create_test_documents.py`

### 3. LibreOffice não disponível em alguns ambientes
**Status:** ⚠️ Pendente
**Solução:** Verificar instalação e adicionar skip condicional nos testes

---

## 📊 Relatório de Execução

### Template de Relatório

```markdown
## Relatório de Testes - DOC2PDF API

**Data:** [DATA]
**Versão:** 1.5.2
**Executor:** [NOME]

### Resumo

- Total de Testes: [X]
- Passou: [X]
- Falhou: [X]
- Skipped: [X]
- Cobertura: [X]%

### Detalhes

#### Testes Unitários
- Validators: [X/Y]
- DOCX Service: [X/Y]
- PDF Service: [X/Y]
- Encoders: [X/Y]

#### Testes de Integração
- API Endpoints: [X/Y]
- Full Conversion: [X/Y]
- Error Handling: [X/Y]

### Problemas Encontrados

[Listar problemas]

### Ações Necessárias

[Listar ações]
```

---

## 🔄 Manutenção do Plano

Este plano deve ser atualizado quando:

- ✅ Novos recursos forem adicionados
- ✅ Bugs forem corrigidos
- ✅ Casos de teste forem adicionados/removidos
- ✅ Documentos de teste forem modificados
- ✅ Critérios de sucesso mudarem

**Última Atualização:** 06/12/2025
**Próxima Revisão:** A cada release

---

## 📞 Contato

**Desenvolvedor:** Maxwell da Silva Oliveira
**Empresa:** M&S do Brasil LTDA
**Email:** maxwbh@gmail.com
**LinkedIn:** /maxwbh
**GitHub:** @Maxwbh

---

<div align="center">

**Plano de Testes DOC2PDF API v1.5.2**

✅ Criado e validado por Maxwell da Silva Oliveira

</div>
