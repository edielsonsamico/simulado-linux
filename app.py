import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time
import os
import glob

# ==========================================
# -1. SISTEMA DE MONITORAMENTO EM TEMPO REAL
# ==========================================
PASTA_SESSIONS = ".active_sessions"
if not os.path.exists(PASTA_SESSIONS):
    try:
        os.makedirs(PASTA_SESSIONS)
    except Exception:
        pass

# Gera um token único para a sessão atual
if "session_token" not in st.session_state:
    st.session_state.session_token = f"sess_{int(time.time())}_{random.randint(1000, 9999)}"

token_atual = st.session_state.session_token
caminho_sessao = os.path.join(PASTA_SESSIONS, token_atual)

try:
    with open(caminho_sessao, "w") as f:
        f.write(str(time.time()))
except Exception:
    pass

def obter_metricas_acesso():
    """Calcula visitantes únicos de forma persistente e usuários online sem duplicar por F5."""
    arquivo_visitas = ".visitas_totais"
    arquivo_log_tokens = ".registro_sessoes" # Guarda os tokens que já visitaram
    
    # 1. Recupera as visitas salvas
    visitas = 0
    if os.path.exists(arquivo_visitas):
        try:
            with open(arquivo_visitas, "r") as f:
                conteudo = f.read().strip()
                visitas = int(conteudo) if conteudo.isdigit() else 0
        except Exception:
            pass
            
    # Recupera a lista de tokens que já foram computados como visitas reais
    tokens_registrados = set()
    if os.path.exists(arquivo_log_tokens):
        try:
            with open(arquivo_log_tokens, "r") as f:
                tokens_registrados = set(f.read().splitlines())
        except Exception:
            pass

    # Se este token de sessão ainda não foi registrado no arquivo de visitas do servidor, conta +1
    if token_atual not in tokens_registrados:
        tokens_registrados.add(token_atual)
        visitas += 1
        try:
            # Atualiza o arquivo de visitas totais
            with open(arquivo_visitas, "w") as f:
                f.write(str(visitas))
            # Registra o token para que ele nunca mais some visitas, mesmo com F5
            with open(arquivo_log_tokens, "a") as f:
                f.write(token_atual + "\n")
        except Exception:
            pass

    # 2. Usuários Online Agora (Baseado em atividade nos últimos 2 minutos)
    agora = time.time()
    limite_inatividade = 120  # 2 minutos
    online = 0
    
    if os.path.exists(PASTA_SESSIONS):
        arquivos = glob.glob(os.path.join(PASTA_SESSIONS, "sess_*"))
        for arq in arquivos:
            try:
                mtime = os.path.getmtime(arq)
                if agora - mtime < limite_inatividade:
                    online += 1
                else:
                    # Limpa sessões antigas que fecharam a aba ou abandonaram o site
                    os.remove(arq)
            except Exception:
                pass
    
    # Garante coerência mínima
    online = max(1, online)
    return online, visitas


# ==========================================
# 0. FUNÇÃO AUXILIAR DE DESDUPLICAÇÃO
# ==========================================
def normalizar_texto(texto):
    """Remove espaços extras e padroniza para evitar duplicados por detalhes de digitação."""
    return " ".join(texto.strip().lower().split())

def desduplicar_questoes(lista_original):
    """Retorna uma nova lista sem perguntas repetidas com base no conteúdo textual."""
    vistas = set()
    lista_limpa = []
    for q in lista_original:
        pergunta_norm = normalizar_texto(q["pergunta"])
        if pergunta_norm not in vistas:
            vistas.add(pergunta_norm)
            lista_limpa.append(q)
    return lista_limpa

# ==========================================
# 1. BANCO DE DADOS INTEGRADO (BASE)
# ==========================================
QUESTOES_POOL_RAW = [
    {"id": 1, "topico": "Tópico 101: Arquitetura", "pergunta": "Qual comando é utilizado para listar informações detalhadas do chipset e dos componentes no barramento PCI?", "opcoes": ["lspci", "lsusb", "lsmod", "dmesg"], "correta": "lspci", "explicacao": "O comando lspci varre o barramento PCI do hardware listando controladores, placas e chipsets integrados."},
    {"id": 2, "topico": "Tópico 102: Pacotes", "pergunta": "De acordo com a hierarquia do FHS, qual diretório é destinado a guardar exclusivamente os arquivos de configuração específicos da máquina local?", "opcoes": ["/etc", "/var", "/usr", "/opt"], "correta": "/etc", "explicacao": "O diretório /etc é o local padronizado pelo FHS para armazenar scripts e arquivos de configuração de texto do sistema."},
    {"id": 3, "topico": "Tópico 103: Comandos", "pergunta": "No histórico do interpretador de comandos Bash, qual atalho de token repete imediatamente a execução do último comando utilizado?", "opcoes": ["!!", "!$", "history -r", "ctrl+r"], "correta": "!!", "explicacao": "As duas exclamações '!!' chamam e executam novamente no prompt a linha exata de comando disparada anteriormente."},
    {"id": 4, "topico": "Tópico 104: Dispositivos", "pergunta": "Qual comando relata em tempo real o espaço livre/disponível e o uso em blocos para todos os sistemas de arquivos atualmente montados?", "opcoes": ["df", "du", "fdisk", "free"], "correta": "df", "explicacao": "O comando df (disk free) lê a tabela de montagens do sistema exibindo capacidades, espaço ocupado e pontos de montagem ativos."},
    {"id": 5, "topico": "Tópico 105: Scripts e SQL", "pergunta": "Em um script executável em shell Bash, qual comando pausa a execução contínua para ler informações digitadas pelo usuário no teclado?", "opcoes": ["read", "input", "get", "scan"], "correta": "read", "explicacao": "O comando embutido 'read' interrompe o script colhendo os caracteres do fluxo de entrada padrão (stdin) e salvando-os em uma variável."},
    {"id": 6, "topico": "Tópico 106: Desktops", "pergunta": "Qual é o caminho completo e o nome do arquivo de configuração central responsável por gerenciar os parâmetros de vídeo e entradas do servidor de janelas X11?", "opcoes": ["/etc/X11/xorg.conf", "/etc/X11/x11.conf", "/etc/xorg.conf", "/var/X11/xorg.conf"], "correta": "/etc/X11/xorg.conf", "explicacao": "O arquivo estático /etc/X11/xorg.conf centraliza os módulos de layout, mouses, teclados, placas de vídeo e monitores na arquitetura XOrg clássica."},
    {"id": 7, "topico": "Tópico 107: Administração", "pergunta": "Qual arquivo confinado abriga de forma criptografada as senhas dos usuários e as regras específicas de expiração de validade da conta?", "opcoes": ["/etc/shadow", "/etc/passwd", "/etc/secure", "/var/shadow"], "correta": "/etc/shadow", "explicacao": "Por motivos de segurança, as hashes de senhas e políticas de obsolescência ficam trancadas no arquivo /etc/shadow com permissões restritas a root."},
    {"id": 8, "topico": "Tópico 108: Serviços", "pergunta": "O protocolo de sincronização temporal NTP executa o seu tráfego vital por meio de qual porta de rede e protocolo de transporte, respectively?", "opcoes": ["Porta UDP 123", "Porta TCP 123", "Porta UDP 53", "Porta TCP 80"], "correta": "Porta UDP 123", "explicacao": "O Network Time Protocol (NTP) dita a troca estruturada de pacotes de timestamp de tempo sobre datagramas na porta UDP 123."},
    {"id": 9, "topico": "Tópico 109: Redes", "pergunta": "Na configuração básica e resolução estática sem domínio real de rede externa, qual arquivo mapeia pares de IP e Nome Local no Linux?", "opcoes": ["/etc/hosts", "/etc/resolv.conf", "/etc/networks", "/etc/hostname"], "correta": "/etc/hosts", "explicacao": "O arquivo /etc/hosts associa IPs a nomes locais manualmente, sem depender de servidores DNS."},
    {"id": 10, "topico": "Tópico 110: Segurança", "pergunta": "Qual a sintaxe restrita aplicada no utilitário de busca find para garimpar especificamente todos e quaisquer arquivos baseados no gatilho do modo especial SUID nos binários ativos da raiz (/)?", "opcoes": ["find / -perm -4000", "find / -perm 777", "find / -type f -suid", "find / -user root"], "correta": "find / -perm -4000", "explicacao": "O bit 4000 identifica de forma octal o SUID, rodando arquivos com privilégios do dono do binário."}
]

# Inicializa o pool aplicando a desduplicação na base de dados integrada
QUESTOES_POOL = desduplicar_questoes(QUESTOES_POOL_RAW)

# ==========================================
# 2. CARREGAMENTO DOS ARQUIVOS EXTERNOS (COM FILTRO DE CONTEÚDO)
# ==========================================
perguntas_existentes = {normalizar_texto(q["pergunta"]) for q in QUESTOES_POOL}

for i in range(101, 111):
    try:
        modulo = __import__(f"topico{i}")
        pool = getattr(modulo, f"POOL_{i}")
        for q in pool:
            if isinstance(q, dict) and "pergunta" in q:
                pergunta_norm = normalizar_texto(q["pergunta"])
                if pergunta_norm not in perguntas_existentes:
                    perguntas_existentes.add(pergunta_norm)
                    QUESTOES_POOL.append(q)
    except Exception:
        pass

# ==========================================
# 3. FUNÇÕES GLOBAIS
# ==========================================
def gerar_40_questoes():
    caderno = list(QUESTOES_POOL)
    random.shuffle(caderno)
    return caderno[:min(40, len(caderno))]

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
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(remetente, senha)
            server.sendmail(remetente, destinatario, msg.as_string())
            server.quit()
            st.sidebar.success("✅ Boletim enviado para o e-mail!")
        else:
            st.sidebar.warning("⚠️ Sem configuração de e-mail nos Secrets.")
    except Exception as e:
        st.sidebar.error(f"❌ Erro no e-mail: {str(e)}")

# ==========================================
# 4. CONFIGURAÇÃO DA INTERFACE & INICIALIZAÇÃO
# ==========================================
st.set_page_config(page_title="Linux Essentials - Plataforma de Estudos", page_icon="🐧", layout="wide")

st.markdown("""
    <style>
        div[data-testid="stRadio"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
            font-weight: 500 !important;
            color: #334155 !important;
            font-size: 16px !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label [data-testid="stWidgetCircle"] {
            border: 2px solid #CBD5E1 !important;
            background-color: #FFFFFF !important;
            width: 20px !important;
            height: 20px !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
            background-color: #F8FAFC !important;
            border-radius: 8px;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"] {
            background-color: #EFF6FF !important; 
            border: 1px solid #3B82F6 !important; 
            border-radius: 8px !important;
            padding: 8px 12px !important;
        }
        div[data-testid="stRadio"] div[role="radiogroup"] label[data-checked="true"] div[data-testid="stMarkdownContainer"] {
            color: #1E40AF !important; 
            font-weight: 700 !important;
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
if 'tempo_limite_simulado' not in st.session_state:
    st.session_state.tempo_limite_simulado = None
if 'inicio_simulado' not in st.session_state:
    st.session_state.inicio_simulado = None

# ==========================================
# 5. CONTROLES DA BARRA LATERAL
# ==========================================
# Executa a função robusta de contagem antes de renderizar a barra lateral
num_online, num_visitas = obter_metricas_acesso()

col_online, col_visitas = st.sidebar.columns(2)
with col_online:
    st.metric(label="🟢 Online Agora", value=num_online)
with col_visitas:
    st.metric(label="👥 Visitas Totais", value=num_visitas)

st.sidebar.divider()

st.sidebar.header("👤 Identificação do Aluno")
nome_usuario = st.sidebar.text_input("Seu Nome para o Placar (Obrigatório):", max_chars=20).strip()
email_usuario = st.sidebar.text_input("Seu E-mail (Opcional):").strip()

st.sidebar.divider()
st.sidebar.subheader("🕹️ Selecione o Modo de Estudo")
modo_selecionado = st.sidebar.radio(
    "Ambiente:", 
    ["📖 Área de Treino (Geral)", "🎯 Treino por Tópico (Focado)", "⏱️ Simulado LPI (Prova Real 40 Q)"]
)

# ==========================================
# 6. FLUXO DOS AMBIENTES DE ESTUDO
# ==========================================

# --- MODO 1: ÁREA DE TREINAMENTO GERAL ---
if modo_selecionado == "📖 Área de Treino (Geral)":
    st.title("📖 Área de Treino e Fixação Técnica")
    st.write("Responda às questões abaixo. O feedback é exibido em tempo real para cada questão.")

    questoes_treino = st.session_state.questoes_treino
    total_acertos_treino = 0

    for idx, q in enumerate(questoes_treino):
        st.markdown(f"### Questão {idx + 1} | `{q['topico']}`")
        st.markdown(f"**{q['pergunta']}**")
        
        hash_pergunta = str(hash(q['pergunta']))
        chave_resposta = f"treino_{hash_pergunta}"
        
        indice_padrao = None
        if chave_resposta in st.session_state.respostas_treino_salvas:
            if st.session_state.respostas_treino_salvas[chave_resposta] in q['opcoes']:
                indice_padrao = q['opcoes'].index(st.session_state.respostas_treino_salvas[chave_resposta])

        resposta = st.radio(
            f"Selecione a opção da Questão {idx + 1}:",
            q['opcoes'],
            index=indice_padrao,
            key=f"radio_treino_{idx}_{hash_pergunta}"
        )
        
        st.session_state.respostas_treino_salvas[chave_resposta] = resposta

        if resposta:
            if resposta == q['correta']:
                st.success("🎯 Resposta Correta!")
                total_acertos_treino += 1
            else:
                st.error(f"❌ Resposta Incorreta. A alternativa certa é: **{q['correta']}**")
            
            with st.expander("📚 Ver Explicação Técnica"):
                st.info(q['explicacao'])
        
        st.divider()

    if nome_usuario:
        st.session_state.ranking_treino[nome_usuario] = f"{total_acertos_treino}/{len(questoes_treino)}"

# --- MODO 2: TREINO POR TÓPICO ---
elif modo_selecionado == "🎯 Treino por Tópico (Focado)":
    st.title("🎯 Treino Direcionado por Tópicos")
    
    topicos_disponiveis = sorted(list(set([q['topico'] for q in QUESTOES_POOL])))
    topico_escolhido = st.selectbox("Escolha o tópico que deseja dominar:", topicos_disponiveis)
    
    questoes_filtradas = [q for q in QUESTOES_POOL if q['topico'] == topico_escolhido]
    st.write(f"Encontradas **{len(questoes_filtradas)}** questões para este tópico.")
    
    total_acertos_topico = 0
    
    for idx, q in enumerate(questoes_filtradas):
        st.markdown(f"### Questão {idx + 1}")
        st.markdown(f"**{q['pergunta']}**")
        
        hash_pergunta = str(hash(q['pergunta']))
        resposta = st.radio(
            f"Opções para a Questão {idx + 1}:",
            q['opcoes'],
            index=None,
            key=f"radio_topico_{idx}_{hash_pergunta}"
        )
        
        if resposta:
            if resposta == q['correta']:
                st.success("🎯 Correto!")
                total_acertos_topico += 1
            else:
                st.error(f"❌ Erro! Alternativa correta: **{q['correta']}**")
            
            with st.expander("📚 Detalhes do Conceito"):
                st.info(q['explicacao'])
        st.divider()

    if nome_usuario and len(questoes_filtradas) > 0:
        st.session_state.ranking_topico[nome_usuario] = f"{total_acertos_topico}/{len(questoes_filtradas)}"

# --- MODO 3: SIMULADO LINUX ESSENTIALS ---
elif modo_selecionado == "⏱️ Simulado LPI (Prova Real 40 Q)":
    st.title("⏱️ Simulado Preparatório - Linux Essentials")
    
    if not nome_usuario:
        st.warning("👤 Por favor, insira seu **Nome** na barra lateral esquerda para iniciar o Simulado.")
    else:
        DURACAO_PROVA = 3600 
        
        if not st.session_state.tempo_limite_simulado:
            st.session_state.tempo_limite_simulado = time.time() + DURACAO_PROVA
            st.session_state.inicio_simulado = time.time()

        tempo_restante = int(st.session_state.tempo_limite_simulado - time.time())

        if tempo_restante <= 0 and not st.session_state.simulado_entregue:
            st.session_state.simulado_entregue = True
            st.error("⏰ O tempo acabou! Seu simulado foi encerrado e computado automaticamente.")
            st.rerun()

        questoes_simulado = st.session_state.questoes_simulado
        
        if not st.session_state.simulado_entregue:
            mins, segs = divmod(tempo_restante, 60)
            st.metric(label="⏳ Tempo Restante de Prova", value=f"{mins:02d}m {segs:02d}s")
            
            if tempo_restante <= 300:
                st.warning("⚠️ **Atenção Aluno!** Faltam menos de 5 minutos para o encerramento automático da sua prova!")
                
            st.write("---")

            for idx, q in enumerate(questoes_simulado):
                st.markdown(f"##### {idx + 1}. {q['pergunta']}")
                
                hash_pergunta = str(hash(q['pergunta']))
                resposta = st.radio(
                    f"Escolha para a Q{idx + 1}:",
                    q['opcoes'],
                    index=None,
                    key=f"simulado_q_{idx}_{hash_pergunta}",
                    label_visibility="collapsed"
                )
                if resposta:
                    st.session_state.respostas_simulado[hash_pergunta] = resposta
                st.divider()

            total_respondidas = len(st.session_state.respostas_simulado)
            total_necessarias = len(questoes_simulado)
            
            if st.button("📥 Entregar Simulado e Gerar Nota", type="primary"):
                if total_respondidas < total_necessarias:
                    st.error(f"⚠️ Incompleto: Você precisa responder todas as questões! Preencheu **{total_respondidas} de {total_necessarias}**.")
                else:
                    st.session_state.simulado_entregue = True
                    st.rerun()

        else:
            # EXIBIÇÃO DE RESULTADOS PÓS-PROVA
            pontuacao = 0
            tempo_decorrido_seg = int(time.time() - st.session_state.inicio_simulado) if st.session_state.inicio_simulado else 0
            t_min, t_seg = divmod(tempo_decorrido_seg, 60)
            tempo_formatado = f"{t_min}m {t_seg}s"

            relatorio_texto = f"--- BOLETIM DE DESEMPENHO LINUX ESSENTIALS ---\n"
            relatorio_texto += f"Aluno: {nome_usuario}\n"
            relatorio_texto += f"Tempo de Prova: {tempo_formatado}\n\n"
            
            st.subheader("📊 Resultado Geral da Prova")
            
            for idx, q in enumerate(questoes_simulado):
                hash_pergunta = str(hash(q['pergunta']))
                resp_aluno = st.session_state.respostas_simulado.get(hash_pergunta, "Não Respondida")
                if resp_aluno == q['correta']:
                    pontuacao += 1
                    status = "CORRETA"
                else:
                    status = "INCORRETA"
                relatorio_texto += f"Q{idx+1}: {status} (Escolheu: {resp_aluno} | Correta: {q['correta']})\n"

            percentual = (pontuacao / len(questoes_simulado)) * 100
            
            if percentual >= 70:
                st.balloons()
                st.success(f"🎉 **Aprovado!** Você acertou {pontuacao} de {len(questoes_simulado)} ({percentual:.1f}%)")
                st.session_state.ranking_simulado[nome_usuario] = f"{pontuacao}/{len(questoes_simulado)} (Aprovado)"
            else:
                st.error(f"📉 **Abaixo da meta de 70%.** Você acertou {pontuacao} de {len(questoes_simulado)} ({percentual:.1f}%)")
                st.session_state.ranking_simulado[nome_usuario] = f"{pontuacao}/{len(questoes_simulado)} (Recuperação)"

            with st.expander("🔍 Ver Gabarito Técnico Detalhado", expanded=True):
                for idx, q in enumerate(questoes_simulado):
                    hash_pergunta = str(hash(q['pergunta']))
                    resp_aluno = st.session_state.respostas_simulado.get(hash_pergunta, "Não Respondida")
                    if resp_aluno == q['correta']:
                        st.write(f"✅ **{idx+1}. {q['pergunta']}**")
                    else:
                        st.write(f"❌ **{idx+1}. {q['pergunta']}**")
                    st.write(f"Sua resposta: *{resp_aluno}* | Resposta certa: **{q['correta']}**")
                    st.info(f"Explicação: {q['explicacao']}")
                    st.divider()

            if email_usuario:
                relatorio_texto += f"\nNota Final: {percentual:.1f}% - Aproveitamento: {pontuacao}/{len(questoes_simulado)}"
                enviar_email_seguro(
                    email_usuario, 
                    f"Resultado Simulado Linux Essentials - {nome_usuario}", 
                    relatorio_texto
                )

            if st.button("🔄 Refazer Novo Simulado"):
                st.session_state.questoes_simulado = gerar_40_questoes()
                st.session_state.respostas_simulado = {}
                st.session_state.simulado_entregue = False
                st.session_state.tempo_limite_simulado = None
                st.session_state.inicio_simulado = None
                st.rerun()

# --- RANKING E PLACAR LIDERES NA BARRA LATERAL ---
st.sidebar.divider()
st.sidebar.subheader("🏆 Placar de Líderes")
if st.sidebar.checkbox("Exibir Rankings Ativos"):
    st.sidebar.markdown("**Área de Treino:**")
    st.sidebar.json(st.session_state.ranking_treino)
    st.sidebar.markdown("**Simulados Linux Essentials:**")
    st.sidebar.json(st.session_state.ranking_simulado)
