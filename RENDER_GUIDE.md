# ☁️ Guia de Deploy no Render - DOC2PDF API

Guia completo para fazer deploy da API no Render com Blueprint (configuração automática).

**Autor:** Maxwell da Silva Oliveira - M&S do Brasil LTDA
**Email:** maxwbh@gmail.com
**Versão:** 1.0.3

---

## 🚀 Deploy Automático (1 Clique)

### Opção 1: Deploy Direto do GitHub (Mais Fácil)

Clique no botão abaixo para fazer deploy automático:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/Maxwbh/doc2pdf)

**O que acontece:**
1. ✅ Conecta automaticamente com GitHub
2. ✅ Detecta o `render.yaml`
3. ✅ Configura todas as variáveis de ambiente
4. ✅ Faz build do Docker
5. ✅ Inicia a aplicação
6. ✅ Fornece URL pública

**Tempo total:** ~5 minutos

---

## 📋 Pré-requisitos

- Conta no GitHub (gratuita)
- Conta no Render (gratuita) - [Criar conta](https://render.com/register)
- Repositório do projeto (fork ou clone)

---

## 🔧 Deploy Manual (Passo a Passo)

### Passo 1: Preparar Repositório

```bash
# Fork o repositório no GitHub
# Ou clone para sua conta:
git clone https://github.com/Maxwbh/doc2pdf.git
cd doc2pdf
git remote set-url origin https://github.com/SEU_USUARIO/doc2pdf.git
git push -u origin main
```

### Passo 2: Conectar Render ao GitHub

1. Acesse [render.com](https://render.com)
2. Faça login ou crie uma conta
3. Vá em **Dashboard**
4. Clique em **New +** → **Blueprint**
5. Conecte sua conta do GitHub (se ainda não conectou)
6. Autorize o Render a acessar seus repositórios

### Passo 3: Selecionar Repositório

1. Na tela de Blueprint, selecione **doc2pdf**
2. O Render detectará automaticamente o `render.yaml`
3. Você verá a configuração:
   ```
   ✓ doc2pdf-api (Web Service)
     Runtime: Docker
     Plan: Free
     Region: Oregon
   ```

### Passo 4: Revisar Configurações

Revise as configurações automáticas:

- **Name:** `doc2pdf-api`
- **Environment:** `Docker`
- **Plan:** `Free` (ou escolha outro)
- **Branch:** `main`
- **Region:** `Oregon` (ou escolha outro)

**Variáveis de Ambiente (já configuradas):**
- `PORT=5000`
- `PYTHONUNBUFFERED=1`
- `FLASK_ENV=production`

### Passo 5: Deploy

1. Clique em **Apply**
2. Aguarde o build (3-5 minutos)
3. Monitore os logs em tempo real

**O que está acontecendo:**
```
[Build] Detectando Dockerfile...
[Build] Instalando LibreOffice...
[Build] Instalando dependências Python...
[Build] Build concluído!
[Deploy] Iniciando aplicação...
[Deploy] Health check OK!
[Deploy] Deploy concluído! ✓
```

### Passo 6: Testar

Sua API estará disponível em:
```
https://doc2pdf-api-XXXX.onrender.com
```

Teste:
```bash
# Health check
curl https://doc2pdf-api-XXXX.onrender.com/health

# Info da API
curl https://doc2pdf-api-XXXX.onrender.com/
```

---

## ⚙️ Configurações Avançadas

### Alterar Plano

Para melhor performance, considere upgrade:

| Plano | Memória | CPU | Preço/mês |
|-------|---------|-----|-----------|
| Free | 512MB | Shared | $0 |
| Starter | 512MB | Shared | $7 |
| Standard | 2GB | 1 CPU | $25 |
| Pro | 4GB | 2 CPU | $85 |

**Como alterar:**
1. Dashboard → seu serviço
2. Settings → Plan
3. Selecione o plano
4. Confirm

### Variáveis de Ambiente Customizadas

Adicionar variáveis via Dashboard:

1. Dashboard → seu serviço
2. Environment → Add Environment Variable
3. Adicione:
   ```
   MAX_CONTENT_LENGTH=16777216  # 16MB
   TIMEOUT=60                    # 60 segundos
   ```
4. Save Changes

Ou edite `render.yaml`:
```yaml
envVars:
  - key: MAX_CONTENT_LENGTH
    value: 16777216
  - key: TIMEOUT
    value: 60
```

### Domínio Customizado

1. Dashboard → seu serviço
2. Settings → Custom Domains
3. Add Custom Domain
4. Configure DNS:
   ```
   CNAME api.seudominio.com -> doc2pdf-api-XXXX.onrender.com
   ```
5. Aguarde propagação (até 48h)

### Configurar HTTPS

**HTTPS é automático no Render!** ✓

Certificado SSL/TLS gratuito via Let's Encrypt.

### Regiões Disponíveis

Escolha a região mais próxima dos seus usuários:

- **Oregon (US West)** - Padrão
- **Ohio (US East)**
- **Frankfurt (EU Central)**
- **Singapore (Asia Pacific)**

**Alterar região:**
1. Edit `render.yaml`:
   ```yaml
   region: frankfurt  # ou ohio, singapore
   ```
2. Commit e push
3. Render fará redeploy automático

---

## 🔄 Atualizações e Redeploy

### Deploy Automático (Recomendado)

Com `autoDeploy: true` no `render.yaml`:

```bash
# Faça suas mudanças
git add .
git commit -m "feat: nova funcionalidade"
git push origin main

# Render detecta e faz deploy automático!
```

Monitore em: Dashboard → seu serviço → Events

### Deploy Manual

Se `autoDeploy: false`:

1. Dashboard → seu serviço
2. Manual Deploy → Deploy latest commit
3. Aguarde build

### Rollback

Para voltar a versão anterior:

1. Dashboard → seu serviço
2. Events
3. Encontre o deploy anterior
4. Rollback

---

## 📊 Monitoramento

### Logs em Tempo Real

```bash
# Via Dashboard
Dashboard → seu serviço → Logs

# Ou via CLI
render logs doc2pdf-api --tail
```

### Métricas

Dashboard → seu serviço → Metrics

Visualize:
- CPU usage
- Memory usage
- Request count
- Response time
- Error rate

### Health Checks

Render verifica `/health` a cada 30 segundos.

Se falhar 3 vezes consecutivas:
- Serviço é marcado como "unhealthy"
- Render tenta restart automático

### Alertas

Configure notificações:

1. Edite `render.yaml`:
   ```yaml
   notifications:
     - events:
         - deploy-succeeded
         - deploy-failed
         - service-unhealthy
       email:
         - maxwbh@gmail.com
   ```
2. Commit e push

---

## 💰 Custos e Limites

### Plano Free

**Incluído:**
- ✅ 750 horas/mês de execução
- ✅ HTTPS gratuito
- ✅ Auto-deploy do GitHub
- ✅ Health checks
- ✅ 512MB RAM

**Limitações:**
- ⚠️ Serviço hiberna após 15min inativo
- ⚠️ Primeiro request após hibernar é lento (~30s)
- ⚠️ 100GB bandwidth/mês

**Dica:** Para evitar hibernação, use serviço de ping:
```bash
# Cron job a cada 10 minutos
*/10 * * * * curl https://sua-api.onrender.com/health
```

Ou use serviços gratuitos:
- [UptimeRobot](https://uptimerobot.com/)
- [Cronit or](https://cron-job.org/)

### Upgrade Recomendações

**Quando fazer upgrade:**
- ✅ Produção com usuários reais
- ✅ Necessita estar sempre ativo
- ✅ > 100 requests/dia
- ✅ Conversões de documentos grandes

---

## 🔒 Segurança

### Secrets

Para dados sensíveis:

1. Dashboard → Environment
2. Add Secret File ou Environment Variable
3. Marque como "secret"
4. Não aparecerá nos logs

### Headers de Segurança

Configurados automaticamente no Flask (`app.py`):

```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    return response
```

**Headers aplicados:**
- ✅ X-Frame-Options: Previne clickjacking
- ✅ X-Content-Type-Options: Previne MIME sniffing
- ✅ X-XSS-Protection: Proteção contra XSS
- ✅ Strict-Transport-Security: Força HTTPS

### Rate Limiting

Para proteger contra abuso, considere adicionar rate limiting:

```python
# Adicione ao app.py
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["100 per hour"]
)

@app.route('/convert', methods=['POST'])
@limiter.limit("10 per minute")
def convert_document():
    # ...
```

---

## ❌ Troubleshooting

### Deploy Falha

**Erro:** "Failed to build"
```bash
# Verifique:
1. Dockerfile existe
2. requirements.txt está correto
3. Logs de build no Dashboard

# Teste localmente:
docker build -t doc2pdf-api .
```

**Erro:** "Port already in use"
```bash
# Render define PORT automaticamente
# Certifique-se de usar:
port = int(os.environ.get('PORT', 5000))
```

### Serviço Não Inicia

**Health check failing:**
```bash
# Verifique:
1. /health endpoint existe
2. App está escutando na porta correta
3. LibreOffice foi instalado

# Logs:
Dashboard → Logs → procure por erros
```

### Timeout na Conversão

Para documentos grandes:

1. Aumente timeout no Render:
   ```yaml
   envVars:
     - key: TIMEOUT
       value: 120  # 2 minutos
   ```

2. Ou use Starter+ plan (mais recursos)

### Serviço Lento

**Causa:** Hibernação (Free plan)

**Soluções:**
1. Upgrade para Starter ($7/mês)
2. Use serviço de ping
3. Mantenha requisições regulares

---

## 🌐 Integração com CI/CD

### GitHub Actions

Adicione `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Render
        run: |
          curl -X POST \
            -H "Authorization: Bearer ${{ secrets.RENDER_API_KEY }}" \
            https://api.render.com/v1/services/${{ secrets.RENDER_SERVICE_ID }}/deploys
```

### Webhook

Configure webhook para deploy automático:

1. Dashboard → Settings → Webhook
2. Copy webhook URL
3. Use em seu CI/CD:
   ```bash
   curl -X POST https://api.render.com/deploy/srv-XXXXX
   ```

---

## 📚 Recursos Adicionais

### Render CLI

Instale:
```bash
npm install -g @render/cli
# ou
brew install render
```

Comandos úteis:
```bash
# Login
render login

# Listar serviços
render services list

# Ver logs
render logs doc2pdf-api

# SSH para container
render shell doc2pdf-api

# Deploy
render deploy doc2pdf-api
```

### Documentação Oficial

- [Render Docs](https://render.com/docs)
- [Blueprint Spec](https://render.com/docs/blueprint-spec)
- [Docker on Render](https://render.com/docs/docker)
- [Environment Variables](https://render.com/docs/environment-variables)

---

## 🎯 Checklist de Deploy

Antes do deploy, verifique:

- [ ] `render.yaml` está configurado
- [ ] `Dockerfile` existe e funciona
- [ ] `requirements.txt` está atualizado
- [ ] Código está no GitHub
- [ ] Branch `main` está atualizado
- [ ] Health check endpoint funciona
- [ ] Variáveis de ambiente definidas
- [ ] Região selecionada
- [ ] Plano escolhido

Após o deploy:

- [ ] URL funcionando
- [ ] Health check OK
- [ ] Testar endpoints
- [ ] Verificar logs
- [ ] Configurar domínio (se necessário)
- [ ] Configurar alertas
- [ ] Documentar URL para equipe

---

## 💡 Dicas e Boas Práticas

1. **Use o plano Free para testes**
   - Depois faça upgrade para produção

2. **Configure auto-deploy**
   - Deploy automático a cada push

3. **Monitore logs regularmente**
   - Identifique problemas cedo

4. **Use health checks**
   - Garantem disponibilidade

5. **Configure domínio customizado**
   - Mais profissional para clientes

6. **Mantenha secrets seguros**
   - Nunca commite credenciais

7. **Teste localmente primeiro**
   - Use Docker para testar antes de deployar

8. **Documente sua URL**
   - Compartilhe com equipe

---

## 📞 Suporte

### Problemas com Render

- 📖 [Render Docs](https://render.com/docs)
- 💬 [Render Community](https://community.render.com/)
- 📧 [Render Support](https://render.com/support)

### Problemas com a API

- 📧 **Email:** [maxwbh@gmail.com](mailto:maxwbh@gmail.com)
- 💼 **LinkedIn:** [/maxwbh](https://linkedin.com/in/maxwbh)
- 🐛 **Issues:** [GitHub Issues](https://github.com/Maxwbh/doc2pdf/issues)

---

## 🎓 Exemplo Completo

### 1. Fork Repositório

```bash
# No GitHub: Fork do repositório Maxwbh/doc2pdf
```

### 2. Deploy no Render

```bash
# Acesse: https://render.com/deploy?repo=https://github.com/SEU_USUARIO/doc2pdf
# Clique em "Apply"
# Aguarde 5 minutos
```

### 3. Teste

```bash
# Substitua XXXX pela sua URL
curl https://doc2pdf-api-XXXX.onrender.com/health

# Deve retornar:
# {"status": "healthy", "service": "doc2pdf-api", "version": "1.0.3"}
```

### 4. Use na sua Aplicação

```python
import requests
import base64

API_URL = "https://doc2pdf-api-XXXX.onrender.com"

with open('documento.docx', 'rb') as f:
    doc_base64 = base64.b64encode(f.read()).decode('utf-8')

response = requests.post(f"{API_URL}/process", json={
    "input_type": "base64",
    "output_type": "pdf",
    "document": doc_base64,
    "replacements": {
        "NOME": "João Silva",
        "DATA": "27/11/2024"
    },
    "filename": "contrato_joao"
})

# Salva PDF
with open('contrato_joao.pdf', 'wb') as f:
    f.write(response.content)
```

---

**Desenvolvido por Maxwell da Silva Oliveira - M&S do Brasil LTDA**
📧 maxwbh@gmail.com | 💼 [LinkedIn: /maxwbh](https://linkedin.com/in/maxwbh)
