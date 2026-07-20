import streamlit as st
import random
import re
import importlib

# 1. FUNÇÃO DE LIMPEZA RIGOROSA
def obter_nucleo_pergunta(pergunta):
    # Remove qualquer sequência numérica inicial (ex: "1.", "Questão 221:", "Q221:")
    nucleo = re.sub(r'^(quest[ãa]o.*?\d+|q\d+|\d+)[:\.\-\s]+', '', pergunta.strip(), flags=re.IGNORECASE)
    return nucleo.lower().strip()

# 2. CARREGAMENTO SEM DUPLICATAS
def carregar_banco_unico():
    pool_bruto = []
    for i in range(101, 111):
        try:
            modulo = importlib.import_module(f"topico{i}")
            if hasattr(modulo, f"POOL_{i}"):
                pool_bruto.extend(getattr(modulo, f"POOL_{i}"))
        except: continue
    
    banco_limpo = {}
    for q in pool_bruto:
        nucleo = obter_nucleo_pergunta(q["pergunta"])
        # Só adiciona ao banco se este núcleo ainda não existir
        if nucleo not in banco_limpo:
            q_copia = q.copy()
            q_copia['opcoes_fixas'] = q['opcoes'].copy()
            random.shuffle(q_copia['opcoes_fixas'])
            banco_limpo[nucleo] = q_copia
            
    return list(banco_limpo.values())

# 3. APP PRINCIPAL
def main():
    st.set_page_config(page_title="Ambiente SAMICOIOT", layout="wide")

    if 'banco_questoes' not in st.session_state:
        st.session_state.banco_questoes = carregar_banco_unico()
        st.session_state.simulado_ativo = random.sample(
            st.session_state.banco_questoes, 
            k=min(40, len(st.session_state.banco_questoes))
        )

    # Sidebar e Navegação
    modo = st.sidebar.radio("Navegação:", ["📖 Treino Geral", "🎯 Treino Focado", "⏱️ Simulado LPI"])

    if modo == "⏱️ Simulado LPI":
        if st.button("Gerar novo simulado"):
            st.session_state.simulado_ativo = random.sample(
                st.session_state.banco_questoes, 
                k=min(40, len(st.session_state.banco_questoes))
            )
            st.rerun()
        
        for i, q in enumerate(st.session_state.simulado_ativo):
            st.markdown(f"**{i+1}. {q['pergunta']}**")
            st.radio(f"sim_{i}", q['opcoes_fixas'], key=f"ans_{i}", index=None, label_visibility="collapsed")
            st.divider()
    # ... (demais abas)
