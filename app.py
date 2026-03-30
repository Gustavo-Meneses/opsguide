import streamlit as st
import streamlit.components.v1 as components

from core.llm import call_mistral_api, stream_response
from core.rag import load_knowledge_base, simple_similarity_search
from core.parser import extract_code, extract_mermaid

# ── Configuração de Página ────────────────────────────────────────────────────
st.set_page_config(page_title="OpsGuide Architect v9.0", page_icon="🖥️", layout="wide")

# ── Estilos ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.stDownloadButton>button {
    width: 100%;
    background-color: #2e7d32;
    color: white;
    border-radius: 8px;
    font-weight: bold;
}
.stCodeBlock {
    border-radius: 10px;
    border-left: 5px solid #f05a28;
}
div[data-testid="stSidebarContent"] .stButton:last-of-type > button {
    background-color: #b71c1c;
    color: white;
    border-radius: 8px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────
def render_mermaid(code: str, os_family: str) -> None:
    """Renderiza um diagrama Mermaid.js inline via HTML."""
    try:
        clean_code = code.replace("`", "").strip()
        if not clean_code.startswith(("graph", "flowchart")):
            clean_code = "graph TD\n" + clean_code

        primary = "#f05a28" if "Linux" in os_family else "#0078d4"
        text_color = "#ffffff" if "Linux" in os_family else "#000000"

        components.html(
            f"""
            <div class="mermaid" style="display:flex;justify-content:center;">{clean_code}</div>
            <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{
                startOnLoad: true,
                theme: 'base',
                themeVariables: {{
                    'primaryColor': '{primary}',
                    'primaryTextColor': '{text_color}',
                    'lineColor': '{primary}'
                }}
            }});
            </script>
            """,
            height=450,
        )
    except Exception:
        pass


def build_enhanced_prompt(pending_prompt: str, knowledge_base: list) -> str:
    """
    Enriquece o prompt do usuário com contexto da base interna (RAG).
    Se a KB estiver vazia, devolve o prompt original sem alteração.
    """
    rag_context = simple_similarity_search(pending_prompt, knowledge_base)

    if not rag_context:
        return pending_prompt

    context_text = "\n\n".join(rag_context)
    return (
        f"Contexto adicional (base interna):\n{context_text}\n\n"
        f"Pergunta:\n{pending_prompt}"
    )


# ── Inicialização do Estado ───────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "emergency_triggered" not in st.session_state:
    st.session_state.emergency_triggered = False

# ── Carregamento da Base de Conhecimento (uma vez por sessão) ─────────────────
if "knowledge_base" not in st.session_state:
    st.session_state.knowledge_base = load_knowledge_base("data/base_conhecimento.txt")

knowledge_base: list = st.session_state.knowledge_base

# ── Validação da API Key ──────────────────────────────────────────────────────
if not st.secrets.get("MISTRAL_API_KEY"):
    st.error("⛔ Configure a MISTRAL_API_KEY nos Secrets do Streamlit (Settings > Secrets).")
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🖥️ OpsGuide Hub")
    st.success("API Engine: RAG + Direct HTTP v9.0", icon="🚀")

    if knowledge_base:
        st.info(f"📚 KB carregada: {len(knowledge_base)} chunks", icon="🗂️")
    else:
        st.warning("KB vazia — adicione conteúdo em data/base_conhecimento.txt", icon="📂")

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
        st.session_state.emergency_triggered = True

    if st.button("🗑️ Limpar Histórico", use_container_width=True):
        st.session_state.messages = []
        st.session_state.emergency_triggered = False
        st.rerun()

# ── System Prompt Dinâmico ────────────────────────────────────────────────────
sys_msg = (
    f"Você é um especialista em {os_ver}. Foco: {focus}. "
    "Responda em PT-BR. "
    "Sempre use Mermaid.js (graph TD) para diagramas técnicos quando explicar processos. "
    "Quando gerar scripts, coloque-os dentro de blocos de código com a linguagem correta "
    "(bash ou powershell)."
)

# ── Título Principal ──────────────────────────────────────────────────────────
st.title(f"Assistente {os_family}")

# ── Exibição do Histórico ─────────────────────────────────────────────────────
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m["role"] == "assistant":
            mermaid_code = extract_mermaid(m["content"])
            if mermaid_code:
                render_mermaid(mermaid_code, os_family)

# ── Resolução do Prompt Pendente ──────────────────────────────────────────────
pending_prompt: str | None = None

if st.session_state.emergency_triggered:
    st.session_state.emergency_triggered = False  # reseta antes de processar
    pending_prompt = (
        "Apresente comandos de emergência e troubleshooting críticos para este ambiente."
    )
elif prompt := st.chat_input("Como posso ajudar na sua infraestrutura?"):
    pending_prompt = prompt

# ── Processamento da Mensagem ─────────────────────────────────────────────────
if pending_prompt:
    # 1. Enriquecer com RAG
    enhanced_prompt = build_enhanced_prompt(pending_prompt, knowledge_base)

    # 2. Exibir a mensagem original (sem o contexto RAG) para o usuário
    with st.chat_message("user"):
        st.markdown(pending_prompt)

    # 3. Salvar o prompt enriquecido no histórico (o modelo recebe o contexto)
    st.session_state.messages.append({"role": "user", "content": enhanced_prompt})

    # 4. Chamar o modelo e fazer streaming
    with st.chat_message("assistant"):
        resp_container = st.empty()
        full_resp = ""

        response_stream = call_mistral_api(sys_msg, st.session_state.messages)

        if response_stream:
            for partial in stream_response(response_stream):
                full_resp = partial
                resp_container.markdown(full_resp + "▌")

            # Renderização final sem cursor
            resp_container.markdown(full_resp)

            # 5. Renderizar diagrama Mermaid, se houver
            mermaid_code = extract_mermaid(full_resp)
            if mermaid_code:
                render_mermaid(mermaid_code, os_family)

            # 6. Botão de download do script, se houver código
            code = extract_code(full_resp)
            if code:
                st.download_button(
                    label=f"💾 Baixar Script ({ext})",
                    data=code,
                    file_name=f"script_gerado{ext}",
                    mime="text/plain",
                )

        # 7. Salvar resposta no histórico
        if full_resp:
            st.session_state.messages.append({"role": "assistant", "content": full_resp})
