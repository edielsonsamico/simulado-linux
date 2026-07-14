import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time
import os

# ==========================================
# 1. SISTEMA DE MONITORIZAÇÃO EM MEMÓRIA (TOTALMENTE SEGURO)
# ==========================================

@st.cache_resource
def obter_armazenamento_global():
    return {
        "usuarios_online": {},     # Chave: usuario_uid -> Valor: timestamp
        "registro_visitas": set(), # Guarda os UIDs de visitas únicas
        "visitas_totais": 0
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
        
    limite_inatividade = 60
    uids_para_remover = [
        uid for uid, ultimo_acesso in memoria_global["usuarios_online"].items()
        if agora - ultimo_acesso > limite_inatividade
    ]
            
    for uid in uids_para_remover:
        memoria_global["usuarios_online"].pop(uid, None)
        
    total_online = max(1, len(memoria_global["usuarios_online"]))
    total_visitas = memoria_global["visitas_totais"]
    
    return total_online, total_visitas


# ==========================================
# 2. FUNÇÕES AUXILIARES DE PROCESSAMENTO DE DADOS
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
# 3. BANCO DE DADOS INTEGRADO (BASE)
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

QUESTOES_POOL = desduplicar_questoes(QUESTOES_POOL_RAW)


# ==========================================
# 4. CARREGAMENTO SEGURO DOS ARQUIVOS EXTERNOS
# ==========================================
preguntas_existentes = {normalizar_texto(q["pergunta"]) for q in QUESTOES_POOL}

for i in range(101, 111):
    try:
        modulo = __import__(f"topico{i}")
        pool = getattr(modulo, f"POOL_{i}")
        for q in pool:
            if isinstance(q, dict) and "pergunta" in q:
                pergunta_norm = normalizar_texto(q["pergunta"])
                if pergunta_norm not in preguntas_existentes:
                    preguntas_existentes.add(pergunta_norm)
                    QUESTOES_POOL.append(q)
    except ModuleNotFoundError:
        # Se o ficheiro de tópico não existir, ignora de forma silenciosa e continua
        pass
    except Exception:
        # Previne erros no caso de o ficheiro existir mas ter falhas de sintaxe
        pass


# ==========================================
# 5. FUNÇÕES GLOBAIS DE SISTEMA
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
# 6. CONFIGURAÇÃO DA INTERFACE & ESTILIZAÇÃO CSS
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


# ==========================================
# 7. INICIALIZAÇÃO DO ESTADO DA SESSÃO (SESSION STATE)
# ==========================================
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

# Agora esta função já foi declarada e pode ser executada sem NameError!
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
# 8. CONFIGURAÇÃO E DESENHO DA BARRA LATERAL (SIDEBAR)
# ==========================================

num_online, num_visitas = gerenciar_acesso_e_obter_metricas()

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
    [
        "📖 Área de Treino (Geral)", 
        "🎯 Treino por Tópico (Focado)", 
        "⏱️ Simulado LPI (Prova Real 40 Q)",
        "ℹ️ Créditos & Desenvolvimento"
    ]
)


# ==========================================
# 9. FLUXO DOS AMBIENTES DE ESTUDO (ÁREA CENTRAL)
# ==========================================

# --- MODO: CRÉDITOS & DESENVOLVIMENTO ---
if modo_selecionado == "ℹ️ Créditos & Desenvolvimento":
    st.title("ℹ️ Créditos & Desenvolvimento")
    st.write("Conheça o desenvolvedor responsável por esta plataforma de estudos e simulados.")
    
    st.markdown("""
    <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 30px; border-radius: 12px; margin-top: 20px;">
        <h2 style="color: #1E3A8A; margin-top: 0px;">Edielson Samico</h2>
        <p style="font-size: 16px; color: #475569;">
            Desenvolvedor e entusiasta de tecnologia Linux, infraestrutura e criação de sistemas web interativos.
        </p>
        <hr style="border: 0; border-top: 1px dashed #CBD5E1; margin: 20px 0;">
        <h4 style="color: #0F172A; margin-bottom: 15px;">Entre em contato:</h4>
        
        <div style="display: flex; flex-direction: column; gap: 12px; font-size: 16px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 20px;">💬</span>
                <a href="https://wa.me/5581987316454" target="_blank" style="color: #25D366; font-weight: bold; text-decoration: none;">
                    WhatsApp (81 98731-6454)
                </a>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 20px;">📸</span>
                <a href="https://instagram.com/edielsonsamico" target="_blank" style="color: #E1306C; font-weight: bold; text-decoration: none;">
                    Instagram (@edielsonsamico)
                </a>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 20px;">🎥</span>
                <a href="https://youtube.com/@EdielsonSamico" target="_blank" style="color: #FF0000; font-weight: bold; text-decoration: none;">
                    YouTube (@EdielsonSamico)
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- MODO 1: ÁREA DE TREINAMENTO GERAL ---
elif modo_selecionado == "📖 Área de Treino (Geral)":
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
