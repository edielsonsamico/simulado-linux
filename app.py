import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time

# INICIALIZA O POOL VAZIO
QUESTOES_POOL = []

# IMPORTAÇÃO SEGURA: CARREGA APENAS OS ARQUIVOS QUE EXISTIREM
try:
    from topico101 import POOL_101
    QUESTOES_POOL += POOL_101
except Exception: pass

try:
    from topico102 import POOL_102
    QUESTOES_POOL += POOL_102
except Exception: pass

try:
    from topico103 import POOL_103
    QUESTOES_POOL += POOL_103
except Exception: pass

try:
    from topico104 import POOL_104
    QUESTOES_POOL += POOL_104
except Exception: pass

try:
    from topico105 import POOL_105
    QUESTOES_POOL += POOL_105
except Exception: pass

try:
    from topico106 import POOL_106
    QUESTOES_POOL += POOL_106
except Exception: pass

try:
    from topico107 import POOL_107
    QUESTOES_POOL += POOL_107
except Exception: pass

try:
    from topico108 import POOL_108
    QUESTOES_POOL += POOL_108
except Exception: pass

try:
    from topico109 import POOL_109
    QUESTOES_POOL += POOL_109
except Exception: pass

try:
    from topico110 import POOL_110
    QUESTOES_POOL += POOL_110
except Exception: pass

if not QUESTOES_POOL:
    QUESTOES_POOL = [{
        "id": 1, "topico": "Geral", 
        "pergunta": "O simulador está carregando os bancos de dados...", 
        "opcoes": ["Aguardar", "Atualizar"], "correta": "Aguardar", 
        "explicacao": "Carregando arquivos."
    }]

st.set_page_config(page_title="Linux Essentials - Plataforma de Estudos", page_icon="🐧", layout="wide")

st.markdown("""
    <style>
        div[data-testid="stRadio"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
            font-weight: 500 !important;
            color: #1E293B !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label [data-testid="stWidgetCircle"] {
            border: 2px solid #1E3A8A !important;
            background-color: #F1F5F9 !important;
            box-shadow: 0px 1px 3px rgba(0,0,0,0.1);
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label:hover [data-testid="stWidgetCircle"] {
            border-color: #3B82F6 !important;
            background-color: #E2E8F0 !important;
        }
        .stCheckbox label {
            background-color: #EFF6FF !important;
            padding: 6px 12px !important;
            border-radius: 6px !important;
            border: 1px solid #BFDBFE !important;
            color: #1E40AF !important;
            font-weight: bold !important;
        }
    </style>
""", unsafe_allow_html=True)

if "ranking_treino" not in st.session_state:
    st.session_state.ranking_treino = {}
if "ranking_simulado" not in st.session_state:
    st.session_state.ranking_simulado = {}
if "ranking_topico" not in st.session_state:
    st.session_state.ranking_topico = {}
if "respostas_treino_salvas" not in st.session_state:
    st.session_state.respostas_treino_salvas = {}

def gerar_40_questoes():
    caderno = list(QUESTOES_POOL)
    random.shuffle(caderno)
    return caderno[:40]

if 'questoes_treino' not in st.session_state:
    questoes_copia = list(QUESTOES_POOL)
    random.shuffle(questoes_copia)
    st.session_state.questoes_treino = questoes_copia

if 'questoes_simulado' not in st.session_state:
    st.session_state.questoes_simulado = gerar_40_questoes()

if 'respostas_simulado' not in st.session_state:
    st.session_state.respostas_simulado = {}
if 'simulado_entregue' not in st.session_state:
    st.session_state.simulado_entregue = False
if 'tempo_inicio_simulado' not in st.session_state:
    st.session_state.tempo_inicio_simulado = None

st.sidebar.header("👤 Identificação do Aluno")
nome_usuario = st.sidebar.text_input("Seu Nome para o Placar:", max_chars=20)
email_usuario = st.sidebar.text_input("Seu E-mail:")

st.sidebar.divider()
st.sidebar.subheader("🕹️ Selecione o Modo de Estudo")
modo_selecionado = st.sidebar.radio(
    "Ambiente:", 
    ["📖 Área de Treino (Geral)", "🎯 Treino por Tópico (Focado)", "⏱️ Simulado LPI (Prova Real 40 Q)"]
)

def enviar_email_seguro(destinatario, assunto, relatorio):
    try:
        if "email" in st.secrets:
            remetente = st.secrets["email"]["usuario"]
            senha = st.secrets["email"]["senha"]
            msg = MIMEMultipart()
            msg['From'] = remetente
            msg['To'] = destinatario
            msg['Subject'] = assunto
            msg.attach(MIMEText(relatorio, 'plain'))
            server = smtplib.SMTP('://gmail.com', 587)
            server.starttls()
            server.login(remetente, senha)
            server.sendmail(remetente, destinatario, msg.as_string())
            server.quit()
            st.sidebar.success("✅ Boletim enviado para o e-mail!")
        else:
            st.sidebar.warning("⚠️ Sem configuração de e-mail nos Secrets.")
    except Exception as e:
        st.sidebar.error(f"❌ Erro no e-mail: {str(e)}")

# --- MODO 1: ÁREA DE TREINAMENTO GERAL ---
if modo_selecionado == "📖 Área de Treino (Geral)":
    st.title("📖 Área de Treino e Fixação Técnica")
    st.write("Dividido em blocos rotativos de no máximo 100 itens para estabilidade do navegador.")

    tamanho_bloco = 100
    total_questoes = len(st.session_state.questoes_treino)
    num_blocos = max(1, (total_questoes + tamanho_bloco - 1) // tamanho_bloco)
    
    opcoes_blocos = [f"Bloco {i+1} (Questões {i*tamanho_bloco+1} a {min((i+1)*tamanho_bloco, total_questoes)})" for i in range(num_blocos)]
    bloco_selecionado_index = st.selectbox("📚 Escolha o Bloco de Exercícios atual:", range(num_blocos), format_func=lambda x: opcoes_blocos[x])
    
    inicio_fatia = bloco_selecionado_index * tamanho_bloco
    fim_fatia = min(inicio_fatia + tamanho_bloco, total_questoes)
    questoes_fatia = st.session_state.questoes_treino[inicio_fatia:fim_fatia]

    aba_treino, aba_rank_treino = st.tabs(["🎯 Exercícios do Bloco", "🏆 Líderes (Treino)"])

    with aba_treino:
        acertos_treino = 0
        respondidas_treino = 0
        
        for idx, q in enumerate(questoes_fatia):
            real_idx = inicio_fatia + idx
            st.markdown(f"### Questão {real_idx+1} — `{q['topico']}`")
            st.write(q['pergunta'])
            
            chave_radio = f"treino_geral_{q['id']}_{real_idx}"
            resp = st.radio("Selecione sua alternativa:", q['opcoes'], key=chave_radio, index=None)
            
            if resp is not None:
                st.session_state.respostas_treino_salvas[chave_radio] = resp
                respondidas_treino += 1

            if st.checkbox("💡 Validar e Ver Explicação", key=f"check_{real_idx}"):
                if resp == q['correta']:
                    st.success(f"🎯 Resposta Correta: {q['correta']}")
                    acertos_treino += 1
                else:
                    st.error(f"❌ Incorreta! A certa é: {q['correta']}")
                st.info(f"📘 **Explicação:** {q['explicacao']}")
            st.divider()

        if respondidas_treino > 0:
            st.metric("📊 Questões Respondidas neste Bloco", f"{respondidas_treino} de {len(questoes_fatia)}")

        if st.button("🏁 Salvar meu Progresso no Ranking", type="primary"):
            if not nome_usuario:
                st.warning("⚠️ Digite seu nome na barra lateral antes de computar!")
            elif respondidas_treino == 0:
                st.error("❌ Você precisa responder pelo menos uma questão antes de salvar.")
            else:
                score = (acertos_treino / len(questoes_fatia)) * 100
                st.session_state.ranking_treino[nome_usuario] = max(score, st.session_state.ranking_treino.get(nome_usuario, 0))
                st.success(f"🎉 Progresso Computado! Você acertou {acertos_treino} questões. Aproveitamento: {score:.1f}%")
                if email_usuario:
                    rel_t = f"Aluno: {nome_usuario}\nAcertos: {acertos_treino} de {len(questoes_fatia)}\nAproveitamento: {score:.1f}%"
                    enviar_email_seguro(email_usuario, f"Treino Geral Linux - {nome_usuario}", rel_t)
                time.sleep(1)
                st.rerun()

    with aba_rank_treino:
        if st.session_state.ranking_treino:
            ranking_ordenado = sorted(st.session_state.ranking_treino.items(), key=lambda x: x, reverse=True)
            for pos, (user, pt) in enumerate(ranking_ordenado, start=1):
                st.write(f"**{pos}º Lugar:** {user} — Aproveitamento de `{pt:.1f}%`")
        else:
            st.info("Nenhum registro ainda.")

# --- MODO 2: TREINO POR TÓPICO ---
elif modo_selecionado == "🎯 Treino por Tópico (Focado)":
    st.title("🎯 Bateria de Exercícios por Assunto")
    st.write("Foque seus estudos! Escolha o assunto específico e a quantidade exata de questões.")

    aba_filtro, aba_rank_filtro = st.tabs(["⚡ Configurar e Responder", "🏆 Líderes (Treino Focado)"])

    with aba_filtro:
        topicos_disponiveis = sorted(list(set(q['topico'] for q in QUESTOES_POOL)))
        topicos_disponiveis.insert(0, "Todos os Assuntos")
        
        col1, col2 = st.columns(2)
        with col1:
            assunto_escolhido = st.selectbox("📚 Escolha o Assunto:", topicos_disponiveis)
        with col2:
            # CORRIGIDO DEFINITIVAMENTE: Inserida a lista de opções numéricas [10, 20, 30, 40]
            qtd_escolhida = st.selectbox("🔢 Quantidade de Questões:", [10, 20, 30, 40])

        chave_bateria = f"bateria_{assunto_escolhido}_{qtd_escolhida}"
        
        if "chave_atual_bateria" not in st.session_state or st.session_state.chave_atual_bateria != chave_bateria:
            if assunto_escolhido == "Todos os Assuntos":
                pool_filtrado = list(QUESTOES_POOL)
            else:
                pool_filtrado = [q for q in QUESTOES_POOL if q['topico'] == assunto_escolhido]
            
            random.shuffle(pool_filtrado)
