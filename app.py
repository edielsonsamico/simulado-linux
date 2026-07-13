import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time

# BANCO DE DADOS INTEGRADO (GARANTE QUE O SIMULADOR NUNCA ABRA EM BRANCO)
QUESTOES_POOL = [
    {"id": 1, "topico": "Tópico 101: Arquitetura", "pergunta": "Qual comando é utilizado para listar informações detalhadas do chipset e dos componentes no barramento PCI?", "opcoes": ["lspci", "lsusb", "lsmod", "dmesg"], "correta": "lspci", "explicacao": "O comando lspci varre o barramento PCI do hardware listando controladores, placas e chipsets integrados."},
    {"id": 2, "topico": "Tópico 102: Pacotes", "pergunta": "De acordo com a hierarquia do FHS, qual diretório é destinado a guardar exclusivamente os arquivos de configuração específicos da máquina local?", "opcoes": ["/etc", "/var", "/usr", "/opt"], "correta": "/etc", "explicacao": "O diretório /etc é o local padronizado pelo FHS para armazenar scripts e arquivos de configuração de texto do sistema."},
    {"id": 3, "topico": "Tópico 103: Comandos", "pergunta": "No histórico do interpretador de comandos Bash, qual atalho de token repete imediatamente a execução do último comando utilizado?", "opcoes": ["!!", "!$", "history -r", "ctrl+r"], "correta": "!!", "explicacao": "As duas exclamações '!!' chamam e executam novamente no prompt a linha exata de comando disparada anteriormente."},
    {"id": 4, "topico": "Tópico 104: Dispositivos", "pergunta": "Qual comando relata em tempo real o espaço livre/disponível e o uso em blocos para todos os sistemas de arquivos atualmente montados?", "opcoes": ["df", "du", "fdisk", "free"], "correta": "df", "explicacao": "O comando df (disk free) lê a tabela de montagens do sistema exibindo capacidades, espaço ocupado e pontos de montagem ativos."},
    {"id": 5, "topico": "Tópico 105: Scripts e SQL", "pergunta": "Em um script executável em shell Bash, qual comando pausa a execução contínua para ler informações digitadas pelo usuário no teclado?", "opcoes": ["read", "input", "get", "scan"], "correta": "read", "explicacao": "O comando embutido 'read' interrompe o script colhendo os caracteres do fluxo de entrada padrão (stdin) e salvando-os em uma variable."},
    {"id": 6, "topico": "Tópico 106: Desktops", "pergunta": "Qual é o caminho completo e o nome do arquivo de configuração central responsável por gerenciar os parâmetros de vídeo e entradas do servidor de janelas X11?", "opcoes": ["/etc/X11/xorg.conf", "/etc/X11/x11.conf", "/etc/xorg.conf", "/var/X11/xorg.conf"], "correta": "/etc/X11/xorg.conf", "explicacao": "O arquivo estático /etc/X11/xorg.conf centraliza os módulos de layout, mouses, teclados, placas de vídeo e monitores na arquitetura XOrg clássica."},
    {"id": 7, "topico": "Tópico 107: Administração", "pergunta": "Qual arquivo confinado abriga de forma criptografada as senhas dos usuários e as regras específicas de expiração de validade da conta?", "opcoes": ["/etc/shadow", "/etc/passwd", "/etc/secure", "/var/shadow"], "correta": "/etc/shadow", "explicacao": "Por motivos de segurança, as hashes de senhas e políticas de obsolescência ficam trancadas no arquivo /etc/shadow com permissões restritas a root."},
    {"id": 8, "topico": "Tópico 108: Serviços", "pergunta": "O protocolo de sincronização temporal NTP executa o seu tráfego vital por meio de qual porta de rede e protocolo de transporte, respectivamente?", "opcoes": ["Porta UDP 123", "Porta TCP 123", "Porta UDP 53", "Porta TCP 80"], "correta": "Porta UDP 123", "explicacao": "O Network Time Protocol (NTP) dita a troca estruturada de pacotes de timestamp de tempo sobre datagramas na porta UDP 123."},
    {"id": 9, "topico": "Tópico 109: Redes", "pergunta": "Na configuração básica e resolução estática sem domínio real de rede externa, qual arquivo mapeia pares de IP e Nome Local no Linux?", "opcoes": ["/etc/hosts", "/etc/resolv.conf", "/etc/networks", "/etc/hostname"], "correta": "/etc/hosts", "explicacao": "O arquivo /etc/hosts associa IPs a nomes locais manualmente, sem depender de servidores DNS."},
    {"id": 10, "topico": "Tópico 110: Segurança", "pergunta": "Qual a sintaxe restrita aplicada no utilitário de busca find para garimpar especificamente todos e quaisquer arquivos baseados no gatilho do modo especial SUID nos binários ativos da raiz (/)?", "opcoes": ["find / -perm -4000", "find / -perm 777", "find / -type f -suid", "find / -user root"], "correta": "find / -perm -4000", "explicacao": "O bit 4000 identifica de forma octal o SUID, rodando arquivos com privilégios do dono do binário."}
]

# TENTATIVA DE IMPORTAÇÃO DOS ARQUIVOS EXTERNOS COMPLEMENTARES
try:
    from topico101 import POOL_101
    for q in POOL_101:
        if q not in QUESTOES_POOL: QUESTOES_POOL.append(q)
except Exception: pass

try:
    from topico102 import POOL_102
    for q in POOL_102:
        if q not in QUESTOES_POOL: QUESTOES_POOL.append(q)
except Exception: pass

try:
    from topico103 import POOL_103
    for q in POOL_103:
        if q not in QUESTOES_POOL: QUESTOES_POOL.append(q)
except Exception: pass

try:
    from topico104 import POOL_104
    for q in POOL_104:
        if q not in QUESTOES_POOL: QUESTOES_POOL.append(q)
except Exception: pass

try:
    from topico105 import POOL_105
    for q in POOL_105:
        if q not in QUESTOES_POOL: QUESTOES_POOL.append(q)
except Exception: pass

try:
    from topico106 import POOL_106
    for q in POOL_106:
        if q not in QUESTOES_POOL: QUESTOES_POOL.append(q)
except Exception: pass

try:
    from topico107 import POOL_107
    for q in POOL_107:
        if q not in QUESTOES_POOL: QUESTOES_POOL.append(q)
except Exception: pass

try:
    from topico108 import POOL_108
    for q in POOL_108:
        if q not in QUESTOES_POOL: QUESTOES_POOL.append(q)
except Exception: pass

try:
    from topico109 import POOL_109
    for q in POOL_109:
        if q not in QUESTOES_POOL: QUESTOES_POOL.append(q)
except Exception: pass

try:
    from topico110 import POOL_110
    for q in POOL_110:
        if q not in QUESTOES_POOL: QUESTOES_POOL.append(q)
except Exception: pass

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
    return caderno[:min(40, len(caderno))]

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
    st.write("Dividido em blocos rotativos para estabilidade do navegador.")

    tamanho_bloco = 100
    total_questoes = len(st.session_state.questoes_treino)
