# 🖥️ OpsGuide Platform v9.2

Plataforma corporativa de infraestrutura com **IA**, **auto-registro de usuários**, **autenticação persistente**, **dashboard em tempo real**, **integração GitHub** e **gerador de Runbooks**.

---

## 📋 Changelog

### v9.2 — Auto-registro + credenciais persistentes
- ✅ **Tela de Criar Conta** — qualquer pessoa pode se registrar diretamente na interface
- ✅ **Credenciais persistidas em `credentials.yaml`** — usuários sobrevivem a restarts do app
- ✅ **Usuário `admin` criado automaticamente** no primeiro boot (senha: `admin123`)
- ✅ **Validação de cadastro** — mínimo 3 chars no usuário, 6 na senha, confirmação de senha
- ✅ **Senhas em bcrypt hash** — `Hasher().hash()` chamado diretamente, sem depender do `auto_hash`
- ✅ **`auto_hash=False`** no `Authenticate` — evita double-hash pois as senhas já chegam hasheadas
- ✅ **Login/Registro em tabs** — UX limpa e intuitiva

### v9.1
- FIX: `Hasher.__init__()` incompatível com v0.4.2 → `auto_hash=True`
- FIX: `login()` retorno nullable
- FIX: chaves únicas nos chips GitHub

### v9.0
- Plataforma comercial: Auth, Dashboard, HN Feed, GitHub API, Runbook Generator, UI dark

---

## 🔐 Primeiro Acesso

Na primeira execução, o sistema cria automaticamente:

| Usuário | Senha |
|---|---|
| `admin` | `admin123` |

> ⚠️ **Troque a senha do admin após o primeiro login** (em versões futuras via painel de perfil).

Novos usuários podem se cadastrar diretamente pela aba **📝 Criar Conta** na tela de login.

---

## 🚀 Funcionalidades

### 🔐 Autenticação
- Tela com duas abas: **Entrar** e **Criar Conta**
- Registro auto-suficiente — sem necessidade de configurar `secrets.toml` para cada usuário
- Credenciais salvas em `credentials.yaml` com bcrypt hash
- Cookie de sessão persistente (7 dias por padrão)
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

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.10+ | Backend |
| Streamlit | ≥1.32.0 | UI |
| streamlit-authenticator | ≥0.4.2 | Auth |
| Mistral AI | — | LLM |
| Hacker News API | — | Feed |
| GitHub REST API | — | Repositórios |
| PyYAML | ≥6.0 | Persistência de credenciais |
| bcrypt | ≥4.0 | Hash de senhas |

---

## 📦 Instalação

```bash
git clone https://github.com/seuusuario/opsguide-platform.git
cd opsguide-platform
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔑 Configuração mínima — `.streamlit/secrets.toml`

```toml
MISTRAL_API_KEY = "SUA_API_KEY_AQUI"

[cookie]
name        = "opsguide_auth"
key         = "string_aleatoria_longa_e_secreta"
expiry_days = 7
```

> Não é necessário configurar usuários no `secrets.toml` — o registro é feito pela própria interface.

---

## ☁️ Deploy — Streamlit Community Cloud

1. Suba os arquivos no GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Selecione o repositório e `app.py` como entry point
4. Em **Settings > Secrets**, cole apenas:
   ```toml
   MISTRAL_API_KEY = "sua_chave"
   [cookie]
   name = "opsguide_auth"
   key  = "string_secreta"
   expiry_days = 7
   ```
5. Deploy → acesse o app → use `admin` / `admin123` no primeiro login

---

## 📁 Estrutura

```
opsguide-platform/
├── app.py
├── README.md
├── requirements.txt
├── credentials.yaml    ← criado automaticamente no primeiro boot
├── user_data/          ← dados por usuário (criado automaticamente)
│   └── admin.json
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

## 📈 Roadmap

| Feature | Status |
|---|---|
| Auth multi-usuário | ✅ v9.0 |
| Dashboard + métricas | ✅ v9.0 |
| Feed HackerNews | ✅ v9.0 |
| GitHub integration | ✅ v9.0 |
| Runbook generator | ✅ v9.0 |
| Hotfix compatibilidade 0.4.2 | ✅ v9.1 |
| Auto-registro de usuários | ✅ v9.2 |
| Persistência de credenciais | ✅ v9.2 |
| Trocar senha no perfil | 🔜 v9.3 |
| Painel admin (listar/remover usuários) | 🔜 v9.3 |
| Upload de logs para análise | 🔜 v9.4 |
| Notificações Slack/Teams | 🔜 v9.5 |

---

## 📜 Licença

MIT — OpsGuide Platform, copiloto de infraestrutura corporativa.
