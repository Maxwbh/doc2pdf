# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

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
