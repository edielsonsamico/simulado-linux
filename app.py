import streamlit as st
import random
import re
import importlib
import hashlib

# 1. FUNÇÃO DE LIMPEZA E HASH (AGRUPAMENTO POR NÚCLEO)
def gerar_hash_conteudo(pergunta):
    texto_limpo = re.sub(r'^(quest[ãa]o.*?\d+|q\d+|\d+)[:\.\-\s]+', '', pergunta.strip(), flags=re.IGNORECASE)
    texto_limpo = " ".join(texto_limpo.lower().split())
    return hashlib.md5(texto_limpo.encode('utf-8')).hexdigest()

def carregar_banco_unico():
    pool_total = []
    for i in range(101, 111):
        try:
            modulo = importlib.import_module(f"topico{i}")
            if hasattr(modulo, f"POOL_{i}"):
                pool_total.extend(getattr(modulo, f"POOL_{i}"))
        except: continue
    
    banco_final = {}
    for q in pool_total:
        h = gerar_hash_conteudo(q["pergunta"])
        if h not in banco_final:
            q_copia = q.copy()
            q_copia['opcoes_fixas'] = q['opcoes'].copy()
            random.shuffle(q_copia['opcoes_fixas'])
            banco_final[h] = q_copia
    return list(banco_final.values())

# 2. APP PRINCIPAL COM MENU FIXO
def main():
    st.set_page_config(page_title="Ambiente SAMICOIOT", layout="wide")

    if 'banco_questoes' not in st.session_state:
        st.session_state.banco_questoes = carregar_banco_unico()
        st.session_state.simulado_ativo = random.sample(
            st.session_state.banco_questoes, 
            k=min(40, len(st.session_state.banco_questoes))
        )

    # MENU DEFINIDO NA SIDEBAR
    st.sidebar.title("Ambiente SAMICOIOT")
    st.sidebar.write("Navegação:")
    modo = st.sidebar.radio(
        "Selecione:", 
        ["📖 Treino Geral", "🎯 Treino Focado", "⏱️ Simulado LPI"],
        key="menu_navegacao"
    )

    # LÓGICA DE EXIBIÇÃO BASEADA NO MENU
    if modo == "📖 Treino Geral":
        st.title("📖 Área de Treino Geral")
        for q in st.session_state.banco_questoes:
            st.markdown(f"**{q['pergunta']}**")
            st.radio(f"t_{q['id']}", q['opcoes_fixas'], index=None, label_visibility="collapsed")
            st.divider()

    elif modo == "🎯 Treino Focado":
        st.title("🎯 Treino por Tópico")
        topicos = sorted(list(set(q['topico'] for q in st.session_state.banco_questoes)))
        t = st.selectbox("Escolha o tópico:", topicos, key="sel_t")
        for q in [q for q in st.session_state.banco_questoes if q['topico'] == t]:
            st.markdown(f"**{q['pergunta']}**")
            st.radio(f"radio_{q['id']}_{t}", q['opcoes_fixas'], index=None, label_visibility="collapsed")
            st.divider()

    elif modo == "⏱️ Simulado LPI":
        st.title("⏱️ Simulado LPI")
        if st.button("Gerar novo simulado"):
            st.session_state.simulado_ativo = random.sample(
                st.session_state.banco_questoes, 
                k=min(40, len(st.session_state.banco_questoes))
            )
            st.rerun()
        
        for i, q in enumerate(st.session_state.simulado_ativo):
            st.markdown(f"**{i+1}. {q['pergunta']}**")
            st.radio(f"sim_{q['id']}", q['opcoes_fixas'], key=f"ans_{i}", index=None, label_visibility="collapsed")
            st.divider()

if __name__ == "__main__":
    main()
