import streamlit as st
from mistralai import Mistral
import streamlit.components.v1 as components

# --- Configuração de Página ---
st.set_page_config(
    page_title="OpsGuide - Architect v5.0",
    page_icon="🖥️",
    layout="wide"
)

# --- Função para Renderizar Diagramas Mermaid com Paleta Dinâmica ---
def render_mermaid(code, os_family):
    # Define cores baseadas no SO
    if "Linux" in os_family:
        primary = "#f05a28"  # Laranja Oracle
        secondary = "#313131"
        text_color = "#ffffff"
    else:
        primary = "#0078d4"  # Azul Microsoft
        secondary = "#ffffff"
        text_color = "#000000"

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
                    'primaryBorderColor': '{secondary}',
                    'lineColor': '{primary}',
                    'secondaryColor': '{secondary}',
                    'tertiaryColor': '#f4f4f4'
                }}
            }});
        </script>
        """,
        height=450,
    )

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
    st.divider()
    
    if os_family == "🐧 Linux (Oracle)":
        os_ver = st.selectbox("Versão:", ["Oracle Linux 9", "Oracle Linux 8", "Oracle Linux 7"])
        focus = st.radio("Foco:", ["Sistema/Kernel", "Docker/Portainer", "PostgreSQL"])
        sys_msg = (
            f"Você é um SysAdmin Linux especialista em {os_ver}. Foco em {focus}. "
            "Use comandos Bash/DNF. Responda em PT-BR. "
            "Sempre inclua um bloco '```mermaid' com 'graph TD' ou 'graph LR' para ilustrar a arquitetura. "
            "Não use subgraphs a menos que seja estritamente necessário."
        )
    else:
        os_ver = st.selectbox("Versão:", ["Windows Server 2022", "2019", "2016"])
        focus = st.radio("Foco:", ["PowerShell", "SQL Server", "Hyper-V", "Rede/Firewall"])
        sys_msg = (
            f"Você é um Admin Windows especialista em {os_ver}. Foco em {focus}. "
            "Use PowerShell. Responda em PT-BR. "
            "Sempre inclua um bloco '```mermaid' com 'graph TD' ou 'graph LR' para ilustrar a arquitetura. "
            "Foque em componentes do Windows como AD, IIS e Hyper-V."
        )

# --- Interface Principal ---
st.title(f"Assistente {os_family}")
st.caption(f"Contexto Ativo: {os_ver} | Paleta: {'Laranja/Oracle' if 'Linux' in os_family else 'Azul/Microsoft'}")

# Mostrar Histórico
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m["role"] == "assistant" and "```mermaid" in m["content"]:
            try:
                mermaid_code = m["content"].split("```mermaid")[-1].split("```")[0]
                render_mermaid(mermaid_code, os_family)
            except:
                pass

# Input do Usuário
if prompt := st.chat_input("Ex: Como configurar um Proxy Reverso Nginx para Docker?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        resp_container = st.empty()
        full_resp = ""
        
        try:
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
            
            if "```mermaid" in full_resp:
                try:
                    mermaid_code = full_resp.split("```mermaid")[-1].split("```")[0]
                    render_mermaid(mermaid_code, os_family)
                except:
                    pass
                    
            st.session_state.messages.append({"role": "assistant", "content": full_resp})
            
        except Exception as e:
            st.error(f"Erro na IA: {str(e)}")

st.divider()
st.caption("🚀 OpsGuide v5.0 - Arquiteturas Híbridas Colorizadas.")
