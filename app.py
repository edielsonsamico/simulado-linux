import streamlit as st
import random
import re
import importlib

# 1. FUNÇÃO DE LIMPEZA (SEM NÚMEROS)
def obter_nucleo_pergunta(pergunta):
    # Remove qualquer sequência numérica inicial e limpa espaços
    nucleo = re.sub(r'^(quest[ãa]o.*?\d+|q\d+|\d+)[:\.\-\s]+', '', pergunta.strip(), flags=re.IGNORECASE)
    return nucleo.lower().strip()

# 2. CARREGAMENTO ROBUSTO (NÃO QUEBRA SE FALTA ARQUIVO)
def carregar_banco_unico():
    pool_bruto = []
    # Tenta carregar apenas arquivos que existem
    for i in range(101, 111):
        try:
            modulo = importlib.import_module(f"topico{i}")
            if hasattr(modulo, f"POOL_{i}"):
                pool_bruto.extend(getattr(modulo, f"POOL_{i}"))
        except ImportError:
            continue # Pula se o arquivo não existir
            
    banco_limpo = {}
    for q in pool_bruto:
        nucleo = obter_nucleo_pergunta(q["pergunta"])
        if nucleo not in banco_limpo:
            q_copia = q.copy()
            # Garante que as opções existem
            q_copia['opcoes_fixas'] = q.get('opcoes', []).copy()
            random.shuffle(q_copia['opcoes_fixas'])
            banco_limpo[nucleo] = q_copia
            
    return list(banco_limpo.values())

# 3. APP PRINCIPAL
def main():
    st.set_page_config(page_title="Ambiente SAMICOIOT", layout="wide")

    # Inicialização segura
    if 'banco_questoes' not in st.session_state:
        banco = carregar_banco_unico()
        if not banco:
            st.error("Erro: Nenhum banco de questões foi carregado. Verifique se os arquivos topicoXXX.py existem.")
            return
        st.session_state.banco_questoes = banco
        st.session_state.simulado_ativo = random.sample(banco, k=min(40, len(banco)))

    # Menu
    modo = st.sidebar.radio("Navegação:", ["📖 Treino Geral", "🎯 Treino Focado", "⏱️ Simulado LPI"])

    if modo == "⏱️ Simulado LPI":
        st.title("⏱️ Simulado LPI")
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
    
    # Adicione aqui o tratamento das outras abas se desejar

if __name__ == "__main__":
    main()
