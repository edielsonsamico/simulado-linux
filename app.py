import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time
import os
import glob

# ==========================================
# -1. SISTEMA DE MONITORIZAÇÃO SEGURO (SEM CONFLITO DE URL)
# ==========================================
PASTA_SESSIONS = ".active_sessions"
if not os.path.exists(PASTA_SESSIONS):
    try:
        os.makedirs(PASTA_SESSIONS)
    except Exception:
        pass

def obter_id_unico():
    """Gera um ID estável na sessão para evitar loops e travamentos de tela."""
    if "usuario_uid" not in st.session_state:
        # Gera uma identificação única baseada no momento do acesso
        st.session_state.usuario_uid = f"user_{int(time.time())}_{random.randint(1000, 9999)}"
    return st.session_state.usuario_uid

# Recupera o identificador seguro
usuario_uid = obter_id_unico()
caminho_sessao = os.path.join(PASTA_SESSIONS, f"sess_{usuario_uid}")

# Atualiza apenas o timestamp de atividade (não causa Rerun)
try:
    with open(caminho_sessao, "w") as f:
        f.write(str(time.time()))
except Exception:
    pass

def obter_metricas_acesso():
    """Calcula visitantes únicos e usuários online sem causar loops na interface."""
    arquivo_visitas = ".visitas_totais"
    arquivo_log_usuarios = ".registro_usuarios_unicos"
    
    # 1. Recupera o histórico de visitas totais
    visitas = 0
    if os.path.exists(arquivo_visitas):
        try:
            with open(arquivo_visitas, "r") as f:
                conteudo = f.read().strip()
                visitas = int(conteudo) if conteudo.isdigit() else 0
        except Exception:
            pass
            
    # Recupera a lista de UIDs que já visitaram historicamente
    usuarios_registrados = set()
    if os.path.exists(arquivo_log_usuarios):
        try:
            with open(arquivo_log_usuarios, "r") as f:
                usuarios_registrados = set(f.read().splitlines())
        except Exception:
            pass

    # Só conta uma nova visita se for um ID de sessão inédito no servidor
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

    # 2. Usuários Online Agora (Baseado em atividade nos últimos 90 segundos)
    agora = time.time()
    limite_inatividade = 90  
    online = 0
    
    if os.path.exists(PASTA_SESSIONS):
        arquivos = glob.glob(os.path.join(PASTA_SESSIONS, "sess_*"))
        for arq in arquivos:
            try:
                mtime = os.path.getmtime(arq)
                if agora - mtime < limite_inatividade:
                    online += 1
                else:
                    # Remove arquivos órfãos de sessões abandonadas
                    os.remove(arq)
            except Exception:
                pass
    
    # Garante que o próprio usuário atual é contado
    online = max(1, online)
    return online, visitas
