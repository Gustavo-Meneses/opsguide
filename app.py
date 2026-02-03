import streamlit as st
from mistralai import Mistral

# --- Configuração da Página ---
st.set_page_config(
    page_title="OpsGuide - Multi-OS",
    page_icon="🖥️",
    layout="wide"
)

# --- Estilos CSS ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; }
    .stCodeBlock { border-left: 5px solid #0078D4; }
    </style>
    """, unsafe_allow_html=True)

# --- Gestão de Estado ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SEGURANÇA: Credenciais ---
api_key = st.secrets.get("MISTRAL_API_KEY")
if not api_key:
    st.error("⛔ Erro: MISTRAL_API_KEY não configurada nos secrets.")
    st.stop()

client = Mistral(api_key=api_key)
model = "mistral-tiny"

# --- Sidebar: Configuração de Contexto ---
with st.sidebar:
    st.title("🖥️ OpsGuide Hub")
    os_family = st.selectbox("Ecossistema:", ["🐧 Linux (Oracle)", "🪟 Windows Server"])
    st.divider()
    
    if os_family == "🐧 Linux (Oracle)":
        os_version = st.selectbox("Versão:", ["Oracle Linux 9", "Oracle Linux 8", "Oracle Linux 7"])
        tech_focus = st.radio("Foco:", ["OS / Kernel", "Docker / Portainer", "PostgreSQL / pgAdmin"])
        system_instruction = (
            f"Você é um SysAdmin Linux Sênior especialista em {os_version} e {tech_focus}. "
            "Priorize comandos dnf/yum e systemctl. Responda em PT-BR."
        )
    else:
        os_version = st.selectbox("Versão:", ["Windows Server 2022", "Windows Server 2019", "Windows Server 2016"])
        tech_focus = st.radio("Foco:", ["PowerShell / OS", "Hyper-V", "SQL Server", "Rede / Firewall", "AD / Task Scheduler"])
        # CORREÇÃO DO ERRO DE SINTAXE AQUI:
        system_instruction = (
            f"Você é um Administrador Windows Server Sênior especialista em {os_version} com foco em {tech_focus}. "
            "Priorize comandos PowerShell. Responda em PT-BR."
        )

# --- Interface Principal ---
st.title(f"Assistente {os_family}")

# Exibe histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input de Usuário
user_input = st.chat_input("Digite sua dúvida técnica...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Usando o método correto da versão v1.0+
            stream_response
