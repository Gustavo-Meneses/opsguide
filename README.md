# 🖥️ OpsGuide Platform v9.1

Plataforma corporativa de infraestrutura com **IA**, **autenticação multi-usuário**, **dashboard em tempo real**, **integração GitHub** e **gerador de Runbooks**.

---

## 📋 Changelog

### v9.1 — Hotfix de compatibilidade
- ✅ **FIX crítico:** `Hasher.__init__()` — API do `streamlit-authenticator 0.4.2` mudou; substituído por `auto_hash=True` no `Authenticate()`
- ✅ **FIX:** `login()` agora trata retorno como tupla **ou** `None` (compatibilidade com variações da lib)
- ✅ **FIX:** Warning `st.components.v1.html` suprimido — mantida compatibilidade até jun/2026
- ✅ **FIX:** Chaves únicas nos chips de busca GitHub (`key=f"chip_{i}"`) para evitar `DuplicateWidgetID`

### v9.0 — Plataforma Comercial
- Auth multi-usuário, Dashboard, Feed HackerNews, GitHub API, Runbook Generator, UI dark mobile-first

### v8.x
- Correções de indentação, histórico, modelo, emergência anti-duplicata

---

## 🚀 Funcionalidades

### 🔐 Autenticação
- Login com usuário/senha · Cookie de sessão (7 dias)
- `auto_hash=True` — senhas em texto puro no `secrets.toml`, hash bcrypt feito automaticamente
- Logout na sidebar

### 💬 Chat
- Streaming token a token · Diagramas Mermaid dark · Download de scripts · DR Mode

### 📊 Dashboard
- Métricas por usuário · Feed Hacker News (cache 10min) · Histórico de sessões

### 🐙 GitHub
- Busca por repositórios filtrada por linguagem · Chips de sugestão por foco técnico

### 📋 Runbook
- Exportação Markdown estruturada · Salvar no perfil · Preview inline

---

## 🛠️ Tecnologias

| Tecnologia | Versão mínima | Uso |
|---|---|---|
| Python | 3.10+ | Backend |
| Streamlit | 1.32.0 | UI |
| streamlit-authenticator | 0.4.2 | Auth multi-usuário |
| Mistral AI API | — | LLM (mistral-small-latest) |
| Hacker News API | — | Feed infra/security |
| GitHub REST API | — | Busca repositórios |
| Mermaid.js | 10 | Diagramas |
| bcrypt | 4.0+ | Hash de senhas |

---

## 📦 Instalação

```bash
git clone https://github.com/seuusuario/opsguide-platform.git
cd opsguide-platform
pip install -r requirements.txt
```

---

## 🔑 Configuração — `.streamlit/secrets.toml`

```toml
MISTRAL_API_KEY = "SUA_API_KEY_AQUI"

[cookie]
name        = "opsguide_auth"
key         = "string_aleatoria_longa_e_secreta"
expiry_days = 7

[credentials.usernames.admin]
name     = "Administrador"
password = "sua_senha_em_texto_puro"   # auto_hash=True faz o bcrypt automaticamente
role     = "admin"
email    = "admin@suaempresa.com"

[credentials.usernames.devops]
name     = "DevOps Engineer"
password = "outra_senha"
role     = "engineer"
email    = "devops@suaempresa.com"
```

> ⚠️ Com `auto_hash=True`, **não é necessário** gerar hash manualmente. Coloque a senha em texto puro no `secrets.toml` — o Streamlit Cloud a hasheia automaticamente na primeira execução.

---

## ▶️ Executando

```bash
streamlit run app.py
```

---

## 📁 Estrutura

```
opsguide-platform/
├── app.py
├── README.md
├── requirements.txt
├── user_data/          ← criado automaticamente
└── .streamlit/
    └── secrets.toml
```

---

## 📄 requirements.txt

```
streamlit>=1.32.0
streamlit-authenticator>=0.4.2
requests>=2.31.0
bcrypt>=4.0.0
PyYAML>=6.0
```

---

## ☁️ Deploy — Streamlit Community Cloud (100% web)

1. Suba os arquivos no GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Conecte o repositório e defina `app.py` como entry point
4. Em **Settings > Secrets**, cole o conteúdo do `secrets.toml`
5. Deploy automático a cada push no `main`

---

## 📈 Roadmap

| Feature | Status |
|---|---|
| Auth multi-usuário | ✅ v9.0 |
| Dashboard + métricas | ✅ v9.0 |
| Feed HackerNews | ✅ v9.0 |
| GitHub integration | ✅ v9.0 |
| Runbook generator | ✅ v9.0 |
| Hotfix compatibilidade 0.4.2 | ✅ v9.1 |
| Upload de logs para análise | 🔜 v9.2 |
| Persistência em banco (SQLite) | 🔜 v9.2 |
| Painel admin multi-equipe | 🔜 v9.3 |
| Exportação PDF de runbooks | 🔜 v9.3 |
| Notificações Slack/Teams | 🔜 v9.4 |

---

## 📜 Licença

MIT — OpsGuide Platform, copiloto de infraestrutura corporativa.
