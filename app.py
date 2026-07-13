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

# CASO TODOS FALHEM POR SEGURANÇA, CRIA UMA QUESTÃO PADRÃO
if not QUESTOES_POOL:
    QUESTOES_POOL = [{
        "id": 1, "topico": "Geral", 
        "pergunta": "O simulador está carregando os bancos de dados...", 
        "opcoes": ["Aguardar", "Atualizar"], "correta": "Aguardar", 
        "explicacao": "Carregando arquivos."
    }]

st.set_page_config(page_title="Linux Essentials - Plataforma de Estudos", page_icon="🐧", layout="wide")

# Inicialização de dados persistentes da sessão
if "ranking_treino" not in st.session_state:
    st.session_state.ranking_treino = {}
if "ranking_simulado" not in st.session_state:
    st.session_state.ranking_simulado = {}
if "ranking_topico" not in st.session_state:
    st.session_state.ranking_topico = {}

def gerar_40_questoes():
    caderno = list(QUESTOES_POOL)
    random.shuffle(caderno)
    return caderno[:40]

if 'questoes_treino' not in st.session_state:
    st.session_state.questoes_treino = list(QUESTOES_POOL)
    random.shuffle(st.session_state.questoes_treino)
if 'questoes_simulado' not in st.session_state:
    st.session_state.questoes_simulado = gerar_40_questoes()

if 'respostas_simulado' not in st.session_state:
    st.session_state.respostas_simulado = {}
if 'simulado_entregue' not in st.session_state:
    st.session_state.simulado_entregue = False
if 'tempo_inicio_simulado' not in st.session_state:
    st.session_state.tempo_inicio_simulado = None

# BARRA LATERAL
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
        st.sidebar.success("✅ Histórico enviado por e-mail!")
    except Exception:
        pass

# --- MODO 1: ÁREA DE TREINAMENTO GERAL ---
if modo_selecionado == "📖 Área de Treino (Geral)":
    st.title("📖 Área de Treino e Fixação Técnica")
    st.write("Estude todas as questões misturadas sem pressão de tempo.")

    aba_treino, aba_rank_treino = st.tabs(["🎯 Exercícios", "🏆 Líderes (Treino)"])

    with aba_treino:
        acertos_treino = 0
        for idx, q in enumerate(st.session_state.questoes_treino):
            st.markdown(f"### Questão {idx+1} — `{q['topico']}`")
            st.write(q['pergunta'])
            resp = st.radio("Selecione sua alternativa:", q['opcoes'], key=f"treino_{idx}", index=None)
            if st.checkbox("💡 Validar e Ver Explicação", key=f"check_{idx}"):
                if resp == q['correta']:
                    st.success(f"🎯 Resposta Correta: {q['correta']}")
                    acertos_treino += 1
                else:
                    st.error(f"❌ Incorreta! A certa é: {q['correta']}")
                st.info(f"📘 **Explicação:** {q['explicacao']}")
            st.divider()

        if st.button("🏁 Salvar meu Progresso no Ranking de Treino", type="primary"):
            if not nome_usuario:
                st.warning("⚠️ Digite seu nome na barra lateral!")
            else:
                score = (acertos_treino / len(st.session_state.questoes_treino)) * 100
                st.session_state.ranking_treino[nome_usuario] = max(score, st.session_state.ranking_treino.get(nome_usuario, 0))
                st.success("Progresso salvo!")
                time.sleep(0.5)
                st.rerun()

    with aba_rank_treino:
        if st.session_state.ranking_treino:
            ranking_ordenado = sorted(st.session_state.ranking_treino.items(), key=lambda x: x, reverse=True)
            for pos, (user, pt) in enumerate(ranking_ordenado, start=1):
                st.write(f"**{pos}º Lugar:** {user} — Aproveitamento de `{pt:.1f}%`")
        else:
            st.info("Nenhum registro ainda.")

# --- MODO 2: TREINO POR TÓPICO E QTD PERSONALIZADA (CORRIGIDO) ---
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
            qtd_escolhida = st.selectbox("🔢 Quantidade de Questões:", [10, 20, 30, 40])

        chave_bateria = f"bateria_{assunto_escolhido}_{qtd_escolhida}"
        
        if "chave_atual_bateria" not in st.session_state or st.session_state.chave_atual_bateria != chave_bateria:
            if assunto_escolhido == "Todos os Assuntos":
                pool_filtrado = list(QUESTOES_POOL)
            else:
                pool_filtrado = [q for q in QUESTOES_POOL if q['topico'] == assunto_escolhido]
            
            random.shuffle(pool_filtrado)
            st.session_state.questoes_bateria_fixas = pool_filtrado[:min(qtd_escolhida, len(pool_filtrado))]
            st.session_state.chave_atual_bateria = chave_bateria

        questoes_bateria = st.session_state.questoes_bateria_fixas

        st.caption(f"Exibindo {len(questoes_bateria)} questões exclusivas sobre '{assunto_escolhido}'.")
        st.divider()

        acertos_focados = 0
        for idx, q in enumerate(questoes_bateria):
            st.markdown(f"**Questão {idx+1} [{q['topico']}]:** {q['pergunta']}")
            
            chave_radio = f"foco_{q['id']}_{assunto_escolhido}_{idx}"
            resp_focada = st.radio("Sua resposta:", q['opcoes'], key=chave_radio, index=None)
            
            if st.checkbox("💡 Corrigir e Ver Comentário", key=f"fococheck_{q['id']}_{assunto_escolhido}_{idx}"):
                if resp_focada == q['correta']:
                    st.success(f"✅ Correto! Resposta: {q['correta']}")
                    acertos_focados += 1
                else:
                    st.error(f"❌ Incorreto. Resposta certa: {q['correta']}")
                st.info(f"📘 **Comentário Técnico:** {q['explicacao']}")
            st.divider()

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🏁 Registrar Bateria", type="primary"):
                if not nome_usuario:
                    st.warning("⚠️ Insira seu nome na barra lateral para registrar no placar!")
                elif len(questoes_bateria) == 0:
                    st.error("Nenhuma questão resolvida.")
                else:
                    score_focado = (acertos_focados / len(questoes_bateria)) * 100
                    st.session_state.ranking_topico[nome_usuario] = max(score_focado, st.session_state.ranking_topico.get(nome_usuario, 0))
                    st.success("Nota salva!")
                    time.sleep(0.5)
                    st.rerun()
        with col_btn2:
            if st.button("🔄 Sortear Novas Questões Deste Tópico"):
                if "chave_atual_bateria" in st.session_state:
                    del st.session_state.chave_atual_bateria
                st.rerun()

    with aba_rank_filtro:
        if st.session_state.ranking_topico:
            r_t_ord = sorted(st.session_state.ranking_topico.items(), key=lambda x: x, reverse=True)
            for pos, (user, pt) in enumerate(r_t_ord, start=1):
                st.write(f"**{pos}º Lugar:** {user} — Melhor aproveitamento: `{pt:.1f}%`")
        else:
            st.info("Nenhum registro nesta categoria ainda.")

# --- MODO 3: SIMULADO PROVA REAL ---
elif modo_selecionado == "⏱️ Simulado LPI (Prova Real 40 Q)":
    st.title("⏱️ Simulado Oficial Linux Essentials")
    st.write("Simulação fiel: **40 Questões exclusivas**, limite de 60 minutos e correção pós-entrega.")

    aba_simulado, aba_rank_simulado = st.tabs(["📝 Caderno de Prova", "🏆 Placar dos Aprovados (Simulado)"])

    if st.session_state.tempo_inicio_simulado is None:
