import streamlit as st
import re
import streamlit.components.v1 as components

# --- Configuração de Página ---
st.set_page_config(page_title="OpsGuide Architect v7.6", page_icon="🖥️", layout="wide")

# --- 🛡️ Gestão de Versão Híbrida ---
# Tenta carregar a biblioteca de forma dinâmica para evitar erros de importação estática
MISTRAL_MODE = None

try:
    import mistralai
    # Verifica se a classe Mistral (v1.x) existe
    if hasattr(mistralai, "Mistral"):
        from mistralai import Mistral
        MISTRAL_MODE = "v1"
    # Senão, tenta a estrutura antiga (v0.x)
    elif hasattr(mistralai, "client") and hasattr(mistralai.client, "MistralClient"):
        from mistralai.client import MistralClient
        from mistralai.models.chat_completion import ChatMessage
        MISTRAL_MODE = "v0"
except Exception:
    pass

if not MISTRAL_MODE:
    st.error("🚨 Falha crítica: O ambiente do Streamlit não carregou a SDK da Mistral corretamente.")
    st.info("Certifique-se de que 'mistralai' está no seu 'requirements.txt' e faça um 'Reboot' no painel 'Manage App'.")
    st.stop()

st.markdown("""
    <style>
    .stDownloadButton>button { width: 100%; background-color: #2e7d32; color: white; border-radius: 8px; font-weight: bold; }
    .stCodeBlock { border-radius: 10px; border-left: 5px solid #f05a28; }
    </style>
    """, unsafe_allow_html=True)

def render_mermaid(code, os_family):
    clean_code = code.replace("`", "").strip()
    primary = "#f05a28" if "Linux" in os_family else "#0078d4"
    text_color = "#ffffff" if "Linux" in os_family else "#000000"
    components.html(
        f"""
        <div class="mermaid" style="display: flex; justify-content: center;">{clean_code}</div>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ 
                startOnLoad: true, 
                theme: 'base', 
                themeVariables: {{ 'primaryColor': '{primary}', 'primaryTextColor': '{text_color}', 'lineColor': '{primary}' }} 
            }});
        </script>
        """, height=450)

if "messages" not in st.session_state: 
    st.session_state.messages = []

# Autenticação via Secrets
api_key = st.secrets.get("MISTRAL_API_KEY")
if not api_key:
    st.error("⛔ Configure a MISTRAL_API_KEY nos Secrets do Streamlit.")
    st.stop()

# Inicialização do Cliente conforme a versão detectada
try:
    if MISTRAL_MODE == "v1":
        client = Mistral(api_key=api_key)
    else:
        client = MistralClient(api_key=api_key)
except Exception as e:
    st.error(f"Erro ao inicializar cliente Mistral: {e}")
    st.stop()

with st.sidebar:
    st.title("🖥️ OpsGuide Hub")
    st.caption(f"Versão da Engine: {MISTRAL_MODE}")
        
    os_family = st.selectbox("Plataforma:", ["🐧 Linux (Oracle)", "🪟 Windows Server"])
    if os_family == "🐧 Linux (Oracle)":
        os_ver = st.selectbox("Versão:", ["Oracle Linux 9", "Oracle Linux 8", "Oracle Linux 7"])
        focus = st.radio("Foco:", ["Sistema/Kernel", "Docker/Portainer", "PostgreSQL"])
        ext = ".sh"
    else:
        os_ver = st.selectbox("Versão:", ["Windows Server 2022", "2019", "2016"])
        focus = st.radio("Foco:", ["PowerShell", "SQL Server", "Hyper-V", "AD/Rede"])
        ext = ".ps1"
    
    st.divider()
    if st.button("🚨 MODO DE EMERGÊNCIA (DR)", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Apresente comandos de emergência e troubleshooting."})

sys_msg = f"Especialista em {os_ver}. Foco: {focus}. PT-BR. Use Mermaid.js (graph TD/LR) para diagramas técnicos."

st.title(f"Assistente {os_family}")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m["role"] == "assistant" and "```mermaid" in m["content"]:
            render_mermaid(m["content"].split("```mermaid")[-1].split("```")[0], os_family)

if prompt := st.chat_input("Ex: Como analisar os logs do Nginx?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        resp_container = st.empty()
        full_resp = ""
        try:
            if MISTRAL_MODE == "v1":
                stream = client.chat.stream(
                    model="mistral-tiny", 
                    messages=[{"role":"system","content":sys_msg},{"role":"user","content":prompt}]
                )
                for chunk in stream:
                    if chunk.data.choices[0].delta.content:
                        full_resp += chunk.data.choices[0].delta.content
                        resp_container.markdown(full_resp + "▌")
            else:
                messages = [
                    ChatMessage(role="system", content=sys_msg),
                    ChatMessage(role="user", content=prompt)
                ]
                stream = client.chat_stream(model="mistral-tiny", messages=messages)
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_resp += chunk.choices[0].delta.content
                        resp_container.markdown(full_resp + "▌")
            
            resp_container.markdown(full_resp)
            
            if "```mermaid" in full_resp:
                render_mermaid(full_resp.split("```mermaid")[-1].split("```")[0], os_family)
            
            code_match = re.search(r'
