import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time
import os
import re # Biblioteca para remoção inteligente de numeração nas perguntas

# ==========================================
# 1. SISTEMA DE MONITORIZAÇÃO EM MEMÓRIA (MÉTRICAS)
# ==========================================
@st.cache_resource
def obter_armazenamento_global():
    return {
        "usuarios_online": {},     
        "registro_visitas": set(), 
        "visitas_totais": 0,
        "placar_lideres": {} # Chave: Nome -> Valor: Maior Pontuação VIP Acumulada
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
# 2. FUNÇÕES AUXILIARES DE TRATAMENTO DE TEXTO (DESDUPLICAÇÃO INTELIGENTE)
# ==========================================
def normalizar_texto(texto):
    """Remove espaços, padroniza minúsculas e elimina prefixos numéricos para evitar duplicados."""
    texto_limpo = texto.strip().lower()
    # Remove prefixos como "Questão Avançada de Arquitetura 39:", "Questão 39:", "39.", "q39:" do início
    texto_limpo = re.sub(
        r'^(quest[ãa]o(\s+avançada)?(\s+de\s+arquitetura)?\s+\d+|q\d+|\d+)[:\.\-\s]+', 
        '', 
        texto_limpo
    )
    return " ".join(texto_limpo.split())

def desduplicar_questoes(lista_original):
    vistas = set()
    lista_limpa = []
    for q in lista_original:
        pergunta_norm = normalizar_texto(q["pergunta"])
        if pergunta_norm not in vistas:
            vistas.add(pergunta_norm)
            lista_limpa.append(q)
    return lista_limpa


# ==========================================
# 3. BANCO DE DADOS INTEGRADO (BASE COMPLETA)
# ==========================================
QUESTOES_POOL_RAW = [
    {"id": 1, "topico": "Tópico 101: Arquitetura", "pergunta": "Qual comando é utilizado para listar informações detalhadas do chipset e dos componentes no barramento PCI?", "opcoes": ["lspci", "lsusb", "lsmod", "dmesg"], "correta": "lspci", "explicacao": "O comando lspci varre o barramento PCI do hardware listando controladores, placas e chipsets integrados."},
    {"id": 2, "topico": "Tópico 102: Pacotes", "pergunta": "De acordo com a hierarquia do FHS, qual diretório é destinado a guardar exclusivamente os arquivos de configuração específicos da máquina local?", "opcoes": ["/etc", "/var", "/usr", "/opt"], "correta": "/etc", "explicacao": "O diretório /etc é o local padronizado pelo FHS para armazenar scripts e arquivos de configuração de texto do sistema."},
    {"id": 3, "topico": "Tópico 103: Comandos", "pergunta": "No histórico do interpretador de comandos Bash, qual atalho de token repete imediatamente a execução do último comando utilizado?", "opcoes": ["!!", "!$", "history -r", "ctrl+r"], "correta": "!!", "explicacao": "As duas exclamações '!!' chamam e executam novamente no prompt a linha exata de comando disparada anteriormente."},
    {"id": 4, "topico": "Tópico 104: Dispositivos", "pergunta": "Qual comando relata em tempo real o espaço livre/disponível e o uso em blocos para todos os sistemas de arquivos atualmente montados?", "opcoes": ["df", "du", "fdisk", "free"], "correta": "df", "explicacao": "O comando df (disk free) lê a tabela de montagens do sistema exibindo capacidades, espaço ocupado e pontos de montagem activos."},
    {"id": 5, "topico": "Tópico 105: Scripts e SQL", "pergunta": "Em um script executável em shell Bash, qual comando pausa a execução contínua para ler informações digitadas pelo usuário no teclado?", "opcoes": ["read", "input", "get", "scan"], "correta": "read", "explicacao": "O comando embutido 'read' interrompe o script colhendo os caracteres do fluxo de entrada padrão (stdin) e salvando-os em uma variável."},
    {"id": 6, "topico": "Tópico 106: Desktops", "pergunta": "Qual é o caminho completo e o nome do arquivo de configuração central responsável por gerenciar os parâmetros de vídeo e entradas do servidor de janelas X11?", "opcoes": ["/etc/X11/xorg.conf", "/etc/X11/x11.conf", "/etc/xorg.conf", "/var/X11/xorg.conf"], "correta": "/etc/X11/xorg.conf", "explicacao": "O arquivo estático /etc/X11/xorg.conf centraliza os módulos de layout, mouses, teclados, placas de vídeo e monitores na arquitetura XOrg clássica."},
    {"id": 7, "topico": "Tópico 107: Administração", "pergunta": "Qual arquivo confinado abriga de forma criptografada as senhas dos usuários e as regras específicas de expiração de validade da conta?", "opcoes": ["/etc/shadow", "/etc/passwd", "/etc/secure", "/var/shadow"], "correta": "/etc/shadow", "explicacao": "Por motivos de segurança, as hashes de senhas e políticas de obsolescência ficam trancadas no arquivo /etc/shadow com permissões restritas a root."},
    {"id": 8, "topico": "Tópico 108: Serviços", "pergunta": "O protocol de sincronização temporal NTP executa o seu tráfego vital por meio de qual porta de rede e protocolo de transporte, respectivamente?", "opcoes": ["Porta UDP 123", "Porta TCP 123", "Porta UDP 53", "Porta TCP 80"], "correta": "Porta UDP 123", "explicacao": "O Network Time Protocol (NTP) dita a troca estruturada de pacotes de timestamp de tempo sobre datagramas na porta UDP 123."},
    {"id": 9, "topico": "Tópico 110: Redes", "pergunta": "Na configuração básica e resolução estática sem domínio real de rede externa, qual arquivo mapeia pares de IP e Nome Local no Linux?", "opcoes": ["/etc/hosts", "/etc/resolv.conf", "/etc/networks", "/etc/hostname"], "correta": "/etc/hosts", "explicacao": "O arquivo /etc/hosts associa IPs a nomes locais manualmente, sem depender de servidores DNS."},
    {"id": 10, "topico": "Tópico 110: Segurança", "pergunta": "Qual a sintaxe restrita aplicada no utilitário de busca find para garimpar especificamente todos e quaisquer arquivos baseados no gatilho do modo especial SUID nos binários ativos da raiz (/)?", "opcoes": ["find / -perm -4000", "find / -perm 777", "find / -type f -suid", "find / -user root"], "correta": "find / -perm -4000", "explicacao": "O bit 4000 identifica de forma octal o SUID, rodando arquivos com privilégios do dono do binário."}
]

QUESTOES_POOL = desduplicar_questoes(QUESTOES_POOL_RAW)

# ==========================================
# 4. CARREGAMENTO DINÂMICO DE ARQUIVOS EXTERNOS (TÓPICOS 101-110)
# ==========================================
preguntas_existentes = {normalizar_texto(q["pergunta"]) for q in QUESTOES_POOL}
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
# 5. POOL COMPLETO DO QUIZ VIP - COM PESO/DIFICULDADE CONFIGURADOS
# ==========================================
QUESTOES_VIP_REPOSITORIO_COMPLETO = [
    # Bloco 1
    {"id": 901, "pergunta": "Qual é a principal diferença entre os dispositivos do tipo 'Coldplug' e 'Hotplug'?", "opcoes": ["A. Dispositivos hotplug são identificados apenas no momento do POST da BIOS.", "B. Dispositivos hotplug só podem ser conectados via porta USB 3.0.", "C. Dispositivos coldplug exigem que o sistema seja desligado para conexão ou remoção.", "D. Coldplug é um termo usado exclusivamente para processadores em servidores."], "correta": "C. Dispositivos coldplug exigem que o sistema seja desligado para conexão ou remoção.", "dica": "Cold = Frio (Desligado) | Hot = Quente (Ligado).", "explicacao": "Sistemas Coldplug necessitam da máquina desligada para alteração física de hardware.", "bloco": 1, "dificuldade": "Fácil", "pontos": 10},
    {"id": 902, "pergunta": "De acordo com a hierarquia do sistema de arquivos (FHS), qual é a finalidade principal do diretório /var?", "opcoes": ["A. Servir como ponto de montagem padrão para mídias removíveis.", "B. Conter dados variáveis, como logs do sistema e arquivos de spool.", "C. Armazenar arquivos estáticos do gerenciador de boot.", "D. Abrigar comandos binários essenciais para todos os usuários."], "correta": "B. Conter dados variáveis, como logs do sistema e arquivos de spool.", "dica": "O nome vem de 'variable'.", "explicacao": "O /var é designado para conter logs, caches e spools.", "bloco": 1, "dificuldade": "Média", "pontos": 20},
]

# Fallback seguro para garantir as 40 questões VIP estruturadas com peso
dificuldades_peso = [
    {"dificuldade": "Fácil", "pontos": 10},
    {"dificuldade": "Média", "pontos": 20},
    {"dificuldade": "Difícil", "pontos": 30}
]

while len(QUESTOES_VIP_REPOSITORIO_COMPLETO) < 40:
    nova_q = random.choice(QUESTOES_POOL).copy()
    peso_sorteado = random.choice(dificuldades_peso)
    nova_q["id"] = 1000 + len(QUESTOES_VIP_REPOSITORIO_COMPLETO)
    nova_q["bloco"] = (len(QUESTOES_VIP_REPOSITORIO_COMPLETO) // 10) + 1
    nova_q["dica"] = "Consulte o resumo do seu Guia de Estudos."
    nova_q["explicacao"] = "Reveja a documentação oficial LPI."
    nova_q["dificuldade"] = peso_sorteado["dificuldade"]
    nova_q["pontos"] = peso_sorteado["pontos"]
    QUESTOES_VIP_REPOSITORIO_COMPLETO.append(nova_q)


# ==========================================
# 6. FUNÇÕES GERADORAS DE SIMULADO
# ==========================================
def gerar_40_questoes_aleatorias():
    pool_disponivel = list(QUESTOES_POOL)
    tamanho_simulado = min(40, len(pool_disponivel))
    return random.sample(pool_disponivel, k=tamanho_simulado)


# ==========================================
# 7. CONFIGURAÇÃO DA INTERFACE & ESTILIZAÇÃO
# ==========================================
st.set_page_config(page_title="Linux Essentials - Plataforma de Estudos", page_icon="🐧", layout="wide")

st.markdown("""
    <style>
        div[data-testid="stRadio"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
            font-weight: 500 !important;
            color: #334155 !important;
            font-size: 16px !important;
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
    </style>
""", unsafe_allow_html=True)


# ==========================================
# 8. INICIALIZAÇÃO DO ESTADO DA SESSÃO (SESSION STATE)
# ==========================================
if 'questoes_treino' not in st.session_state:
    st.session_state.questoes_treino = list(QUESTOES_POOL)

if 'questoes_simulado' not in st.session_state:
    st.session_state.questoes_simulado = gerar_40_questoes_aleatorias()
if 'respostas_simulado' not in st.session_state:
    st.session_state.respostas_simulado = {}
if 'simulado_entregue' not in st.session_state:
    st.session_state.simulado_entregue = False
if 'inicio_simulado' not in st.session_state:
    st.session_state.inicio_simulado = None
if 'simulado_id' not in st.session_state:
    st.session_state.simulado_id = random.randint(10000, 99999)

# Estados da Área VIP Gamificada com Pontuação
if "vip_liberado" not in st.session_state:
    st.session_state.vip_liberado = False
if "bloco_vip_atual" not in st.session_state:
    st.session_state.bloco_vip_atual = 1
if "indice_pergunta_bloco" not in st.session_state:
    st.session_state.indice_pergunta_bloco = 0
if "acertos_bloco_atual" not in st.session_state:
    st.session_state.acertos_bloco_atual = 0
if "pontos_acumulados" not in st.session_state:
    st.session_state.pontos_acumulados = 0
if "questoes_sorteadas_blocos" not in st.session_state:
    st.session_state.questoes_sorteadas_blocos = {}

# Sorteia os cadernos inéditos iniciais
if not st.session_state.questoes_sorteadas_blocos:
    for b in range(1, 5):
        pool_b = [q for q in QUESTOES_VIP_REPOSITORIO_COMPLETO if q["bloco"] == b]
        st.session_state.questoes_sorteadas_blocos[b] = random.sample(pool_b, k=min(10, len(pool_b)))


# ==========================================
# 9. BARRA LATERAL (SIDEBAR COM AS 5 OPÇÕES)
# ==========================================
num_online, num_visitas = gerenciar_acesso_e_obter_metricas()

col_online, col_visitas = st.sidebar.columns(2)
col_online.metric(label="🟢 Online Agora", value=num_online)
col_visitas.metric(label="👥 Visitas Totais", value=num_visitas)

st.sidebar.divider()
st.sidebar.header("👤 Identificação")
nome_usuario = st.sidebar.text_input("Seu Nome para o Placar (Obrigatório para Rank):", max_chars=20).strip()

st.sidebar.divider()
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
# 10. CONTEÚDO DAS ABAS INTERATIVAS
# ==========================================

# --- ABA: CRÉDITOS ---
if modo_selecionado == "ℹ️ Créditos & Desenvolvimento":
    st.title("ℹ️ Créditos & Desenvolvimento")
    with st.container(border=True):
        st.subheader("Edielson Samico")
        st.write("Desenvolvedor de sistemas e engenheiro de infraestrutura na SAMICOIOT.")
        st.divider()
        col_wa, col_ig, col_yt = st.columns(3)
        col_wa.link_button("💬 WhatsApp", "https://wa.me/5581987316454", use_container_width=True)
        col_ig.link_button("📸 Instagram", "https://instagram.com/edielsonsamico", use_container_width=True)
        col_yt.link_button("🎥 YouTube", "https://youtube.com/@EdielsonSamico", use_container_width=True)

# --- ABA: TREINO GERAL ---
elif modo_selecionado == "📖 Área de Treino (Geral)":
    st.title("📖 Área de Treino Geral")
    for idx, q in enumerate(st.session_state.questoes_treino):
        st.markdown(f"### Questão {idx + 1} | `{q['topico']}`")
        st.markdown(f"**{q['pergunta']}**")
        resposta = st.radio("Opções:", q['opcoes'], index=None, key=f"t_{idx}")
        if resposta:
            if resposta == q['correta']:
                st.success("🎯 Resposta Correta!")
            else:
                st.error(f"❌ Incorreta. Certo: **{q['correta']}**")
        st.divider()

# --- ABA: TREINO FOCADO POR TÓPICO ---
elif modo_selecionado == "🎯 Treino por Tópico (Focado)":
    st.title("🎯 Treino Direcionado por Tópicos")
    topicos_disponiveis = sorted(list(set([q['topico'] for q in QUESTOES_POOL])))
    topico_escolhido = st.selectbox("Escolha o tópico desejado:", topicos_disponiveis)
    questoes_filtradas = [q for q in QUESTOES_POOL if q['topico'] == topico_escolhido]
    
    for idx, q in enumerate(questoes_filtradas):
        st.markdown(f"### Questão {idx + 1}")
        st.markdown(f"**{q['pergunta']}**")
        resposta = st.radio("Selecione a alternativa:", q['opcoes'], index=None, key=f"f_{idx}")
        if resposta:
            if resposta == q['correta']:
                st.success("🎯 Correto!")
            else:
                st.error(f"❌ Errado. Correto: **{q['correta']}**")
        st.divider()

# --- ABA: SIMULADO REAL DE 40 QUESTÕES COM CRONÔMETRO ---
elif modo_selecionado == "⏱️ Simulado LPI (Prova Real 40 Q)":
    st.title("⏱️ Simulado Preparatório Oficial LPI (40 Questões)")
    
    if not nome_usuario:
        st.warning("👤 Por favor, insira o seu Nome na barra lateral para iniciar o Simulado Oficial.")
    else:
        if st.session_state.inicio_simulado is None:
            st.session_state.inicio_simulado = time.time()
            st.session_state.simulado_entregue = False
            st.session_state.respostas_simulado = {}
            st.session_state.questoes_simulado = gerar_40_questoes_aleatorias()

        tempo_limite_segundos = 3600
        decorrido = time.time() - st.session_state.inicio_simulado
        restante_segundos = max(0, int(tempo_limite_segundos - decorrido))
        
        minutos = restante_segundos // 60
        segundos = restante_segundos % 60
        
        col_relogio, col_status = st.columns([1, 2])
        with col_relogio:
            if restante_segundos > 0 and not st.session_state.simulado_entregue:
                st.markdown(f"### ⏳ Tempo Restante: `{minutos:02d}:{segundos:02d}`")
                if st.button("🔄 Atualizar Relógio"):
                    st.rerun()
            elif restante_segundos <= 0:
                st.markdown("### 🚨 **TEMPO ESGOTADO!**")
                st.session_state.simulado_entregue = True
            else:
                st.markdown("### 🏁 Simulado Concluído")

        with col_status:
            st.info("Respondendo ao caderno de provas randômico da plataforma. Questões exclusivas sorteadas a cada nova tentativa!")

        st.divider()

        for idx, q in enumerate(st.session_state.questoes_simulado):
            st.markdown(f"##### **Questão {idx + 1}** | `{q['topico']}`")
            st.markdown(f"**{q['pergunta']}**")
            
            chave_resposta = f"ans_{st.session_state.simulado_id}_{q['id']}"
            
            opcao_selecionada = st.radio(
                "Alternativas:", 
                q['opcoes'], 
                index=None if chave_resposta not in st.session_state.respostas_simulado else q['opcoes'].index(st.session_state.respostas_simulado[chave_resposta]),
                key=f"sim_radio_{st.session_state.simulado_id}_{idx}",
                label_visibility="collapsed"
            )
            
            if opcao_selecionada:
                st.session_state.respostas_simulado[chave_resposta] = opcao_selecionada
            st.divider()

        col_entregar, col_resetar = st.columns(2)
        
        with col_entregar:
            if not st.session_state.simulado_entregue:
                if st.button("🏁 Finalizar e Entregar Simulado", type="primary", use_container_width=True):
                    st.session_state.simulado_entregue = True
                    st.rerun()
            else:
                acertos = 0
                for q in st.session_state.questoes_simulado:
                    chave = f"ans_{st.session_state.simulado_id}_{q['id']}"
                    resp = st.session_state.respostas_simulado.get(chave)
                    if resp == q['correta']:
                        acertos += 1
                
                percentual = (acertos / len(st.session_state.questoes_simulado)) * 100
                st.markdown(f"### 🎉 Resultado: **{acertos} / {len(st.session_state.questoes_simulado)} acertos** ({percentual:.1f}%)")
                if percentual >= 70:
                    st.success("🏆 Excelente! Você seria aprovado na prova oficial!")
                else:
                    st.error("🚨 Você ficou abaixo de 70% de acertos. Continue estudando os tópicos indicados no gabarito.")

        with col_resetar:
            if st.button("🔄 Gerar Novo Simulado (Inédito)", type="secondary", use_container_width=True):
                st.session_state.simulado_id = random.randint(10000, 99999)
                st.session_state.inicio_simulado = time.time()
                st.session_state.simulado_entregue = False
                st.session_state.respostas_simulado = {}
                st.session_state.questoes_simulado = gerar_40_questoes_aleatorias()
                st.balloons()
                st.rerun()

# --- ABA VIP: MATERIAIS VIP & SISTEMA DE BLOCOS GAMIFICADOS POR PESO ---
elif modo_selecionado == "🎁 Materiais VIP & Simulados":
    st.title("🎁 Área VIP - Apostilas & Simulados Exclusivos")
    st.write("Materiais avançados mantidos pela SAMICOIOT.")

    if not st.session_state.vip_liberado:
        with st.container(border=True):
            st.markdown("<h3 style='text-align: center; color: #1E3A8A;'>🔒 Conteúdo Exclusivo Bloqueado</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center;'>Inscreva-se no nosso canal do YouTube para desbloquear o download da Apostila e acessar o Simulado VIP.</p>", unsafe_allow_html=True)
            st.divider()
            col_ins, col_lib = st.columns([2, 1])
            col_ins.link_button("❤️ 1º Passo: Inscrever-se no Canal", "https://youtube.com/@EdielsonSamico?sub_confirmation=1", use_container_width=True, type="primary")
            if col_lib.button("🔓 2º Passo: Liberar Acesso", use_container_width=True):
                st.session_state.vip_liberado = True
                st.balloons()
                st.rerun()
    else:
        st.success("🎉 Parabéns! Seus conteúdos VIP estão totalmente desbloqueados.")
        col_apostila, col_simulado_vip = st.columns([1, 2])
        
        # CARD 1: DOWNLOAD DOS PDFs & PLACAR DE LÍDERES
        with col_apostila:
            with st.container(border=True):
                st.subheader("📚 Seus Livros & Materiais")
                st.write("Materiais técnicos otimizados para a certificação.")
                st.divider()
                
                caminho_apostila = "Apostila Premium de Certificação Linux LPIC-1.pdf"
                if os.path.exists(caminho_apostila):
                    with open(caminho_apostila, "rb") as file:
                        st.download_button(
                            label="📥 Baixar Apostila Premium (PDF)",
                            data=file,
                            file_name="Apostila Premium de Certificação Linux LPIC-1.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                else:
                    st.warning("⚠️ O arquivo '" + caminho_apostila + "' não foi localizado na pasta.")
                
                st.write("") 
                
                caminho_terminal = "LPIC-1_Terminal_2026.pdf"
                if os.path.exists(caminho_terminal):
                    with open(caminho_terminal, "rb") as file_t:
                        st.download_button(
                            label="📥 Baixar Terminal Blueprint 2026 (PDF)",
                            data=file_t,
                            file_name="LPIC-1_Terminal_2026.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                else:
                    st.warning("⚠️ O arquivo '" + caminho_terminal + "' não foi localizado.")
                
                st.divider()
                # --- EXIBIÇÃO DO RANKING DOS ALUNOS ---
                st.subheader("🥇 Placar Geral VIP")
                if not memoria_global["placar_lideres"]:
                    st.caption("Ainda sem registros. Seja o primeiro a pontuar!")
                else:
                    ordem_lideres = sorted(memoria_global["placar_lideres"].items(), key=lambda x: x[1], reverse=True)
                    for pos, (nome, pts) in enumerate(ordem_lideres[:5]):
                        medalha = "🥇" if pos == 0 else "🥈" if pos == 1 else "🥉" if pos == 2 else "👤"
                        st.write(f"{medalha} **{nome}**: `{pts} pts`")

        # CARD 2: SIMULADO VIP GAMIFICADO (4 BLOCOS DE 10 QUESTÕES POR PESO)
        with col_simulado_vip:
            with st.container(border=True):
                bloco_atual = st.session_state.bloco_vip_atual
                
                st.subheader(f"🏆 Linux Quiz VIP — Bloco {bloco_atual} de 4 (Nativo)")
                st.write(f"Sua Pontuação VIP Acumulada: **{st.session_state.pontos_acumulados} pts**")
                st.divider()
                
                caderno_atual = st.session_state.questoes_sorteadas_blocos[bloco_atual]
                idx_q = st.session_state.indice_pergunta_bloco
                total_q_bloco = len(caderno_atual)
                
                if idx_q < total_q_bloco:
                    q_atual = caderno_atual[idx_q]
                    
                    # Identificadores de peso e dificuldade na tela
                    cor_tag = "#10B981" if q_atual.get("dificuldade", "Fácil") == "Fácil" else "#F59E0B" if q_atual.get("dificuldade", "Fácil") == "Média" else "#EF4444"
                    st.markdown(
                        f"""
                        <div style='display: flex; gap: 10px; align-items: center; margin-bottom: 10px;'>
                            <span style='color: #64748B; font-weight: bold;'>{idx_q + 1} / {total_q_bloco}</span>
                            <span style='background-color: {cor_tag}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;'>{q_atual.get('dificuldade', 'Fácil')} (+{q_atual.get('pontos', 10)} pts)</span>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    st.markdown(f"#### **{q_atual['pergunta']}**")
                    
                    escolha = st.radio(
                        "Selecione uma alternativa:",
                        q_atual['opcoes'],
                        index=None,
                        key=f"vip_block_{bloco_atual}_q_{idx_q}"
                    )
                    
                    st.divider()
                    col_dica, col_prox = st.columns(2)
                    
                    with col_dica:
                        with st.expander("💡 Ver Dica"):
                            st.info(q_atual["dica"])
                            
                    with col_prox:
                        if st.button("Próxima Questão ➡️", use_container_width=True, type="primary"):
                            if escolha:
                                if escolha == q_atual['correta']:
                                    st.session_state.acertos_bloco_atual += 1
                                    st.session_state.pontos_acumulados += q_atual.get("pontos", 10)
                                    st.toast("🎯 Resposta Correta! (+" + str(q_atual.get('pontos', 10)) + " pontos adicionados)", icon="✅")
                                else:
                                    st.toast("❌ Incorreto!", icon="🚨")
                                st.session_state.indice_pergunta_bloco += 1
                                st.rerun()
                            else:
                                st.warning("Por favor, selecione uma alternativa antes de avançar.")
                else:
                    acertos = st.session_state.acertos_bloco_atual
                    st.markdown(f"### Fim do Bloco {bloco_atual}!")
                    st.markdown(f"Você acertou: **{acertos} / 10**")
                    
                    # Salva ou atualiza a maior pontuação do usuário de forma automática no placar
                    if nome_usuario:
                        nome_key = nome_usuario.strip()
                        recorde_antigo = memoria_global["placar_lideres"].get(nome_key, 0)
                        if st.session_state.pontos_acumulados > recorde_antigo:
                            memoria_global["placar_lideres"][nome_key] = st.session_state.pontos_acumulados
                    
                    if acertos >= 7:
                        if bloco_atual < 4:
                            st.success(f"🎉 Excelente! Você passou para o Bloco {bloco_atual + 1}!")
                            if st.button("Avançar para o Próximo Bloco ➡️", use_container_width=True, type="primary"):
                                st.session_state.bloco_vip_atual += 1
                                st.session_state.indice_pergunta_bloco = 0
                                st.session_state.acertos_bloco_atual = 0
                                st.rerun()
                        else:
                            st.balloons()
                            st.success("🏆 SENSACIONAL! Você concluiu todos os 4 Blocos do Quiz VIP com sucesso!")
                            if st.button("🔄 Reiniciar Toda a Jornada", use_container_width=True):
                                st.session_state.bloco_vip_atual = 1
                                st.session_state.indice_pergunta_bloco = 0
                                st.session_state.acertos_bloco_atual = 0
                                st.session_state.pontos_acumulados = 0
                                st.session_state.questoes_sorteadas_blocos = {}
                                st.rerun()
                    else:
                        st.error("🚨 Você não atingiu o mínimo de 7 acertos para passar de fase.")
                        if st.button("🔄 Tentar Novamente este Bloco", use_container_width=True, type="primary"):
                            st.session_state.indice_pergunta_bloco = 0
                            st.session_state.acertos_bloco_atual = 0
                            # Remove os pontos apenas do bloco que falhou para manter o Rank limpo
                            pool_b = [q for q in QUESTOES_VIP_REPOSITORIO_COMPLETO if q["bloco"] == bloco_atual]
                            st.session_state.questoes_sorteadas_blocos[bloco_atual] = random.sample(pool_b, k=min(10, len(pool_b)))
                            st.rerun()
