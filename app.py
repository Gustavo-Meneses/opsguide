import streamlit as st
from mistralai import Mistral

# --- Configuração da Página ---
st.set_page_config(
    page_title="OpsGuide - Multi-OS",
    page_icon="🖥️",
    layout="wide"
)

# --- Gestão de Estado (Para não perder o chat ao clicar) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SEGURANÇA: Chave da API ---
api_key = st.secrets.get("MISTRAL_API_KEY")

if not api_key:
    st.error("⛔ Chave 'MISTRAL_API_KEY' não encontrada nos Secrets do Streamlit.")
    st.stop()

# Inicialização do Cliente
client = Mistral(api_key=api_key)
model = "mistral-tiny"

# --- Sidebar: Configuração de Contexto ---
with st.sidebar:
    st.title("🖥️ OpsGuide Hub")
    os_family = st.selectbox("Plataforma:", ["🐧 Linux (Oracle)", "🪟 Windows Server"])
    st.divider()
    
    if os_family == "🐧 Linux (Oracle)":
        os_version = st.selectbox("Versão:", ["Oracle Linux 9", "Oracle Linux 8", "Oracle Linux 7"])
        tech_focus = st.radio("Foco:", ["OS / Kernel", "Docker / Portainer", "PostgreSQL / pgAdmin"])
        system_instruction = (
            f"Você é um SysAdmin Linux Sênior especialista em {os_version} e {tech_focus}. "
            "Forneça comandos precisos (dnf/yum). Responda em Português do Brasil."
        )
    else:
        os_version = st.selectbox("Versão:", ["Windows Server 2022", "Windows Server 2019", "Windows Server 2016"])
        tech_focus = st.radio("Foco:", ["PowerShell / OS", "Hyper-V", "SQL Server", "Rede / Firewall", "AD / Task Scheduler"])
        system_instruction = (
            f"Você é um Administrador Windows Server Sênior especialista em {os_version} com foco em {tech_focus}. "
            "Priorize scripts PowerShell. Responda em Português do Brasil."
        )

# --- Interface Principal ---
st.title(f"Assistente {os_family}")
st.caption(f"Contexto: {os_version} | Foco: {tech_focus}")

# Exibir histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de Input
user_input = st.chat_input("Como posso ajudar hoje?")

if
