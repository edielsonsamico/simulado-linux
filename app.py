import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time

# IMPORTAÇÃO SEGURA DAS 40 QUESTÕES DE ARQUIVOS SEPARADOS
from questoes_parte1 import POOL_1
from questoes_parte2 import POOL_2

# Une as duas metades em uma lista oficial com 40 questões exclusivas
QUESTOES_POOL = POOL_1 + POOL_2

st.set_page_config(page_title="Linux Essentials - Treino e Simulado", page_icon="🐧", layout="wide")

if "ranking_treino" not in st.session_state:
    st.session_state.ranking_treino = {}
if "ranking_simulado" not in st.session_state:
    st.session_state.ranking_simulado = {}

# Sorteia exatamente as 40 questões sem nenhuma repetição
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

st.sidebar.header("👤 Identificação do Aluno")
nome_usuario = st.sidebar.text_input("Seu Nome para o Placar:", max_chars=20)
email_usuario = st.sidebar.text_input("Seu E-mail:")

st.sidebar.divider()
st.sidebar.subheader("🕹️ Ambiente")
modo_selecionado = st.sidebar.radio("Escolha o Modo:", ["📖 Área de Treino (Fixação)", "⏱️ Simulado LPI (Prova Real 40 Q)"])

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

# --- MODO 1: ÁREA DE TREINAMENTO ---
if modo_selecionado == "📖 Área de Treino (Fixação)":
    st.title("📖 Área de Treino e Fixação Técnica")
    st.write("Estude sem pressão. Responda e marque a caixa para ver a correção na hora com a explicação técnica.")

    aba_treino, aba_rank_treino = st.tabs(["🎯 Exercícios de Fixação", "🏆 Placar de Líderes (Treino)"])

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
                st.success("Progresso salvo com sucesso!")
                time.sleep(0.5)
                st.rerun()

    with aba_rank_treino:
        st.subheader("🏆 Melhores Pontuações na Área de Estudos")
        if st.session_state.ranking_treino:
            ranking_ordenado = sorted(st.session_state.ranking_treino.items(), key=lambda x: x[1], reverse=True)
            for pos, (user, pt) in enumerate(ranking_ordenado, start=1):
                st.write(f"**{pos}º Lugar:** {user} — Aproveitamento de `{pt:.1f}%`")
        else:
            st.info("Nenhum registro ainda.")

# --- MODO 2: SIMULADO REAL ---
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
                st.error("⚠️ Insira seu nome na barra lateral esquerda antes de entregar!")
            else:
                st.session_state.simulado_entregue = True
                acertos = sum(1 for i, q in enumerate(st.session_state.questoes_simulado) if st.session_state.respostas_simulado.get(f"q_{i}") == q['correta'])
                
                porcentagem_acertos = acertos / 40
                pontuacao_lpi = int(200 + (porcentagem_acertos * 600))
                status = "🟢 APROVADO" if pontuacao_lpi >= 500 else "🔴 REPROVADO"

                st.session_state.ranking_simulado[nome_usuario] = max(pontuacao_lpi, st.session_state.ranking_simulado.get(nome_usuario, 0))

                if email_usuario:
                    rel_corpo = f"Boletim Oficial do Simulado Linux Essentials\nNome: {nome_usuario}\nPontuação Final: {pontuacao_lpi} pontos de 800\nResultado: {status}"
                    enviar_email_seguro(email_usuario, f"Resultado Simulado Linux - {pontuacao_lpi} Pontos", rel_corpo)
                st.rerun()

    with aba_rank_simulado:
        st.subheader("🏆 Quadro Geral de Notas do Exame Oficial (Escala LPI 200-800)")
        if st.session_state.ranking_simulado:
            rank_sim_ordenado = sorted(st.session_state.ranking_simulado.items(), key=lambda x: x[1], reverse=True)
            for pos, (user, pontos) in enumerate(rank_sim_ordenado, start=1):
                medalha = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else "🎖️"
                sel_status = "🟢 APROVADO" if pontos >= 500 else "🔴 REPROVADO"
                st.markdown(f"### {medalha} **{pos}º Lugar:** {user} — `{pontos} pontos` ({sel_status})")

        if st.button("🔄 Reiniciar e Gerar Novo Simulado"):
            st.session_state.questoes_simulado = gerar_40_questoes()
            st.session_state.respostas_simulado = {}
            st.session_state.simulado_entregue = False
            st.session_state.tempo_inicio_simulado = time.time()
            st.rerun()
