# Guia de Contribuição

Obrigado por considerar contribuir com o DOC2PDF API! Este documento fornece diretrizes para contribuir com o projeto.

## 📋 Índice

- [Código de Conduta](#código-de-conduta)
- [Como Contribuir](#como-contribuir)
- [Processo de Desenvolvimento](#processo-de-desenvolvimento)
- [Padrões de Código](#padrões-de-código)
- [Sistema de Versionamento](#sistema-de-versionamento)
- [Testes](#testes)
- [Documentação](#documentação)

---

## Código de Conduta

Este projeto adere a um código de conduta. Ao participar, você concorda em manter um ambiente respeitoso e profissional.

---

## Como Contribuir

### Reportar Bugs

Se você encontrou um bug, por favor:

1. Verifique se o bug já não foi reportado nas [Issues](https://github.com/Maxwbh/doc2pdf/issues)
2. Se não existir, crie uma nova issue incluindo:
   - Descrição clara do problema
   - Passos para reproduzir
   - Comportamento esperado vs atual
   - Versão do Python e SO
   - Logs de erro (se aplicável)

### Sugerir Melhorias

Para sugerir novas funcionalidades:

1. Abra uma issue com a tag `enhancement`
2. Descreva detalhadamente a funcionalidade
3. Explique o caso de uso e benefícios
4. Se possível, sugira uma implementação

### Pull Requests

1. Faça fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/minha-feature`)
3. Faça commit das mudanças (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/minha-feature`)
5. Abra um Pull Request

---

## Processo de Desenvolvimento

### Configuração do Ambiente

```bash
# Clone o repositório
git clone https://github.com/Maxwbh/doc2pdf.git
cd doc2pdf

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências de desenvolvimento
pip install -e ".[dev]"

# Instale LibreOffice
# Ubuntu/Debian
sudo apt-get install libreoffice libreoffice-writer

# macOS
brew install libreoffice
```

### Executando Localmente

```bash
# Execute a API
python app.py

# Em outro terminal, teste
curl http://localhost:5000/health
```

### Executando Testes

```bash
# Execute todos os testes
pytest

# Com cobertura
pytest --cov=. --cov-report=html

# Testes específicos
pytest tests/test_app.py
```

---

## Padrões de Código

### Estilo de Código

- Siga [PEP 8](https://pep8.org/)
- Use [Black](https://github.com/psf/black) para formatação
- Máximo de 100 caracteres por linha

```bash
# Formatar código
black .

# Verificar estilo
flake8 .

# Type checking
mypy .
```

### Convenções de Nomenclatura

- **Funções e variáveis**: `snake_case`
- **Classes**: `PascalCase`
- **Constantes**: `UPPER_CASE`
- **Arquivos**: `snake_case.py`

### Docstrings

Use docstrings no formato Google:

```python
def convert_doc_to_pdf(doc_bytes, replacements):
    """
    Converte documento Word para PDF com substituição de tags.

    Args:
        doc_bytes: Bytes do documento Word
        replacements: Dicionário com as substituições {tag: valor}

    Returns:
        bytes: Conteúdo do PDF gerado

    Raises:
        ValueError: Se o documento for inválido
    """
    pass
```

### Mensagens de Commit

Siga o padrão [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>[escopo opcional]: <descrição>

[corpo opcional]

[rodapé opcional]
```

**Tipos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Mudanças na documentação
- `style`: Formatação, ponto e vírgula, etc
- `refactor`: Refatoração de código
- `test`: Adição de testes
- `chore`: Manutenção (build, dependências, etc)

**Exemplos:**
```bash
feat: adiciona endpoint para conversão batch
fix: corrige erro na substituição de tags em tabelas
docs: atualiza README com exemplos de cURL
chore: atualiza dependências
```

---

## Sistema de Versionamento

O projeto usa [Versionamento Semântico](https://semver.org/):

- **MAJOR** (X.0.0): Mudanças incompatíveis com versões anteriores
- **MINOR** (0.X.0): Novas funcionalidades compatíveis
- **PATCH** (0.0.X): Correções de bugs compatíveis

### Como Incrementar Versão

```bash
# Patch (1.0.0 -> 1.0.1)
python bump_version.py patch

# Minor (1.0.0 -> 1.1.0)
python bump_version.py minor

# Major (1.0.0 -> 2.0.0)
python bump_version.py major
```

O script atualiza automaticamente:
- `version.py`
- `CHANGELOG.md`

### Após Bump de Versão

1. Atualize o `CHANGELOG.md` com as mudanças
2. Commit as mudanças
3. Crie uma tag
4. Push com tags

```bash
git add version.py CHANGELOG.md
git commit -m "chore: bump version to 1.0.3"
git tag v1.0.3
git push && git push --tags
```

---

## Testes

### Estrutura de Testes

```
tests/
├── __init__.py
├── test_app.py          # Testes da API
├── test_conversion.py   # Testes de conversão
└── test_utils.py        # Testes de utilitários
```

### Escrevendo Testes

```python
import pytest
from app import app

def test_health_check():
    """Testa o endpoint de health check"""
    client = app.test_client()
    response = client.get('/health')

    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
```

### Cobertura de Testes

Mantenha a cobertura acima de 80%:

```bash
pytest --cov=. --cov-report=term-missing
```

---

## Documentação

### README

- Mantenha o README atualizado
- Adicione exemplos claros
- Documente todas as funcionalidades

### Comentários no Código

- Comente código complexo
- Explique o "porquê", não o "o quê"
- Mantenha comentários atualizados

### API Documentation

- Documente todos os endpoints
- Inclua exemplos de request/response
- Documente códigos de erro

---

## Checklist de Pull Request

Antes de submeter um PR, verifique:

- [ ] Código segue os padrões de estilo
- [ ] Testes foram adicionados/atualizados
- [ ] Todos os testes passam
- [ ] Documentação foi atualizada
- [ ] CHANGELOG foi atualizado (se aplicável)
- [ ] Commit messages seguem o padrão
- [ ] Branch está atualizada com main
- [ ] Código foi revisado

---

## Estrutura do Projeto

```
doc2pdf/
├── app.py                     # Aplicação Flask principal
├── version.py                 # Informações de versão
├── requirements.txt           # Dependências
├── setup.py                   # Setup para pip
├── pyproject.toml            # Configuração moderna
├── Dockerfile                # Container Docker
├── render.yaml               # Config Render
├── bump_version.py           # Script de versionamento
├── example_usage.py          # Exemplos de uso
├── README.md                 # Documentação principal
├── CHANGELOG.md              # Histórico de versões
├── CONTRIBUTING.md           # Este arquivo
├── LICENSE                   # Licença MIT
├── POSTMAN_GUIDE.md          # Guia Postman
├── DOC2PDF_API.postman_collection.json  # Coleção Postman
├── .gitignore                # Git ignore
└── .dockerignore             # Docker ignore
```

---

## Recursos Úteis

- [Flask Documentation](https://flask.palletsprojects.com/)
- [python-docx Documentation](https://python-docx.readthedocs.io/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [RESTful API Design](https://restfulapi.net/)

---

## Dúvidas?

Se tiver dúvidas, abra uma issue ou entre em contato:

- 📧 Email: maxwbh@gmail.com
- 💼 LinkedIn: [/maxwbh](https://linkedin.com/in/maxwbh)

---

**Obrigado por contribuir com o DOC2PDF API!** 🎉

**Desenvolvido por Maxwell da Silva Oliveira - M&S do Brasil LTDA**
