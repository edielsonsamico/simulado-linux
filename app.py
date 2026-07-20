import streamlit as st
import random
import re
import importlib

# ==========================================
# 1. LÓGICA DE LIMPEZA (CORE)
# ==========================================
def normalizar_texto(texto):
    # Remove prefixos numéricos de forma agressiva para identificar duplicatas
    texto_limpo = re.sub(r'^(quest[ãa]o(\s+avançada)?(\s+de\s+[a-z\s]+)?\s*\d+|q\d+|\d+)[:\.\-\s]+', '', texto.strip().lower())
    return " ".join(texto_limpo.split())

def carregar_e_limpar_banco():
    """Carrega de todos os tópicos e remove duplicatas na fonte."""
    pool_bruto = []
    for i in range(101, 111):
        try:
            modulo = importlib.import_module(f"topico{i}")
            if hasattr(modulo, f"POOL_{i}"):
                pool_bruto.extend(getattr(modulo, f"POOL_{i}"))
        except (ModuleNotFoundError, AttributeError):
            continue
    
    # Filtro rigoroso: se a pergunta normalizada já existe, pula
    vistas = set()
    lista_limpa = []
    for q in pool_bruto:
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

    # Inicialização ÚNICA e LIMPA
    if 'banco_questoes' not in st.session_state:
        st.session_state.banco_questoes = carregar_e_limpar_banco()
        st.session_state.iniciado = True

    st.sidebar.title("Ambiente SAMICOIOT")
    modo = st.sidebar.radio("Navegação:", [
        "📖 Área de Treino (Geral)", 
        "🎯 Treino por Tópico (Focado)", 
        "⏱️ Simulado LPI (Prova Real 40 Q)",
        "🎁 Materiais VIP & Simulados",
        "ℹ️ Créditos & Desenvolvimento"
    ])

    questoes = st.session_state.banco_questoes

    # --- ABA 1: TREINO GERAL ---
    if modo == "📖 Área de Treino (Geral)":
        st.title("📖 Área de Treino Geral")
        for q in questoes:
            st.markdown(f"**{q['pergunta']}**")
            opcoes = q['opcoes'].copy()
            random.shuffle(opcoes)
            res = st.radio(f"t_{q['id']}", opcoes, index=None, label_visibility="collapsed")
            if res == q['correta']: st.success("🎯 Correto!")
            elif res: st.error(f"❌ Errado. Certo: {q['correta']}")
            st.divider()

    # --- ABA 2: TREINO POR TÓPICO ---
    elif modo == "🎯 Treino por Tópico (Focado)":
        st.title("🎯 Treino por Tópico (Focado)")
        topicos = sorted(list(set(q['topico'] for q in questoes)))
        t = st.selectbox("Escolha o tópico:", topicos, key="sel_topico")
        for q in [q for q in questoes if q['topico'] == t]:
            st.markdown(f"**{q['pergunta']}**")
            opcoes = q['opcoes'].copy()
            random.shuffle(opcoes)
            res = st.radio(f"radio_{q['id']}_{t}", opcoes, index=None, label_visibility="collapsed")
            if res == q['correta']: st.success("🎯 Correto!")
            elif res: st.error(f"❌ Errado. Certo: {q['correta']}")
            st.divider()

    # --- ABA 3: SIMULADO ---
    elif modo == "⏱️ Simulado LPI (Prova Real 40 Q)":
        st.title("⏱️ Simulado LPI (Prova Real 40 Q)")
        if st.button("Gerar novo simulado"):
            # Garante que sorteia apenas das questões já limpas
            st.session_state.simulado_ativo = random.sample(questoes, k=min(40, len(questoes)))
            st.rerun()
            
        # Garante que, se não existir, cria o primeiro simulado
        if 'simulado_ativo' not in st.session_state:
            st.session_state.simulado_ativo = random.sample(questoes, k=min(40, len(questoes)))

        for idx, q in enumerate(st.session_state.simulado_ativo):
            st.markdown(f"**{q['pergunta']}**") # Removi o idx para não ter numerais
            opcoes = q['opcoes'].copy()
            random.shuffle(opcoes)
            st.radio(f"sim_{q['id']}", opcoes, index=None, label_visibility="collapsed")
            st.divider()

    elif modo == "🎁 Materiais VIP & Simulados":
        st.title("🎁 Materiais VIP & Simulados")
        st.info("Conteúdo exclusivo disponível para membros.")

    elif modo == "ℹ️ Créditos & Desenvolvimento":
        st.title("ℹ️ Créditos & Desenvolvimento")
        st.write("Desenvolvido por Edielson Samico - SAMICOIOT.")

if __name__ == "__main__":
    main()
