import streamlit as st
import random
import time
import os

# ==========================================
# 1. FUNÇÃO DE EMBARALHAMENTO COM SEMENTE (SEGURO)
# ==========================================
def obter_opcoes_embaralhadas(q):
    """Embaralha as opções usando o ID da questão como semente."""
    opcoes = q['opcoes'].copy()
    state = random.Random(q['id']) # Semente fixa por ID para não mudar ao rolar a página
    state.shuffle(opcoes)
    return opcoes

# ==========================================
# 2. SISTEMA DE MONITORIZAÇÃO E CONFIGURAÇÃO
# ==========================================
@st.cache_resource
def obter_armazenamento_global():
    return {
        "usuarios_online": {}, "registro_visitas": set(), "visitas_totais": 0, "placar_lideres": {}
    }

memoria_global = obter_armazenamento_global()

def gerenciar_acesso_e_obter_metricas():
    if "usuario_uid" not in st.session_state:
        st.session_state.usuario_uid = f"user_{int(time.time())}_{random.randint(1000, 9999)}"
    uid_atual = st.session_state.usuario_uid
    agora = time.time()
    memoria_global["usuarios_online"][uid_atual] = agora
    if uid_atual not in memoria_global["registro_visitas"]:
        memoria_global["registro_visitas"].add(uid_atual)
        memoria_global["visitas_totais"] += 1
    return max(1, len(memoria_global["usuarios_online"])), memoria_global["visitas_totais"]

# ==========================================
# 3. DADOS DO SIMULADO (MANTENHA A SUA ESTRUTURA)
# ==========================================
# (Aqui entram as suas listas QUESTOES_POOL_RAW e QUESTOES_VIP_REPOSITORIO_COMPLETO que tínhamos)
# [IMPORTANTE: Se as suas variáveis QUESTOES_POOL estiverem em arquivos externos .py, certifique-se que eles estão na pasta]

# ==========================================
# 4. CONFIGURAÇÃO E SIDEBAR
# ==========================================
st.set_page_config(page_title="Linux Essentials", layout="wide")

num_online, num_visitas = gerenciar_acesso_e_obter_metricas()
st.sidebar.metric("🟢 Online", num_online)
nome_usuario = st.sidebar.text_input("Seu Nome:")

modo_selecionado = st.sidebar.radio("Ambiente:", [
    "📖 Área de Treino (Geral)", 
    "🎯 Treino por Tópico (Focado)", 
    "⏱️ Simulado LPI (Prova Real 40 Q)",
    "🎁 Materiais VIP & Simulados",
    "ℹ️ Créditos & Desenvolvimento"
])

# ==========================================
# 5. ABAS DO SISTEMA (IMPLEMENTAÇÃO COMPLETA)
# ==========================================
if modo_selecionado == "📖 Área de Treino (Geral)":
    st.title("📖 Área de Treino Geral")
    for idx, q in enumerate(st.session_state.questoes_treino):
        opcoes = obter_opcoes_embaralhadas(q) # <--- EMBARALHADO
        st.markdown(f"**{q['pergunta']}**")
        res = st.radio(f"Opt_{idx}", opcoes, index=None, label_visibility="collapsed")
        if res == q['correta']: st.success("Correto!")
        elif res: st.error(f"Errado. Certo: {q['correta']}")
        st.divider()

elif modo_selecionado == "🎯 Treino por Tópico (Focado)":
    st.title("🎯 Treino por Tópico")
    # ... (seu código de filtragem por tópico com: obter_opcoes_embaralhadas(q))

elif modo_selecionado == "⏱️ Simulado LPI (Prova Real 40 Q)":
    st.title("⏱️ Simulado Oficial")
    # ... (seu código completo do simulado com: obter_opcoes_embaralhadas(q))

elif modo_selecionado == "🎁 Materiais VIP & Simulados":
    st.title("🎁 Área VIP")
    # ... (seu código da área VIP com: obter_opcoes_embaralhadas(q))

elif modo_selecionado == "ℹ️ Créditos & Desenvolvimento":
    st.title("ℹ️ Créditos")
    # ... (seu código de créditos)
