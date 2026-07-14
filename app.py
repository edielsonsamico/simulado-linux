import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time
import os

# ==========================================
# -1. SISTEMA DE MONITORIZAÇÃO EM MEMÓRIA (IMUNE A LOOPS E F5)
# ==========================================

# Usamos st.cache_resource para manter um dicionário global na memória do servidor.
# Este dicionário persiste entre todos os utilizadores e sobrevive a F5s individuais!
@st.cache_resource
def obter_armazenamento_global():
    return {
        "usuarios_online": {},  # Estrutura: {usuario_uid: timestamp_atividade}
        "registro_visitas": set(), # Guarda os UIDs que já visitaram historicamente
        "visitas_totais": 0
    }

# Inicializa o armazenamento na memória
memoria_global = obter_armazenamento_global()

def gerenciar_acesso_e_obter_metricas():
    # 1. Identifica o utilizador atual na sessão
    if "usuario_uid" not in st.session_state:
        # Gera uma chave única que dura enquanto a aba do navegador estiver aberta
        st.session_state.usuario_uid = f"user_{int(time.time())}_{random.randint(1000, 9999)}"
    
    uid_atual = st.session_state.usuario_uid
    agora = time.time()
    
    # 2. Atualiza o timestamp de atividade deste utilizador na memória global
    memoria_global["usuarios_online"][uid_atual] = agora
    
    # 3. Regista nova visita se for um UID inédito
    if uid_atual not in memoria_global["registro_visitas"]:
        memoria_global["registro_visitas"].add(uid_atual)
        memoria_global["visitas_totais"] += 1
        
    # 4. Limpa utilizadores inativos da memória (offline há mais de 45 segundos)
    limite_inatividade = 45
    uids_para_remover = []
    
    for uid, ultimo_acesso in memoria_global["usuarios_online"].items():
        if agora - ultimo_acesso > limite_inatividade:
            uids_para_remover.append(uid)
            
    for uid in uids_para_remover:
        memoria_global["usuarios_online"].pop(uid, None)
        
    # Retorna o total de online (mínimo 1) e o total de visitas únicas acumuladas
    total_online = max(1, len(memoria_global["usuarios_online"]))
    total_visitas = memoria_global["visitas_totais"]
    
    return total_online, total_visitas
