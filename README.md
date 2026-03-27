# 🖥️ OpsGuide Architect v8.6

Assistente DevOps interativo desenvolvido com **Streamlit** que utiliza **IA (Mistral API)** para ajudar administradores de sistemas a resolver problemas, gerar scripts e visualizar arquiteturas técnicas através de **diagramas Mermaid**.

O objetivo do projeto é fornecer um **copiloto para operações de infraestrutura**, auxiliando profissionais de **Linux, Windows Server, DevOps e SRE** com troubleshooting, automação e documentação técnica.

---

## 📋 Changelog

### v8.6 — Correções críticas
- ✅ **Bug de indentação corrigido** — renderização de diagramas e botão de download agora executam corretamente após o fim do streaming
- ✅ **Histórico persistido** — respostas do assistente são salvas em `st.session_state`, mantendo o contexto entre turnos
- ✅ **Contexto multi-turno** — histórico completo é enviado à API a cada requisição, permitindo conversas coerentes
- ✅ **Modelo atualizado** — `mistral-tiny` (descontinuado) substituído por `mistral-small-latest`
- ✅ **Botão de emergência com proteção** — evita inserção duplicada de mensagens ao clicar repetidamente
- ✅ **Botão de limpar histórico** — nova opção na sidebar para reiniciar a conversa
- ✅ **Timeout aumentado** — de 30s para 60s para respostas mais longas

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

A IA pode gerar **diagramas técnicos automaticamente**, que são renderizados no navegador utilizando **Mermaid.js**.

Exemplo de diagrama gerado:

```
graph TD
A[Cliente] --> B[Load Balancer]
B --> C[Servidor Web]
C --> D[Database]
```

---

### 💾 Download Automático de Scripts

Quando a IA gera scripts dentro de blocos de código:

````markdown
```bash
systemctl restart docker
```
````

O sistema automaticamente:
- Detecta o código
- Extrai o conteúdo
- Gera um botão para download

---

### 🚨 Modo de Emergência (Disaster Recovery)

Botão especial na interface que solicita à IA comandos críticos de diagnóstico e recuperação para o ambiente selecionado.

Ideal para:
- Incidentes de produção
- Troubleshooting rápido
- Resposta a falhas de infraestrutura

> **v8.6:** Proteção contra cliques duplicados adicionada.

---

## 🧠 Arquitetura da Aplicação

```
Streamlit UI
     │
     │ session_state (histórico completo)
     ▼
OpsGuide App
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

Clone o repositório:

```bash
git clone https://github.com/seuusuario/opsguide-architect.git
cd opsguide-architect
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## 🔑 Configuração da API

Crie o arquivo de secrets do Streamlit:

```
.streamlit/secrets.toml
```

Adicione sua chave da Mistral:

```toml
MISTRAL_API_KEY="SUA_API_KEY_AQUI"
```

---

## ▶️ Executando a aplicação

```bash
streamlit run app.py
```

A interface abrirá automaticamente no navegador.

---

## 🖥️ Interface

A sidebar permite selecionar:
- **Plataforma** (Linux / Windows Server)
- **Versão** do sistema operacional
- **Área de foco** técnico
- **Modo de Emergência DR**
- **Limpar Histórico** (novo em v8.6)

Todas as seleções ajustam automaticamente o prompt enviado para a IA.

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

A comunicação com a IA é feita via **HTTP direto para a API da Mistral**, sem bibliotecas intermediárias.

Características:
- Streaming de resposta token a token
- Timeout de segurança (60s)
- Tratamento de erros de rede
- Validação de status HTTP da API
- API Key nunca exposta no código-fonte

---

## 📈 Possíveis Melhorias Futuras

- Upload de **logs para análise automática**
- Integração com **Kubernetes**
- Diagnóstico automático de infraestrutura
- Geração de **Runbooks DevOps**
- Suporte a **Terraform / Ansible**
- Histórico persistente entre sessões (banco de dados)
- Exportação de diagramas em PNG/SVG
- Suporte a múltiplos modelos de IA

---

## 👨‍💻 Autor

Projeto criado para auxiliar **operações de infraestrutura e DevOps** através de IA aplicada à administração de sistemas.

---

## 📜 Licença

Este projeto está licenciado sob a licença **MIT**.

---

## ⭐ Contribuições

Pull requests são bem-vindos. Se você trabalha com DevOps, SRE, Infraestrutura, Cloud ou Automação, sinta-se à vontade para contribuir.

---

## 🚀 OpsGuide

Um **copiloto de infraestrutura inteligente** para administradores de sistemas.
