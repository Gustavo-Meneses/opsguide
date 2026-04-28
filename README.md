# 🖥️ OpsGuide Platform v9.0

Plataforma corporativa de infraestrutura com **IA**, **autenticação multi-usuário**, **dashboard em tempo real**, **integração GitHub** e **gerador de Runbooks** — desenvolvida com Streamlit e Mistral AI.

---

## 📋 Changelog

### v9.0 — Plataforma Comercial
- ✅ **Autenticação multi-usuário** via `streamlit-authenticator` com cookies persistentes
- ✅ **Perfil por usuário** — histórico individual salvo em JSON por sessão
- ✅ **Dashboard com métricas** — sessões, mensagens, interações e runbooks gerados
- ✅ **Feed Hacker News** — notícias de infra/segurança em tempo real (cache 10min)
- ✅ **Integração GitHub API** — busca repositórios de scripts por linguagem e tema
- ✅ **Chips de sugestão** — atalhos contextuais de busca por foco técnico
- ✅ **Gerador de Runbooks** — exporta a conversa como `.md` estruturado
- ✅ **Salvar Runbook no perfil** — persistência de documentação por usuário
- ✅ **UI comercial dark** — design profissional com Inter font, cards, gradientes
- ✅ **Mobile-first** — layout responsivo, sidebar colapsável, touch-friendly
- ✅ **Contexto multi-turno completo** — histórico enviado à API a cada requisição
- ✅ **DR Mode aprimorado** — checklist estruturado por categoria

### v8.7
- Botão Limpar Histórico visível na sidebar
- Emergência anti-duplicata via flag de estado
- Fluxo unificado com `pending_prompt`

### v8.6
- Bug de indentação corrigido
- Histórico persistido no session_state
- Modelo atualizado para `mistral-small-latest`
- Timeout aumentado para 60s

---

## 🚀 Funcionalidades

### 🔐 Autenticação Multi-Usuário

- Login com usuário e senha
- Cookie de sessão com expiração configurável (padrão: 7 dias)
- Credenciais configuráveis via `secrets.toml`
- Perfil individual por usuário com dados persistidos em `user_data/`

### 💬 Chat de Infraestrutura

- IA especializada com contexto dinâmico por ambiente
- Streaming token a token com cursor animado
- Suporte a diagramas Mermaid.js (dark theme)
- Download automático de scripts (`.sh` / `.ps1`)
- DR Mode com checklist estruturado por categoria

### 📊 Dashboard

- **Métricas do usuário**: sessões totais, mensagens, interações na sessão, runbooks
- **Feed Hacker News**: top stories filtradas por keywords de infra/devops/security
  - Cache de 10 minutos para performance
  - Filtros: linux, docker, kubernetes, postgres, security, cloud, devops, sre, etc.
- **Histórico de sessões**: últimas 8 sessões com ambiente e quantidade de mensagens

### 🐙 GitHub Integration

- Busca de repositórios por tema e linguagem (`Shell` ou `PowerShell`)
- Ordenação por estrelas
- **Chips de sugestão contextuais** por foco técnico:
  - Sistema/Kernel → oracle linux tuning, hardening, sysctl
  - Docker/Portainer → compose production, container security
  - PostgreSQL → backup scripts, performance tuning
  - PowerShell → sysadmin scripts, AD management
  - SQL Server → maintenance, backup automation
  - Hyper-V → VM deployment, backup
  - AD/Rede → user management, network automation

### 📋 Runbook Generator

- Exporta a conversa completa como Markdown estruturado
- Inclui: ambiente, data/hora, total de interações, cada pergunta e resposta
- Download como `.md` com nome personalizado por usuário e data
- Salvar no perfil do usuário para rastreamento histórico
- Preview inline com scroll

---

## 🧠 Arquitetura

```
OpsGuide Platform v9.0
│
├── 🔐 streamlit-authenticator
│       └── Cookies + credenciais via secrets
│
├── 💬 Chat Engine
│       ├── Mistral AI (mistral-small-latest, streaming)
│       └── session_state (histórico multi-turno)
│
├── 📊 Dashboard
│       ├── Hacker News API (feed filtrado, cache 10min)
│       └── user_data/*.json (métricas por usuário)
│
├── 🐙 GitHub API
│       └── /search/repositories (por linguagem e tema)
│
└── 📋 Runbook Generator
        └── Exportação Markdown estruturada
```

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.10+ | Backend |
| Streamlit | UI framework |
| streamlit-authenticator | Auth multi-usuário |
| Mistral AI API | LLM (mistral-small-latest) |
| Hacker News Firebase API | Feed de infra/segurança |
| GitHub REST API | Busca de repositórios |
| Mermaid.js | Diagramas técnicos |
| Requests | HTTP client |
| Pathlib + JSON | Persistência local |

---

## 📦 Instalação

```bash
git clone https://github.com/seuusuario/opsguide-platform.git
cd opsguide-platform
pip install -r requirements.txt
```

---

## 🔑 Configuração

Crie `.streamlit/secrets.toml`:

```toml
MISTRAL_API_KEY = "SUA_API_KEY_AQUI"

[cookie]
name        = "opsguide_auth"
key         = "sua_chave_secreta_aleatoria"
expiry_days = 7

[credentials.usernames.admin]
name     = "Administrador"
password = "$2b$12$HASH_GERADO_PELO_STREAMLIT_AUTH"
role     = "admin"
email    = "admin@suaempresa.com"

[credentials.usernames.devops]
name     = "DevOps Engineer"
password = "$2b$12$HASH_GERADO_PELO_STREAMLIT_AUTH"
role     = "engineer"
email    = "devops@suaempresa.com"
```

### Gerar hash de senha

```python
import streamlit_authenticator as stauth
print(stauth.Hasher(["sua_senha_aqui"]).generate()[0])
```

---

## ▶️ Executando

```bash
streamlit run app.py
```

---

## 📁 Estrutura do Projeto

```
opsguide-platform/
│
├── app.py                  ← Aplicação principal
├── README.md
├── requirements.txt
│
├── user_data/              ← Dados persistidos por usuário (auto-criado)
│   ├── admin.json
│   └── devops.json
│
└── .streamlit/
    └── secrets.toml        ← API keys + credenciais
```

---

## 📄 requirements.txt

```
streamlit>=1.32.0
streamlit-authenticator>=0.3.2
requests>=2.31.0
bcrypt>=4.0.0
PyYAML>=6.0
```

---

## 🔐 Segurança

- Senhas armazenadas como **bcrypt hash** — nunca em texto puro
- API Key nunca exposta no código-fonte
- Comunicação HTTP direta com Mistral (sem intermediários)
- Cookies de sessão com chave secreta configurável
- Timeout de 90s para respostas longas
- GitHub API sem autenticação (rate limit: 60 req/h — suficiente para uso normal)

---

## 📈 Roadmap

| Feature | Status |
|---|---|
| Auth multi-usuário | ✅ v9.0 |
| Dashboard + métricas | ✅ v9.0 |
| Feed HackerNews | ✅ v9.0 |
| GitHub integration | ✅ v9.0 |
| Runbook generator | ✅ v9.0 |
| Upload de logs para análise | 🔜 v9.1 |
| Integração Kubernetes | 🔜 v9.1 |
| Histórico persistente em banco (SQLite/Postgres) | 🔜 v9.2 |
| Painel admin multi-equipe | 🔜 v9.2 |
| Exportação PDF de runbooks | 🔜 v9.3 |
| Suporte Terraform / Ansible | 🔜 v9.3 |
| Notificações de incidente (Slack/Teams) | 🔜 v9.4 |

---

## 👨‍💻 Contribuições

Pull requests são bem-vindos. Se você trabalha com DevOps, SRE, Infraestrutura, Cloud ou Automação, contribua com melhorias.

---

## 📜 Licença

MIT

---

## 🚀 OpsGuide Platform

O **copiloto de infraestrutura corporativa** para equipes de DevOps e SRE.
