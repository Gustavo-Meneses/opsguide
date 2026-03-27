# 🖥️ OpsGuide Architect v8.7

Assistente DevOps interativo desenvolvido com **Streamlit** que utiliza **IA (Mistral API)** para ajudar administradores de sistemas a resolver problemas, gerar scripts e visualizar arquiteturas técnicas através de **diagramas Mermaid**.

O objetivo do projeto é fornecer um **copiloto para operações de infraestrutura**, auxiliando profissionais de **Linux, Windows Server, DevOps e SRE** com troubleshooting, automação e documentação técnica.

---

## 📋 Changelog

### v8.7 — Correções de UX e estado
- ✅ **Botão de Limpar Histórico** — visível na sidebar com estilo vermelho destacado
- ✅ **Botão de Emergência anti-duplicata** — usa flag `emergency_triggered` no `session_state`; a flag é resetada antes do processamento, evitando múltiplas injeções mesmo com cliques rápidos
- ✅ **Fluxo de mensagem unificado** — `pending_prompt` centraliza o processamento, evitando race conditions entre o botão de emergência e o `chat_input`

### v8.6 — Correções críticas
- ✅ Bug de indentação corrigido — renderização de diagramas e botão de download fora do loop de streaming
- ✅ Histórico persistido no `session_state`
- ✅ Contexto multi-turno — histórico completo enviado à API
- ✅ Modelo atualizado — `mistral-tiny` → `mistral-small-latest`
- ✅ Timeout aumentado de 30s para 60s

---

## 🚀 Funcionalidades

### 🤖 Assistente de Infraestrutura

- Chat interativo com IA especializada em ambientes de servidores
- Respostas em **Português (PT-BR)**
- Contexto ajustado automaticamente conforme plataforma selecionada
- **Memória de conversa** — a IA lembra das mensagens anteriores dentro da sessão

### 🐧 Suporte a Linux

Ambientes suportados:
- Oracle Linux 9
- Oracle Linux 8
- Oracle Linux 7

Focos técnicos:
- Sistema / Kernel
- Docker / Portainer
- PostgreSQL

Scripts gerados em `.sh`

---

### 🪟 Suporte a Windows Server

Ambientes suportados:
- Windows Server 2022
- Windows Server 2019
- Windows Server 2016

Focos técnicos:
- PowerShell
- SQL Server
- Hyper-V
- Active Directory / Rede

Scripts gerados em `.ps1`

---

### 📊 Diagramas Automáticos com Mermaid

A IA gera **diagramas técnicos automaticamente**, renderizados no navegador via **Mermaid.js**.

Exemplo:

```
graph TD
A[Cliente] --> B[Load Balancer]
B --> C[Servidor Web]
C --> D[Database]
```

---

### 💾 Download Automático de Scripts

Quando a IA gera scripts dentro de blocos de código, o sistema detecta, extrai e gera um botão de download automaticamente.

---

### 🚨 Modo de Emergência (Disaster Recovery)

Botão especial na sidebar que solicita comandos críticos de diagnóstico e recuperação para o ambiente selecionado. Protegido contra cliques duplicados via flag de estado.

### 🗑️ Limpar Histórico

Botão na sidebar (destaque vermelho) que reinicia a conversa e limpa todo o histórico da sessão.

---

## 🧠 Arquitetura da Aplicação

```
Streamlit UI
     │
     │  session_state
     │  ├── messages[]         ← histórico completo
     │  └── emergency_triggered ← flag anti-duplicata
     ▼
OpsGuide App (pending_prompt)
     │
     │ HTTP API (streaming)
     ▼
Mistral AI — mistral-small-latest
     │
     ▼
Resposta com:
 • explicação técnica (PT-BR)
 • scripts (.sh / .ps1)
 • diagramas Mermaid
```

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **Streamlit**
- **Mistral AI API** (`mistral-small-latest`)
- **Mermaid.js**
- **Requests**
- **Regex Parsing**

---

## 📦 Instalação

```bash
git clone https://github.com/seuusuario/opsguide-architect.git
cd opsguide-architect
pip install -r requirements.txt
```

---

## 🔑 Configuração da API

Crie `.streamlit/secrets.toml`:

```toml
MISTRAL_API_KEY="SUA_API_KEY_AQUI"
```

---

## ▶️ Executando

```bash
streamlit run app.py
```

---

## 📁 Estrutura do Projeto

```
opsguide-architect/
│
├── app.py
├── README.md
├── requirements.txt
│
└── .streamlit/
    └── secrets.toml
```

---

## 📄 requirements.txt

```
streamlit>=1.32.0
requests>=2.31.0
```

---

## 🔐 Segurança

- Comunicação HTTP direta com a API da Mistral
- Streaming com timeout de 60s
- API Key nunca exposta no código-fonte
- Tratamento de erros de rede e status HTTP

---

## 📈 Possíveis Melhorias Futuras

- Upload de logs para análise automática
- Integração com Kubernetes
- Geração de Runbooks DevOps
- Suporte a Terraform / Ansible
- Histórico persistente entre sessões
- Exportação de diagramas em PNG/SVG
- Suporte a múltiplos modelos de IA

---

## 📜 Licença

MIT

---

## 🚀 OpsGuide

Um **copiloto de infraestrutura inteligente** para administradores de sistemas.
