import streamlit as st
import random
import re

# ==========================================
# 1. FUNÇÕES DE APOIO
# ==========================================
def desduplicar_questoes(lista_original):
    vistas = set()
    lista_limpa = []
    for q in lista_original:
        p = re.sub(r'^(quest[ãa]o(\s+avançada)?(\s+de\s+arquitetura)?\s+\d+|q\d+|\d+)[:\.\-\s]+', '', q["pergunta"].strip().lower())
        if p not in vistas:
            vistas.add(p)
            lista_limpa.append(q)
    return lista_limpa

def obter_opcoes_embaralhadas(q):
    opcoes = q['opcoes'].copy()
    state = random.Random(q['id'])
    state.shuffle(opcoes)
    return opcoes

# Banco de dados
QUESTOES_POOL = desduplicar_questoes([
    {"id": 1, "topico": "Tópico 101", "pergunta": "Qual comando PCI?", "opcoes": ["lspci", "lsusb", "lsmod", "dmesg"], "correta": "lspci"},
    {"id": 2, "topico": "Tópico 102", "pergunta": "Qual diretório FHS?", "opcoes": ["/etc", "/var", "/usr", "/opt"], "correta": "/etc"}
])

# ==========================================
# 2. APLICATIVO
# ==========================================
st.set_page_config(page_title="Linux Essentials", layout="wide")

if 'iniciado' not in st.session_state:
    st.session_state.questoes_treino = QUESTOES_POOL
    st.session_state.iniciado = True

modo = st.sidebar.radio("Ambiente:", [
    "📖 Área de Treino (Geral)", 
    "🎯 Treino por Tópico (Focado)", 
    "⏱️ Simulado LPI (Prova Real 40 Q)",
    "🎁 Materiais VIP & Simulados",
    "ℹ️ Créditos & Desenvolvimento"
])

# --- ABA 1: TREINO GERAL ---
if modo == "📖 Área de Treino (Geral)":
    st.title("📖 Área de Treino Geral")
    for idx, q in enumerate(st.session_state.questoes_treino):
        opcoes = obter_opcoes_embaralhadas(q)
        st.markdown(f"**{q['pergunta']}**")
        res = st.radio(f"g_{idx}", opcoes, index=None, label_visibility="collapsed")
        if res == q['correta']: st.success("🎯 Correto!")
        elif res: st.error(f"❌ Errado. Certo: {q['correta']}")
        st.divider()

# --- ABA 2: TREINO POR TÓPICO ---
elif modo == "🎯 Treino por Tópico (Focado)":
    st.title("🎯 Treino por Tópico (Focado)")
    topicos = sorted(list(set(q['topico'] for q in QUESTOES_POOL)))
    t = st.selectbox("Escolha o tópico:", topicos)
    for idx, q in enumerate([q for q in QUESTOES_POOL if q['topico'] == t]):
        opcoes = obter_opcoes_embaralhadas(q)
        st.markdown(f"**{q['pergunta']}**")
        res = st.radio(f"t_{idx}", opcoes, index=None, label_visibility="collapsed")
        if res == q['correta']: st.success("🎯 Correto!")
        elif res: st.error(f"❌ Errado. Certo: {q['correta']}")
        st.divider()

# --- ABA 3: SIMULADO ---
elif modo == "⏱️ Simulado LPI (Prova Real 40 Q)":
    st.title("⏱️ Simulado LPI (Prova Real 40 Q)")
    simulado = random.sample(QUESTOES_POOL, k=min(40, len(QUESTOES_POOL)))
    for idx, q in enumerate(simulado):
        opcoes = obter_opcoes_embaralhadas(q)
        st.markdown(f"**{idx+1}. {q['pergunta']}**")
        st.radio(f"s_{idx}", opcoes, index=None, label_visibility="collapsed")
        st.divider()

# --- ABA 4: VIP ---
elif modo == "🎁 Materiais VIP & Simulados":
    st.title("🎁 Materiais VIP & Simulados")
    st.info("Conteúdo exclusivo disponível após inscrição.")

# --- ABA 5: CRÉDITOS ---
elif modo == "ℹ️ Créditos & Desenvolvimento":
    st.title("ℹ️ Créditos & Desenvolvimento")
    st.write("Desenvolvido por Edielson Samico.")
