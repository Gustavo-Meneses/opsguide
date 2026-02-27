import streamlit as st
from mistralai import Mistral
import streamlit.components.v1 as components
import re

# --- Configuração de Página ---
st.set_page_config(
    page_title="OpsGuide Architect v7.0",
    page_icon="🖥️",
    layout="wide"
)

# --- Estilos Customizados ---
st.markdown("""
    <style>
    .stDownloadButton>button { width: 100%; background-color: #2e7d32; color: white; border-radius: 8px; }
    .emergency-btn>button { background-color: #d32f2f !important; color: white !important; }
    .stCodeBlock { border-radius: 10px; border-left: 5px solid #f05a28; }
    </style>
    """, unsafe_allow_html=True)

# --- Função Mermaid Blindada ---
def render_mermaid(code, os_family):
    # Limpeza básica para evitar erros de sintaxe comuns da IA
    clean_code = code.replace("`", "").strip()
    
    primary = "#f05a28" if "Linux" in os_family else "#0078d4"
    text_color = "#ffffff" if "Linux" in os_family else "#000000"
    secondary = "#313131" if "Linux" in os_family else "#ffffff"

    components.html(
        f"""
        <div class="mermaid" style="display: flex; justify-content: center;">
            {clean_code}
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
                    'fontFamily': 'arial'
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
        ext, lang = ".sh", "bash"
    else:
        os_ver = st.selectbox("Versão:", ["Windows Server 2022", "2019", "2016"])
        focus = st.radio("Foco:", ["PowerShell", "SQL Server", "Hyper-V", "AD/Rede"])
        ext, lang = ".ps1", "powershell"

    st.divider()
    st.subheader("🆘 Modo de Emergência")
    if st.button("🚨 Comandos de DR", use_container_width=True):
        emergency_prompt = "Quais os comandos de emergência para recuperação de desastres (DR) e troubleshooting de rede neste SO?"
        st.session_state.messages.append({"role": "user", "content": emergency_prompt})
        # O processamento ocorrerá no bloco principal abaixo

# --- Sistema de Mensagem do Sistema ---
sys_msg = (
    f"Você é um especialista em {os_ver}. Foco: {focus}. "
    f"Responda em PT-BR. Sempre que possível, inclua um diagrama 'graph TD' ou 'graph LR' "
    "dentro de um bloco ```mermaid. IMPORTANTE: Evite caracteres especiais como parênteses ou "
    "pontos dentro dos nós do diagrama para não quebrar a sintaxe Mermaid."
)

# --- Interface Principal ---
st.title(f"Assistente {os_family}")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m["role"] == "assistant" and "```mermaid" in m["content"]:
            m_code = m["content"].split("```mermaid")[-1].split("```")[0]
            render_mermaid(m_code, os_family)

# Processar Input
user_input = st.chat_input("Ex: Como configurar um Proxy Reverso Nginx?")
if user_input or (len(st.session_state.messages) > 0 and st.session_state.messages[-1]["content"].startswith("Quais os comandos de emergência")):
    
    actual_prompt = user_input if user_input else st.session_state.messages[-1]["content"]
    
    if user_input: # Se veio do input, adiciona. Se veio do botão DR, já foi adicionado.
        st.session_state.messages.append({"role": "user", "content": actual_prompt})
        with st.chat_message("user"):
            st.markdown(actual_prompt)

    with st.chat_message("assistant"):
        resp_container = st.empty()
        full_resp = ""
        
        try:
            stream = client.chat.stream(
                model="mistral-tiny",
                messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": actual_prompt}]
            )
            
            for chunk in stream:
                if chunk.data.choices[0].delta.content:
                    full_resp += chunk.data.choices[0].delta.content
                    resp_container.markdown(full_resp + "▌")
            
            resp_container.markdown(full_resp)
            
            # Renderização de Diagrama
            if "```mermaid" in full_resp:
                m_code = full_resp.split("```mermaid")[-1].split("```")[0]
                render_mermaid(m_code, os_family)
            
            # Exportação de Script
            if "```" in full_resp:
                code_blocks = re.findall(r'```(?:\w+)?\n(.*?)\n```', full_resp, re.DOTALL)
                if code_blocks:
                    st.download_button(
                        label=f"📥 Baixar Script de Solução ({ext})",
                        data=code_blocks[0],
                        file_name=f"opsguide_solucao{ext}",
                        mime="text/plain"
                    )
            
            st.session_state.messages.append({"role": "assistant", "content": full_resp})
            
        except Exception as e:
            st.error(f"Erro na IA: {str(e)}")
