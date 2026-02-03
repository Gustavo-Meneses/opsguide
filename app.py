import streamlit as st
from mistralai import Mistral
import time

# --- Configuração da Página ---
st.set_page_config(
    page_title="OpsGuide - Multi-OS Assistant",
    page_icon="🖥️",
    layout="wide"
)

# --- Estilos CSS (Adaptação Visual) ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    /* Diferenciação visual sutil para blocos de código */
    .stCodeBlock { border-left: 5px solid #0078D4; } /* Azul Microsoft */
    </style>
    """, unsafe_allow_html=True)

# --- Gestão de Estado ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SEGURANÇA: Credenciais ---
api_key = st.secrets.get("MISTRAL_API_KEY")
if not api_key:
    st.error("⛔ Erro Crítico: MISTRAL_API_KEY não configurada nos secrets.")
    st.stop()

client = Mistral(api_key=api_key)
model = "mistral-tiny"

# --- Sidebar: Seletor de Ecossistema ---
with st.sidebar:
    st.title("🖥️ OpsGuide Hub")
    
    # O Grande Filtro: Linux ou Windows
    os_family = st.selectbox(
        "Selecione o Ecossistema:",
        ["🐧 Linux (Oracle)", "🪟 Windows Server"],
        index=0
    )
    
    st.markdown("---")
    
    # Lógica Dinâmica baseada na Família do OS
    if os_family == "🐧 Linux (Oracle)":
        os_version = st.selectbox("Versão:", ["Oracle Linux 9 (UEK R7)", "Oracle Linux 8", "Oracle Linux 7"])
        tech_focus = st.radio("Foco:", ["OS / Kernel", "Docker / Portainer", "PostgreSQL / pgAdmin"])
        
        st.caption("Ações Rápidas (Linux):")
        col1, col2 = st.columns(2)
        if col1.button("🔥 Firewall"):
            st.session_state.prompt_input = f"Listar regras ativas no firewall-cmd para {os_version}."
        if col2.button("🐳 Logs"):
            st.session_state.prompt_input = "Como ver logs de um container Docker em tempo real?"

    else: # Windows Server
        os_version = st.selectbox("Versão:", ["Windows Server 2022", "Windows Server 2019", "Windows Server 2016"])
        tech_focus = st.radio("Foco:", ["PowerShell / OS", "Hyper-V / Virtualização", "SQL Server / DB", "Rede / Firewall", "AD / Task Scheduler"])
        
        st.caption("Ações Rápidas (Windows):")
        col1, col2 = st.columns(2)
        if col1.button("🛡️ Firewall Rules"):
            st.session_state.prompt_input = "PowerShell para listar regras de firewall bloqueando a porta 80 ou 443."
        if col2.button("⚙️ Serviços"):
            st.session_state.prompt_input = "PowerShell para listar serviços parados (Stopped) que deveriam ser automáticos."
        if st.button("📅 Agendador"):
            st.session_state.prompt_input = "Como criar uma tarefa agendada via PowerShell que roda um script .ps1 todo dia às 8h?"

# --- Lógica de Prompt do Sistema (A "Personalidade") ---
if os_family == "🐧 Linux (Oracle)":
    system_instruction = (
        f"Você é um SysAdmin Linux Sênior especialista em {os_version} e {tech_focus}. "
        "Regras: "
        "1. Priorize comandos 'dnf'/'yum' e 'systemctl'. "
        "2. Para Docker, use CLI. Para pgAdmin, foque em configuração. "
        "3. Responda em PT-BR. Use Markdown para código."
    )
else:
    system_instruction = (
        f"Você é um Administrador Windows Server Sênior especialista em {os_version} com
