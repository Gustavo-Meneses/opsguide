import streamlit as st
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Configuração da página
st.set_page_config(page_title="OpsGuide - Oracle Linux Assistant", page_icon="🐧")

# Estilização customizada
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stCodeBlock { border: 1px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

st.title("🐧 OpsGuide: Oracle Linux & DB Helper")
st.subheader("Seu assistente para comandos OL, Containers e pgAdmin")

# Sidebar para configuração da API
with st.sidebar:
    st.header("Configurações")
    api_key = st.text_input("Insira sua Mistral API Key", type="password")
    model = "mistral-tiny" # Modelo econômico e rápido para comandos

def generate_response(user_query):
    client = MistralClient(api_key=api_key)
    
    # System Prompt para garantir a "vibe" técnica e segura
    system_prompt = (
        "Você é um especialista em infraestrutura focado em Oracle Linux (todas as versões), "
        "Docker/Portainer e administração de PostgreSQL via pgAdmin. "
        "Sua tarefa é fornecer comandos precisos, explicações breves e avisos de segurança. "
        "Sempre use blocos de código para os comandos. "
        "Se o comando for perigoso (como rm -rf), adicione um aviso de atenção."
    )
    
    messages = [
        ChatMessage(role="system", content=system_prompt),
        ChatMessage(role="user", content=user_query)
    ]
    
    chat_response = client.chat(model=model, messages=messages)
    return chat_response.choices[0].message.content

# Interface de busca
query = st.text_input("O que você deseja fazer no servidor?", placeholder="Ex: Como liberar a porta 80 no firewall do Oracle Linux 8?")

if query:
    if not api_key:
        st.error("Por favor, insira a chave da API da Mistral na barra lateral.")
    else:
        with st.spinner("Consultando guia de Ops..."):
            try:
                response = generate_response(query)
                st.markdown(response)
            except Exception as e:
                st.error(f"Erro ao consultar a API: {e}")

# Rodapé instrutivo
st.divider()
st.caption("Focado em: Oracle Linux (yum/dnf), UEK, Portainer Stacks e pgAdmin Query Tool.")
