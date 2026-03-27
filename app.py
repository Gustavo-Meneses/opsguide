import streamlit as st
import re
import streamlit.components.v1 as components
import requests
import json

# --- Configuração de Página ---
st.set_page_config(page_title="OpsGuide Architect v8.7", page_icon="🖥️", layout="wide")

# --- 🛡️ Comunicação Direta via API ---
def call_mistral_api(api_key, system_msg, messages):
    """
    Envia o histórico completo de mensagens para a API da Mistral com streaming.
    """
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    api_messages = [{"role": "system", "content": system_msg}] + messages

    payload = {
        "model": "mistral-small-latest",
        "messages": api_messages,
        "stream": True
    }

    try:
        response = requests.post(url, headers=headers, json=payload, stream=True, timeout=60)
        if response.status_code != 200:
            st.error(f"Erro da API Mistral (Status {response.status_code}): {response.text}")
            return None
        return response
    except Exception as e:
        st.error(f"Falha na conexão de rede: {e}")
        return None


# --- UI e Estilos ---
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


def render_mermaid(code, os_family):
    """Renderiza um diagrama Mermaid.js no navegador."""
    try:
        clean_code = code.replace("`", "").strip()
        if not clean_code.startswith("graph") and not clean_code.startswith("flowchart"):
            clean_code = "graph TD\n" + clean_code

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
                themeVariables: {{
                    'primaryColor': '{primary}',
                    'primaryTextColor': '{text_color}',
                    'lineColor': '{primary}'
                }}
            }});
            </script>
            """, height=450)
    except Exception:
        pass


# --- Inicialização do Estado ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# FIX: Flag de disparo único para o botão de emergência
if "emergency_triggered" not in st.session_state:
    st.session_state.emergency_triggered = False

# --- Autenticação via Secrets ---
api_key = st.secrets.get("MISTRAL_API_KEY")
if not api_key:
    st.error("⛔ Configure a MISTRAL_API_KEY nos Secrets do Streamlit (Settings > Secrets).")
    st.stop()

# --- Sidebar ---
with st.sidebar:
    st.title("🖥️ OpsGuide Hub")
    st.success("API Engine: Direct HTTP v8.7", icon="🚀")

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

    # FIX: Usa flag de estado para garantir disparo único sem rerun imediato
    if st.button("🚨 MODO DE EMERGÊNCIA (DR)", use_container_width=True):
        st.session_state.emergency_triggered = True

    # Botão de limpar com estilo vermelho (via CSS acima)
    if st.button("🗑️ Limpar Histórico", use_container_width=True):
        st.session_state.messages = []
        st.session_state.emergency_triggered = False
        st.rerun()

# --- System Prompt Dinâmico ---
sys_msg = (
    f"Você é um especialista em {os_ver}. Foco: {focus}. "
    "Responda em PT-BR. "
    "Sempre use Mermaid.js (graph TD) para diagramas técnicos quando explicar processos. "
    "Quando gerar scripts, coloque-os dentro de blocos de código com a linguagem correta (bash ou powershell)."
)

# --- Título Principal ---
st.title(f"Assistente {os_family}")

# --- Exibição do Histórico ---
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m["role"] == "assistant" and "```mermaid" in m["content"]:
            try:
                render_mermaid(m["content"].split("```mermaid")[-1].split("```")[0], os_family)
            except Exception:
                pass

# --- Resolução da mensagem a processar ---
# Prioridade: emergência (flag) > input do usuário
pending_prompt = None

if st.session_state.emergency_triggered:
    emergency_msg = "Apresente comandos de emergência e troubleshooting críticos para este ambiente."
    st.session_state.emergency_triggered = False  # FIX: reseta flag ANTES de processar
    pending_prompt = emergency_msg
elif prompt := st.chat_input("Como posso ajudar na sua infraestrutura?"):
    pending_prompt = prompt

# --- Processamento da Mensagem ---
if pending_prompt:
    st.session_state.messages.append({"role": "user", "content": pending_prompt})
    with st.chat_message("user"):
        st.markdown(pending_prompt)

    with st.chat_message("assistant"):
        resp_container = st.empty()
        full_resp = ""

        response_stream = call_mistral_api(api_key, sys_msg, st.session_state.messages)

        if response_stream:
            for line in response_stream.iter_lines():
                if line:
                    try:
                        line_text = line.decode('utf-8').strip()
                        if line_text.startswith("data: "):
                            data_content = line_text[6:].strip()
                            if data_content == "[DONE]":
                                break
                            if data_content:
                                data_json = json.loads(data_content)
                                if 'choices' in data_json and len(data_json['choices']) > 0:
                                    delta = data_json['choices'][0].get('delta', {})
                                    content = delta.get('content', '')
                                    full_resp += content
                                    resp_container.markdown(full_resp + "▌")
                    except Exception:
                        continue

            # Renderização final — FORA do loop
            resp_container.markdown(full_resp)

            # Renderização de Diagramas Mermaid
            if "```mermaid" in full_resp:
                try:
                    render_mermaid(
                        full_resp.split("```mermaid")[-1].split("```")[0],
                        os_family
                    )
                except Exception:
                    pass

            # Extração de código para download
            try:
                code_match = re.search(r"```(?:\w+)?\n(.*?)```", full_resp, re.S)
                if code_match:
                    extracted_code = code_match.group(1)
                    st.download_button(
                        label=f"💾 Baixar Script ({ext})",
                        data=extracted_code,
                        file_name=f"script_gerado{ext}",
                        mime="text/plain"
                    )
            except Exception as e:
                st.warning(f"Não foi possível gerar o botão de download: {e}")

        # Salva resposta do assistente no histórico
        if full_resp:
            st.session_state.messages.append({"role": "assistant", "content": full_resp})
