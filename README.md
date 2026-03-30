# 🖥️ OpsGuide Architect v9.0

Assistente DevOps interativo desenvolvido com **Streamlit** que utiliza **IA (Mistral API)** para ajudar administradores de sistemas a resolver problemas, gerar scripts e visualizar arquiteturas técnicas através de **diagramas Mermaid**.

O objetivo do projeto é fornecer um **copiloto para operações de infraestrutura**, auxiliando profissionais de **Linux, Windows Server, DevOps e SRE** com troubleshooting, automação e documentação técnica.

---

## 📋 Changelog

### v9.0 — Arquitetura modular + RAG

* ✅ **Módulo `core/llm.py`** — chamada à API Mistral e streaming isolados do `app.py`
* ✅ **Módulo `core/rag.py`** — sistema RAG com busca por similaridade léxica sobre base de conhecimento interna
* ✅ **Módulo `core/parser.py`** — extração de código e diagramas Mermaid desacoplada do `app.py`
* ✅ **Base de conhecimento em `data/base_conhecimento.txt`** — chunks separados por linha em branco
* ✅ **RAG com fallback seguro** — envio do prompt original quando não há contexto relevante
* ✅ **Indicador de KB na sidebar**

---

## 🚀 Funcionalidades

### 🤖 Assistente de Infraestrutura

* Chat interativo com IA especializada
* Respostas em **Português (PT-BR)**
* **Memória de conversa**
* **RAG interno** com base local

---

## 🧠 Arquitetura da Aplicação

```
Streamlit UI
     │
     ▼
OpsGuide App
     │
     ├── core/rag.py
     ├── core/llm.py
     └── core/parser.py
     ▼
Mistral AI
```

---

## 🧠 Decisões de Arquitetura

### 1. RAG Simples (léxico)

Optou-se por similaridade por palavras-chave para:

* Reduzir complexidade
* Evitar dependências externas
* Facilitar manutenção

---

### 2. Modularização

Separação clara:

* `llm.py` → API
* `rag.py` → contexto
* `parser.py` → pós-processamento

---

### 3. Streaming

* Melhor UX
* Menor latência percebida

---

### 4. Session State

* Histórico
* Controle de estado

---

### 5. Parser desacoplado

* Reutilização
* Testabilidade

---

### 6. Mermaid

* Visual nativo
* Sem dependências externas

---

## 🗂️ Base de Conhecimento (RAG)

Arquivo: `data/base_conhecimento.txt`

Formato: blocos separados por linha em branco.

---

## 🔍 Exemplo de RAG em ação

**Pergunta:**

```
Como verificar uso de disco no Linux?
```

**Contexto recuperado:**

```
df -hT
du -sh /*
```

**Prompt enviado ao modelo:**

```
Contexto adicional:
df -hT
du -sh /*

Pergunta:
Como verificar uso de disco no Linux?
```

**Resposta:**

* Explicação dos comandos
* Diagnóstico de uso de disco

💡 Usa similaridade léxica simples.

---

## ⚠️ Limitações Técnicas

* RAG léxico (sem embeddings)
* Sem banco vetorial
* Busca O(n)
* Base estática
* Sem re-ranking
* Sem persistência de histórico

---

## 🛠️ Tecnologias

* Python
* Streamlit
* Mistral API
* Requests
* Mermaid.js

---

## 📦 Instalação

```bash
git clone https://github.com/Gustavo-Meneses/opsguide.git
cd opsguide
pip install -r requirements.txt
```

---

## 🔑 Configuração

`.streamlit/secrets.toml`

```toml
MISTRAL_API_KEY="SUA_API_KEY"
```

---

## ▶️ Execução

```bash
streamlit run app.py
```

---

## 📈 Melhorias Futuras

* Embeddings
* Vector DB
* Kubernetes
* Terraform

---

## 📜 Licença

MIT

---

## 🚀 OpsGuide

Copiloto inteligente para infraestrutura.
