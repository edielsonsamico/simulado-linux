import streamlit as st
import random
import re
import importlib
import hashlib

# 1. FUNÇÃO DE LIMPEZA E HASH (AGRUPAMENTO POR NÚCLEO)
def gerar_hash_conteudo(pergunta):
    """
    Cria uma impressão digital ignorando números de questão e numerações iniciais.
    """
    texto_limpo = re.sub(r'^(quest[ãa]o.*?\d+|q\d+|\d+)\s*[\.\:\-]?\s*', '', pergunta.strip(), flags=re.IGNORECASE)
    texto_limpo = " ".join(texto_limpo.lower().split())
    return hashlib.md5(texto_limpo.encode('utf-8')).hexdigest()

def carregar_banco_unico():
    pool_total = []
    # Tenta carregar módulos de tópicos de 101 a 110
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
            q_copia['opcoes_fixas'] = q.get('opcoes', []).copy()
            random.shuffle(q_copia['opcoes_fixas'])
            banco_final[h] = q_copia
    return list(banco_final.values())

# 2. APP PRINCIPAL COM MENU COMPLETO E CORREÇÃO VIP
def main():
    st.set_page_config(page_title="Ambiente SAMICOIOT", layout="wide")

    if 'banco_questoes' not in st.session_state:
        st.session_state.banco_questoes = carregar_banco_unico()
        st.session_state.simulado_ativo = random.sample(
            st.session_state.banco_questoes, 
            k=min(40, len(st.session_state.banco_questoes))
        )

    # MENU COMPLETO E FIXO
    st.sidebar.title("Ambiente SAMICOIOT")
    st.sidebar.write("Navegação:")
    modo = st.sidebar.radio(
        "Selecione:", 
        [
            "📖 Área de Treino (Geral)", 
            "🎯 Treino por Tópico (Focado)", 
            "⏱️ Simulado LPI (Prova Real 40 Q)",
            "🎁 Materiais VIP & Simulados",
            "ℹ️ Créditos & Desenvolvimento"
        ],
        key="menu_navegacao"
    )

    # LÓGICA DE EXIBIÇÃO
    if modo == "📖 Área de Treino (Geral)":
        st.title("📖 Área de Treino Geral")
        for q in st.session_state.banco_questoes:
            st.markdown(f"**{q['pergunta']}**")
            st.radio(f"t_{q['id']}", q['opcoes_fixas'], index=None, label_visibility="collapsed")
            st.divider()

    elif modo == "🎯 Treino por Tópico (Focado)":
        st.title("🎯 Treino por Tópico (Focado)")
        topicos = sorted(list(set(q.get('topico', 'Geral') for q in st.session_state.banco_questoes)))
        t = st.selectbox("Escolha o tópico:", topicos, key="sel_t")
        for q in [q for q in st.session_state.banco_questoes if q.get('topico') == t]:
            st.markdown(f"**{q['pergunta']}**")
            st.radio(f"radio_{q['id']}_{t}", q['opcoes_fixas'], index=None, label_visibility="collapsed")
            st.divider()

    elif modo == "⏱️ Simulado LPI (Prova Real 40 Q)":
        st.title("⏱️ Simulado LPI (Prova Real 40 Q)")
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
            
    elif modo == "🎁 Materiais VIP & Simulados":
        st.title("🎁 Materiais VIP & Simulados")
        st.subheader("Conteúdo Exclusivo")
        # Substitua os links abaixo pelos endereços reais dos seus materiais
        materiais = {
            "Guia de Comandos LPI": "#",
            "Simulado LPI - Módulos Avançados": "#",
            "Acesso à Área de Membros": "#"
        }
        for nome, link in materiais.items():
            st.markdown(f"- [{nome}]({link})")
        st.warning("Área restrita. Certifique-se de estar logado.")
        
    elif modo == "ℹ️ Créditos & Desenvolvimento":
        st.title("ℹ️ Créditos & Desenvolvimento")
        st.write("Desenvolvido por Edielson Samico - SAMICOIOT.")

if __name__ == "__main__":
    main()
