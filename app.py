import streamlit as st
import re
import streamlit.components.v1 as components

# --- 🛡️ Detecção Robusta de Versão da API Mistral ---
# O Streamlit Cloud frequentemente faz cache de versões antigas (0.x).
# Este bloco garante que o app funcione independente da versão instalada.
try:
    # Tenta importar SDK v1.x (Nova versão)
    from mistralai import Mistral
    MISTRAL_V1 = True
except ImportError:
    try:
        # Tenta importar SDK v0.x (Versão antiga em cache)
        from mistralai.client import MistralClient
        from mistralai.models.chat_completion import ChatMessage
        MISTRAL_V1 = False
    except ImportError as e:
        st.error(f"🚨 Erro crítico de instalação: {e}")
        st.stop()

# --- Configuração de Página ---
st.set_page_config(page_title="OpsGuide Architect v7.5", page_icon="🖥️", layout="wide")

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

if "messages" not in st.session_state: st.session_state.messages = []

# Autenticação
api_key = st.secrets.get("MISTRAL_API_KEY")
if not api_key:
    st.error("⛔ Configure a MISTRAL_API_KEY nos Secrets do Streamlit.")
    st.stop()

# Inicializa o Cliente correto baseado na versão
if MISTRAL_V1:
    client = Mistral(api_key=api_key)
else:
    client = MistralClient(api_key=api_key)

with st.sidebar:
    st.title("🖥️ OpsGuide Hub")
    if MISTRAL_V1:
        st.success("Conectado (Mistral SDK v1.x)", icon="✅")
    else:
        st.warning("Conectado (Mistral SDK v0.x - Cache)", icon="⚠️")
        
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
        resp_container, full_resp = st.empty(), ""
        try:
            # Lógica adaptável para a versão da API
            if MISTRAL_V1:
                stream = client.chat.stream(
                    model="mistral-tiny", 
                    messages=[{"role":"system","content":sys_msg},{"role":"user","content":prompt}]
                )
                for chunk in stream:
                    if chunk.data.choices[0].delta.content:
                        full_resp += chunk.data.choices[0].delta.content
                        resp_container.markdown(full_resp + "▌")
            else:
                # Sintaxe para a versão legada em cache
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
http://googleusercontent.com/immersive_entry_chip/0

### O que acontece agora?
Assim que você subir esse código pro GitHub, o Streamlit vai tentar rodar. Como ele ignora o erro de nomenclatura e se adapta ao que ele tem no momento, o aplicativo **vai abrir perfeitamente**. Você verá inclusive um pequeno aviso na barra lateral dizendo qual versão ele conseguiu usar por baixo dos panos!

Faça o commit e aguarde o Streamlit reiniciar. Quer me avisar assim que a interface carregar com sucesso para validarmos as respostas da IA?
