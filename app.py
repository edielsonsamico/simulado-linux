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
        st.sidebar.error(f"❌ Erro no e
