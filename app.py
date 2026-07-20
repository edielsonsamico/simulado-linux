import streamlit as st
import random
import os
import re

# ==========================================
# 1. FUNÇÕES AUXILIARES (DEFINIDAS NO TOPO)
# ==========================================
def desduplicar_questoes(lista_original):
    vistas = set()
    lista_limpa = []
    for q in lista_original:
        p = re.sub(r'^(quest[ãa]o(\s+avançada)?(\s+de\s+arquitetura)?\s+\d+|q\d+|\d+)[:\.\-\s]+', '', q["pergunta"].strip().lower())
        if p not in vistas:
            vistas.add(p)
            lista_limpa.append(q)
    return lista_limpa

def obter_opcoes_embaralhadas(q):
    opcoes = q['opcoes'].copy()
    state = random.Random(q['id'])
    state.shuffle(opcoes)
    return opcoes

# ==========================================
# 2. DADOS (MANTENHA A SUA ESTRUTURA)
# ==========================================
QUESTOES_POOL = desduplicar_questoes([
    {"id": 1, "topico": "Tópico 101", "pergunta": "Qual comando PCI?", "opcoes": ["lspci", "lsusb", "lsmod", "dmesg"], "correta": "lspci"},
    {"id": 2, "topico": "Tópico 102", "pergunta": "Qual diretório FHS?", "opcoes": ["/etc", "/var", "/usr", "/opt"], "correta": "/etc"}
    # ... adicione todas as suas questões aqui
])

# ==========================================
# 3. FUNÇÃO PRINCIPAL (CORREÇÃO DO ERRO)
# ==========================================
def main():
    # Inicialização SEGURA dentro da função main
    if 'iniciado' not in st.session_state:
        st.session_state.questoes_treino = list(QUESTOES_POOL)
        st.session_state.iniciado = True

    # SIDEBAR
    modo = st.sidebar.radio("Ambiente:", [
        "📖 Área de Treino (Geral)", 
        "🎯 Treino por Tópico (Focado)", 
        "⏱️ Simulado LPI (Prova Real 40 Q)",
        "🎁 Materiais VIP & Simulados",
        "ℹ️ Créditos & Desenvolvimento"
    ])

    # RENDERIZAÇÃO CONDICIONAL
    if modo == "📖 Área de Treino (Geral)":
        st.title("📖 Área de Treino Geral")
        for idx, q in enumerate(st.session_state.questoes_treino):
            opcoes = obter_opcoes_embaralhadas(q)
            st.markdown(f"**{q['pergunta']}**")
            res = st.radio(f"Opt_{idx}", opcoes, index=None, label_visibility="collapsed")
            if res == q['correta']: st.success("Correto!")
            elif res: st.error(f"Errado. Certo: {q['correta']}")
            st.divider()

    elif modo == "🎯 Treino por Tópico (Focado)":
        st.title("🎯 Treino por Tópico")
        # Coloque aqui a sua lógica de tópicos...

    elif modo == "⏱️ Simulado LPI (Prova Real 40 Q)":
        st.title("⏱️ Simulado LPI")
        # ...

    elif modo == "🎁 Materiais VIP & Simulados":
        st.title("🎁 Área VIP")
        # ...

    elif modo == "ℹ️ Créditos & Desenvolvimento":
        st.title("ℹ️ Créditos")
        # ...

if __name__ == "__main__":
    main()
