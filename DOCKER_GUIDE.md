# 🐳 Guia de Instalação Docker - DOC2PDF API

Guia completo para instalação e execução da API usando Docker e Docker Compose.

**Autor:** Maxwell da Silva Oliveira - M&S do Brasil LTDA
**Email:** maxwbh@gmail.com
**Versão:** 1.0.3

---

## 📋 Pré-requisitos

- Docker 20.10+ instalado
- Docker Compose 1.29+ instalado
- 1GB de RAM disponível
- 2GB de espaço em disco

### Verificar Instalação

```bash
docker --version
docker-compose --version
```

---

## 🚀 Instalação Rápida

### Opção 1: Docker Compose (Recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/Maxwbh/doc2pdf.git
cd doc2pdf

# 2. Inicie os containers
docker-compose up -d

# 3. Verifique o status
docker-compose ps

# 4. Acesse a API
curl http://localhost:5000/health
```

### Opção 2: Docker Build Manual

```bash
# 1. Clone o repositório
git clone https://github.com/Maxwbh/doc2pdf.git
cd doc2pdf

# 2. Build da imagem
docker build -t doc2pdf-api:latest .

# 3. Execute o container
docker run -d \
  --name doc2pdf-api \
  -p 5000:5000 \
  -e PORT=5000 \
  doc2pdf-api:latest

# 4. Verifique o status
docker ps

# 5. Acesse a API
curl http://localhost:5000/health
```

---

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` baseado em `.env.example`:

```bash
cp .env.example .env
```

Edite `.env` conforme necessário:

```env
PORT=5000
FLASK_ENV=production
PYTHONUNBUFFERED=1
```

### Portas Customizadas

Para usar uma porta diferente:

```bash
# Via docker-compose
PORT=8080 docker-compose up -d

# Via docker run
docker run -d \
  --name doc2pdf-api \
  -p 8080:5000 \
  -e PORT=5000 \
  doc2pdf-api:latest
```

---

## 📊 Gerenciamento

### Comandos Docker Compose

```bash
# Iniciar serviços
docker-compose up -d

# Parar serviços
docker-compose stop

# Reiniciar serviços
docker-compose restart

# Ver logs
docker-compose logs -f

# Ver logs das últimas 100 linhas
docker-compose logs --tail=100 -f

# Parar e remover containers
docker-compose down

# Parar, remover e limpar volumes
docker-compose down -v

# Rebuild da imagem
docker-compose build --no-cache

# Ver status dos serviços
docker-compose ps

# Executar comando dentro do container
docker-compose exec doc2pdf-api bash
```

### Comandos Docker Diretos

```bash
# Ver containers em execução
docker ps

# Ver todos os containers
docker ps -a

# Ver logs
docker logs doc2pdf-api

# Ver logs em tempo real
docker logs -f doc2pdf-api

# Parar container
docker stop doc2pdf-api

# Iniciar container
docker start doc2pdf-api

# Reiniciar container
docker restart doc2pdf-api

# Remover container
docker rm doc2pdf-api

# Remover container (forçado)
docker rm -f doc2pdf-api

# Acessar shell do container
docker exec -it doc2pdf-api bash

# Ver estatísticas de recursos
docker stats doc2pdf-api

# Inspecionar container
docker inspect doc2pdf-api
```

---

## 🔍 Health Check

A API possui health check automático:

```bash
# Via curl
curl http://localhost:5000/health

# Via docker
docker inspect --format='{{json .State.Health}}' doc2pdf-api | jq

# Resposta esperada
{
    "status": "healthy",
    "service": "doc2pdf-api",
    "version": "1.0.3"
}
```

---

## 📝 Logs e Debugging

### Ver Logs

```bash
# Últimas 100 linhas
docker-compose logs --tail=100 doc2pdf-api

# Em tempo real
docker-compose logs -f doc2pdf-api

# Logs desde uma data específica
docker-compose logs --since="2024-11-27T12:00:00" doc2pdf-api

# Logs com timestamps
docker-compose logs -t doc2pdf-api
```

### Debug Mode

Para executar em modo debug:

```bash
# Edite docker-compose.yml e adicione:
environment:
  - FLASK_ENV=development
  - FLASK_DEBUG=1

# Reinicie
docker-compose restart
```

---

## 🔒 Segurança

### Limites de Recursos

O `docker-compose.yml` já inclui limites:

```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 1G
    reservations:
      cpus: '0.5'
      memory: 512M
```

### Network Isolation

A API roda em uma rede isolada:

```bash
# Ver networks
docker network ls

# Inspecionar network
docker network inspect doc2pdf-network
```

---

## 🚀 Deploy em Produção

### Docker Compose Produção

```yaml
version: '3.8'

services:
  doc2pdf-api:
    image: doc2pdf-api:1.0.3
    container_name: doc2pdf-api
    restart: always
    ports:
      - "80:5000"
    environment:
      - PORT=5000
      - FLASK_ENV=production
      - PYTHONUNBUFFERED=1
    networks:
      - doc2pdf-network
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G

  nginx:
    image: nginx:alpine
    container_name: doc2pdf-nginx
    restart: always
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - doc2pdf-api
    networks:
      - doc2pdf-network

networks:
  doc2pdf-network:
    driver: bridge
```

### Com Nginx Reverse Proxy

Crie `nginx.conf`:

```nginx
events {
    worker_connections 1024;
}

http {
    upstream doc2pdf {
        server doc2pdf-api:5000;
    }

    server {
        listen 80;
        server_name api.seudominio.com;

        location / {
            proxy_pass http://doc2pdf;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # Timeout para conversões longas
            proxy_read_timeout 300s;
            proxy_connect_timeout 300s;
        }
    }
}
```

---

## 🔄 Atualização

### Atualizar para Nova Versão

```bash
# 1. Pull das mudanças
git pull origin main

# 2. Rebuild da imagem
docker-compose build --no-cache

# 3. Reinicie os serviços
docker-compose up -d

# 4. Verifique a versão
curl http://localhost:5000/health
```

---

## 🧪 Testes

### Testar Instalação

```bash
# 1. Health check
curl http://localhost:5000/health

# 2. Info da API
curl http://localhost:5000/

# 3. Teste de conversão (use a coleção do Postman)
```

### Teste de Carga

```bash
# Usando Apache Bench
ab -n 100 -c 10 http://localhost:5000/health

# Usando wrk
wrk -t4 -c100 -d30s http://localhost:5000/health
```

---

## ❌ Troubleshooting

### Container não inicia

```bash
# Ver logs de erro
docker-compose logs doc2pdf-api

# Verificar se a porta está em uso
lsof -i :5000

# Tentar outra porta
PORT=8080 docker-compose up -d
```

### Erro de permissão

```bash
# Linux: Adicione seu usuário ao grupo docker
sudo usermod -aG docker $USER

# Recarregue os grupos
newgrp docker
```

### Imagem não atualiza

```bash
# Force rebuild sem cache
docker-compose build --no-cache --pull

# Remova imagens antigas
docker image prune -a
```

### Limpeza Completa

```bash
# Parar e remover tudo
docker-compose down -v

# Remover imagens
docker rmi doc2pdf-api:latest

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

---

## 📊 Monitoramento

### Docker Stats

```bash
# Monitoramento em tempo real
docker stats doc2pdf-api

# Output:
# CONTAINER ID   CPU %   MEM USAGE / LIMIT   MEM %   NET I/O
# abc123def456   5.2%    512MiB / 1GiB      50.0%   1.5MB / 2MB
```

### Logs Estruturados

```bash
# JSON format
docker logs doc2pdf-api --format='{{json .}}'

# Com jq
docker logs doc2pdf-api | jq
```

---

## 🌐 Integração com CI/CD

### GitHub Actions

```yaml
name: Build and Push Docker Image

on:
  push:
    tags:
      - 'v*'

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build image
        run: docker build -t doc2pdf-api:${{ github.ref_name }} .

      - name: Test image
        run: |
          docker run -d --name test -p 5000:5000 doc2pdf-api:${{ github.ref_name }}
          sleep 10
          curl -f http://localhost:5000/health || exit 1
          docker stop test
```

---

## 📚 Recursos Adicionais

- [Dockerfile](Dockerfile) - Configuração da imagem
- [docker-compose.yml](docker-compose.yml) - Configuração dos serviços
- [.env.example](.env.example) - Variáveis de ambiente
- [README.md](README.md) - Documentação principal

---

## 💡 Dicas

1. **Use volumes para desenvolvimento**
   ```yaml
   volumes:
     - ./app.py:/app/app.py:ro
   ```

2. **Configure limites de recursos apropriados**
   - Produção: 1-2 CPUs, 1-2GB RAM
   - Desenvolvimento: 0.5 CPU, 512MB RAM

3. **Use health checks**
   - Garante que o container está saudável
   - Permite restart automático em caso de falha

4. **Monitore logs regularmente**
   ```bash
   docker-compose logs -f --tail=100
   ```

5. **Backup de configurações**
   - Faça backup do `docker-compose.yml`
   - Faça backup do `.env`

---

**Desenvolvido por Maxwell da Silva Oliveira - M&S do Brasil LTDA**
📧 maxwbh@gmail.com | 💼 [LinkedIn: /maxwbh](https://linkedin.com/in/maxwbh)
