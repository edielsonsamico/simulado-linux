import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time
import os
import glob

# ==========================================
# -1. SISTEMA DE MONITORIZAÇÃO EM TEMPO REAL (TOTALMENTE IMUNE A F5)
# ==========================================
PASTA_SESSIONS = ".active_sessions"
if not os.path.exists(PASTA_SESSIONS):
    try:
        os.makedirs(PASTA_SESSIONS)
    except Exception:
        pass

def obter_ou_criar_uid_usuario():
    """
    Recupera o UID do utilizador através dos Query Params da URL.
    Se não existir, gera um novo, grava na URL e atualiza a aplicação.
    """
    # 1. Tenta ler o UID diretamente da URL (sobrevive ao F5)
    if "uid" in st.query_params:
        return st.query_params["uid"]
    
    # 2. Caso não exista na URL, verifica se já está na sessão ativa (temporário)
    if "usuario_uid" in st.session_state:
        # Garante que o UID também vai para a URL para as próximas atualizações
        st.query_params["uid"] = st.session_state.usuario_uid
        return st.session_state.usuario_uid

    # 3. Se for um visitante totalmente novo sem UID na URL nem na Sessão:
    novo_uid = f"user_{random.randint(100000, 999999)}_{int(time.time())}"
    st.session_state.usuario_uid = novo_uid
    st.query_params["uid"] = novo_uid
    
    # Rerun imediato para garantir que o Streamlit regista o parâmetro na barra de navegação
    st.rerun()

# Identificador único definitivo do utilizador (gravado na URL do navegador)
usuario_uid = obter_ou_criar_uid_usuario()
caminho_sessao = os.path.join(PASTA_SESSIONS, f"sess_{usuario_uid}")

# Atualiza o timestamp de atividade deste utilizador específico
try:
    with open(caminho_sessao, "w") as f:
        f.write(str(time.time()))
except Exception:
    pass

def obter_metricas_acesso():
    """Calcula visitantes únicos e utilizadores online com precisão absoluta."""
    arquivo_visitas = ".visitas_totais"
    arquivo_log_usuarios = ".registro_usuarios_unicos" # Guarda os UIDs históricos
    
    # 1. Recupera o total de visitas salvas
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

    # Se este UID na URL nunca foi registado antes, conta como uma visita nova
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

    # 2. Utilizadores Online Agora (Sessões que interagiram nos últimos 45 segundos)
    agora = time.time()
    limite_inatividade = 45  # Tempo de tolerância curto e dinâmico
    online = 0
    
    if os.path.exists(PASTA_SESSIONS):
        arquivos = glob.glob(os.path.join(PASTA_SESSIONS, "sess_*"))
        for arq in arquivos:
            try:
                # Verifica a última modificação do ficheiro
                mtime = os.path.getmtime(arq)
                if agora - mtime < limite_inatividade:
                    online += 1
                else:
                    # Limpa automaticamente sessões antigas/abandonadas
                    os.remove(arq)
            except Exception:
                pass
    
    # Garante que pelo menos o utilizador atual é contabilizado
    online = max(1, online)
    return online, visitas
