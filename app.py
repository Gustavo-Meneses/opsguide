import streamlit as st
from mistralai import Mistral
import os

# Configuração da página
st.set_page_config(
    page_title="OpsGuide - Oracle Linux Assistant",
    page_icon="🐧",
    layout="centered"
)

# --- SEGURANÇA: Recuperação de Credenciais ---
# A chave nunca é exposta no frontend. Ela deve estar em .streamlit/secrets.toml
# ou nas Variáveis de Ambiente do serviço de hospedagem.
api_key = st.secrets.get("MISTRAL_API_KEY")

# Se a chave não for encontrada, bloqueia a aplicação imediatamente.
if not api_key:
    st.error("⛔ Erro Crítico: A chave de API não foi configurada no servidor.")
    st.info("Para o administrador: Configure 'MISTRAL_API_KEY' nos secrets do Streamlit ou variáveis de ambiente.")
    st.stop() # Interrompe a execução do script aqui.

# Inicializa o cliente Mistral de forma segura (v1.0.0+)
client = Mistral(api_key=api_key)
model = "mistral-tiny"

# --- Estilização (UI) ---
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stCodeBlock { border-left: 5px solid #d9534f; background-color: #f8f9fa; }
    div[data-testid="stToolbar"] { visibility: hidden; } /* Esconde menu de dev do Streamlit */
    footer { visibility: hidden; } /* Esconde rodapé padrão */
    </style>
    """, unsafe_allow_html=True)

# --- Cabeçalho ---
st.title("🐧 OpsGuide: Oracle Linux & DB Helper")
st.markdown("### Copiloto de Infraestrutura")
st.caption("Base de conhecimento ativa para Oracle Linux, Portainer e pgAdmin.")

# --- Lógica de Geração (Backend) ---
def generate_response(user_query):
    system_prompt = (
        "Você é um Engenheiro de DevOps Sênior focado em Oracle Linux (todas as versões), "
        "Docker/Portainer e administração de PostgreSQL via pgAdmin. "
        "Regras:"
        "1. Forneça comandos precisos em blocos de código."
        "2. Se o comando for destrutivo (ex: rm, drop table, stop service), adicione um aviso de PERIGO."
        "3. Seja conciso e direto. "
        "4. Responda em Português do Brasil."
    )
    
    try:
        chat_response = client.chat.complete(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ]
        )
        return chat_response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro ao processar solicitação: {str(e)}"

# --- Interface Principal ---
query = st.text_input("Digite sua dúvida técnica ou tarefa:", placeholder="Ex: Listar containers parados no Portainer via CLI...")

if query:
    with st.spinner("Analisando documentação e gerando comandos..."):
        response = generate_response(query)
        st.markdown("---")
        st.markdown(response)

# --- Rodapé Informativo ---
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 12px;'>
    Ferramenta interna para uso em servidores Oracle Linux.<br>
    Verifique sempre os comandos antes de executar em produção.
    </div>
    """, 
    unsafe_allow_html=True
)
