import streamlit as st
from mistralai import Mistral
import streamlit.components.v1 as components

# --- Configuração de Página ---
st.set_page_config(
    page_title="OpsGuide Architect v6.0",
    page_icon="🖥️",
    layout="wide"
)

# --- Estilos Customizados ---
st.markdown("""
    <style>
    .stDownloadButton>button { width: 100%; background-color: #2e7d32; color: white; }
    .stCodeBlock { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- Função Mermaid com Paleta Dinâmica ---
def render_mermaid(code, os_family):
    primary = "#f05a28" if "Linux" in os_family else "#0078d4"
    text_color = "#ffffff" if "Linux" in os_family else "#000000"
    secondary = "#313131" if "Linux" in os_family else "#ffffff"

    components.html(
        f"""
        <div class="mermaid" style="display: flex; justify-content: center;">
            {code}
        </div>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ 
                startOnLoad: true, 
                theme: 'base',
                themeVariables: {{
                    'primaryColor': '{primary}',
                    'primaryTextColor': '{text_color}',
                    'primaryBorderColor': '#444',
                    'lineColor': '{primary}',
                    'tertiaryColor': '#222'
                }}
            }});
        </script>
        """,
        height=450,
    )

# --- Gestão de Estado ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Segurança ---
api_key = st.secrets.get("MISTRAL_API_KEY")
if not api_key:
    st.error("⛔ Configure a MISTRAL_API_KEY nos Secrets.")
    st.stop()

client = Mistral(api_key=api_key)

# --- Sidebar ---
with st.sidebar:
    st.title("🖥️ OpsGuide Hub")
    os_family = st.selectbox("Plataforma:", ["🐧 Linux (Oracle)", "🪟 Windows Server"])
    st.divider()
    
    if os_family == "🐧 Linux (Oracle)":
        os_ver = st.selectbox("Versão:", ["Oracle Linux 9", "Oracle Linux 8", "Oracle Linux 7"])
        focus = st.radio("Foco:", ["Sistema/Kernel", "Docker/Portainer", "PostgreSQL"])
        ext = ".sh"
        sys_msg = f"Especialista {os_ver}. Use Bash/DNF. Responda em PT-BR. Use Mermaid.js para diagramas (graph TD/LR)."
    else:
        os_ver = st.selectbox("Versão:", ["Windows Server 2022", "2019", "2016"])
        focus = st.radio("Foco:", ["PowerShell", "SQL Server", "Hyper-V", "AD/Rede"])
        ext = ".ps1"
        sys_msg = f"Especialista {os_ver}. Use PowerShell. Responda em PT-BR. Use Mermaid.js para diagramas (graph TD/LR)."

# --- Chat Principal ---
st.title(f"Assistente {os_family}")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m["role"] == "assistant" and "```mermaid" in m["content"]:
            mermaid_code = m["content"].split("```mermaid")[-1].split("```")[0]
            render_mermaid(mermaid_code, os_family)

if prompt := st.chat_input("Ex: Como configurar um Proxy Reverso Nginx?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        resp_container = st.empty()
        full_resp = ""
        
        try:
            stream = client.chat.stream(
                model="mistral-tiny",
                messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": prompt}]
            )
            
            for chunk in stream:
                if chunk.data.choices[0].delta.content:
                    full_resp += chunk.data.choices[0].delta.content
                    resp_container.markdown(full_resp + "▌")
            
            resp_container.markdown(full_resp)
            
            # --- Renderização Visual ---
            if "```mermaid" in full_resp:
                mermaid_code = full_resp.split("```mermaid")[-1].split("```")[0]
                render_mermaid(mermaid_code, os_family)
            
            # --- Funcionalidade de Download (Otimização) ---
            if "```" in full_resp:
                script_content = full_resp.split("```")[1].split("```")[0] # Pega o primeiro bloco de código
                st.download_button(
                    label=f"📥 Baixar Script Automático ({ext})",
                    data=script_content,
                    file_name=f"opsguide_script{ext}",
                    mime="text/plain"
                )
                    
            st.session_state.messages.append({"role": "assistant", "content": full_resp})
            
        except Exception as e:
            st.error(f"Erro: {str(e)}")
