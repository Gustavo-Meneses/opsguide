import streamlit as st
from mistralai import Mistral
import time

# --- Configuração da Página ---
st.set_page_config(
    page_title="OpsGuide - Oracle Linux",
    page_icon="🐧",
    layout="wide" # Mudamos para wide para aproveitar melhor a tela com logs
)

# --- Estilos CSS (Dark/Light Mode friendly) ---
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    .reportview-container {
        margin-top: -2em;
    }
    /* Destaque para avisos de perigo */
    .warning-box {
        background-color: #ffcccc;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #d9534f;
        color: #a94442;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Gestão de Estado (Session State) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SEGURANÇA: Credenciais ---
api_key = st.secrets.get("MISTRAL_API_KEY")
if not api_key:
    st.error("⛔ Erro Crítico: MISTRAL_API_KEY não configurada nos secrets.")
    st.stop()

client = Mistral(api_key=api_key)
model = "mistral-tiny" # Rápido e suficiente para comandos

# --- Sidebar: Contexto Técnico ---
with st.sidebar:
    st.title("🔧 Contexto do Servidor")
    
    os_version = st.selectbox(
        "Versão do Oracle Linux:",
        ["Oracle Linux 9 (UEK R7)", "Oracle Linux 8 (UEK R6)", "Oracle Linux 7 (Legacy)"],
        index=0
    )
    
    tech_focus = st.radio(
        "Foco da Tarefa:",
        ["Sistema Operacional (OS)", "Docker / Portainer", "PostgreSQL / pgAdmin"]
    )
    
    st.divider()
    st.caption("Ações Rápidas:")
    
    # Botões que preenchem o chat automaticamente
    col1, col2 = st.columns(2)
    if col1.button("🔥 Firewall"):
        st.session_state.prompt_input = f"Como listar e abrir portas no firewall-cmd para o {os_version}?"
    if col2.button("🐳 Logs Docker"):
        st.session_state.prompt_input = "Comando para ver logs de um container específico em tempo real."
    if st.button("💾 Espaço em Disco"):
        st.session_state.prompt_input = "Comando para listar espaço em disco human readable e ordenar por pastas maiores."

# --- Função Principal de Chat ---
st.title("🐧 OpsGuide Copilot")
st.markdown(f"**Contexto Ativo:** `{os_version}` | Foco: `{tech_focus}`")

# Exibe histórico de mensagens da sessão atual
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Input do Usuário ---
# Verifica se veio de um botão rápido ou digitação manual
if "prompt_input" in st.session_state and st.session_state.prompt_input:
    user_input = st.session_state.prompt_input
    del st.session_state.prompt_input # Limpa para não repetir
else:
    user_input = st.chat_input("Digite sua tarefa (ex: Como criar um volume no Portainer?)")

if user_input:
    # 1. Adiciona pergunta ao histórico visual
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Monta o Prompt de Sistema Enriquecido
    system_instruction = (
        f"Você é um SysAdmin Sênior especialista em {os_version} e {tech_focus}. "
        "Regras: "
        "1. Priorize comandos 'dnf' para OL8/9 e 'yum' para OL7. "
        "2. Se for sobre Portainer/Docker, use 'docker compose' ou CLI. "
        "3. Se for pgAdmin, explique se é via Interface Web ou Query Tool. "
        "4. Responda em Português BR. Seja conciso. Use Markdown para código."
    )

    # 3. Chamada Streaming à API
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            stream_response = client.chat.stream(
                model=model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_input}
                ]
            )
            
            # Processa o stream chunk por chunk
            for chunk in stream_response:
                content = chunk.data.choices[0].delta.content
                if content:
                    full_response += content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            
            # Salva resposta no histórico
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Erro na API: {str(e)}")

# --- Rodapé ---
st.markdown("---")
st.caption("Nota: Verifique os comandos antes de executar em produção (Principalmente `rm`, `drop`, `stop`).")
