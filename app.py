import streamlit as st
import random
import re
import importlib

# ==========================================
# 1. FUNÇÕES DE LIMPEZA E LÓGICA (CORE)
# ==========================================
def normalizar_texto(texto):
    # Remove prefixos numéricos (ex: "33.", "Questão 33:", "Unix 145:")
    texto_limpo = re.sub(r'^(quest[ãa]o(\s+avançada)?(\s+de\s+[a-z\s]+)?\s*\d+|q\d+|\d+)[:\.\-\s]+', '', texto.strip().lower())
    return " ".join(texto_limpo.split())

def carregar_banco_de_dados():
    """Carrega questões de todos os arquivos topicoXXX.py e desduplica."""
    pool_total = []
    # Itera sobre seus arquivos de tópicos na pasta
    for i in range(101, 111):
        try:
            modulo = importlib.import_module(f"topico{i}")
            # Assume que cada arquivo tem uma lista chamada POOL_{i}
            if hasattr(modulo, f"POOL_{i}"):
                pool_total.extend(getattr(modulo, f"POOL_{i}"))
        except (ModuleNotFoundError, AttributeError):
            continue
    
    # Desduplicação baseada na pergunta normalizada
    vistas = set()
    lista_limpa = []
    for q in pool_total:
        p = normalizar_texto(q["pergunta"])
        if p not in vistas:
            vistas.add(p)
            lista_limpa.append(q)
    return lista_limpa

# ==========================================
# 2. APP PRINCIPAL
# ==========================================
def main():
    st.set_page_config(page_title="Ambiente SAMICOIOT", layout="wide")

    # Inicialização SEGURA do Session State
    if 'banco_questoes' not in st.session_state:
        st.session_state.banco_questoes = carregar_banco_de_dados()
        st.session_state.simulado_ativo = random.sample(st.session_state.banco_questoes, k=min(40, len(st.session_state.banco_questoes)))
        st.session_state.iniciado = True

    st.sidebar.title("Ambiente SAMICOIOT")
    modo = st.sidebar.radio("Navegação:", [
        "📖 Área de Treino (Geral)", 
        "🎯 Treino por Tópico (Focado)", 
        "⏱️ Simulado LPI (Prova Real 40 Q)",
        "🎁 Materiais VIP & Simulados",
        "ℹ️ Créditos & Desenvolvimento"
    ])

    # Acesso centralizado ao banco
    questoes = st.session_state.banco_questoes

    # --- ABA 1: TREINO GERAL ---
    if modo == "📖 Área de Treino (Geral)":
        st.title("📖 Área de Treino Geral")
        for idx, q in enumerate(questoes):
            opcoes = q['opcoes'].copy()
            random.shuffle(opcoes) # Embaralhamento real
            st.markdown(f"**{q['pergunta']}**")
            res = st.radio(f"treino_{q['id']}", opcoes, index=None, label_visibility="collapsed")
            if res == q['correta']: st.success("🎯 Correto!")
            elif res: st.error(f"❌ Errado. Certo: {q['correta']}")
            st.divider()

    # --- ABA 2: TREINO POR TÓPICO ---
    elif modo == "🎯 Treino por Tópico (Focado)":
        st.title("🎯 Treino por Tópico (Focado)")
        topicos = sorted(list(set(q['topico'] for q in questoes)))
        t = st.selectbox("Escolha o tópico:", topicos, key="select_topic_main")
        
        # Filtra questões e usa chave dinâmica com o tópico 't'
        for idx, q in enumerate([q for q in questoes if q['topico'] == t]):
            opcoes = q['opcoes'].copy()
            random.shuffle(opcoes)
            st.markdown(f"**{q['pergunta']}**")
            # Chave única dinâmica: radio_{id}_{topico}
            res = st.radio(f"radio_{q['id']}_{t}", opcoes, index=None, label_visibility="collapsed")
            if res == q['correta']: st.success("🎯 Correto!")
            elif res: st.error(f"❌ Errado. Certo: {q['correta']}")
            st.divider()

    # --- ABA 3: SIMULADO ---
    elif modo == "⏱️ Simulado LPI (Prova Real 40 Q)":
        st.title("⏱️ Simulado LPI (Prova Real 40 Q)")
        if st.button("Gerar novo simulado (Inédito)"):
            st.session_state.simulado_ativo = random.sample(questoes, k=min(40, len(questoes)))
            st.rerun()
            
        for idx, q in enumerate(st.session_state.simulado_ativo):
            opcoes = q['opcoes'].copy()
            random.shuffle(opcoes)
            st.markdown(f"**{idx+1}. {q['pergunta']}**")
            # Chave única para o simulado
            st.radio(f"sim_{q['id']}", opcoes, index=None, label_visibility="collapsed")
            st.divider()

    # --- ABA 4: MATERIAIS VIP ---
    elif modo == "🎁 Materiais VIP & Simulados":
        st.title("🎁 Materiais VIP & Simulados")
        st.info("Conteúdo exclusivo disponível para membros.")

    # --- ABA 5: CRÉDITOS ---
    elif modo == "ℹ️ Créditos & Desenvolvimento":
        st.title("ℹ️ Créditos & Desenvolvimento")
        st.write("Desenvolvido por Edielson Samico - SAMICOIOT.")

if __name__ == "__main__":
    main()
