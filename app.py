import streamlit as st
from mistralai import Mistral

# --- Configuração de Página ---
st.set_page_config(page_title="OpsGuide - Multi-OS", page_icon="🖥️", layout="wide")

# --- Estado da Sessão ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Segurança: API Key ---
api_key = st.secrets.get("MISTRAL_API_KEY")
if not api_key:
    st.error("⛔ Configure a MISTRAL_API_KEY nos Secrets do Streamlit.")
    st.stop()

client = Mistral(api_key=api_key)

# --- Sidebar: Filtros de Contexto ---
with st.sidebar:
    st.title("🖥️ OpsGuide Hub")
    os_family = st.selectbox("Sistema Operacional:", ["🐧 Linux (Oracle)", "🪟 Windows Server"])
    
    if os_family == "🐧 Linux (Oracle)":
        os_ver = st.selectbox("Versão:", ["Oracle Linux 9", "Oracle Linux 8", "Oracle Linux 7"])
        focus = st.radio("Foco:", ["Sistema/Kernel", "Docker/Portainer", "PostgreSQL"])
        # String limpa para evitar SyntaxError
        sys_msg = f"Você é um SysAdmin Linux especialista em {os_ver}. Foco em {focus}. Use comandos Bash/DNF. Responda em PT-BR."
    else:
        os_ver = st.selectbox("Versão:", ["Windows Server 2022", "2019", "2016"])
        focus = st.radio("Foco:", ["PowerShell", "SQL Server", "Hyper-V", "Rede/Firewall"])
        # String limpa para evitar SyntaxError
        sys_msg = f"Você é um Admin Windows especialista em {os_ver}. Foco em {focus}. Use PowerShell. Responda em PT-BR."

# --- Interface Principal ---
st.title(f"Assistente {os_family}")

# Mostrar Histórico
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Input do Usuário
if prompt := st.chat_input("Como posso ajudar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        resp_container = st.empty()
        full_resp = ""
        
        try:
            # Novo método de streaming da SDK 1.0+
            stream = client.chat.stream(
                model="mistral-tiny",
                messages=[
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": prompt}
                ]
            )
            
            for chunk in stream:
                if chunk.data.choices[0].delta.content:
                    full_resp += chunk.data.choices[0].delta.content
                    resp_container.markdown(full_resp + "▌")
            
            resp_container.markdown(full_resp)
            st.session_state.messages.append({"role": "assistant", "content": full_resp})
            
        except Exception as e:
            st.error(f"Erro na IA: {str(e)}")
