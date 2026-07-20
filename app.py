import streamlit as st
import random
import re
import importlib

# ==========================================
# 1. FUNÇÃO DE LIMPEZA DEFINITIVA
# ==========================================
def normalizar_texto(texto):
    # Esta regex remove TUDO que for número ou texto identificador no início da frase
    # Ex: "Questão 244:", "Q216:", "221." -> tudo vira vazio
    texto_limpo = re.sub(r'^(quest[ãa]o.*?\d+|q\d+|\d+)[:\.\-\s]+', '', texto.strip().lower())
    return " ".join(texto_limpo.split())

def carregar_e_limpar_banco():
    pool_total = []
    # Carrega de todos os arquivos tópicos
    for i in range(101, 111):
        try:
            modulo = importlib.import_module(f"topico{i}")
            if hasattr(modulo, f"POOL_{i}"):
                pool_total.extend(getattr(modulo, f"POOL_{i}"))
        except: continue
    
    # Filtro de desduplicação rigoroso
    vistas = set()
    lista_limpa = []
    for q in pool_total:
        p = normalizar_texto(q["pergunta"])
        if p not in vistas:
            vistas.add(p)
            q_copia = q.copy()
            q_copia['opcoes_fixas'] = q['opcoes'].copy()
            random.shuffle(q_copia['opcoes_fixas']) # Embaralha uma única vez
            lista_limpa.append(q_copia)
    return lista_limpa

# ==========================================
# 2. APP PRINCIPAL
# ==========================================
def main():
    st.set_page_config(page_title="Ambiente SAMICOIOT", layout="wide")

    if 'banco_questoes' not in st.session_state:
        st.session_state.banco_questoes = carregar_e_limpar_banco()
        st.session_state.simulado_ativo = random.sample(st.session_state.banco_questoes, k=min(40, len(st.session_state.banco_questoes)))

    st.sidebar.title("Ambiente SAMICOIOT")
    modo = st.sidebar.radio("Navegação:", [
        "📖 Área de Treino (Geral)", 
        "🎯 Treino por Tópico (Focado)", 
        "⏱️ Simulado LPI (Prova Real 40 Q)",
        "🎁 Materiais VIP & Simulados",
        "ℹ️ Créditos & Desenvolvimento"
    ])

    # --- RENDERIZAÇÃO ESTÁVEL ---
    if modo == "📖 Área de Treino (Geral)":
        for q in st.session_state.banco_questoes:
            st.markdown(f"**{q['pergunta']}**")
            res = st.radio(f"t_{q['id']}", q['opcoes_fixas'], index=None, label_visibility="collapsed")
            if res == q['correta']: st.success("🎯 Correto!")
            elif res: st.error(f"❌ Errado. Certo: {q['correta']}")
            st.divider()

    elif modo == "🎯 Treino por Tópico (Focado)":
        topicos = sorted(list(set(q['topico'] for q in st.session_state.banco_questoes)))
        t = st.selectbox("Escolha o tópico:", topicos, key="sel_t")
        for q in [q for q in st.session_state.banco_questoes if q['topico'] == t]:
            st.markdown(f"**{q['pergunta']}**")
            res = st.radio(f"radio_{q['id']}_{t}", q['opcoes_fixas'], index=None, label_visibility="collapsed")
            if res == q['correta']: st.success("🎯 Correto!")
            elif res: st.error(f"❌ Errado. Certo: {q['correta']}")
            st.divider()

    elif modo == "⏱️ Simulado LPI (Prova Real 40 Q)":
        if st.button("Gerar novo simulado"):
            st.session_state.simulado_ativo = random.sample(st.session_state.banco_questoes, k=min(40, len(st.session_state.banco_questoes)))
            st.rerun()
        for q in st.session_state.simulado_ativo:
            st.markdown(f"**{q['pergunta']}**")
            st.radio(f"sim_{q['id']}", q['opcoes_fixas'], index=None, label_visibility="collapsed")
            st.divider()
    
    elif modo == "🎁 Materiais VIP & Simulados":
        st.title("Materiais VIP")
    elif modo == "ℹ️ Créditos & Desenvolvimento":
        st.title("Créditos")
        st.write("Desenvolvido por Edielson Samico.")

if __name__ == "__main__":
    main()
