import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time

# INICIALIZAÇÃO SEGURA DO BANCO DE QUESTÕES
QUESTOES_POOL = []

# Tenta carregar cada arquivo de tópico individualmente; se houver erro, ignora sem quebrar o site
try:
    from topico101 import POOL_101
    QUESTOES_POOL += POOL_101
except: pass

try:
    from topico102 import POOL_102
    QUESTOES_POOL += POOL_102
except: pass

try:
    from topico103 import POOL_103
    QUESTOES_POOL += POOL_103
except: pass

try:
    from topico104 import POOL_104
    QUESTOES_POOL += POOL_104
except: pass

try:
    from topico105 import POOL_105
    QUESTOES_POOL += POOL_105
except: pass

try:
    from topico106 import POOL_106
    QUESTOES_POOL += POOL_106
except: pass

try:
    from topico107 import POOL_107
    QUESTOES_POOL += POOL_107
except: pass

try:
    from topico108 import POOL_108
    QUESTOES_POOL += POOL_108
except: pass

try:
    from topico109 import POOL_109
    QUESTOES_POOL += POOL_109
except: pass

try:
    from topico110 import POOL_110
    QUESTOES_POOL += POOL_110
except: pass

# Backup caso nenhum arquivo consiga carregar
if not QUESTOES_POOL:
    QUESTOES_POOL = [
        {
            "id": 1, "topico": "Sistema", 
            "pergunta": "O simulador está sincronizando os novos bancos de dados na nuvem...", 
            "opcoes": ["Aguardar", "Atualizar"], "correta": "Aguardar", 
            "explicacao": "Arquivos sendo carregados no servidor."
        }
    ]

st.set_page_config(page_title="Plataforma de Estudos Linux", page_icon="🐧", layout="wide")

if "ranking_treino" not in st.session_state:
    st.session_state.ranking_treino = {}
if "ranking_simulado" not in st.session_state:
    st.session_state.ranking_simulado = {}
if "ranking_topico" not in st.session_state:
    st.session_state.ranking_topico = {}

def gerar_40_questoes():
    caderno = list(QUESTOES_POOL)
    random.shuffle(caderno)
    return caderno[:min(40, len(caderno))]

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

st.sidebar.header("👤 Aluno")
nome_usuario = st.sidebar.text_input("Seu Nome/Apelido:", max_chars=20)
email_usuario = st.sidebar.text_input("Seu E-mail:")

st.sidebar.divider()
st.sidebar.subheader("🕹️ Modo de Estudo")
modo_selecionado = st.sidebar.radio("Ambiente:", ["📖 Treino Geral", "🎯 Treino por Tópico", "⏱️ Simulado Oficial (40 Q)"])

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
    except: pass

if modo_selecionado == "📖 Treino Geral":
    st.title("📖 Área de Treino Geral")
    st.write("Estude as questões de forma livre e sem tempo correndo.")
    aba_treino, aba_rank_treino = st.tabs(["🎯 Exercícios", "🏆 Líderes"])

    with aba_treino:
        acertos_treino = 0
        for idx, q in enumerate(st.session_state.questoes_treino):
            st.markdown(f"### Questão {idx+1} — `{q['topico']}`")
            st.write(q['pergunta'])
            resp = st.radio("Alternativa:", q['opcoes'], key=f"treino_{idx}", index=None)
            if st.checkbox("💡 Validar e Ver Explicação", key=f"check_{idx}"):
                if resp == q['correta']:
                    st.success(f"🎯 Correto: {q['correta']}")
                    acertos_treino += 1
                else:
                    st.error(f"❌ Incorreto! A certa é: {q['correta']}")
                st.info(f"📘 **Explicação:** {q['explicacao']}")
            st.divider()

        if st.button("🏁 Salvar no Ranking", type="primary"):
            if not nome_usuario: st.warning("⚠️ Insira seu nome na barra lateral!")
            else:
                score = (acertos_treino / len(st.session_state.questoes_treino)) * 100
                st.session_state.ranking_treino[nome_usuario] = max(score, st.session_state.ranking_treino.get(nome_usuario, 0))
                st.success("Progresso salvo!")
                time.sleep(0.5)
                st.rerun()

    with aba_rank_treino:
        if st.session_state.ranking_treino:
            r_ord = sorted(st.session_state.ranking_treino.items(), key=lambda x: x[1], reverse=True)
            for pos, (user, pt) in enumerate(r_ord, start=1):
                st.write(f"**{pos}º Lugar:** {user} — Aproveitamento: `{pt:.1f}%`")
        else: st.info("Placar vazio.")

elif modo_selecionado == "🎯 Treino por Tópico":
    st.title("🎯 Bateria por Assunto")
    aba_filtro, aba_rank_filtro = st.tabs(["⚡ Responder", "🏆 Líderes"])

    with aba_filtro:
        topicos_disponiveis = sorted(list(set(q['topico'] for q in QUESTOES_POOL)))
        topicos_disponiveis.insert(0, "Todos os Assuntos")
        col1, col2 = st.columns(2)
        with col1: assunto_escolhido = st.selectbox("📚 Assunto:", topicos_disponiveis)
        with col2: qtd_escolhida = st.selectbox("🔢 Quantidade:", [10, 20, 30, 40])

        pool_filtrado = list(QUESTOES_POOL) if assunto_escolhido == "Todos os Assuntos" else [q for q in QUESTOES_POOL if q['topico'] == assunto_escolhido]
        random.shuffle(pool_filtrado)
        questoes_bateria = pool_filtrado[:min(qtd_escolhida, len(pool_filtrado))]

        st.caption(f"Exibindo {len(questoes_bateria)} questões sobre '{assunto_escolhido}'.")
        st.divider()

        acertos_focados = 0
        for idx, q in enumerate(questoes_bateria):
            st.markdown(f"**Questão {idx+1} [{q['topico']}]:** {q['pergunta']}")
            resp_focada = st.radio("Sua resposta:", q['opcoes'], key=f"foco_{q['id']}_{idx}", index=None)
            if st.checkbox("💡 Corrigir e Ver Comentário", key=f"fococheck_{q['id']}_{idx}"):
                if resp_focada == q['correta']:
                    st.success(f"✅ Correto! Resposta: {q['correta']}")
                    acertos_focados += 1
                else: st.error(f"❌ Incorreto. Certa: {q['correta']}")
                st.info(f"📘 **Comentário:** {q['explicacao']}")
            st.divider()

        if st.button("🏁 Registrar Pontuação", type="primary"):
            if not nome_usuario: st.warning("⚠️ Insira seu nome na barra lateral!")
            elif len(questoes_bateria) == 0: st.error("Sem questões.")
            else:
                score_focado = (acertos_focados / len(questoes_bateria)) * 100
                st.session_state.ranking_topico[nome_usuario] = max(score_focado, st.session_state.ranking_topico.get(nome_usuario, 0))
                st.success("Nota salva!")
                time.sleep(0.5)
                st.rerun()

    with aba_rank_filtro:
        if st.session_state.ranking_topico:
            r_t_ord = sorted(st.session_state.ranking_topico.items(), key=lambda x: x[1], reverse=True)
            for pos, (user, pt) in enumerate(r_t_ord, start=1):
                st.write(f"**{pos}º Lugar:** {user} — Melhor aproveitamento: `{pt:.1f}%`")
        else: st.info("Placar vazio.")

elif modo_selecionado == "⏱️ Simulado Oficial (40 Q)":
    st.title("⏱️ Simulado Oficial Linux")
    st.write("40 Questões, limite de 60 minutos e gabarito pós-entrega.")
    aba_simulado, aba_rank_simulado = st.tabs(["📝 Caderno de Prova", "🏆 Quadro Geral"])

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
        for idx, q in enumerate(st.session_state.questoes_simulado):
            st.markdown(f"**Questão {idx+1} [{q['topico']}]:** {q['pergunta']}")
            resp_sim = st.radio("Escolha uma opção:", q['opcoes'], key=f"sim_{idx}", index=None, disabled=st.session_state.simulado_entregue)
            st.session_state.respostas_simulado[f"q_{idx}"] = resp_sim

            if st.session_state.simulado_entregue:
                if resp_sim == q['correta']: st.success(f"✅ Correto! Gabarito: {q['correta']}")
                else: st.error(f"❌ Incorreto. Gabarito Oficial: {q['correta']}")
                st.info(f"💡 **Explicação:** {q['explicacao']}")
            st.divider()

        if st.button("🏁 Entregar Caderno", type="primary", disabled=st.session_state.simulado_entregue):
            if not nome_usuario: st.error("⚠️ Insira seu nome na barra lateral!")
            else:
                st.session_state.simulado_entregue = True
                acertos = sum(1 for i, q in enumerate(st.session_state.questoes_simulado) if st.session_state.respostas_simulado.get(f"q_{i}") == q['correta'])
                
                porcentagem_acertos = acertos / max(1, len(st.session_state.questoes_simulado))
