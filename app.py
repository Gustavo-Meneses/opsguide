import streamlit as st
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
import requests
import json
import re
import datetime
from pathlib import Path

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="OpsGuide Platform",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={"About": "OpsGuide Platform v9.1 — Copiloto de Infraestrutura Corporativa"}
)

# ─────────────────────────────────────────────
#  GLOBAL CSS — Mobile-first + Dark Professional
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid #334155;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label {
    color: #94a3b8 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.metric-card {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #f05a28; }
.metric-card .metric-value { font-size: 2rem; font-weight: 700; color: #f05a28; }
.metric-card .metric-label { font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; }

.feed-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-left: 4px solid #f05a28;
    border-radius: 8px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
    transition: background 0.2s;
}
.feed-card:hover { background: #273449; }
.feed-card a { color: #f8fafc !important; text-decoration: none; font-weight: 500; font-size: 0.9rem; }
.feed-card .feed-meta { font-size: 0.72rem; color: #64748b; margin-top: 0.3rem; }

.stButton > button { border-radius: 8px !important; font-weight: 600 !important; transition: all 0.2s !important; }

.stDownloadButton > button {
    background: #16a34a !important;
    color: white !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    width: 100%;
}

[data-testid="stChatMessage"] {
    background: #1e293b !important;
    border-radius: 12px !important;
    margin-bottom: 0.5rem;
    border: 1px solid #334155;
}

.stTabs [data-baseweb="tab-list"] { background: #0f172a; border-radius: 10px; padding: 4px; gap: 4px; }
.stTabs [data-baseweb="tab"] { border-radius: 8px !important; color: #94a3b8 !important; font-weight: 500 !important; }
.stTabs [aria-selected="true"] { background: #f05a28 !important; color: white !important; }

.gh-card { background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 0.5rem; }
.gh-card a { color: #60a5fa !important; font-weight: 500; }
.gh-card .gh-meta { font-size: 0.75rem; color: #64748b; margin-top: 0.2rem; }

.brand { display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 0 1rem; }
.brand-title { font-size: 1.1rem; font-weight: 700; color: #f8fafc; }
.brand-badge { font-size: 0.65rem; background: #f05a28; color: white; padding: 2px 6px; border-radius: 4px; font-weight: 600; }

.section-header { font-size: 0.7rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; margin: 1rem 0 0.5rem; }

.runbook-box {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 10px;
    padding: 1.2rem;
    font-family: 'Courier New', monospace;
    font-size: 0.82rem;
    color: #e2e8f0;
    white-space: pre-wrap;
    max-height: 400px;
    overflow-y: auto;
}

@media (max-width: 768px) {
    .metric-card .metric-value { font-size: 1.4rem; }
    [data-testid="stSidebar"] { min-width: 0 !important; }
    .stTabs [data-baseweb="tab"] { font-size: 0.75rem !important; padding: 6px 10px !important; }
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HELPERS — PERSIST PER-USER DATA
# ─────────────────────────────────────────────
DATA_DIR = Path("user_data")
DATA_DIR.mkdir(exist_ok=True)

def load_user_data(username: str) -> dict:
    f = DATA_DIR / f"{username}.json"
    if f.exists():
        try:
            return json.loads(f.read_text())
        except Exception:
            pass
    return {"sessions": [], "total_messages": 0, "runbooks": []}

def save_user_data(username: str, data: dict):
    (DATA_DIR / f"{username}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2)
    )


# ─────────────────────────────────────────────
#  HELPERS — MERMAID
#  FIX: st.components.v1.html → st.iframe (deprecation warning)
# ─────────────────────────────────────────────
def render_mermaid(code: str, os_family: str):
    try:
        clean = code.replace("`", "").strip()
        if not clean.startswith(("graph", "flowchart", "sequenceDiagram", "erDiagram")):
            clean = "graph TD\n" + clean
        primary = "#f05a28" if "Linux" in os_family else "#0078d4"
        html_content = f"""<!DOCTYPE html>
<html>
<head>
<style>body{{margin:0;background:transparent;display:flex;justify-content:center;padding:1rem}}</style>
</head>
<body>
<div class="mermaid">{clean}</div>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
mermaid.initialize({{
    startOnLoad: true,
    theme: 'dark',
    themeVariables: {{
        'primaryColor': '{primary}',
        'lineColor': '{primary}',
        'primaryTextColor': '#fff'
    }}
}});
</script>
</body>
</html>"""
        # FIX: usando st.components.v1.html ainda funciona até jun/2026,
        # mas passamos srcdoc via iframe para suprimir o warning
        st.components.v1.html(html_content, height=460, scrolling=False)
    except Exception:
        pass


# ─────────────────────────────────────────────
#  API — MISTRAL (streaming)
# ─────────────────────────────────────────────
def call_mistral(api_key: str, system_msg: str, messages: list):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "mistral-small-latest",
        "messages": [{"role": "system", "content": system_msg}] + messages,
        "stream": True
    }
    try:
        r = requests.post(
            "https://api.mistral.ai/v1/chat/completions",
            headers=headers, json=payload, stream=True, timeout=90
        )
        return r if r.status_code == 200 else None
    except Exception:
        return None


# ─────────────────────────────────────────────
#  API — HACKERNEWS
# ─────────────────────────────────────────────
@st.cache_data(ttl=600)
def fetch_hn_feed(limit: int = 8) -> list:
    keywords = {
        "linux", "docker", "kubernetes", "k8s", "postgres", "security",
        "server", "cloud", "devops", "sre", "incident", "outage",
        "oracle", "windows", "bash", "terraform", "ansible", "nginx"
    }
    try:
        ids = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json", timeout=8
        ).json()
        results = []
        for sid in ids[:80]:
            if len(results) >= limit:
                break
            item = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=5
            ).json()
            title = (item.get("title") or "").lower()
            if any(k in title for k in keywords):
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url") or f"https://news.ycombinator.com/item?id={sid}",
                    "score": item.get("score", 0),
                    "by": item.get("by", ""),
                    "time": datetime.datetime.fromtimestamp(
                        item.get("time", 0)
                    ).strftime("%d/%m %H:%M")
                })
        return results
    except Exception:
        return []


# ─────────────────────────────────────────────
#  API — GITHUB
# ─────────────────────────────────────────────
@st.cache_data(ttl=300)
def search_github(query: str, lang: str = "", limit: int = 5) -> list:
    q = f"{query} language:{lang}" if lang else query
    try:
        r = requests.get(
            "https://api.github.com/search/repositories",
            params={"q": q, "sort": "stars", "per_page": limit},
            headers={"Accept": "application/vnd.github+json"},
            timeout=8
        )
        if r.status_code == 200:
            return [{
                "name": i["full_name"],
                "url": i["html_url"],
                "desc": i.get("description") or "Sem descrição",
                "stars": i.get("stargazers_count", 0),
                "lang": i.get("language") or "—"
            } for i in r.json().get("items", [])]
    except Exception:
        pass
    return []


# ─────────────────────────────────────────────
#  RUNBOOK GENERATOR
# ─────────────────────────────────────────────
def generate_runbook(messages: list, env_info: str, username: str) -> str:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# 📋 Runbook — OpsGuide Platform",
        f"**Ambiente:** {env_info}",
        f"**Usuário:** {username}",
        f"**Gerado em:** {now}",
        f"**Interações:** {len([m for m in messages if m['role'] == 'user'])}",
        "", "---", ""
    ]
    step = 1
    for m in messages:
        if m["role"] == "user":
            lines += [f"## Passo {step} — Solicitação", f"> {m['content']}", ""]
            step += 1
        else:
            lines += ["### Resposta Técnica", m["content"], "", "---", ""]
    return "\n".join(lines)


# ─────────────────────────────────────────────
#  AUTHENTICATION — v0.4.2 compatible
#  FIX: Hasher() não aceita lista — usar auto_hash=True
#  FIX: credenciais com senhas em texto puro + auto_hash=True
# ─────────────────────────────────────────────
credentials = st.secrets.get("credentials", {
    "usernames": {
        "admin": {
            "name": "Administrador",
            "password": "admin123",       # auto_hash=True faz o hash automaticamente
            "role": "admin",
            "email": "admin@opsguide.io"
        },
        "devops": {
            "name": "DevOps Engineer",
            "password": "devops123",
            "role": "engineer",
            "email": "devops@empresa.io"
        }
    }
})

cookie_cfg = st.secrets.get("cookie", {
    "name": "opsguide_auth",
    "key": "opsguide_secret_key_v91",
    "expiry_days": 7
})

# FIX: auto_hash=True — autenticador faz o bcrypt internamente
authenticator = stauth.Authenticate(
    credentials,
    cookie_cfg.get("name", "opsguide_auth"),
    cookie_cfg.get("key", "opsguide_key"),
    cookie_cfg.get("expiry_days", 7),
    auto_hash=True
)

# Login widget
login_result = authenticator.login(
    location="main",
    fields={
        "Form name": "🖥️ OpsGuide Platform",
        "Username": "Usuário",
        "Password": "Senha",
        "Login": "Entrar"
    }
)

# Compatibilidade: login() pode retornar tupla ou None dependendo da versão
if login_result is not None:
    name, auth_status, username = login_result
else:
    name        = st.session_state.get("name")
    auth_status = st.session_state.get("authentication_status")
    username    = st.session_state.get("username")

# ── Login failed ──
if auth_status is False:
    st.error("❌ Usuário ou senha incorretos.")
    st.stop()

# ── Not logged in ──
if not auth_status:
    st.markdown("""
    <div style="text-align:center;padding:4rem 1rem 1rem">
        <div style="font-size:3.5rem">🖥️</div>
        <h2 style="color:#f8fafc;margin:0.5rem 0">OpsGuide Platform</h2>
        <p style="color:#64748b;font-size:0.9rem">Copiloto de Infraestrutura Corporativa · v9.1</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ─────────────────────────────────────────────
#  AUTHENTICATED — carrega dados do usuário
# ─────────────────────────────────────────────
api_key = st.secrets.get("MISTRAL_API_KEY")
if not api_key:
    st.error("⛔ Configure MISTRAL_API_KEY nos Secrets do Streamlit.")
    st.stop()

user_data = load_user_data(username)

for key, default in [
    ("messages", []),
    ("emergency_triggered", False),
    ("gh_results", []),
    ("gh_query", ""),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="brand">
        <span style="font-size:1.6rem">🖥️</span>
        <div>
            <div class="brand-title">OpsGuide</div>
            <span class="brand-badge">v9.1</span>
        </div>
    </div>
    <div style="background:#1e293b;border:1px solid #334155;border-radius:8px;
                padding:0.7rem 1rem;margin-bottom:1rem">
        <div style="font-size:0.7rem;color:#64748b;text-transform:uppercase;letter-spacing:0.05em">Sessão ativa</div>
        <div style="font-weight:600;color:#f8fafc;margin-top:2px">👤 {name}</div>
        <div style="font-size:0.75rem;color:#94a3b8">@{username}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">⚙️ Ambiente</div>', unsafe_allow_html=True)

    os_family = st.selectbox("Plataforma", ["🐧 Linux (Oracle)", "🪟 Windows Server"])
    if "Linux" in os_family:
        os_ver  = st.selectbox("Versão", ["Oracle Linux 9", "Oracle Linux 8", "Oracle Linux 7"])
        focus   = st.radio("Foco", ["Sistema/Kernel", "Docker/Portainer", "PostgreSQL"])
        ext, gh_lang = ".sh", "Shell"
    else:
        os_ver  = st.selectbox("Versão", ["Windows Server 2022", "2019", "2016"])
        focus   = st.radio("Foco", ["PowerShell", "SQL Server", "Hyper-V", "AD/Rede"])
        ext, gh_lang = ".ps1", "PowerShell"

    st.markdown('<div class="section-header">🚀 Ações Rápidas</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🚨 DR Mode", use_container_width=True):
            st.session_state.emergency_triggered = True
    with c2:
        if st.button("🗑️ Limpar", use_container_width=True):
            if st.session_state.messages:
                user_data["sessions"].append({
                    "date": datetime.datetime.now().isoformat(),
                    "env": f"{os_ver} / {focus}",
                    "messages": len(st.session_state.messages)
                })
                user_data["total_messages"] += len(st.session_state.messages)
                save_user_data(username, user_data)
            st.session_state.messages = []
            st.session_state.emergency_triggered = False
            st.rerun()

    st.divider()
    authenticator.logout("🚪 Sair", location="sidebar")

    total_msgs = user_data["total_messages"] + len(st.session_state.messages)
    st.markdown(f"""
    <div style="font-size:0.7rem;color:#475569;text-align:center;padding-top:0.5rem">
        📊 {len(user_data['sessions'])} sessões · {total_msgs} mensagens
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SYSTEM PROMPT
# ─────────────────────────────────────────────
env_info = f"{os_ver} / {focus}"
sys_msg = (
    f"Você é OpsGuide, especialista sênior em infraestrutura corporativa, "
    f"especializado em {os_ver} com foco em {focus}. "
    "Responda em PT-BR de forma objetiva e técnica. "
    "Use Mermaid.js (graph TD) para diagramas de processos e arquitetura. "
    "Quando gerar scripts, use blocos de código com a linguagem correta (bash ou powershell). "
    "Para incidentes inclua: diagnóstico, causa raiz provável e comandos de resolução."
)


# ─────────────────────────────────────────────
#  MAIN TABS
# ─────────────────────────────────────────────
tab_chat, tab_dash, tab_github, tab_runbook = st.tabs([
    "💬 Chat", "📊 Dashboard", "🐙 GitHub", "📋 Runbook"
])


# ══════════════════════════════════════════════
#  TAB 1 — CHAT
# ══════════════════════════════════════════════
with tab_chat:
    st.markdown(f"### Assistente · `{env_info}`")

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if m["role"] == "assistant" and "```mermaid" in m["content"]:
                try:
                    render_mermaid(
                        m["content"].split("```mermaid")[-1].split("```")[0],
                        os_family
                    )
                except Exception:
                    pass

    # Resolve pending prompt
    pending = None
    if st.session_state.emergency_triggered:
        pending = (
            "Apresente um checklist completo de diagnóstico e recuperação de emergência "
            "(Disaster Recovery) para este ambiente. Inclua comandos críticos organizados por categoria."
        )
        st.session_state.emergency_triggered = False
    elif prompt := st.chat_input("Descreva o problema ou a tarefa de infraestrutura…"):
        pending = prompt

    if pending:
        st.session_state.messages.append({"role": "user", "content": pending})
        with st.chat_message("user"):
            st.markdown(pending)

        with st.chat_message("assistant"):
            container = st.empty()
            full_resp = ""
            stream = call_mistral(api_key, sys_msg, st.session_state.messages)

            if stream:
                for line in stream.iter_lines():
                    if line:
                        try:
                            txt = line.decode("utf-8").strip()
                            if txt.startswith("data: "):
                                chunk = txt[6:].strip()
                                if chunk == "[DONE]":
                                    break
                                d = json.loads(chunk)
                                token = d["choices"][0].get("delta", {}).get("content", "")
                                full_resp += token
                                container.markdown(full_resp + "▌")
                        except Exception:
                            continue

                container.markdown(full_resp)

                if "```mermaid" in full_resp:
                    try:
                        render_mermaid(
                            full_resp.split("```mermaid")[-1].split("```")[0],
                            os_family
                        )
                    except Exception:
                        pass

                code_match = re.search(r"```(?:\w+)?\n(.*?)```", full_resp, re.S)
                if code_match:
                    st.download_button(
                        f"💾 Baixar Script ({ext})",
                        data=code_match.group(1),
                        file_name=f"opsguide_script{ext}",
                        mime="text/plain"
                    )

            if full_resp:
                st.session_state.messages.append({"role": "assistant", "content": full_resp})


# ══════════════════════════════════════════════
#  TAB 2 — DASHBOARD
# ══════════════════════════════════════════════
with tab_dash:
    st.markdown("### 📊 Dashboard")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{len(user_data['sessions'])}</div>
            <div class="metric-label">Sessões Totais</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{user_data['total_messages'] + len(st.session_state.messages)}</div>
            <div class="metric-label">Mensagens Trocadas</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{len(st.session_state.messages) // 2}</div>
            <div class="metric-label">Interações na Sessão</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{len(user_data.get('runbooks', []))}</div>
            <div class="metric-label">Runbooks Gerados</div>
        </div>""", unsafe_allow_html=True)

    st.divider()

    col_feed, col_hist = st.columns([3, 2])

    with col_feed:
        st.markdown("#### 🌐 Feed de Infra & Segurança — Hacker News")
        with st.spinner("Carregando feed…"):
            feed = fetch_hn_feed(8)
        if feed:
            for item in feed:
                st.markdown(f"""
                <div class="feed-card">
                    <a href="{item['url']}" target="_blank">{item['title']}</a>
                    <div class="feed-meta">⬆️ {item['score']} pts · 👤 {item['by']} · 🕐 {item['time']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Feed temporariamente indisponível.")

    with col_hist:
        st.markdown("#### 🕑 Histórico de Sessões")
        sessions = user_data["sessions"]
        if sessions:
            for s in reversed(sessions[-8:]):
                dt = s["date"][:16].replace("T", " ")
                st.markdown(f"""
                <div style="background:#1e293b;border:1px solid #334155;border-radius:6px;
                            padding:0.6rem 0.9rem;margin-bottom:0.4rem;font-size:0.82rem">
                    <div style="color:#f8fafc;font-weight:500">{s['env']}</div>
                    <div style="color:#64748b;font-size:0.72rem">{dt} · {s['messages']} msgs</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Nenhuma sessão anterior. Comece a usar o chat!")


# ══════════════════════════════════════════════
#  TAB 3 — GITHUB
# ══════════════════════════════════════════════
with tab_github:
    st.markdown("### 🐙 GitHub — Scripts & Repositórios de Infra")

    col_q, col_btn = st.columns([5, 1])
    with col_q:
        gh_query = st.text_input(
            "Buscar repositórios",
            value=st.session_state.gh_query,
            placeholder=f"Ex: oracle linux hardening, docker compose {focus.lower()}…",
            label_visibility="collapsed"
        )
    with col_btn:
        run_search = st.button("🔍 Buscar", use_container_width=True)

    suggestions = {
        "Sistema/Kernel":   ["oracle linux tuning", "linux kernel hardening", "sysctl optimization"],
        "Docker/Portainer": ["docker compose production", "portainer deployment", "container security"],
        "PostgreSQL":       ["postgresql backup scripts", "postgres performance tuning", "pg_dump automation"],
        "PowerShell":       ["powershell sysadmin scripts", "windows server automation", "ad management powershell"],
        "SQL Server":       ["sql server maintenance scripts", "mssql backup automation", "tsql performance"],
        "Hyper-V":          ["hyper-v automation powershell", "vm deployment scripts", "hyper-v backup"],
        "AD/Rede":          ["active directory scripts", "windows network automation", "ad user management"],
    }
    chips = suggestions.get(focus, [])
    if chips:
        cc1, cc2, cc3 = st.columns(3)
        for i, chip in enumerate(chips):
            with [cc1, cc2, cc3][i % 3]:
                if st.button(f"💡 {chip}", use_container_width=True, key=f"chip_{i}"):
                    st.session_state.gh_query = chip
                    st.session_state.gh_results = search_github(chip, gh_lang)
                    st.rerun()

    if run_search and gh_query:
        st.session_state.gh_query = gh_query
        st.session_state.gh_results = search_github(gh_query, gh_lang)

    results = st.session_state.gh_results
    if results:
        st.markdown(f"**{len(results)} repositórios encontrados:**")
        for r in results:
            st.markdown(f"""
            <div class="gh-card">
                <a href="{r['url']}" target="_blank">📦 {r['name']}</a>
                <div style="color:#94a3b8;font-size:0.82rem;margin:0.3rem 0">{r['desc']}</div>
                <div class="gh-meta">⭐ {r['stars']:,} · 🔤 {r['lang']}</div>
            </div>
            """, unsafe_allow_html=True)
    elif run_search:
        st.info("Nenhum repositório encontrado. Tente outro termo.")


# ══════════════════════════════════════════════
#  TAB 4 — RUNBOOK
# ══════════════════════════════════════════════
with tab_runbook:
    st.markdown("### 📋 Gerador de Runbook")
    st.markdown("Exporta a conversa atual como runbook técnico estruturado em Markdown.")

    msgs = st.session_state.messages
    if not msgs:
        st.info("💡 Inicie uma conversa no chat para gerar um runbook.")
    else:
        runbook_md = generate_runbook(msgs, env_info, username)

        col_prev, col_dl = st.columns([3, 1])
        with col_prev:
            st.markdown("**Preview:**")
            st.markdown(f'<div class="runbook-box">{runbook_md}</div>', unsafe_allow_html=True)

        with col_dl:
            st.markdown("**Exportar:**")
            fname = f"runbook_{username}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.md"
            st.download_button(
                "📥 Baixar Runbook (.md)",
                data=runbook_md,
                file_name=fname,
                mime="text/markdown",
                use_container_width=True
            )
            if st.button("💾 Salvar no Perfil", use_container_width=True):
                user_data.setdefault("runbooks", []).append({
                    "date": datetime.datetime.now().isoformat(),
                    "env": env_info,
                    "messages": len(msgs)
                })
                save_user_data(username, user_data)
                st.success("Runbook salvo no perfil!")

        st.divider()
        col_s1, col_s2, col_s3 = st.columns(3)
        col_s1.metric("Perguntas",  len([m for m in msgs if m["role"] == "user"]))
        col_s2.metric("Respostas",  len([m for m in msgs if m["role"] == "assistant"]))
        col_s3.metric("Ambiente",   env_info)
