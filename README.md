# 🖥️ OpsGuide - Multi-OS Architect & Copilot

O **OpsGuide** é um assistente avançado de infraestrutura que une a precisão dos comandos de terminal (Linux/Windows) com a clareza de diagramas de arquitetura gerados em tempo real.

## ✨ Diferenciais da Versão 4.0

* **Visualização de Arquitetura (Fator Uau):** Agora o assistente não apenas fala o que fazer, mas **desenha** a solução utilizando diagramas **Mermaid.js**. Ideal para entender topologias de rede, containers Docker e switches de Hyper-V.
* **Inteligência Contextual:** Respostas calibradas para as nuances entre as versões do Oracle Linux (7, 8, 9) e Windows Server (2016 a 2022).
* **Hardening de Segurança:** Proteção nativa de credenciais via Streamlit Secrets. Sem inputs de chaves na interface.
* **Streaming de Resposta:** Feedback visual imediato durante a geração de scripts complexos.

## 🛠️ Tecnologias Utilizadas
- **Mistral AI:** Core de processamento de linguagem natural.
- **Streamlit:** Interface web reativa.
- **Mermaid.js:** Motor de renderização de diagramas de infraestrutura.
- **Python:** Backend da aplicação.

## 🚀 Como Iniciar

1. **Instale os requisitos:**
   ```bash
   pip install streamlit mistralai
Configure os Segredos (.streamlit/secrets.toml):

Isto, TOML
MISTRAL_API_KEY = "sua_chave_mistral_aqui"
Inicie o Assistente:

Bash
streamlit run app.py
📊 Exemplos de Teste
Linux: "Como configurar um Proxy Reverso Nginx para um container Docker?" (Gera diagrama de tráfego).

Windows: "Como montar um Cluster de SQL Server simples?" (Gera diagrama de nós/storage).
