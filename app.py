import streamlit as st
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Configuração da página
st.set_page_config(page_title="OpsGuide - Oracle Linux Assistant", page_icon="🐧")

# --- Lógica de Secrets ---
# Tenta pegar a chave do st.secrets, se não existir, fica em branco
if "MISTRAL_API_KEY" in st.secrets:
    default_api_key = st.secrets["MISTRAL_API_KEY"]
else:
    default_api_key = ""

# Estilização customizada
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stCodeBlock { border: 1px solid #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

st.title("🐧 OpsGuide: Oracle Linux & DB Helper")

# Sidebar para configuração da API
with st.sidebar:
    st.header("Configurações")
    # Se a chave já veio do secrets, o campo já inicia preenchido
    api_key = st.text_input("Mistral API Key", value=default_api_key, type="password")
    model = "mistral-tiny"

def generate_response(user_query):
    client = MistralClient(api_key=api_key)
    
    system_prompt = (
        "Você é um especialista em infraestrutura focado em Oracle Linux (todas as versões), "
        "Docker/Portainer e administração de PostgreSQL via pgAdmin. "
        "Sua tarefa é fornecer comandos precisos, explicações breves e avisos de segurança. "
        "Responda sempre em Português do Brasil."
    )
    
    messages = [
        ChatMessage(role="system", content=system_prompt),
        ChatMessage(role="user", content=user_query)
    ]
    
    chat_response = client.chat(model=model, messages=messages)
    return chat_response.choices[0].message.content

# Interface de busca
query = st.text_input("O que você deseja fazer no servidor?", placeholder="Ex: Como atualizar o kernel no Oracle Linux 8?")

if query:
    if not api_key:
        st.error("Chave da API não encontrada. Configure no arquivo secrets ou insira na barra lateral.")
    else:
        with st.spinner("Consultando guia de Ops..."):
            try:
                response = generate_response(query)
                st.markdown(response)
            except Exception as e:
                st.error(f"Erro ao consultar a API: {e}")

st.divider()
st.caption("Focado em: Oracle Linux (yum/dnf), UEK, Portainer e pgAdmin.")
