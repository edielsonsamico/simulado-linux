import streamlit as st
import random
import re

# ==========================================
# 1. FUNÇÕES DE LIMPEZA E LÓGICA (CORE)
# ==========================================
def normalizar_texto(texto):
    # Remove prefixos de numeração de questões para identificar duplicatas reais
    # Remove: "Questão 33:", "33.", "Questão Avançada 331:", etc.
    texto_limpo = re.sub(r'^(quest[ãa]o(\s+avançada)?(\s+de\s+[a-z\s]+)?\s*\d+|q\d+|\d+)[:\.\-\s]+', '', texto.strip().lower())
    return " ".join(texto_limpo.split())

def desduplicar_questoes(lista_original):
    vistas = set()
    lista_limpa = []
    for q in lista_original:
        p = normalizar_texto(q["pergunta"])
        if p not in vistas:
            vistas.add(p)
            lista_limpa.append(q)
    return lista_limpa

def obter_opcoes_embaralhadas(q):
    # Embaralhamento aleatório real (não fixo)
    opcoes = q['opcoes'].copy()
    random.shuffle(opcoes)
    return opcoes

# ==========================================
# 2. BANCO DE DADOS (INSIRA TODAS SUAS QUESTÕES AQUI)
# ==========================================
QUESTOES_POOL = desduplicar_questoes([
    {"id": 1, "topico": "Tópico 103: Comandos", "pergunta": "Qual caractere canalizador conecta o stdout de um comando direto no stdin do comando seguinte?", "opcoes": ["|", ">", "<", ">>"], "correta": "|"},
    {"id": 2, "topico": "Tópico 105: Scripts e SQL", "pergunta": "Qual operador lógico condicional do bash é usado para testar se um arquivo regular existe (-f)?", "opcoes": ["test -f", "test -d", "test -z", "test -x"], "correta": "test -f"},
    {"id": 3, "topico": "Tópico 107: Administração", "pergunta": "Qual opção do crontab remove permanentemente todas as tarefas agendadas do usuário ativo?", "opcoes": ["crontab -r", "crontab -l", "crontab -e", "crontab -d"], "correta": "crontab -r"},
    # [ADICIONE O RESTANTE DO SEU BANCO AQUI]
])

# ==========================================
# 3. APP PRINCIPAL (ESTRUTURA BLINDADA)
# ==========================================
st.set_page_config(page_title="Linux Essentials - SAMICOIOT", layout="wide")

# Inicialização segura
if 'iniciado' not in st.session_state:
    st.session_state.simulado_ativo = random.sample(QUESTOES_POOL, k=min(40, len(QUESTOES_POOL)))
    st.session_state.iniciado = True

# SIDEBAR
st.sidebar.title("Ambiente SAMICOIOT")
modo = st.sidebar.radio("Navegação:", [
    "📖 Área de Treino (Geral)", 
    "🎯 Treino por Tópico (Focado)", 
    "⏱️ Simulado LPI (Prova Real 40 Q)",
    "🎁 Materiais VIP & Simulados",
    "ℹ️ Créditos & Desenvolvimento"
])

# ==========================================
# 4. LÓGICA DE RENDERIZAÇÃO
# ==========================================
if modo == "📖 Área de Treino (Geral)":
    st.title("📖 Área de Treino Geral")
    for idx, q in enumerate(QUESTOES_POOL):
        opcoes = obter_opcoes_embaralhadas(q)
        st.markdown(f"**{q['pergunta']}**")
        res = st.radio(f"treino_{q['id']}", opcoes, index=None, label_visibility="collapsed")
        if res == q['correta']: st.success("🎯 Correto!")
        elif res: st.error(f"❌ Errado. Certo: {q['correta']}")
        st.divider()

elif modo == "🎯 Treino por Tópico (Focado)":
    st.title("🎯 Treino por Tópico (Focado)")
    topicos = sorted(list(set(q['topico'] for q in QUESTOES_POOL)))
    t = st.selectbox("Escolha o tópico:", topicos)
    for idx, q in enumerate([q for q in QUESTOES_POOL if q['topico'] == t]):
        opcoes = obter_opcoes_embaralhadas(q)
        st.markdown(f"**{q['pergunta']}**")
        res = st.radio(f"topico_{q['id']}", opcoes, index=None, label_visibility="collapsed")
        if res == q['correta']: st.success("🎯 Correto!")
        elif res: st.error(f"❌ Errado. Certo: {q['correta']}")
        st.divider()

elif modo == "⏱️ Simulado LPI (Prova Real 40 Q)":
    st.title("⏱️ Simulado LPI (Prova Real 40 Q)")
    if st.button("Gerar novo simulado (Inédito)"):
        st.session_state.simulado_ativo = random.sample(QUESTOES_POOL, k=min(40, len(QUESTOES_POOL)))
        st.rerun()
        
    for idx, q in enumerate(st.session_state.simulado_ativo):
        opcoes = obter_opcoes_embaralhadas(q)
        st.markdown(f"**{idx+1}. {q['pergunta']}**")
        st.radio(f"sim_{idx}_{q['id']}", opcoes, index=None, label_visibility="collapsed")
        st.divider()

elif modo == "🎁 Materiais VIP & Simulados":
    st.title("🎁 Materiais VIP & Simulados")
    st.info("Conteúdo exclusivo disponível para membros.")

elif modo == "ℹ️ Créditos & Desenvolvimento":
    st.title("ℹ️ Créditos & Desenvolvimento")
    st.write("Desenvolvido por Edielson Samico - SAMICOIOT.")
