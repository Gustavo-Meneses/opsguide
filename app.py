import streamlit as st
from mistralai import Mistral
import streamlit.components.v1 as components

# --- Configuração de Página ---
st.set_page_config(
    page_title="OpsGuide - Multi-OS Architect",
    page_icon="🖥️",
    layout="wide"
)

# --- Função para Renderizar Diagramas Mermaid ---
def render_mermaid(code):
    components.html(
        f"""
        <div class="mermaid" style="display: flex; justify-content: center;">
            {code}
        </div>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
        </script>
        """,
        height=400,
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
            "Sempre que explicar fluxos de rede, docker ou serviços, inclua um bloco de código Mermaid.js "
            "iniciando com 'graph TD' ou 'graph LR' para ilustrar a arquitetura visualmente."
        )
    else:
        os_ver = st.selectbox("Versão:", ["Windows Server 2022", "2019", "2016"])
        focus = st.radio("Foco:", ["PowerShell", "SQL Server", "Hyper-V", "Rede/Firewall"])
        sys_msg = (
            f"Você é um Admin Windows especialista em {os_ver}. Foco em {focus}. "
            "Use PowerShell. Responda em PT-BR. "
            "Sempre que explicar topologias de rede, Hyper-V ou clusters de SQL, inclua um bloco de código "
            "Mermaid.js iniciando com 'graph TD' ou 'graph LR' para ilustrar a arquitetura visualmente."
        )

# --- Interface Principal ---
st.title(f"Assistente {os_family}")
st.caption(f"Contexto: {os_ver} | Foco: {focus}")

# Mostrar Histórico
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        # Se houver código mermaid na mensagem da IA, tenta renderizar
        if m["role"] == "assistant" and "graph " in m["content"]:
            try:
                # Extrai o bloco mermaid simples (melhorado em produção com regex)
                mermaid_code = m["content"].split("```mermaid")[-1].split("```")[0]
                render_mermaid(mermaid_code)
            except:
                pass

# Input do Usuário
if prompt := st.chat_input("Como posso ajudar?"):
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
            
            # Se a resposta contém diagrama, renderiza após o texto
            if "graph " in full_resp:
                try:
                    mermaid_code = full_resp.split("```mermaid")[-1].split("```")[0]
                    render_mermaid(mermaid_code)
                except:
                    pass
                    
            st.session_state.messages.append({"role": "assistant", "content": full_resp})
            
        except Exception as e:
            st.error(f"Erro na IA: {str(e)}")

st.divider()
st.caption("🚀 OpsGuide v4.0 - Gerando comandos e arquiteturas visuais.")
