import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time
import os
import glob
from streamlit.web.server.websocket_headers import _get_websocket_headers

# ==========================================
# -1. SISTEMA DE MONITORAMENTO EM TEMPO REAL (IMUNE A F5)
# ==========================================
PASTA_SESSIONS = ".active_sessions"
if not os.path.exists(PASTA_SESSIONS):
    try:
        os.makedirs(PASTA_SESSIONS)
    except Exception:
        pass

def obter_assinatura_usuario():
    """Gera uma chave única baseada no IP e Navegador do aluno para evitar duplicados no F5."""
    try:
        headers = _get_websocket_headers()
        # Captura o IP real do usuário através do proxy do Streamlit Cloud
        ip = headers.get("X-Forwarded-For", "127.0.0.1").split(",")[0].strip()
        # Captura a assinatura do navegador (User-Agent)
        user_agent = headers.get("User-Agent", "unknown_browser")
        # Cria um identificador único e limpo para este computador/dispositivo
        uid = f"{ip}_{hash(user_agent)}"
        return uid
    except Exception:
        # Fallback caso ocorra erro ao ler os cabeçalhos em ambiente de desenvolvimento local
        if "fallback_uid" not in st.session_state:
            st.session_state.fallback_uid = f"local_{random.randint(100000, 999900)}"
        return st.session_state.fallback_uid

# Identificador único do dispositivo deste aluno (não muda com F5)
usuario_uid = obter_assinatura_usuario()
caminho_sessao = os.path.join(PASTA_SESSIONS, f"sess_{usuario_uid}")

# Atualiza o timestamp de atividade deste usuário específico
try:
    with open(caminho_sessao, "w") as f:
        f.write(str(time.time()))
except Exception:
    pass

def obter_metricas_acesso():
    """Calcula visitantes únicos e usuários ativos de forma extremamente precisa."""
    arquivo_visitas = ".visitas_totais"
    arquivo_log_usuarios = ".registro_usuarios_unicos" # Guarda os UIDs que já visitaram
    
    # 1. Recupera as visitas salvas
    visitas = 0
    if os.path.exists(arquivo_visitas):
        try:
            with open(arquivo_visitas, "r") as f:
                conteudo = f.read().strip()
                visitas = int(conteudo) if conteudo.isdigit() else 0
        except Exception:
            pass
            
    # Recupera a lista de dispositivos (UIDs) que já foram computados historicamente
    usuarios_registrados = set()
    if os.path.exists(arquivo_log_usuarios):
        try:
            with open(arquivo_log_usuarios, "r") as f:
                usuarios_registrados = set(f.read().splitlines())
        except Exception:
            pass

    # Se o dispositivo atual nunca visitou a página antes, registra como visita nova
    if usuario_uid not in usuarios_registrados:
        usuarios_registrados.add(usuario_uid)
        visitas += 1
        try:
            with open(arquivo_visitas, "w") as f:
                f.write(str(visitas))
            with open(arquivo_log_usuarios, "a") as f:
                f.write(usuario_uid + "\n")
        except Exception:
            pass

    # 2. Usuários Online Agora (Sessões ativas que interagiram nos últimos 60 segundos)
    agora = time.time()
    limite_inatividade = 60  # Reduzido para 60 segundos para maior precisão de "Tempo Real"
    online = 0
    
    if os.path.exists(PASTA_SESSIONS):
        arquivos = glob.glob(os.path.join(PASTA_SESSIONS, "sess_*"))
        for arq in arquivos:
            try:
                mtime = os.path.getmtime(arq)
                if agora - mtime < limite_inatividade:
                    online += 1
                else:
                    # Limpa registros inativos antigos
                    os.remove(arq)
            except Exception:
                pass
    
    # Garante que o próprio usuário atual sempre conte como pelo menos 1 online
    online = max(1, online)
    return online, visitas
