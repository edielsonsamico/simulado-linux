import streamlit as st
import random
import re

# ==========================================
# 1. FUNÇÕES DE LIMPEZA E LÓGICA (CORE)
# ==========================================
def normalizar_texto(texto):
    texto_limpo = re.sub(r'^(quest[ãa]o(\s+avançada)?(\s+de\s+[a-z\s]+)?\s*\d+|q\d+|\d+)[:\.\-\s]+', '', texto.strip().lower())
    return " ".join(texto_limpo.split())

def desduplicar_questoes(lista_original):
    vistas = set()
    lista_limpa = []
    for q in lista_original:
        p = normalizar_texto(q["pergunta"])
        if p not in vistas:
            vistas.add(p)
            lista_limpa.append(q)
    return lista_limpa

# ==========================================
# 2. BANCO DE DADOS
# ==========================================
QUESTOES_POOL = desduplicar_questoes([
    {"id": 1, "topico": "Tópico 103: Comandos", "pergunta": "Qual caractere canalizador conecta o stdout?", "opcoes": ["|", ">", "<", ">>"], "correta": "|"},
    {"id": 2, "topico": "Tópico 105: Scripts e SQL", "pergunta": "Qual operador testa arquivo regular (-f)?", "opcoes": ["test -f", "test -d", "test -z", "test -x"], "correta": "test -f"},
])

# ==========================================
# 3. APP PRINCIPAL
# ==========================================
st.set_page_config(page_title="Ambiente SAMICOIOT", layout="wide")

# Inicialização centralizada e segura
if 'iniciado' not in st.session_state:
    st.session_state.questoes = QUESTOES_POOL
    st.session_state.simulado_ativo = random.sample(QUESTOES_POOL, k=min(40, len(QUESTOES_POOL)))
    st.session_state.iniciado = True

st.sidebar.title("Ambiente SAMICOIOT")
modo = st.sidebar.radio("Navegação:", [
    "📖 Área de Treino (Geral)", 
    "🎯 Treino por Tópico (Focado)", 
    "⏱️ Simulado LPI (Prova Real 40 Q)",
    "🎁 Materiais VIP & Simulados",
    "ℹ️ Créditos & Desenvolvimento"
])

# ==========================================
# 4. RENDERIZAÇÃO (PROTEGIDA POR .get())
# ==========================================
if modo == "📖 Área de Treino (Geral)":
    st.title("📖 Área de Treino Geral")
    # Acesso seguro via .get()
    questoes = st.session_state.get('questoes', QUESTOES_POOL)
    for idx, q in enumerate(questoes):
        opcoes = q['opcoes'].copy()
        random.shuffle(opcoes)
        st.markdown(f"**{q['pergunta']}**")
        res = st.radio(f"treino_{q['id']}", opcoes, index=None, label_visibility="collapsed")
        if res == q['correta']: st.success("🎯 Correto!")
        elif res: st.error(f"❌ Errado. Certo: {q['correta']}")
        st.divider()

elif modo == "🎯 Treino por Tópico (Focado)":
    st.title("🎯 Treino por Tópico (Focado)")
    topicos = sorted(list(set(q['topico'] for q in QUESTOES_POOL)))
    t = st.selectbox("Escolha o tópico:", topicos)
    for idx, q in enumerate([q for q in QUESTOES_POOL if q['topico'] == t]):
        opcoes = q['opcoes'].copy()
        random.shuffle(opcoes)
        st.markdown(f"**{q['pergunta']}**")
        res = st.radio(f"topico_{q['id']}", opcoes, index=None, label_visibility="collapsed")
        if res == q['correta']: st.success("🎯 Correto!")
        elif res: st.error(f"❌ Errado. Certo: {q['correta']}")
        st.divider()

elif modo == "⏱️ Simulado LPI (Prova Real 40 Q)":
    st.title("⏱️ Simulado LPI (Prova Real 40 Q)")
    if st.button("Gerar novo simulado (Inédito)"):
        st.session_state.simulado_ativo = random.sample(QUESTOES_POOL, k=min(40, len(QUESTOES_POOL)))
        st.rerun()
        
    # Acesso seguro usando .get() com valor padrão
    simulado = st.session_state.get('simulado_ativo', random.sample(QUESTOES_POOL, k=min(40, len(QUESTOES_POOL))))
    for idx, q in enumerate(simulado):
        opcoes = q['opcoes'].copy()
        random.shuffle(opcoes)
        st.markdown(f"**{idx+1}. {q['pergunta']}**")
        st.radio(f"sim_{q['id']}", opcoes, index=None, label_visibility="collapsed")
        st.divider()

elif modo == "🎁 Materiais VIP & Simulados":
    st.title("🎁 Materiais VIP & Simulados")
    st.info("Conteúdo exclusivo disponível para membros.")

elif modo == "ℹ️ Créditos & Desenvolvimento":
    st.title("ℹ️ Créditos & Desenvolvimento")
    st.write("Desenvolvido por Edielson Samico - SAMICOIOT.")
