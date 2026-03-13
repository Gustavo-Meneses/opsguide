# 🖥️ OpsGuide Architect v8.5

Assistente DevOps interativo desenvolvido com **Streamlit** que utiliza **IA (Mistral API)** para ajudar administradores de sistemas a resolver problemas, gerar scripts e visualizar arquiteturas técnicas através de **diagramas Mermaid**.

O objetivo do projeto é fornecer um **copiloto para operações de infraestrutura**, auxiliando profissionais de **Linux, Windows Server, DevOps e SRE** com troubleshooting, automação e documentação técnica.

---

# 🚀 Funcionalidades

### 🤖 Assistente de Infraestrutura

* Chat interativo com IA especializada em ambientes de servidores.
* Respostas em **Português (PT-BR)**.
* Contexto ajustado automaticamente conforme plataforma selecionada.

### 🐧 Suporte a Linux

Ambientes suportados:

* Oracle Linux 9
* Oracle Linux 8
* Oracle Linux 7

Focos técnicos:

* Sistema / Kernel
* Docker / Portainer
* PostgreSQL

Scripts gerados em:

```
.sh
```

---

### 🪟 Suporte a Windows Server

Ambientes suportados:

* Windows Server 2022
* Windows Server 2019
* Windows Server 2016

Focos técnicos:

* PowerShell
* SQL Server
* Hyper-V
* Active Directory / Rede

Scripts gerados em:

```
.ps1
```

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

* Detecta o código
* Extrai o conteúdo
* Gera um botão para download

---

### 🚨 Modo de Emergência (Disaster Recovery)

Botão especial na interface que solicita à IA:

> comandos críticos de diagnóstico e recuperação para o ambiente selecionado.

Ideal para:

* incidentes de produção
* troubleshooting rápido
* resposta a falhas de infraestrutura

---

# 🧠 Arquitetura da Aplicação

```
Streamlit UI
     │
     │
     ▼
OpsGuide App
     │
     │ HTTP API
     ▼
Mistral AI (chat completions)
     │
     ▼
Resposta com:
 • explicação técnica
 • scripts
 • diagramas Mermaid
```

---

# 🛠️ Tecnologias Utilizadas

* **Python**
* **Streamlit**
* **Mistral AI API**
* **Mermaid.js**
* **Requests**
* **Regex Parsing**

---

# 📦 Instalação

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

# 🔑 Configuração da API

Crie um arquivo de secrets do Streamlit:

```
.streamlit/secrets.toml
```

Adicione sua chave da Mistral:

```toml
MISTRAL_API_KEY="SUA_API_KEY_AQUI"
```

---

# ▶️ Executando a aplicação

Execute:

```bash
streamlit run app.py
```

A interface abrirá automaticamente no navegador.

---

# 🖥️ Interface

A interface permite selecionar:

* Plataforma
* Versão do sistema operacional
* Área de foco técnico

Isso ajusta automaticamente o **prompt enviado para a IA**.

---

# 📁 Estrutura do Projeto

```
opsguide-architect
│
├── app.py
├── README.md
├── requirements.txt
│
└── .streamlit
    └── secrets.toml
```

---

# 🔐 Segurança

A comunicação com a IA é feita via **HTTP direto para a API da Mistral**, sem bibliotecas intermediárias.

Características:

* Streaming de resposta
* Timeout de segurança
* Tratamento de erros de rede
* Validação de status da API

---

# 📈 Possíveis Melhorias Futuras

* Upload de **logs para análise automática**
* Integração com **Kubernetes**
* Diagnóstico automático de infraestrutura
* Geração de **Runbooks DevOps**
* Suporte a **Terraform / Ansible**
* Histórico persistente de conversas
* Exportação de diagramas

---

# 👨‍💻 Autor

Projeto criado para auxiliar **operações de infraestrutura e DevOps** através de IA aplicada à administração de sistemas.

---

# 📜 Licença

Este projeto está licenciado sob a licença **MIT**.

---

# ⭐ Contribuições

Pull requests são bem-vindos.

Se você trabalha com:

* DevOps
* SRE
* Infraestrutura
* Cloud
* Automação

sinta-se à vontade para contribuir com melhorias.

---

# 🚀 OpsGuide

Um **copiloto de infraestrutura inteligente** para administradores de sistemas.
