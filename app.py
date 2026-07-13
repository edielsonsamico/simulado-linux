import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

# Configuração da página do simulador
st.set_page_config(page_title="Simulado Linux Essentials", page_icon="🐧", layout="wide")

# BANCO DE DADOS EXPANDIDO DE QUESTÕES
QUESTOES_POOL = [
    {
        "id": 1, "topico": "Comandos Básicos",
        "pergunta": "Qual comando é utilizado para listar os arquivos de um diretório exibindo permissões e donos?",
        "opcoes": ["ls -l", "ls -a", "list -d", "show files"], "correta": "ls -l",
        "explicacao": "O comando 'ls -l' ativa o formato de listagem longa, mostrando permissões, proprietário, grupo, tamanho e data."
    },
    {
        "id": 2, "topico": "Licenciamento",
        "pergunta": "Qual das seguintes licenças garante que o código derivado continue sendo software livre?",
        "opcoes": ["GPL", "BSD", "MIT", "Apache"], "correta": "GPL",
        "explicacao": "A licença GPL possui a característica de 'copyleft', exigindo que trabalhos derivados também usem a GPL."
    },
    {
        "id": 3, "topico": "Permissões",
        "pergunta": "Qual permissão octal corresponde aos acessos 'rwxr-xr-x'?",
        "opcoes": ["755", "644", "777", "700"], "correta": "755",
        "explicacao": "rwx = 7, r-x = 5, r-x = 5. Portanto, 755."
    },
    {
        "id": 4, "topico": "Diretórios",
        "pergunta": "Em qual diretório do padrão FHS ficam armazenados os arquivos de configuração do sistema?",
        "opcoes": ["/etc", "/var", "/bin", "/usr"], "correta": "/etc",
        "explicacao": "O diretório /etc é reservado exclusivamente para arquivos de configuração estáticos do sistema operacional."
    },
    {
        "id": 5, "topico": "Processos",
        "pergunta": "Qual comando envia o sinal padrão SIGTERM (15) para encerrar um processo através do seu PID?",
        "opcoes": ["kill", "stop", "terminate", "ps -k"], "correta": "kill",
        "explicacao": "O comando kill, quando executado apenas com o PID (ex: kill 1234), envia por padrão o sinal 15 (SIGTERM)."
    },
    {
        "id": 6, "topico": "FHS",
        "pergunta": "Qual diretório armazena os arquivos de log do sistema e dados altamente variáveis?",
        "opcoes": ["/var", "/tmp", "/opt", "/home"], "correta": "/var",
        "explicacao": "O diretório /var (variable) guarda dados dinâmicos como filas de impressão, spools e logs do sistema (/var/log)."
    },
    {
        "id": 7, "topico": "Comandos de Texto",
        "pergunta": "Qual comando é usado para exibir as primeiras 10 linhas de um arquivo de texto?",
        "opcoes": ["head", "tail", "cat", "less"], "correta": "head",
        "explicacao": "O comando 'head' exibe por padrão as primeiras 10 linhas. O 'tail' exibe as últimas 10."
    },
    {
        "id": 8, "topico": "Usuários e Grupos",
        "pergunta": "Qual arquivo armazena as senhas criptografadas dos usuários no Linux por questões de segurança?",
        "opcoes": ["/etc/shadow", "/etc/passwd", "/etc/secure", "/var/shadow"], "correta": "/etc/shadow",
        "explicacao": "O arquivo /etc/passwd guarda dados públicos (UID, shell), enquanto as senhas cifradas ficam protegidas no /etc/shadow."
    },
    {
        "id": 9, "topico": "Redes",
        "pergunta": "Qual utilitário envia pacotes ICMP ECHO_REQUEST para verificar a conectividade com um host remoto?",
        "opcoes": ["ping", "ifconfig", "netstat", "route"], "correta": "ping",
        "explicacao": "O 'ping' utiliza o protocolo ICMP para testar a comunicação direta e latência entre duas máquinas na rede."
    },
    {
        "id": 10, "topico": "Comandos de Arquivo",
        "pergunta": "Qual comando cria um diretório vazio no Linux?",
        "opcoes": ["mkdir", "newdir", "md", "create -d"], "correta": "mkdir",
        "explicacao": "O comando 'mkdir' (make directory) é a ferramenta padrão POSIX para criação de novas pastas."
    }
]

# CONEXÃO AUTOMÁTICA COM O BANCO DE DADOS EM NUVEM
if "ranking_lpi" not in st.session_state:
    try:
        db_conn = st.connection("ranking_db", type="dict")
        st.session_state.ranking_lpi = db_conn
    except Exception:
        st.session_state.ranking_lpi = st.session_state.get("ranking_local_backup", {})

db = {"ranking_lpi": st.session_state.ranking_lpi}

def gerar_blocos():
    qtd_questoes = min(40, len(QUESTOES_POOL))
    return {
        "Bloco A": random.sample(QUESTOES_POOL, k=qtd_questoes),
        "Bloco B": random.sample(QUESTOES_POOL, k=qtd_questoes),
        "Bloco C": random.sample(QUESTOES_POOL, k=qtd_questoes)
    }

if 'blocos' not in st.session_state:
    st.session_state.blocos = gerar_blocos()
if 'respostas' not in st.session_state:
    st.session_state.respostas = {}
if 'corrigido' not in st.session_state:
    st.session_state.corrigido = False

st.title("🎓 Simulador & Ranking - Linux Essentials")
st.write("Estude com seus amigos! Faça o teste, entre para o placar de líderes e receba o gabarito detalhado por e-mail.")

aba_prova, aba_ranking = st.tabs(["📝 Responder Simulado", "🏆 Ranking dos Amigos"])

st.sidebar.header("👤 Identificação")
nome_usuario = st.sidebar.text_input("Seu Nome/Apelido para o Ranking:", max_chars=20)
email_usuario = st.sidebar.text_input("Seu E-mail para receber as respostas:")

st.sidebar.divider()
st.sidebar.subheader("🎮 Opções do Jogo")
bloco_selecionado = st.sidebar.selectbox("Escolha o Bloco:", ["Bloco A", "Bloco B", "Bloco C"])

if st.sidebar.button("♻️ Solicitar Novas Questões (Reset Geral)"):
    st.session_state.blocos = gerar_blocos()
    st.session_state.respostas = {}
    st.session_state.corrigido = False
    st.rerun()

def enviar_email_seguro(destinatario, relatorio):
    try:
        remetente = st.secrets["email"]["usuario"]
        senha = st.secrets["email"]["senha"]
        
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = "Desempenho - Simulado Linux Essentials"
        msg.attach(MIMEText(relatorio, 'plain'))
        
        server = smtplib.SMTP('://gmail.com', 587)
        server.starttls()
        server.login(remetente, senha)
        server.sendmail(remetente, destinatario, msg.as_string())
        server.quit()
        st.sidebar.success("✅ Histórico enviado para o seu e-mail!")
    except Exception:
        st.sidebar.error("⚠️ Configuração de e-mail pendente nos Secrets.")

with aba_prova:
    questoes_do_bloco = st.session_state.blocos[bloco_selecionado]
    st.subheader(f"Testando conhecimentos: {bloco_selecionado}")
    
    for i, q in enumerate(questoes_do_bloco):
        chave = f"{bloco_selecionado}_q_{i}"
        st.markdown(f"**Questão {i+1}:** {q['pergunta']}")
        
        res_atual = st.radio("Alternativas:", q['opcoes'], key=chave, index=None, disabled=st.session_state.corrigido)
        st.session_state.respostas[chave] = res_atual
        
        if st.session_state.corrigido:
            if res_atual == q['correta']:
                st.success(f"🎯 Acertou! Resposta: {q['correta']}")
            else:
                st.error(f"❌ Errou. Sua escolha: {res_atual} | Correta: {q['correta']}")
            st.info(f"💡 **Explicação:** {q['explicacao']}")
        st.divider()

    if st.button("🏁 Entregar Prova e Calcular Nota", type="primary"):
        if not nome_usuario:
            st.warning("⚠️ Digite seu nome na barra lateral antes de finalizar para salvar sua pontuação no ranking!")
        else:
            st.session_state.corrigido = True
            acertos = sum(1 for idx, quest in enumerate(questoes_do_bloco) if st.session_state.respostas.get(f"{bloco_selecionado}_q_{idx}") == quest['correta'])
            total = len(questoes_do_bloco)
            porcentagem = (acertos / total) * 100
            
            ranking_atual = db["ranking_lpi"]
            if nome_usuario not in ranking_atual or porcentagem > ranking_atual[nome_usuario]:
                ranking_atual[nome_usuario] = porcentagem
                db["ranking_lpi"] = ranking_atual
            
            relatorio = f"Resultados de {nome_usuario} no {bloco_selecionado}\nAcertos: {acertos}/{total} ({porcentagem:.1f}%)\n\n"
            for idx, quest in enumerate(questoes_do_bloco):
                u_resp = st.session_state.respostas.get(f"{bloco_selecionado}_q_{idx}")
                relatorio += f"Q{idx+1}: {quest['pergunta']}\nSua Resposta: {u_resp} | Correta: {quest['correta']}\n\n"
            
            st.success(f"Resultado computado: Acertou {acertos} de {total} questões ({porcentagem:.1f}%)!")
            if email_usuario:
                enviar_email_seguro(email_usuario, relatorio)
            st.rerun()

with aba_ranking:
    st.subheader("🏆 Líderes do Simulado")
    ranking_dados = db["ranking_lpi"]
    if ranking_dados:
        ranking_ordenado = sorted(ranking_dados.items(), key=lambda item: item[1], reverse=True)
        for posicao, (usuario, nota) in enumerate(ranking_ordenado, start=1):
            emoji = "🥇" if posicao == 1 else "🥈" if posicao == 2 else "🥉" if posicao == 3 else "🎖️"
            st.markdown(f"### {emoji} **{posicao}º Lugar:** {usuario} — `{nota:.1f}% de aproveitamento`")
    else:
        st.info("Nenhum registro no placar ainda. Seja o primeiro a fazer a prova!")
