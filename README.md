# 🐧 OpsGuide - Assistente de Infraestrutura

Este é um portal de pesquisa inteligente desenvolvido para auxiliar colaboradores com pouca experiência em ambientes **Oracle Linux**, **Containers (Portainer)** e **Bancos de Dados (pgAdmin/PostgreSQL)**.

A ferramenta utiliza a inteligência artificial da **Mistral AI** para converter perguntas em linguagem natural em comandos técnicos precisos.

## 🚀 Tecnologias Utilizadas

* **Python 3.9+**
* **Streamlit**: Para a interface web rápida.
* **Mistral AI API**: Como motor de processamento de linguagem natural.
* **Oracle Linux Context**: Otimizado para comandos `dnf`, `yum`, `nmcli`, `firewall-cmd` e gestão de kernel UEK.

## 🛠️ Como Instalar e Rodar

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/ops-guide.git](https://github.com/seu-usuario/ops-guide.git)
    cd ops-guide
    ```

2.  **Crie um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install streamlit mistralai
    ```

4.  **Execute a aplicação:**
    ```bash
    streamlit run app.py
    ```

## 📋 Requisitos de Uso

* Uma **API Key** válida da Mistral AI (obtenha em [console.mistral.ai](https://console.mistral.ai/)).
* Acesso à internet para consultas à API.

## 💡 Exemplos de Pesquisa
* *"Como verificar o log do kernel no Oracle Linux 9?"*
* *"Criar uma stack de container no Portainer para Nginx."*
* *"Como resetar a senha de um usuário no pgAdmin?"*
