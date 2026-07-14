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
        "registro_visitas": set(), # Guarda os UIDs de visitas uniques
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
# 3. BANCO DE DADOS INTEGRADO RESTAURADO
# ==========================================
QUESTOES_POOL_RAW = [
    {"id": 1, "topico": "Tópico 101: Arquitetura", "pergunta": "Qual comando é utilizado para listar informações detalhadas do chipset e dos componentes no barramento PCI?", "opcoes": ["lspci", "lsusb", "lsmod", "dmesg"], "correta": "lspci", "explicacao": "O comando lspci varre o barramento PCI do hardware listando controladores, placas e chipsets integrados."},
    {"id": 2, "topico": "Tópico 102: Pacotes", "pergunta": "De acordo com a hierarquia do FHS, qual diretório é destinado a guardar exclusivamente os arquivos de configuração específicos da máquina local?", "opcoes": ["/etc", "/var", "/usr", "/opt"], "correta": "/etc", "explicacao": "O diretório /etc é o local padronizado pelo FHS para armazenar scripts e arquivos de configuração de texto do sistema."},
    {"id": 3, "topico": "Tópico 103: Comandos", "pergunta": "No histórico do interpretador de comandos Bash, qual atalho de token repete imediatamente a execução do Classification do último comando utilizado?", "opcoes": ["!!", "!$", "history -r", "ctrl+r"], "correta": "!!", "explicacao": "As duas exclamações '!!' chamam e executam novamente no prompt a linha exata de comando disparada anteriormente."},
    {"id": 4, "topico": "Tópico 104: Dispositivos", "pergunta": "Qual comando relata em tempo real o espaço livre/disponível e o uso em blocos para todos os sistemas de arquivos atualmente montados?", "opcoes": ["df", "du", "fdisk", "free"], "correta": "df", "explicacao": "O comando df (disk free) lê a tabela de montagens do sistema exibindo capacidades, space ocupado e pontos de montagem activos."},
    {"id": 5, "topico": "Tópico 105: Scripts e SQL", "pergunta": "Em um script executável em shell Bash, qual comando pausa a execução contínua para ler informações digitadas pelo usuário no teclado?", "opcoes": ["read", "input", "get", "scan"], "correta": "read", "explicacao": "O comando embutido 'read' interrompe o script colhendo os caracteres do fluxo de entrada padrão (stdin) e salvando-os em uma variável."},
    {"id": 6, "topico": "Tópico 106: Desktops", "pergunta": "Qual é o caminho completo e o nome do arquivo de configuração central responsável por gerenciar os parâmetros de vídeo e entradas do servidor de janelas X11?", "opcoes": ["/etc/X11/xorg.conf", "/etc/X11/x11.conf", "/etc/xorg.conf", "/var/X11/xorg.conf"], "correta": "/etc/X11/xorg.conf", "explicacao": "O arquivo estático /etc/X11/xorg.conf centraliza os módulos de layout, mouses, teclados, placas de vídeo e monitores na arquitetura XOrg clássica."},
    {"id": 7, "topico": "Tópico 107: Administração", "pergunta": "Qual arquivo confinado abriga de forma criptografada as senhas dos usuários e as regras específicas de expiração de validade da conta?", "opcoes": ["/etc/shadow", "/etc/passwd", "/etc/secure", "/var/shadow"], "correta": "/etc/shadow", "explicacao": "Por motivos de segurança, as hashes de senhas e políticas de obsolescência ficam trancadas no arquivo /etc/shadow com permissões restritas a root."},
    {"id": 8, "topico": "Tópico 108: Serviços", "pergunta": "O protocolo de sincronização temporal NTP executa o seu tráfego vital por meio de qual porta de rede e protocolo de transporte, respectively?", "opcoes": ["Porta UDP 123", "Porta TCP 123", "Porta UDP 53", "Porta TCP 80"], "correta": "Porta UDP 123", "explicacao": "O Network Time Protocol (NTP) dita a troca estruturada de pacotes de timestamp de tempo sobre datagramas na porta UDP 123."},
    {"id": 9, "topico": "Tópico 110: Redes", "pergunta": "Na configuração básica e resolução estática sem domínio real de rede externa, qual arquivo mapeia pares de IP e Nome Local no Linux?", "opcoes": ["/etc/hosts", "/etc/resolv.conf", "/etc/networks", "/etc/hostname"], "correta": "/etc/hosts", "explicacao": "O arquivo /etc/hosts associa IPs a nomes locais manualmente, sem depender de servidores DNS."},
    {"id": 10, "topico": "Tópico 110: Segurança", "pergunta": "Qual a sintaxe restrita aplicada no utilitário de busca find para garimpar especificamente todos e quaisquer arquivos baseados no gatilho do modo especial SUID nos binários ativos da raiz (/)?", "opcoes": ["find / -perm -4000", "find / -perm 777", "find / -type f -suid", "find / -user root"], "correta": "find / -perm -4000", "explicacao": "O bit 4000 identifica de forma octal o SUID, rodando arquivos com privilégios do dono do binário."}
]

QUESTOES_POOL = desduplicar_questoes(QUESTOES_POOL_RAW)


# ==========================================
# 4. CARREGAMENTO SEGURO DOS ARQUIVOS EXTERNOS
# ==========================================
preguntas_existentes = {normalizar_texto(q["pergunta"]) for q in QUESTOES_POOL}

# Atribui IDs únicos sequenciais às novas perguntas importadas para evitar colisões
proximo_id = max([q.get("id", 100) for q in QUESTOES_POOL]) + 1 if QUESTOES_POOL else 101

for i in range(101, 111):
    try:
        modulo = __import__(f"topico{i}")
        pool = getattr(modulo, f"POOL_{i}")
        for q in pool:
            if isinstance(q, dict) and "pergunta" in q:
                pergunta_norm = normalizar_texto(q["pergunta"])
                if pergunta_norm not in preguntas_existentes:
                    preguntas_existentes.add(pergunta_norm)
                    q_copia = q.copy()
                    if "id" not in q_copia:
                        q_copia["id"] = proximo_id
                        proximo_id += 1
                    QUESTOES_POOL.append(q_copia)
    except ModuleNotFoundError:
        pass
    except Exception:
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

# Estados de controle para a Área VIP bloqueada
if "vip_liberado" not in st.session_state:
    st.session_state.vip_liberado = False


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
        "🎁 Materiais VIP & Simulados",
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
    
    with st.container(border=True):
        st.subheader("Edielson Samico")
        st.write("Desenvolvedor de sistemas e aplicativos, especialista em criação de soluções web interativas, logos, identidades visuais corporativas, análise de tráfego web e suporte tecnológico completo para empresas e clientes finais.")
        
        st.divider()
        st.markdown("### 📞 Entre em contato:")
        
        col_wa, col_ig, col_yt = st.columns(3)
        
        with col_wa:
            st.link_button("💬 WhatsApp", "https://wa.me/5581987316454", use_container_width=True)
            st.caption("81 98731-6454")
            
        with col_ig:
            st.link_button("📸 Instagram", "https://instagram.com/edielsonsamico", use_container_width=True)
            st.caption("@edielsonsamico")
            
        with col_yt:
            st.link_button("🎥 YouTube", "https://youtube.com/@EdielsonSamico", use_container_width=True)
            st.caption("@EdielsonSamico")

# --- MODO: MATERIAIS VIP & SIMULADOS (SOCIAL LOCKER CORRIGIDO) ---
elif modo_selecionado == "🎁 Materiais VIP & Simulados":
    st.title("🎁 Área VIP - Apostilas & Simulados Exclusivos")
    st.write("Acelere sua aprovação nas certificações resgatando materiais avançados de estudo.")

    if not st.session_state.vip_liberado:
        with st.container(border=True):
            st.markdown("<h3 style='text-align: center; color: #1E3A8A;'>🔒 Conteúdo Exclusivo Bloqueado</h3>", unsafe_allow_html=True)
            st.markdown(
                """
                <p style='text-align: center; font-size: 16px;'>
                    Para liberar o download da nossa <b>Apostila Preparatória Completa</b> e acessar o <b>Simulado VIP</b>, 
                    inscreva-se no nosso canal do YouTube! É totalmente gratuito e apoia nosso trabalho.
                </p>
                """, 
                unsafe_allow_html=True
            )
            st.divider()
            col_inscrever, col_liberar = st.columns([2, 1])
            with col_inscrever:
                st.link_button("❤️ 1º Passo: Inscrever-se no Canal", "https://youtube.com/@EdielsonSamico?sub_confirmation=1", use_container_width=True, type="primary")
            with col_liberar:
                if st.button("🔓 2º Passo: Liberar Acesso", use_container_width=True):
                    st.session_state.vip_liberado = True
                    st.balloons()
                    st.rerun() # Linha corrigida de forma segura!
    else:
        st.success("🎉 Parabéns! Seus conteúdos e recursos VIP estão totalmente desbloqueados.")
        col_apostila, col_simulado_vip = st.columns(2)
        
        with col_apostila:
            with st.container(border=True):
                st.subheader("📚 Apostila de Certificação VIP")
                st.write("Material completo cobrando comandos Linux essenciais, mapas mentais de arquitetura de diretórios e guias de redes.")
                st.link_button("📥 Baixar Apostila (PDF)", "https://github.com/EdielsonSamico", use_container_width=True)
                st.caption("Apostila de 10 páginas configurada com sucesso para a marca SAMICOIOT.")
                
        with col_simulado_vip:
            with st.container(border=True):
                st.subheader("🏆 Simulado VIP Avançado")
                st.write("Questões de nível de dificuldade elevado selecionadas e comentadas para testar seus limites reais antes da prova.")
                st.link_button(
                    "🚀 Abrir Simulado VIP", 
                    "https://notebooklm.google.com/notebook/5c438fb6-d069-4b7f-b64c-542d53add525/artifact/f5d7b6b8-9e48-4582-bbe8-e491bb4171c9?utm_source=nlm_web_share&utm_medium=google_oo&utm_campaign=art_share_1&utm_content=&utm_smc=nlm_web_share_google_oo_art_share_1_", 
                    use_container_width=True,
                    type="primary"
                )
                st.caption("Link externo integrado com sucesso na plataforma SAMICOIOT.")

# --- MODO 1: ÁREA DE TREINAMENTO GERAL ---
elif modo_selecionado == "📖 Área de Treino (Geral)":
    st.title("📖 Área de Treino e Fixação Técnica")
    st.write("Responda às questões abaixo. O feedback é exibido em tempo real para cada questão.")

    if not QUESTOES_POOL:
        st.info("ℹ️ Nenhuma questão encontrada.")
    else:
        for idx, q in enumerate(st.session_state.questoes_treino):
            st.markdown(f"### Questão {idx + 1} | `{q['topico']}`")
            st.markdown(f"**{q['pergunta']}**")
            resposta = st.radio(f"Selecione a opção da Q{idx + 1}:", q['opcoes'], index=None, key=f"t_{idx}")
            if resposta:
                if resposta == q['correta']:
                    st.success("🎯 Resposta Correta!")
                else:
                    st.error(f"❌ Incorreta. Certo: **{q['correta']}**")
            st.divider()

# --- MODO 2: TREINO POR TÓPICO ---
elif modo_selecionado == "🎯 Treino por Tópico (Focado)":
    st.title("🎯 Treino Direcionado por Tópicos")
    topicos_disponiveis = sorted(list(set([q['topico'] for q in QUESTOES_POOL])))
    topico_escolhido = st.selectbox("Escolha o tópico:", topicos_disponiveis)
    questoes_filtradas = [q for q in QUESTOES_POOL if q['topico'] == topico_escolhido]
    for idx, q in enumerate(questoes_filtradas):
        st.markdown(f"### Questão {idx + 1}")
        st.markdown(f"**{q['pergunta']}**")
        resposta = st.radio(f"Opções Q{idx + 1}:", q['opcoes'], index=None, key=f"f_{idx}")
        if resposta:
            if resposta == q['correta']:
                st.success("🎯 Correto!")
            else:
                st.error(f"❌ Erro! Certo: **{q['correta']}**")
        st.divider()

# --- MODO 3: SIMULADO LINUX ESSENTIALS ---
elif modo_selecionado == "⏱️ Simulado LPI (Prova Real 40 Q)":
    st.title("⏱️ Simulado Preparatório - Linux Essentials")
    if not nome_usuario:
        st.warning("👤 Por favor, insira seu Nome na barra lateral esquerda.")
    else:
        st.write("Estrutura padrão de simulado ativa.")
        for idx, q in enumerate(st.session_state.questoes_simulado):
            st.markdown(f"##### {idx + 1}. {q['pergunta']}")
            st.radio(f"Escolha para a Q{idx + 1}:", q['opcoes'], index=None, key=f"s_{idx}", label_visibility="collapsed")
            st.divider()
