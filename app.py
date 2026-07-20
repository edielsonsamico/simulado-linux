import streamlit as st
import random
import re
import importlib
import hashlib

# ==========================================
# 1. LÓGICA DE LIMPEZA E AGRUPAMENTO
# ==========================================
def gerar_hash_conteudo(pergunta):
    """Cria uma impressão digital apenas do texto, ignorando a numeração."""
    # Remove qualquer sequência de números no início da string
    texto_limpo = re.sub(r'^(quest[ãa]o.*?\d+|q\d+|\d+)[:\.\-\s]+', '', pergunta.strip(), flags=re.IGNORECASE)
    # Remove espaços extras e converte para minúsculas
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
    
    # Dicionário de controle: A chave é o HASH do conteúdo
    # Isso garante que perguntas iguais (mesmo com números diferentes) sejam ignoradas
    banco_final = {}
    for q in pool_total:
        h = gerar_hash_conteudo(q["pergunta"])
        if h not in banco_final:
            q_copia = q.copy()
            q_copia['opcoes_fixas'] = q['opcoes'].copy()
            random.shuffle(q_copia['opcoes_fixas'])
            banco_final[h] = q_copia
            
    return list(banco_final.values())

# ==========================================
# 2. APP PRINCIPAL
# ==========================================
def main():
    st.set_page_config(page_title="Ambiente SAMICOIOT", layout="wide")

    if 'banco_questoes' not in st.session_state:
        st.session_state.banco_questoes = carregar_banco_unico()
        # O simulado é sorteado a partir do banco já filtrado de duplicatas
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

    # --- ABA: TREINO GERAL ---
    if modo == "📖 Área de Treino (Geral)":
        for q in st.session_state.banco_questoes:
            st.markdown(f"**{q['pergunta']}**")
            res = st.radio(f"t_{q['id']}", q['opcoes_fixas'], index=None, label_visibility="collapsed")
            if res == q['correta']: st.success("🎯 Correto!")
            elif res: st.error("❌ Errado.")
            st.divider()

    # --- ABA: TREINO POR TÓPICO ---
    elif modo == "🎯 Treino por Tópico (Focado)":
        topicos = sorted(list(set(q['topico'] for q in st.session_state.banco_questoes)))
        t = st.selectbox("Escolha o tópico:", topicos, key="sel_t")
        for q in [q for q in st.session_state.banco_questoes if q['topico'] == t]:
            st.markdown(f"**{q['pergunta']}**")
            res = st.radio(f"radio_{q['id']}_{t}", q['opcoes_fixas'], index=None, label_visibility="collapsed")
            if res == q['correta']: st.success("🎯 Correto!")
            elif res: st.error("❌ Errado.")
            st.divider()

    # --- ABA: SIMULADO ---
    elif modo == "⏱️ Simulado LPI (Prova Real 40 Q)":
        if st.button("Gerar novo simulado"):
            st.session_state.simulado_ativo = random.sample(
                st.session_state.banco_questoes, 
                k=min(40, len(st.session_state.banco_questoes))
            )
            st.rerun()
        
        # Exibição com numeração original da pergunta
        for i, q in enumerate(st.session_state.simulado_ativo):
            st.markdown(f"**{i+1}. {q['pergunta']}**")
            st.radio(f"sim_{q['id']}", q['opcoes_fixas'], index=None, label_visibility="collapsed")
            st.divider()

    elif modo == "🎁 Materiais VIP & Simulados":
        st.title("Materiais VIP")
    elif modo == "ℹ️ Créditos & Desenvolvimento":
        st.title("Créditos")
        st.write("Desenvolvido por Edielson Samico.")

if __name__ == "__main__":
    main()
