# 🖥️ OpsGuide Architect v9.0

Assistente DevOps interativo desenvolvido com **Streamlit** que utiliza **IA (Mistral API)** para ajudar administradores de sistemas a resolver problemas, gerar scripts e visualizar arquiteturas técnicas através de **diagramas Mermaid**.

O objetivo do projeto é fornecer um **copiloto para operações de infraestrutura**, auxiliando profissionais de **Linux, Windows Server, DevOps e SRE** com troubleshooting, automação e documentação técnica.

---

## 📋 Changelog

### v9.0 — Arquitetura modular + RAG
- ✅ **Módulo `core/llm.py`** — chamada à API Mistral e streaming isolados do `app.py`
- ✅ **Módulo `core/rag.py`** — sistema RAG com busca por similaridade léxica sobre base de conhecimento interna
- ✅ **Módulo `core/parser.py`** — extração de código e diagramas Mermaid desacoplada do `app.py`
- ✅ **Base de conhecimento em `data/base_conhecimento.txt`** — chunks separados por linha em branco, carregados uma vez por sessão
- ✅ **RAG com fallback seguro** — se o arquivo não existir ou não houver contexto relevante, o prompt original é enviado sem alteração
- ✅ **Indicador de KB na sidebar** — exibe quantos chunks foram carregados ou avisa se a base está vazia

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
- **RAG interno** — respostas enriquecidas com conteúdo da base de conhecimento local antes de chamar o modelo

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
     │  ├── messages[]          ← histórico completo
     │  ├── knowledge_base[]    ← chunks da KB (carregado 1x por sessão)
     │  └── emergency_triggered ← flag anti-duplicata
     ▼
OpsGuide App (pending_prompt)
     │
     ├── core/rag.py
     │   └── simple_similarity_search()  ← enriquece o prompt com contexto interno
     │
     ├── core/llm.py
     │   └── call_mistral_api() + stream_response()  ← HTTP streaming
     │
     └── core/parser.py
         ├── extract_code()     ← detecta script para download
         └── extract_mermaid()  ← detecta diagrama para renderização
     │
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
git clone https://github.com/Gustavo-Meneses/opsguide.git
cd opsguide
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
opsguide/
│
├── app.py
├── README.md
├── requirements.txt
│
├── core/
│   ├── __init__.py
│   ├── llm.py        ← API Mistral + streaming
│   ├── rag.py        ← base de conhecimento + busca
│   └── parser.py     ← extração de código e Mermaid
│
├── data/
│   └── base_conhecimento.txt  ← base RAG (chunks separados por linha em branco)
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

## 🗂️ Base de Conhecimento (RAG)

O arquivo `data/base_conhecimento.txt` é a base interna do assistente. Adicione procedimentos, runbooks e referências técnicas do seu ambiente — o sistema recupera automaticamente os trechos mais relevantes antes de cada resposta.

**Formato:** texto livre, com blocos separados por uma linha em branco.

```
Reiniciar serviço no Oracle Linux:
sudo systemctl restart <servico>
sudo systemctl status <servico>

Verificar uso de disco:
df -hT
du -sh /* 2>/dev/null | sort -rh | head -20
```

Quanto mais específico for o conteúdo (comandos do seu ambiente, IPs internos, nomes de serviços), mais úteis serão as respostas.

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
- Embeddings vetoriais para substituir o RAG léxico

---

## 📜 Licença

MIT

---

## 🚀 OpsGuide

Um **copiloto de infraestrutura inteligente** para administradores de sistemas.
