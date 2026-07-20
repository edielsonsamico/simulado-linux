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

# ==========================================
# 2. DADOS (MANTENHA A SUA ESTRUTURA)
# ==========================================
QUESTOES_POOL = desduplicar_questoes([
    {"id": 1, "topico": "Tópico 101", "pergunta": "Qual comando PCI?", "opcoes": ["lspci", "lsusb", "lsmod", "dmesg"], "correta": "lspci"},
    {"id": 2, "topico": "Tópico 102", "pergunta": "Qual diretório FHS?", "opcoes": ["/etc", "/var", "/usr", "/opt"], "correta": "/etc"}
])

# ==========================================
# 3. ESTRUTURA DO APLICATIVO
# ==========================================
st.set_page_config(page_title="Linux Essentials", layout="wide")

if 'iniciado' not in st.session_state:
    st.session_state.questoes_treino = QUESTOES_POOL
    st.session_state.iniciado = True

# SIDEBAR
modo = st.sidebar.radio("Ambiente:", [
    "📖 Área de Treino (Geral)", 
    "🎯 Treino por Tópico (Focado)", 
    "⏱️ Simulado LPI (Prova Real 40 Q)",
    "🎁 Materiais VIP & Simulados",
    "ℹ️ Créditos & Desenvolvimento"
])

# CONTAINER PRINCIPAL PARA GARANTIR RENDERIZAÇÃO
content_area = st.container()

with content_area:
    if modo == "📖 Área de Treino (Geral)":
        st.title("📖 Área de Treino Geral")
        for idx, q in enumerate(st.session_state.questoes_treino):
            opcoes = obter_opcoes_embaralhadas(q)
            st.markdown(f"**{q['pergunta']}**")
            res = st.radio(f"q_{idx}", opcoes, index=None, label_visibility="collapsed")
            if res == q['correta']: st.success("🎯 Correto!")
            elif res: st.error(f"❌ Errado. Certo: {q['correta']}")
            st.divider()

    elif modo == "🎯 Treino por Tópico (Focado)":
        st.title("🎯 Treino por Tópico (Focado)")
        st.write("Aqui serão listadas as questões filtradas por tópico.")

    elif modo == "⏱️ Simulado LPI (Prova Real 40 Q)":
        st.title("⏱️ Simulado LPI (Prova Real 40 Q)")
        simulado = random.sample(st.session_state.questoes_treino, k=min(40, len(st.session_state.questoes_treino)))
        for idx, q in enumerate(simulado):
            opcoes = obter_opcoes_embaralhadas(q)
            st.markdown(f"**{idx+1}. {q['pergunta']}**")
            st.radio(f"s_{idx}", opcoes, index=None, label_visibility="collapsed")
            st.divider()

    elif modo == "🎁 Materiais VIP & Simulados":
        st.title("🎁 Materiais VIP & Simulados")
        st.write("Conteúdo exclusivo da Área VIP.")

    elif modo == "ℹ️ Créditos & Desenvolvimento":
        st.title("ℹ️ Créditos & Desenvolvimento")
        st.write("Desenvolvido por Edielson Samico.")
