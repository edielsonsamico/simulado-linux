import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time

# IMPORTAÇÃO DAS 40 QUESTÕES DOS ARQUIVOS SEPARADOS
from questoes_parte1 import POOL_1
from questoes_parte2 import POOL_2

# Lista oficial unificada
QUESTOES_POOL = POOL_1 + POOL_2

st.set_page_config(page_title="Linux Essentials - Plataforma de Estudos", page_icon="🐧", layout="wide")

# Inicialização dos rankings na sessão
if "ranking_treino" not in st.session_state:
    st.session_state.ranking_treino = {}
if "ranking_simulado" not in st.session_state:
    st.session_state.ranking_simulado = {}
if "ranking_topico" not in st.session_state:
    st.session_state.ranking_topico = {}

# Função para gerar simulado de 40 questões sem repetição
def gerar_40_questoes():
    caderno = list(QUESTOES_POOL)
    random.shuffle(caderno)
    return caderno

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

# BARRA LATERAL - IDENTIFICAÇÃO
st.sidebar.header("👤 Identificação do Aluno")
nome_usuario = st.sidebar.text_input("Seu Nome para o Placar:", max_chars=20)
email_usuario = st.sidebar.text_input("Seu E-mail:")

st.sidebar.divider()
st.sidebar.subheader("🕹️ Selecione o Modo de Estudo")
# Nova opção adicionada no menu dinâmico
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

# --- NOVO MODO: TREINO POR TÓPICO E QTD PERSONALIZADA ---
elif modo_selecionado == "🎯 Treino por Tópico (Focado)":
    st.title("🎯 Bateria de Exercícios por Assunto")
    st.write("Foque seus estudos! Escolha o assunto específico e a quantidade exata de questões que deseja resolver.")

    aba_filtro, aba_rank_filtro = st.tabs(["⚡ Configurar e Responder", "🏆 Líderes (Treino Focado)"])

    with aba_filtro:
        # Extrai dinamicamente todos os tópicos únicos do banco de dados
        topicos_disponiveis = sorted(list(set(q['topico'] for q in QUESTOES_POOL)))
        topicos_disponiveis.insert(0, "Todos os Assuntos")
        
        col1, col2 = st.columns(2)
        with col1:
            assunto_escolhido = st.selectbox("📚 Escolha o Assunto:", topicos_disponiveis)
        with col2:
            qtd_escolhida = st.selectbox("🔢 Quantidade de Questões:", [10, 20, 30, 40])

        # Filtra o banco baseado no assunto selecionado
        if assunto_escolhido == "Todos os Assuntos":
            pool_filtrado = list(QUESTOES_POOL)
        else:
            pool_filtrado = [q for q in QUESTOES_POOL if q['topico'] == assunto_escolhido]

        # Embaralha e limita ao tamanho escolhido pelo usuário ou ao máximo disponível
        random.shuffle(pool_filtrado)
        questoes_bateria = pool_filtrado[:min(qtd_escolhida, len(pool_filtrado))]

        st.caption(f"Exibindo {len(questoes_bateria)} questões exclusivas sobre '{assunto_escolhido}'.")
        st.divider()

        acertos_focados = 0
        for idx, q in enumerate(questoes_bateria):
            st.markdown(f"**Questão {idx+1} [{q['topico']}]:** {q['pergunta']}")
            resp_focada = st.radio("Sua resposta:", q['opcoes'], key=f"foco_{q['id']}_{idx}", index=None)
            
            # Validação instantânea e comentada para fixação
            if st.checkbox("💡 Corrigir e Ver Comentário", key=f"fococheck_{q['id']}_{idx}"):
                if resp_focada == q['correta']:
                    st.success(f"✅ Correto! Resposta: {q['correta']}")
                    acertos_focados += 1
                else:
                    st.error(f"❌ Incorreto. Resposta certa: {q['correta']}")
                st.info(f"📘 **Comentário Técnico:** {q['explicacao']}")
            st.divider()

        if st.button("🏁 Registrar Pontuação da Bateria", type="primary"):
            if not nome_usuario:
                st.warning("⚠️ Insira seu nome na barra lateral para registrar no placar!")
            elif len(questoes_bateria) == 0:
                st.error("Nenhuma questão resolvida.")
            else:
                score_focado = (acertos_focados / len(questoes_bateria)) * 100
                st.session_state.ranking_topico[nome_usuario] = max(score_focado, st.session_state.ranking_topico.get(nome_usuario, 0))
                st.success("Nota salva no ranking focado!")
                time.sleep(0.5)
                st.rerun()

    with aba_rank_filtro:
        st.subheader("🏆 Placar de Aproveitamento - Filtro por Assunto")
        if st.session_state.ranking_topico:
            r_t_ord = sorted(st.session_state.ranking_topico.items(), key=lambda x: x, reverse=True)
            for pos, (user, pt) in enumerate(r_t_ord, start=1):
                st.write(f"**{pos}º Lugar:** {user} — Melhor aproveitamento: `{pt:.1f}%`")
        else:
            st.info("Nenhum registro nesta categoria ainda.")

# --- MODO 3: SIMULADO PROVA REAL ---
elif modo_selecionado == "⏱️ Simulado LPI (Prova Real 40 Q)":
    st.title("⏱️ Simulado Oficial Linux Essentials")
    st.write("Simulação fiel: **40 Questões**, limite de **60 minutos** e gabarito apenas após a entrega.")

    aba_simulado, aba_rank_simulado = st.tabs(["📝 Caderno de Prova", "🏆 Placar dos Aprovados (Simulado)"])

    if st.session_state.tempo_inicio_simulado is None:
        st.session_state.tempo_inicio_simulado = time.time()

    tempo_decorrido = time.time() - st.session_state.tempo_inicio_simulado
    tempo_restante = max(0, (60 * 60) - tempo_decorrido)

    if tempo_restante > 0 and not st.session_state.simulado_entregue:
        m, s = divmod(int(tempo_restante), 60)
        st.sidebar.subheader(f"⏳ Cronômetro: {m:02d}:{s:02d}")
    elif not st.session_state.simulado_entregue:
        st.session_state.simulado_entregue = True
        st.sidebar.error("🚨 O tempo acabou!")

    with aba_simulado:
        st.subheader("⚠️ Responda todas as perguntas. O resultado sairá no final da página após a submissão.")
        st.divider()

        for idx, q in enumerate(st.session_state.questoes_simulado):
            st.markdown(f"**Questão {idx+1} [{q['topico']}]:** {q['pergunta']}")
            resp_sim = st.radio("Escolha uma opção:", q['opcoes'], key=f"sim_{idx}", index=None, disabled=st.session_state.simulado_entregue)
            st.session_state.respostas_simulado[f"q_{idx}"] = resp_sim

            if st.session_state.simulado_entregue:
                if resp_sim == q['correta']:
                    st.success(f"✅ Correto! Gabarito: {q['correta']}")
                else:
                    st.error(f"❌ Incorreto. Sua resposta: {resp_sim} | Gabarito Oficial: {q['correta']}")
                st.info(f"💡 **Explicação:** {q['explicacao']}")
            st.divider()

        if st.button("🏁 Entregar Caderno de Questões", type="primary", disabled=st.session_state.simulado_entregue):
            if not nome_usuario:
