import streamlit as st
import random
import re

# ==========================================
# 1. FUNÇÕES DE LIMPEZA E LÓGICA (CORE)
# ==========================================
def normalizar_texto(texto):
    texto_limpo = re.sub(r'^(quest[ãa]o(\s+avançada)?(\s+de\s+[a-z\s]+)?\s*\d+|q\d+|\d+)[:\.\-\s]+', '', texto.strip().lower())
    return " ".join(texto_limpo.split())

def desduplicar_questoes(lista_original):
    vistas = set()
    lista_limpa = []
    for q in lista_original:
        p = normalizar_texto(q["pergunta"])
        if p not in vistas:
            vistas.add(p)
            lista_limpa.append(q)
    return lista_limpa

# ==========================================
# 2. BANCO DE DADOS (40 QUESTÕES ÚNICAS)
# ==========================================
QUESTOES_BASE = [
    {"id": 1, "topico": "Comandos", "pergunta": "Qual comando PCI lista chipsets?", "opcoes": ["lspci", "lsusb", "lsmod", "dmesg"], "correta": "lspci"},
    {"id": 2, "topico": "Diretórios", "pergunta": "Qual diretório FHS armazena configs?", "opcoes": ["/etc", "/var", "/usr", "/opt"], "correta": "/etc"},
    {"id": 3, "topico": "Comandos", "pergunta": "Qual comando repete o último comando?", "opcoes": ["!!", "!$", "history", "ctrl+r"], "correta": "!!"},
    {"id": 4, "topico": "Sistema", "pergunta": "Qual comando vê espaço em disco?", "opcoes": ["df", "du", "fdisk", "free"], "correta": "df"},
    {"id": 5, "topico": "Scripts", "pergunta": "Qual comando lê entrada do usuário?", "opcoes": ["read", "input", "get", "scan"], "correta": "read"},
    {"id": 6, "topico": "X11", "pergunta": "Onde fica o xorg.conf?", "opcoes": ["/etc/X11/", "/etc/xorg/", "/var/X11/", "/opt/X11/"], "correta": "/etc/X11/"},
    {"id": 7, "topico": "Segurança", "pergunta": "Onde ficam as senhas (hash)?", "opcoes": ["/etc/shadow", "/etc/passwd", "/etc/group", "/var/log"], "correta": "/etc/shadow"},
    {"id": 8, "topico": "Redes", "pergunta": "Qual porta do NTP?", "opcoes": ["UDP 123", "TCP 123", "UDP 53", "TCP 80"], "correta": "UDP 123"},
    {"id": 9, "topico": "Redes", "pergunta": "Arquivo de hosts locais?", "opcoes": ["/etc/hosts", "/etc/resolv", "/etc/net", "/etc/host"], "correta": "/etc/hosts"},
    {"id": 10, "topico": "Segurança", "pergunta": "Permissão SUID em octal?", "opcoes": ["4000", "2000", "1000", "755"], "correta": "4000"},
    {"id": 11, "topico": "Processos", "pergunta": "Qual sinal encerra processo (kill)?", "opcoes": ["SIGTERM", "SIGHUP", "SIGINT", "SIGKILL"], "correta": "SIGTERM"},
    {"id": 12, "topico": "Arquivos", "pergunta": "Qual comando altera dono?", "opcoes": ["chown", "chmod", "chgrp", "chuser"], "correta": "chown"},
    {"id": 13, "topico": "Arquivos", "pergunta": "Qual comando altera permissão?", "opcoes": ["chmod", "chown", "chgrp", "chattr"], "correta": "chmod"},
    {"id": 14, "topico": "Boot", "pergunta": "Qual o primeiro processo?", "opcoes": ["init/systemd", "kernel", "bash", "grub"], "correta": "init/systemd"},
    {"id": 15, "topico": "Kernel", "pergunta": "Onde ficam módulos?", "opcoes": ["/lib/modules", "/etc/modules", "/boot/modules", "/var/lib"], "correta": "/lib/modules"},
    {"id": 16, "topico": "Comandos", "pergunta": "Qual comando mostra memória?", "opcoes": ["free", "top", "vmstat", "df"], "correta": "free"},
    {"id": 17, "topico": "Logs", "pergunta": "Onde ficam logs?", "opcoes": ["/var/log", "/etc/log", "/tmp/log", "/usr/log"], "correta": "/var/log"},
    {"id": 18, "topico": "Arquivos", "pergunta": "Qual link aponta para outro?", "opcoes": ["Simbólico", "Hard", "Soft", "Root"], "correta": "Simbólico"},
    {"id": 19, "topico": "User", "pergunta": "Qual arquivo lista grupos?", "opcoes": ["/etc/group", "/etc/passwd", "/etc/shadow", "/etc/gshadow"], "correta": "/etc/group"},
    {"id": 20, "topico": "Shell", "pergunta": "Qual variável lista PATH?", "opcoes": ["$PATH", "$HOME", "$USER", "$PWD"], "correta": "$PATH"},
    {"id": 21, "topico": "Redes", "pergunta": "Comando para pingar?", "opcoes": ["ping", "netstat", "ip", "ifconfig"], "correta": "ping"},
    {"id": 22, "topico": "Sistema", "pergunta": "Quem gerencia pacotes .deb?", "opcoes": ["dpkg", "rpm", "yum", "pacman"], "correta": "dpkg"},
    {"id": 23, "topico": "Sistema", "pergunta": "Quem gerencia pacotes .rpm?", "opcoes": ["rpm", "dpkg", "apt", "dnf"], "correta": "rpm"},
    {"id": 24, "topico": "Processos", "pergunta": "Qual comando lista processos?", "opcoes": ["ps", "top", "htop", "kill"], "correta": "ps"},
    {"id": 25, "topico": "Arquivos", "pergunta": "O que faz 'touch'?", "opcoes": ["Cria arquivo", "Deleta", "Edita", "Move"], "correta": "Cria arquivo"},
    {"id": 26, "topico": "Comandos", "pergunta": "Como ver conteúdo arquivo?", "opcoes": ["cat", "ls", "cd", "pwd"], "correta": "cat"},
    {"id": 27, "topico": "Redes", "pergunta": "Qual DNS é usado?", "opcoes": ["/etc/resolv.conf", "/etc/dns", "/etc/hosts", "/etc/network"], "correta": "/etc/resolv.conf"},
    {"id": 28, "topico": "Sistema", "pergunta": "O que é GRUB?", "opcoes": ["Bootloader", "Kernel", "Shell", "Editor"], "correta": "Bootloader"},
    {"id": 29, "topico": "Comandos", "pergunta": "Comando para copiar?", "opcoes": ["cp", "mv", "rm", "ln"], "correta": "cp"},
    {"id": 30, "topico": "Comandos", "pergunta": "Comando para mover?", "opcoes": ["mv", "cp", "rm", "ln"], "correta": "mv"},
    {"id": 31, "topico": "Arquivos", "pergunta": "Comando para diretórios?", "opcoes": ["mkdir", "touch", "ls", "cd"], "correta": "mkdir"},
    {"id": 32, "topico": "Sistema", "pergunta": "Como sair do vi?", "opcoes": [":q!", ":exit", ":save", ":close"], "correta": ":q!"},
    {"id": 33, "topico": "Permissões", "pergunta": "O que significa 'r'?", "opcoes": ["Read", "Write", "Execute", "Root"], "correta": "Read"},
    {"id": 34, "topico": "Permissões", "pergunta": "O que significa 'w'?", "opcoes": ["Write", "Read", "Execute", "Wait"], "correta": "Write"},
    {"id": 35, "topico": "Permissões", "pergunta": "O que significa 'x'?", "opcoes": ["Execute", "Write", "Read", "Xerox"], "correta": "Execute"},
    {"id": 36, "topico": "Sistema", "pergunta": "Comando ver usuários?", "opcoes": ["who", "ls", "ps", "top"], "correta": "who"},
    {"id": 37, "topico": "Sistema", "pergunta": "Onde ficam binários?", "opcoes": ["/bin", "/etc", "/home", "/proc"], "correta": "/bin"},
    {"id": 38, "topico": "Comandos", "pergunta": "Comando manual?", "opcoes": ["man", "help", "info", "whatis"], "correta": "man"},
    {"id": 39, "topico": "Arquivos", "pergunta": "Comando find busca o que?", "opcoes": ["Arquivos", "Texto", "Processos", "Rede"], "correta": "Arquivos"},
    {"id": 40, "topico": "Shell", "pergunta": "O que faz 'grep'?", "opcoes": ["Busca texto", "Copia", "Move", "Deleta"], "correta": "Busca texto"}
]

QUESTOES_POOL = desduplicar_questoes(QUESTOES_BASE)

# ==========================================
# 3. APP PRINCIPAL
# ==========================================
def main():
    st.set_page_config(page_title="Ambiente SAMICOIOT", layout="wide")

    if 'iniciado' not in st.session_state:
        st.session_state.questoes = QUESTOES_POOL
        st.session_state.simulado_ativo = random.sample(QUESTOES_POOL, k=min(40, len(QUESTOES_POOL)))
        st.session_state.iniciado = True

    st.sidebar.title("Ambiente SAMICOIOT")
    modo = st.sidebar.radio("Navegação:", [
        "📖 Área de Treino (Geral)", 
        "🎯 Treino por Tópico (Focado)", 
        "⏱️ Simulado LPI (Prova Real 40 Q)",
        "🎁 Materiais VIP & Simulados",
        "ℹ️ Créditos & Desenvolvimento"
    ])

    # RENDERIZAÇÃO
    if modo == "📖 Área de Treino (Geral)":
        st.title("📖 Área de Treino Geral")
        for idx, q in enumerate(st.session_state.questoes):
            opcoes = q['opcoes'].copy()
            random.shuffle(opcoes)
            st.markdown(f"**{q['pergunta']}**")
            res = st.radio(f"treino_{q['id']}", opcoes, index=None, label_visibility="collapsed")
            if res == q['correta']: st.success("🎯 Correto!")
            elif res: st.error(f"❌ Errado. Certo: {q['correta']}")
            st.divider()

    elif modo == "🎯 Treino por Tópico (Focado)":
        st.title("🎯 Treino por Tópico (Focado)")
        topicos = sorted(list(set(q['topico'] for q in QUESTOES_POOL)))
        t = st.selectbox("Escolha o tópico:", topicos, key="select_topic_main")
        for idx, q in enumerate([q for q in QUESTOES_POOL if q['topico'] == t]):
            opcoes = q['opcoes'].copy()
            random.shuffle(opcoes)
            st.markdown(f"**{q['pergunta']}**")
            res = st.radio(f"radio_{q['id']}_{t}", opcoes, index=None, label_visibility="collapsed")
            if res == q['correta']: st.success("🎯 Correto!")
            elif res: st.error(f"❌ Errado. Certo: {q['correta']}")
            st.divider()

    elif modo == "⏱️ Simulado LPI (Prova Real 40 Q)":
        st.title("⏱️ Simulado LPI (Prova Real 40 Q)")
        if st.button("Gerar novo simulado (Inédito)"):
            st.session_state.simulado_ativo = random.sample(QUESTOES_POOL, k=min(40, len(QUESTOES_POOL)))
            st.rerun()
        for idx, q in enumerate(st.session_state.get('simulado_ativo', QUESTOES_POOL)):
            opcoes = q['opcoes'].copy()
            random.shuffle(opcoes)
            st.markdown(f"**{idx+1}. {q['pergunta']}**")
            st.radio(f"sim_{q['id']}", opcoes, index=None, label_visibility="collapsed")
            st.divider()

    elif modo == "🎁 Materiais VIP & Simulados":
        st.title("🎁 Materiais VIP & Simulados")
        st.info("Conteúdo exclusivo disponível para membros.")

    elif modo == "ℹ️ Créditos & Desenvolvimento":
        st.title("ℹ️ Créditos & Desenvolvimento")
        st.write("Desenvolvido por Edielson Samico - SAMICOIOT.")

if __name__ == "__main__":
    main()
