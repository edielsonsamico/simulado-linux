import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time
import os

# ==========================================
# 1. SISTEMA DE MONITORIZAÇÃO EM MEMÓRIA (MÉTRICAS)
# ==========================================
@st.cache_resource
def obter_armazenamento_global():
    return {
        "usuarios_online": {},     
        "registro_visitas": set(), 
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
# 2. FUNÇÕES AUXILIARES DE TRATAMENTO DE TEXTO
# ==========================================
def normalizar_texto(texto):
    return " ".join(texto.strip().lower().split())

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
# 3. BANCO DE DADOS INTEGRADO (TREINO GERAL)
# ==========================================
QUESTOES_POOL_RAW = [
    {"id": 1, "topico": "Tópico 101: Arquitetura", "pergunta": "Qual comando é utilizado para listar informações detalhadas do chipset e dos componentes no barramento PCI?", "opcoes": ["lspci", "lsusb", "lsmod", "dmesg"], "correta": "lspci", "explicacao": "O comando lspci varre o barramento PCI do hardware listando controladores, placas e chipsets integrados."},
    {"id": 2, "topico": "Tópico 102: Pacotes", "pergunta": "De acordo com a hierarquia do FHS, qual diretório é destinado a guardar exclusivamente os arquivos de configuração específicos da máquina local?", "opcoes": ["/etc", "/var", "/usr", "/opt"], "correta": "/etc", "explicacao": "O diretório /etc é o local padronizado pelo FHS para armazenar scripts e arquivos de configuração de texto do sistema."},
    {"id": 3, "topico": "Tópico 103: Comandos", "pergunta": "No histórico do interpretador de comandos Bash, qual atalho de token repete imediatamente a execução do último comando utilizado?", "opcoes": ["!!", "!$", "history -r", "ctrl+r"], "correta": "!!", "explicacao": "As duas exclamações '!!' chamam e executam novamente no prompt a linha exata de comando disparada anteriormente."},
    {"id": 4, "topico": "Tópico 104: Dispositivos", "pergunta": "Qual comando relata em tempo real o espaço livre/disponível e o uso em blocos para todos os sistemas de arquivos atualmente montados?", "opcoes": ["df", "du", "fdisk", "free"], "correta": "df", "explicacao": "O comando df (disk free) lê a tabela de montagens do sistema exibindo capacidades, espaço ocupado e pontos de montagem activos."}
]

QUESTOES_POOL = desduplicar_questoes(QUESTOES_POOL_RAW)


# ==========================================
# 4. REPOSITÓRIO EXCLUSIVO DO QUIZ VIP (PROTEGIDO)
# ==========================================
QUESTOES_VIP_REPOSITORIO = [
    {
        "id": 901,
        "pergunta": "Qual é a principal diferença entre os dispositivos do tipo 'Coldplug' e 'Hotplug'?",
        "opcoes": [
            "A. Dispositivos hotplug são identificados apenas no momento do POST da BIOS.",
            "B. Dispositivos hotplug só podem ser conectados via porta USB 3.0.",
            "C. Dispositivos coldplug exigem que o sistema seja desligado para conexão ou remoção.",
            "D. Coldplug é um termo usado exclusivamente para processadores e módulos de memória em servidores."
        ],
        "correta": "C. Dispositivos coldplug exigem que o sistema seja desligado para conexão ou remoção.",
        "dica": "Pense na temperatura operacional: 'Cold' (Frio/Desligado) e 'Hot' (Quente/Ligado em tempo de execução).",
        "explicacao": "Dispositivos Coldplug exigem que o hardware esteja completamente desligado para evitar danos elétricos ou falhas de barramento, enquanto os Hotplug podem ser acoplados dinamicamente."
    },
    {
        "id": 902,
        "pergunta": "De acordo com a hierarquia do sistema de arquivos (FHS), qual é a finalidade principal do diretório /var?",
        "opcoes": [
            "A. Servir como ponto de montagem padrão para mídias removíveis.",
            "B. Conter dados variáveis, como logs do sistema e arquivos de spool.",
            "C. Armazenar arquivos estáticos do gerenciador de boot.",
            "D. Abrigar comandos binários essenciais para todos os usuários."
        ],
        "correta": "B. Conter dados variáveis, como logs do sistema e arquivos de spool.",
        "dica": "O nome vem de 'variable'. Pense em ficheiros cujo tamanho de armazenamento muda constantemente enquanto os serviços rodam.",
        "explicacao": "O diretório /var armazena dados de tamanho altamente dinâmico e variável, como filas de e-mail, spools de impressão e os logs gerados em /var/log."
    }
]


# ==========================================
# 5. CONFIGURAÇÃO DA INTERFACE & ESTILO CSS
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
# 6. INICIALIZAÇÃO DO ESTADO DA SESSÃO
# ==========================================
if 'questoes_treino' not in st.session_state:
    st.session_state.questoes_treino = list(QUESTOES_POOL)
if "vip_liberado" not in st.session_state:
    st.session_state.vip_liberado = False
if "indice_vip" not in st.session_state:
    st.session_state.indice_vip = 0

# ==========================================
# 7. BARRA LATERAL (SIDEBAR)
# ==========================================
num_online, num_visitas = gerenciar_acesso_e_obter_metricas()

col_online, col_visitas = st.sidebar.columns(2)
col_online.metric(label="🟢 Online Agora", value=num_online)
col_visitas.metric(label="👥 Visitas Totais", value=num_visitas)

st.sidebar.divider()
st.sidebar.header("👤 Identificação")
nome_usuario = st.sidebar.text_input("Seu Nome para o Placar:", max_chars=20).strip()

st.sidebar.divider()
modo_selecionado = st.sidebar.radio(
    "Ambiente:", 
    [
        "📖 Área de Treino (Geral)", 
        "🎁 Materiais VIP & Simulados",
        "ℹ️ Créditos & Desenvolvimento"
    ]
)


# ==========================================
# 8. PROCESSAMENTO DAS ABAS
# ==========================================

# --- ABA: CRÉDITOS & DESENVOLVIMENTO ---
if modo_selecionado == "ℹ️ Créditos & Desenvolvimento":
    st.title("ℹ️ Créditos & Desenvolvimento")
    with st.container(border=True):
        st.subheader("Edielson Samico")
        st.write("Desenvolvedor de sistemas e engenheiro técnico na SAMICOIOT.")
        st.divider()
        col_wa, col_ig, col_yt = st.columns(3)
        col_wa.link_button("💬 WhatsApp", "https://wa.me/5581987316454", use_container_width=True)
        col_ig.link_button("📸 Instagram", "https://instagram.com/edielsonsamico", use_container_width=True)
        col_yt.link_button("🎥 YouTube", "https://youtube.com/@EdielsonSamico", use_container_width=True)

# --- ABA VIP: APOSTILAS & SIMULADOS (NATIVO E SEGURO) ---
elif modo_selecionado == "🎁 Materiais VIP & Simulados":
    st.title("🎁 Área VIP - Apostilas & Simulados Exclusivos")
    st.write("Acelere sua aprovação nas certificações resgatando materiais avançados de estudo.")

    if not st.session_state.vip_liberado:
        with st.container(border=True):
            st.markdown("<h3 style='text-align: center; color: #1E3A8A;'>🔒 Conteúdo Exclusivo Bloqueado</h3>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-size: 16px;'>Inscreva-se no nosso canal do YouTube para desbloquear o download da Apostila Completa e acessar o Simulado VIP.</p>", unsafe_allow_html=True)
            st.divider()
            col_inscrever, col_liberar = st.columns([2, 1])
            col_inscrever.link_button("❤️ 1º Passo: Inscrever-se no Canal", "https://youtube.com/@EdielsonSamico?sub_confirmation=1", use_container_width=True, type="primary")
            if col_liberar.button("🔓 2º Passo: Liberar Acesso", use_container_width=True):
                st.session_state.vip_liberado = True
                st.balloons()
                st.rerun()
    else:
        st.success("🎉 Parabéns! Seus conteúdos VIP estão totalmente desbloqueados.")
        col_apostila, col_simulado_vip = st.columns([1, 2])
        
        # CARD 1: DOWNLOAD DO PDF COM O NOVO NOMES DE ARQUIVO
        with col_apostila:
            with st.container(border=True):
                st.subheader("📚 Apostila de Certificação VIP")
                st.write("Material oficial completo com comandos Linux essenciais, mapas mentais de arquitetura e guias de redes.")
                
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
                    st.warning(f"⚠️ O arquivo '{caminho_apostila}' não foi encontrado na pasta. Rode o script de geração primeiro.")
                st.caption("Download local direto e seguro mantido pela SAMICOIOT.")
                
        # CARD 2: SIMULADO VIP COMPLETAMENTE INTERATIVO E PROTEGIDO
        with col_simulado_vip:
            with st.container(border=True):
                st.subheader("🏆 Linux Quiz VIP (Nativo)")
                st.write("Simulação interativa baseada nos seus tópicos avançados. Fontes originais 100% protegidas contra vazamento ou download.")
                st.divider()
                
                idx = st.session_state.indice_vip
                total_q = len(QUESTOES_VIP_REPOSITORIO)
                
                if idx < total_q:
                    q_atual = QUESTOES_VIP_REPOSITORIO[idx]
                    
                    # Progresso do Quiz (Ex: 1 / 30)
                    st.markdown(f"<p style='color: #64748B; font-weight: bold;'>{idx + 1} / {total_q}</p>", unsafe_allow_html=True)
                    st.markdown(f"#### **{q_atual['pergunta']}**")
                    
                    escolha = st.radio(
                        "Selecione uma alternativa:",
                        q_atual['opcoes'],
                        index=None,
                        key=f"vip_q_{idx}"
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
                                    st.toast("🎯 Resposta Correta!", icon="✅")
                                else:
                                    st.toast("❌ Incorreto!", icon="🚨")
                                st.session_state.indice_vip += 1
                                st.rerun()
                            else:
                                st.warning("Por favor, selecione uma alternativa antes de avançar.")
                else:
                    st.balloons()
                    st.success("🏆 Sensacional! Você concluiu todas as etapas do Quiz VIP com sucesso!")
                    if st.button("🔄 Reiniciar Simulado VIP", use_container_width=True):
                        st.session_state.indice_vip = 0
                        st.rerun()

# --- ABA: ÁREA DE TREINO GERAL ---
elif modo_selecionado == "📖 Área de Treino (Geral)":
    st.title("📖 Área de Treino Geral")
    for idx, q in enumerate(st.session_state.questoes_treino):
        st.markdown(f"### Questão {idx + 1}")
        st.markdown(f"**{q['pergunta']}**")
        resposta = st.radio("Selecione a opção:", q['opcoes'], index=None, key=f"t_{idx}")
        if resposta:
            if resposta == q['correta']:
                st.success("🎯 Resposta Correta!")
            else:
                st.error(f"❌ Incorreta. Correta: **{q['correta']}**")
        st.divider()
