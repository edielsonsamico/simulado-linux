import streamlit as st
import random
import re
import importlib
import hashlib

# ==========================================
# 1. FUNÇÃO DE LIMPEZA E HASH (NÃO DÁ PRA ERRAR)
# ==========================================
def criar_hash_pergunta(texto):
    """Cria uma impressão digital única da pergunta."""
    # Remove TUDO que não for letra ou número antes de criar o hash
    texto_limpo = re.sub(r'[^a-zA-Z0-9]', '', texto.lower())
    return hashlib.md5(texto_limpo.encode('utf-8')).hexdigest()

def carregar_e_limpar_banco():
    pool_total = []
    for i in range(101, 111):
        try:
            modulo = importlib.import_module(f"topico{i}")
            if hasattr(modulo, f"POOL_{i}"):
                pool_total.extend(getattr(modulo, f"POOL_{i}"))
        except: continue
    
    # Dicionário usando o Hash como chave única
    banco_unico = {}
    for q in pool_total:
        h = criar_hash_pergunta(q["pergunta"])
        if h not in banco_unico:
            q_copia = q.copy()
            # Embaralhamento único e persistente
            q_copia['opcoes_fixas'] = q['opcoes'].copy()
            random.shuffle(q_copia['opcoes_fixas'])
            banco_unico[h] = q_copia
            
    return list(banco_unico.values())

# ==========================================
# 2. APP PRINCIPAL
# ==========================================
def main():
    st.set_page_config(page_title="Ambiente SAMICOIOT", layout="wide")

    if 'banco_questoes' not in st.session_state:
        st.session_state.banco_questoes = carregar_e_limpar_banco()
        st.session_state.simulado_ativo = random.sample(
            st.session_state.banco_questoes, 
            k=min(40, len(st.session_state.banco_questoes))
        )

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
            elif res: st.error("❌ Errado.")
            st.divider()

    elif modo == "🎯 Treino por Tópico (Focado)":
        topicos = sorted(list(set(q['topico'] for q in st.session_state.banco_questoes)))
        t = st.selectbox("Escolha o tópico:", topicos, key="sel_t")
        for q in [q for q in st.session_state.banco_questoes if q['topico'] == t]:
            st.markdown(f"**{q['pergunta']}**")
            res = st.radio(f"radio_{q['id']}_{t}", q['opcoes_fixas'], index=None, label_visibility="collapsed")
            if res == q['correta']: st.success("🎯 Correto!")
            elif res: st.error("❌ Errado.")
            st.divider()

    elif modo == "⏱️ Simulado LPI (Prova Real 40 Q)":
        if st.button("Gerar novo simulado"):
            st.session_state.simulado_ativo = random.sample(
                st.session_state.banco_questoes, 
                k=min(40, len(st.session_state.banco_questoes))
            )
            st.rerun()
        
        # Renderização do simulado final
        for i, q in enumerate(st.session_state.simulado_ativo):
            st.markdown(f"**{q['pergunta']}**")
            # A chave inclui o ID original da questão para garantir unicidade
            st.radio(f"sim_{q['id']}", q['opcoes_fixas'], index=None, label_visibility="collapsed")
            st.divider()

    elif modo == "🎁 Materiais VIP & Simulados":
        st.title("Materiais VIP")
    elif modo == "ℹ️ Créditos & Desenvolvimento":
        st.title("Créditos")
        st.write("Desenvolvido por Edielson Samico.")

if __name__ == "__main__":
    main()
