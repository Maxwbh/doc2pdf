# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).



## [1.1.0] - 2025-12-05

### Adicionado
- Sistema completo de logging estruturado para monitoramento em produção (Render)
- Middleware de logging de requisições com detalhes de IP, método, endpoint e User-Agent
- Middleware de logging de respostas com status, tempo de processamento e tamanho
- Logs detalhados de inicialização da API com versão e informações do autor
- Logging step-by-step (Etapas 1/4 a 4/4) em todos os endpoints de conversão
- Métricas de tempo individual para cada operação (decodificação, substituição, salvamento, conversão)
- Logs de resumo com tamanhos de arquivos e tempo total de conversão
- Indicadores visuais de progresso (✓, ✅, >>>. <<<, ---) nos logs
- Logs de erro detalhados com contexto específico
- Rastreamento completo do ciclo de vida de cada requisição

### Alterado
- Endpoint `/convert` com logging detalhado de todas as 4 etapas do processo
- Endpoint `/convert-file` com logging detalhado de todas as 4 etapas do processo
- Endpoint `/process` com logging específico para cada tipo de saída (pdf, doc, base64_pdf, base64_doc)
- Função `decode_base64_file` com logging de erros
- Função `replace_tags_in_doc` com logging de erros de processamento
- Função `convert_docx_to_pdf` com logging de erros do LibreOffice
- Formato de logs inclui timestamp, nível, nome da função e mensagem

### Melhorias
- Logs estruturados facilitam debug em produção no Render
- Métricas de performance para identificar gargalos
- Rastreabilidade completa de cada conversão
- Melhor visibilidade de erros e exceções
- Logs no formato human-readable para fácil análise

## [1.0.3] - 2024-11-27

### Adicionado
- Novo endpoint `POST /process` flexível com suporte para múltiplos formatos
  - Entrada: `base64` ou `doc`
  - Saída: `pdf`, `doc`, `base64_pdf`, `base64_doc`
- Arquivo `TEST_EXAMPLES.md` com exemplos completos de JSON para todos os endpoints
- Arquivo `DOCKER_GUIDE.md` com guia completo de instalação via Docker
- Arquivo `docker-compose.yml` para instalação simplificada
- Arquivo `.env.example` para configuração de variáveis de ambiente
- Exemplos de casos de uso completos (contratos, certificados, propostas)

### Alterado
- Endpoint raiz `/` agora inclui informações sobre o novo endpoint `/process`
- Coleção do Postman atualizada com novo endpoint e exemplos de teste
- README atualizado com instruções de instalação via Docker Compose

### Melhorias
- Documentação profissional mantida e expandida
- Guias específicos para Docker e testes
- Maior flexibilidade no processamento de documentos
- Suporte para retorno de documentos Word editados

## [1.0.2] - 2024-11-27

### Adicionado
- Sistema de versionamento automático
- Arquivo `version.py` para gerenciamento centralizado de versão
- Suporte para instalação via pip (`setup.py` e `pyproject.toml`)
- `CHANGELOG.md` para documentação de versões
- `CONTRIBUTING.md` com guidelines de desenvolvimento
- Badges profissionais no README
- Script de versionamento automático (`bump_version.py`)
- Documentação profissionalizada

### Alterado
- README com estrutura mais profissional e badges
- Documentação reorganizada com melhor estrutura
- API agora retorna informações de versão

## [1.0.1] - 2024-11-27

### Adicionado
- Novo endpoint `POST /convert-file` para retorno de arquivo PDF direto
- Coleção completa do Postman (`DOC2PDF_API.postman_collection.json`)
- Guia detalhado de uso do Postman (`POSTMAN_GUIDE.md`)
- Script de exemplo interativo com menu de opções
- Suporte para nome de arquivo customizado
- Exemplos de cURL para ambos os endpoints

### Alterado
- README atualizado com exemplos de ambos os endpoints
- Script `example_usage.py` com opções interativas
- Documentação expandida com mais exemplos

### Melhorias
- Limpeza automática de arquivos temporários
- Melhor tratamento de erros
- Logs mais informativos

## [1.0.0] - 2024-11-27

### Adicionado
- API Flask inicial para conversão de DOC para PDF
- Endpoint `POST /convert` para conversão com retorno Base64
- Endpoint `GET /health` para health check
- Endpoint `GET /` para informações da API
- Suporte para substituição de tags no formato `%%TAG%%`
- Preservação de formatação do documento original
- Suporte para tags em parágrafos e tabelas
- Dockerfile otimizado para Render
- Documentação completa (README.md)
- Script de exemplo (`example_usage.py`)
- Configuração para deploy no Render (`render.yaml`)
- Licença MIT
- `.gitignore` e `.dockerignore`

### Recursos
- Conversão de documentos Word (.DOC/.DOCX) para PDF
- Substituição de múltiplas tags em um único documento
- Conversão usando LibreOffice para alta qualidade
- API RESTful com retornos em JSON
- CORS habilitado para integração frontend
- Logs estruturados
- Tratamento robusto de erros
- Timeout configurável (30 segundos)

---

## Tipos de Mudanças

- **Adicionado** para novas funcionalidades
- **Alterado** para mudanças em funcionalidades existentes
- **Descontinuado** para funcionalidades que serão removidas em breve
- **Removido** para funcionalidades removidas
- **Corrigido** para correções de bugs
- **Segurança** para vulnerabilidades

---

**Desenvolvido por Maxwell da Silva Oliveira - M&S do Brasil LTDA**
