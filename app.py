import streamlit as st
import random
import time
import os

# ==========================================
# 1. FUNÇÕES DE EMBARALHAMENTO (SEMENTE ÚNICA)
# ==========================================
def obter_opcoes_embaralhadas(q):
    """Embaralha as opções usando o ID da questão como semente para manter consistência."""
    opcoes = q['opcoes'].copy()
    # Usamos o ID da questão como semente para a ordem ser sempre a mesma 
    # para aquela questão específica durante a sessão, mas variada entre questões.
    state = random.Random(q['id'])
    state.shuffle(opcoes)
    return opcoes

# ==========================================
# 2. CONFIGURAÇÃO DA INTERFACE & MÓDULOS (MANTENHA SUAS FUNÇÕES ORIGINAIS)
# ==========================================
st.set_page_config(page_title="Linux Essentials - Plataforma de Estudos", page_icon="🐧", layout="wide")

# ... (Mantenha as suas funções 'gerenciar_acesso_e_obter_metricas', 'desduplicar_questoes', etc.) ...

# ==========================================
# 3. BARRA LATERAL
# ==========================================
modo_selecionado = st.sidebar.radio(
    "Ambiente:", 
    [
        "📖 Área de Treino (Geral)", 
        "🎯 Treino por Tópico (Focado)", 
        "⏱️ Simulado LPI (Prova Real 40 Q)",
        "🎁 Materiais VIP & Simulados",
        "ℹ️ Créditos & Desenvolvimento"
    ]
)

# ==========================================
# 4. ESTRUTURA CORRETA DOS ELIFs (SOLUÇÃO DO ERRO)
# ==========================================
if modo_selecionado == "ℹ️ Créditos & Desenvolvimento":
    st.title("ℹ️ Créditos & Desenvolvimento")
    # ... (seu conteúdo)

elif modo_selecionado == "📖 Área de Treino (Geral)":
    st.title("📖 Área de Treino Geral")
    for idx, q in enumerate(st.session_state.questoes_treino):
        opcoes_embaralhadas = obter_opcoes_embaralhadas(q)
        st.markdown(f"### Questão {idx + 1} | `{q['topico']}`")
        st.markdown(f"**{q['pergunta']}**")
        resposta = st.radio("Opções:", opcoes_embaralhadas, index=None, key=f"t_{idx}")
        if resposta:
            if resposta == q['correta']:
                st.success("🎯 Resposta Correta!")
            else:
                st.error(f"❌ Incorreta. Certo: **{q['correta']}**")
        st.divider()

elif modo_selecionado == "🎯 Treino por Tópico (Focado)":
    st.title("🎯 Treino Direcionado por Tópicos")
    # ... (seu código de tópicos usando: opcoes = obter_opcoes_embaralhadas(q))

elif modo_selecionado == "⏱️ Simulado LPI (Prova Real 40 Q)":
    st.title("⏱️ Simulado Preparatório Oficial LPI")
    # ... (seu código do simulado usando: opcoes = obter_opcoes_embaralhadas(q))

elif modo_selecionado == "🎁 Materiais VIP & Simulados":
    st.title("🎁 Área VIP")
    # ... (seu código da área VIP)
