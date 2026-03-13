import streamlit as st
import re
import streamlit.components.v1 as components
import requests
import json
import time

# --- Configuração de Página ---
st.set_page_config(page_title="OpsGuide Architect v8.3", page_icon="🖥️", layout="wide")

# --- 🛡️ Comunicação Direta via API (Blindagem v8.3) ---
def call_mistral_api(api_key, system_msg, user_msg):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "mistral-tiny",
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ],
        "stream": True
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, stream=True, timeout=30)
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
    .stDownloadButton>button { width: 100%; background-color: #2e7d32; color: white; border-radius: 8px; font-weight: bold; }
    .stCodeBlock { border-radius: 10px; border-left: 5px solid #f05a28; }
    </style>
    """, unsafe_allow_html=True)

def render_mermaid(code, os_family):
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
                themeVariables: {{ 'primaryColor': '{primary}', 'primaryTextColor': '{text_color}', 'lineColor': '{primary}' }} 
            }});
        </script>
        """, height=450)

if "messages" not in st.session_state: 
    st.session_state.messages = []

# Autenticação via Secrets
api_key = st.secrets.get("MISTRAL_API_KEY")
if not api_key:
    st.error("⛔ Configure a MISTRAL_API_KEY nos Secrets do Streamlit (Settings > Secrets).")
    st.stop()

with st.sidebar:
    st.title("🖥️ OpsGuide Hub")
    st.success("API Engine: Direct HTTP v8.3", icon="🚀")
        
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
        st.session_state.messages.append({"role": "user", "content": "Apresente comandos de emergência e troubleshooting críticos para este ambiente."})

sys_msg = f"Você é um especialista em {os_ver}. Foco: {focus}. Responda em PT-BR. Sempre use Mermaid.js (graph TD) para diagramas técnicos quando explicar processos."

st.title(f"Assistente {os_family}")

# Exibir histórico
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m["role"] == "assistant" and "```mermaid" in m["content"]:
            try:
                render_mermaid(m["content"].split("```mermaid")[-1].split("```")[0], os_family)
            except: pass

# Input do Usuário
if prompt := st.chat_input("Como posso ajudar na sua infraestrutura?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    
    with st.chat_message("assistant"):
        resp_container = st.empty()
        full_resp = ""
        
        response_stream = call_mistral_api(api_key, sys_msg, prompt)
        
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
                                # Verificação segura da estrutura do JSON
                                if 'choices' in data_json and len(data_json['choices']) > 0:
                                    delta = data_json['choices'][0].get('delta', {})
                                    content = delta.get('content', '')
                                    full_resp += content
                                    resp_container.markdown(full_resp + "▌")
                                elif 'error' in data_json:
                                    st.error(f"Erro na resposta da API: {data_json['error']}")
                    except Exception as e:
                        # Silencia erros de decodificação de fragmentos, mas permite debug se necessário
                        continue
            
            resp_container.markdown(full_resp)
            
            # Processamento Pós-Resposta
            if "```mermaid" in full_resp:
                try:
                    render_mermaid(full_resp.split("```mermaid")[-1].split("```")[0], os_family)
                except: pass
            
            code_match = re.search(r'
