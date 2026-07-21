import streamlit as st
import random
import re
import importlib
import hashlib
import string
import time
from datetime import datetime

def aplicar_estilo_acessivel(nivel_zoom, modo_escuro):
    escala = {
        "Padrão (100%)": "16px",
        "Ampliado (115%)": "19px",
        "Grande (130%)": "22px"
    }
    tamanho_fonte = escala.get(nivel_zoom, "16px")
    
    if modo_escuro:
        st.markdown(f"""
            <style>
            .stApp {{ background-color: #0b0f19; color: #f3f4f6; overflow-x: hidden !important; }}
            section[data-testid="stSidebar"] {{ background-color: #111827; color: #f3f4f6; }}
            .stMarkdown, p, span, label, .stRadio div, .stCheckbox label {{ font-size: {tamanho_fonte} !important; color: #f3f4f6 !important; }}
            h1, h2, h3 {{ color: #60a5fa !important; }}
            input, .stTextInput input {{ background-color: #1f2937 !important; color: #ffffff !important; border: 1px solid #374151 !important; }}
            .stButton button {{ background-color: #1f2937 !important; color: #ffffff !important; border: 1px solid #4b5563 !important; }}
            .stButton button:hover {{ background-color: #374151 !important; border-color: #60a5fa !important; color: #60a5fa !important; }}
            code, pre, .stCodeBlock {{ background-color: #1f2937 !important; color: #60a5fa !important; border: 1px solid #374151 !important; }}
            .custom-link-btn {{
                display: block;
                width: 100%;
                background-color: #1d4ed8;
                color: #ffffff !important;
                text-align: center;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                text-decoration: none;
                border: 1px solid #3b82f6;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            }}
            .custom-link-btn:hover {{
                background-color: #2563eb;
                color: #ffffff !important;
                border-color: #60a5fa;
            }}
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <style>
            .stApp {{ background-color: #ffffff; color: #111827; overflow-x: hidden !important; }}
            section[data-testid="stSidebar"] {{ background-color: #f8fafc; color: #111827; }}
            .stMarkdown, p, span, label, .stRadio div, .stCheckbox label {{ font-size: {tamanho_fonte} !important; color: #1f2937 !important; }}
            h1 {{ color: #1d4ed8 !important; font-size: 1.8rem !important; }}
            h2 {{ color: #1d4ed8 !important; font-size: 1.4rem !important; }}
            h3 {{ color: #1d4ed8 !important; font-size: 1.2rem !important; }}
            .custom-link-btn {{
                display: block;
                width: 100%;
                background-color: #1d4ed8;
                color: #ffffff !important;
                text-align: center;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                text-decoration: none;
                border: 1px solid #2563eb;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .custom-link-btn:hover {{
                background-color: #2563eb;
                color: #ffffff !important;
            }}
            </style>
        """, unsafe_allow_html=True)

def gerar_hash_conteudo(pergunta):
    texto_limpo = re.sub(r'^(quest[ãa]o.*?\d+|q\d+|\d+)\s*[\.\:\-]?\s*', '', pergunta.strip(), flags=re.IGNORECASE)
    texto_limpo = " ".join(texto_limpo.lower().split())
    return hashlib.md5(texto_limpo.encode('utf-8')).hexdigest()

def inferir_resposta_correta(pergunta, opcoes):
    p = pergunta.lower()
    termos_chave = {
        "swap": "swap",
        "exclusivamente os arquivos de comandos executáveis do usuário": "/usr",
        "gerenciador de boot alternativo ao antigo lilo": "syslinux",
        "chipset e dos componentes no barramento pci": "lspci",
        "sysvinit": "/var/log/messages",
        "módulos de drivers estão atualmente carregados": "lsmod",
        "geometria e dados técnicos sobre uma janela gráfica": "xwininfo",
        "representação octal tradicional de permissões": "leitura é 4",
        "lsof utilizando especificamente a flag -i": "processos atrelados a conexões de rede e portas abertas",
        "protocolo de sincronização temporal ntp": "porta udp 123",
        "hotplug": "permitir conexão e desconexão de dispositivos com a máquina ligada",
        "desligar ou reiniciar a máquina de forma segura, permitindo alertar": "shutdown",
        "variável especial de shell identificada pelo token": "código de retorno",
        "opção do comando ls deve ser usada": "-l",
        "abriga de forma criptografada as senhas": "/etc/shadow",
        "centralizar, processar e despachar mensagens": "syslogd",
        "cotas virtuais": "quota",
        "pausa a execução": "read",
        "configura o nome da máquina local": "/etc/hostname",
        "display=192.168": "direcionar a saída gráfica",
        "suid": "-perm",
        "conectividad": "ping",
        "cron.allow": "todos",
        "linha inteira": "dd",
        "pacotes atualmente instalados": "rpm -qa",
        "máxima criticidade": "emerg",
        "syslog": "emerg",
        "árvore genealógica": "pstree",
        "bibliotecas compartilhadas": "/etc/ld.so.conf",
        "redirecionamento envia a saída padrão": ">>",
        "protocolo de sincronização temporal": "123",
        "ordenada de forma alfabética": "order by",
        "inserção de novos dados": "insert into",
        "cláusula é usada para especificar uma condição": "where",
        "proprietário usuário e o grupo": "chown",
        "primeiro processo": "init",
        "diretório padrão o sistema copia": "/etc/skel",
        "compactação": "gzip",
        "reiniciar a máquina": "reboot",
        "variável já carregada": "unset",
        "servidor x11": "/etc/x11/xorg.conf",
        "i18n": "iconv",
        "arquivo regular existe": "-f",
        "detalhes como modelo de fábrica": "/proc/cpuinfo",
        "variáveis de ambiente que foram exportadas": "export",
        "localiza caminhos": "locate",
        "intervalo regulamentado": "-20 a +19"
    }
    for chave, termo in termos_chave.items():
        if chave in p:
            for op in opcoes:
                if termo in op.lower():
                    return op
    return opcoes[0] if opcoes else "Não informada"

def obter_comentario(pergunta, resposta_certa):
    p = pergunta.lower()
    if "swap" in p:
        return "💡 **Comentário Técnico:** A partição/espaço de swap é utilizada pelo kernel como memória virtual quando a RAM física atinge o limite."
    elif "fhs" in p or "usr" in p:
        return "💡 **Comentário Técnico:** Segundo o FHS (Filesystem Hierarchy Standard), o diretório `/usr` armazena dados secundários, utilitários e aplicativos executáveis."
    elif "lilo" in p or "syslinux" in p:
        return "💡 **Comentário Técnico:** O Syslinux é uma família de carregadores de boot leves frequentemente usados para mídias removíveis e sistemas alternativos."
    elif "pci" in p:
        return "💡 **Comentário Técnico:** O comando `lspci` lista detalhadamente todos os dispositivos PCI e o chipset conectado na placa-mãe."
    elif "sysvinit" in p or "messages" in p:
        return "💡 **Comentário Técnico:** O arquivo `/var/log/messages` centraliza logs gerais do sistema e de eventos do syslog no padrão tradicional."
    elif "módulos" in p or "lsmod" in p:
        return "💡 **Comentário Técnico:** O comando `lsmod` lê o arquivo `/proc/modules` para exibir os módulos de driver atualmente carregados na memória."
    else:
        return f"💡 **Comentário Técnico:** A alternativa correta é **'{resposta_certa}'**, pois atende diretamente aos requisitos técnicos descritos no enunciado da questão."

def carregar_banco_essentials():
    pool_total = []
    for i in range(101, 111):
        try:
            modulo = importlib.import_module(f"topico{i}")
            if hasattr(modulo, f"POOL_{i}"):
                pool_total.extend(getattr(modulo, f"POOL_{i}"))
        except: continue
    
    banco_final = {}
    for q in pool_total:
        h = gerar_hash_conteudo(q["pergunta"])
        if h not in banco_final:
            q_copia = q.copy()
            opcoes_originais = q.get('opcoes', [])
            q_copia['opcoes_fixas'] = opcoes_originais.copy()
            random.shuffle(q_copia['opcoes_fixas'])
            
            resp_oficial = None
            if 'correta' in q and q['correta'] is not None:
                val = q['correta']
                try:
                    idx = int(val)
                    if 0 <= idx < len(opcoes_originais):
                        resp_oficial = str(opcoes_originais[idx]).strip()
                except ValueError:
                    resp_oficial = str(val).strip()
            
            if not resp_oficial or resp_oficial == "":
                resp_oficial = inferir_resposta_correta(q['pergunta'], q_copia['opcoes_fixas'])
                
            q_copia['resposta_oficial'] = resp_oficial
            banco_final[h] = q_copia
            
    return list(banco_final.values())

def carregar_banco_lpic1():
    questoes_lpic1 = []
    topicos_avancados = [
        ("Gerenciamento de Boot GRUB2", "Qual arquivo de configuração principal do GRUB2 é gerado automaticamente e não deve ser editado manualmente?", ["/boot/grub2/grub.cfg", "/etc/default/grub", "/etc/grub.d/40_custom", "/boot/grub/menu.lst"], "/boot/grub2/grub.cfg"),
        ("LVM Logical Volume Manager", "Qual comando é utilizado para expandir um volume lógico (Logical Volume) e o seu sistema de arquivos ext4 simultaneamente em uma única operação?", ["lvextend -r", "lvresize -f", "vgextend", "resize2fs"], "lvextend -r"),
        ("Gerenciamento de Processos", "Qual comando exibe os processos em execução em formato de árvore hierárquica?", ["pstree", "top", "ps aux", "htop"], "pstree"),
        ("Compilação de Kernel", "Qual diretório contém tradicionalmente o código-fonte padrão ou os arquivos de cabeçalho do kernel Linux no sistema?", ["/usr/src/linux", "/lib/modules", "/proc/sys", "/etc/kernel"], "/usr/src/linux"),
        ("Redes e Roteamento", "Qual comando exibe a tabela de roteamento IP do kernel no Linux?", ["ip route show", "netstat -r", "route -n", "Todas as alternativas estão corretas"], "Todas as alternativas estão corretas"),
        ("Gerenciamento de Pacotes APT", "Qual comando do APT remove um pacote do sistema juntamente com seus arquivos de configuração globais?", ["apt purge", "apt remove", "apt clean", "apt autoremove"], "apt purge"),
        ("Controle de Acesso ACL", "Qual comando é utilizado para definir permissões avançadas de ACL (Access Control List) em um arquivo?", ["setfacl", "getfacl", "chmod +acl", "chacl"], "setfacl"),
        ("Agendamento Cron", "Em qual diretório do sistema são colocados os scripts que devem ser executados de forma diária pelo sistema de cron (anacron)?", ["/etc/cron.daily", "/var/spool/cron", "/etc/crontab", "/usr/bin/cron"], "/etc/cron.daily"),
        ("Logs do Sistema Journald", "Qual utilitário do systemd é utilizado para consultar e visualizar os logs binários gerados pelo journald?", ["journalctl", "syslog-ng", "tail -f /var/log/messages", "logger"], "journalctl"),
        ("Limites de Recursos Ulimit", "Qual comando exibe os limites de recursos atuais definidos para o shell e os processos do usuário?", ["ulimit -a", "quotacheck", "limit", "sysctl -a"], "ulimit -a")
    ]
    for i in range(1, 41):
        base = topicos_avancados[(i - 1) % len(topicos_avancados)]
        q_texto = f"Questão LPIC-1 #{i}: {base[1]} (Tópico: {base[0]})"
        ops = base[2].copy()
        random.shuffle(ops)
        questoes_lpic1.append({
            "id": f"lpic1_{i}",
            "topico": base[0],
            "pergunta": q_texto,
            "opcoes": base[2],
            "opcoes_fixas": ops,
            "resposta_oficial": base[3]
        })
    return questoes_lpic1

def carregar_banco_lpic2():
    questoes_lpic2 = []
    topicos_lpic2 = [
        ("DNS BIND Avançado", "Qual arquivo de zona do DNS contém os registros de mapeamento reverso de endereços IP para nomes de domínio (PTR)?", ["db.127.0.0", "named.conf", "resolv.conf", "hosts.allow"], "db.127.0.0"),
        ("Servidor Web Apache/Nginx", "Qual diretiva do Apache httpd é utilizada para configurar hosts virtuais baseados em nome (Name-based Virtual Hosts)?", ["<VirtualHost>", "<ServerName>", "<Directory>", "<HostConfig>"], "<VirtualHost>"),
        ("Armazenamento iSCSI e NFS", "Qual daemon no servidor Linux gerencia as exportações de arquivos compartilhados via protocolo NFS?", ["nfs-kernel-server (nfsd)", "smbd", "vsftpd", "bind9"], "nfs-kernel-server (nfsd)"),
        ("Segurança e Firewall iptables/nftables", "Qual tabela do iptables é responsável por realizar operações de NAT (Network Address Translation)?", ["nat", "filter", "mangle", "raw"], "nat"),
        ("Servidor LDAP OpenLDAP", "Qual utilitário de linha de comando é utilizado no OpenLDAP para consultar e pesquisar entradas no diretório de forma estruturada?", ["ldapsearch", "ldapadd", "slapd", "getent"], "ldapsearch"),
        ("Servidor de E-mail Postfix/Dovecot", "Qual porta padrão é utilizada pelo protocolo IMAPS (IMAP seguro sobre TLS/SSL)?", ["993", "143", "25", "465"], "993"),
        ("Autenticação PAM e Kerberos", "Qual arquivo principal gerencia a configuração dos módulos de autenticação plugáveis (PAM) para os serviços do sistema?", ["/etc/pam.conf", "/etc/security/limits.conf", "/etc/passwd", "/etc/login.defs"], "/etc/pam.conf"),
        ("Monitoramento de Rede SNMP", "Qual comando do pacote net-snmp é utilizado para consultar variáveis e dados de agentes SNMP remotos?", ["snmpwalk", "snmpd", "tcpdump", "nmap"], "snmpwalk"),
        ("Roteamento Avançado e Tunelamento", "Qual utilitário avançado de rede substituiu o antigo comando 'route' nas distribuições modernas do Linux?", ["ip", "ifconfig", "arp", "route"], "ip"),
        ("Planejamento e Desempenho", "Qual ferramenta interativa de monitoramento de desempenho exibe estatísticas de CPU, memória e E/S em tempo real?", ["sar / sysstat", "free", "uptime", "uname"], "sar / sysstat")
    ]
    for i in range(1, 41):
        base = topicos_lpic2[(i - 1) % len(topicos_lpic2)]
        q_texto = f"Questão LPIC-2 #{i}: {base[1]} (Tópico: {base[0]})"
        ops = base[2].copy()
        random.shuffle(ops)
        questoes_lpic2.append({
            "id": f"lpic2_{i}",
            "topico": base[0],
            "pergunta": q_texto,
            "opcoes": base[2],
            "opcoes_fixas": ops,
            "resposta_oficial": base[3]
        })
    return questoes_lpic2

def verificar_acerto(resp_user, resp_certa):
    if resp_user is None or resp_certa is None:
        return False
    u = " ".join(str(resp_user).strip().lower().split())
    c = " ".join(str(resp_certa).strip().lower().split())
    return u == c

def processar_finalizacao(tipo_simulado, tempo_decorrido):
    if tipo_simulado == "essentials":
        banco_ativo = st.session_state.simulado_essentials
        respostas_ativas = st.session_state.respostas_essentials
    elif tipo_simulado == "lpic1":
        banco_ativo = st.session_state.simulado_lpic1
        respostas_ativas = st.session_state.respostas_lpic1
    elif tipo_simulado == "lpic2":
        banco_ativo = st.session_state.simulado_lpic2
        respostas_ativas = st.session_state.respostas_lpic2
    elif tipo_simulado == "misto12":
        banco_ativo = st.session_state.simulado_misto12
        respostas_ativas = st.session_state.respostas_misto12
    else:
        banco_ativo = st.session_state.simulado_geral
        respostas_ativas = st.session_state.respostas_geral
    
    total_questoes = len(banco_ativo)
    questoes_respondidas = sum(1 for k in range(total_questoes) if respostas_ativas.get(k) is not None and str(respostas_ativas.get(k)).strip() != "")
    
    if questoes_respondidas < total_questoes:
        st.session_state.erro_finalizacao = f"❌ Você respondeu apenas {questoes_respondidas} de {total_questoes} questões. É obrigatório responder TODAS as questões antes de finalizar!"
        st.rerun()
        return

    acertos = 0
    for i, q in enumerate(banco_ativo):
        resp_user = respostas_ativas.get(i)
        resp_certa = q.get('resposta_oficial')
        if verificar_acerto(resp_user, resp_certa):
            acertos += 1
            
    minimo_acertos = total_questoes * 0.5
    
    if acertos < minimo_acertos:
        st.session_state.erro_finalizacao = f"❌ Você concluiu a prova, mas acertou {acertos} de {total_questoes} questões ({(acertos/total_questoes)*100:.1f}%). Para liberar o gabarito e entrar no Ranking Top 10, é necessário atingir no mínimo 50% de acertos ({int(minimo_acertos)} acertos). Continue treinando!"
    else:
        st.session_state.erro_finalizacao = None
        st.session_state.tempo_gasto = tempo_decorrido
        st.session_state.simulado_em_andamento = None

        if tipo_simulado == "essentials":
            st.session_state.finalizado_essentials = True
            st.session_state.nick_salvo_essentials = False
        elif tipo_simulado == "lpic1":
            st.session_state.finalizado_lpic1 = True
            st.session_state.nick_salvo_lpic1 = False
        elif tipo_simulado == "lpic2":
            st.session_state.finalizado_lpic2 = True
            st.session_state.nick_salvo_lpic2 = False
        elif tipo_simulado == "misto12":
            st.session_state.finalizado_misto12 = True
            st.session_state.nick_salvo_misto12 = False
        else:
            st.session_state.finalizado_geral = True
            st.session_state.nick_salvo_geral = False
    st.rerun()

def renderizar_modulo_simulado(titulo_pagina, tipo_key, banco_questoes_ref, qtd_questoes=40, tempo_minutos=60):
    st.markdown(f"## {titulo_pagina}")
    
    ativo_key = f"ativo_{tipo_key}"
    inicio_key = f"inicio_{tipo_key}"
    finalizado_key = f"finalizado_{tipo_key}"
    respostas_key = f"respostas_{tipo_key}"
    simulado_ativo_key = f"simulado_{tipo_key}"
    nick_salvo_key = f"nick_salvo_{tipo_key}"

    if ativo_key not in st.session_state: st.session_state[ativo_key] = False
    if finalizado_key not in st.session_state: st.session_state[finalizado_key] = False
    if simulado_ativo_key not in st.session_state: st.session_state[simulado_ativo_key] = random.sample(banco_questoes_ref, k=min(qtd_questoes, len(banco_questoes_ref)))
    if respostas_key not in st.session_state: st.session_state[respostas_key] = {}
    if nick_salvo_key not in st.session_state: st.session_state[nick_salvo_key] = False

    if st.session_state.get("simulado_em_andamento") and st.session_state.get("simulado_em_andamento") != tipo_key:
        outro_ativo = st.session_state.get("simulado_em_andamento")
        st.warning(f"⚠️ **Atenção:** Você já possui um simulado ativo em andamento (`{outro_ativo.upper()}`). \n\nVocê precisa **finalizar** ou **abandonar** a prova atual antes de iniciar um novo simulado em outra categoria!")
        if st.button("🗑️ Abandonar Prova Atual e Iniciar Esta", key=f"btn_abandonar_{tipo_key}"):
            st.session_state[f"ativo_{outro_ativo}"] = False
            st.session_state[f"finalizado_{outro_ativo}"] = True
            st.session_state.simulado_em_andamento = tipo_key
            st.session_state[ativo_key] = True
            st.session_state[inicio_key] = time.time()
            st.session_state[respostas_key] = {}
            st.session_state.erro_finalizacao = None
            st.rerun()
        return

    if not st.session_state[ativo_key] and not st.session_state[finalizado_key]:
        st.info(f"📌 **Diretrizes do Exame Oficial:**\n- **{qtd_questoes}** Questões de múltipla escolha.\n- **{tempo_minutos} minutos** de tempo limite estrito.\n- Obrigatório responder **todas** as questões.\n- Nota mínima de corte: **50%** para liberação do gabarito e certificação no ranking.")
        
        if st.button("Iniciar Exame Oficial", key=f"btn_iniciar_{tipo_key}"):
            st.session_state.simulado_em_andamento = tipo_key
            st.session_state[ativo_key] = True
            st.session_state[inicio_key] = time.time()
            st.session_state[respostas_key] = {}
            st.session_state.erro_finalizacao = None
            st.rerun()
        return

    TEMPO_OFICIAL = tempo_minutos * 60 

    if st.session_state[ativo_key] and not st.session_state[finalizado_key]:
        tempo_decorrido = int(time.time() - st.session_state[inicio_key])
        tempo_restante = TEMPO_OFICIAL - tempo_decorrido
        
        if tempo_restante > 0:
            st.metric("Tempo Restante", f"{tempo_restante // 60:02d}:{tempo_restante % 60:02d}")
        else:
            st.error("TEMPO ESGOTADO!")
            st.session_state.tempo_gasto = TEMPO_OFICIAL
            st.session_state[finalizado_key] = True
            st.session_state[ativo_key] = False
            st.session_state.simulado_em_andamento = None
            st.rerun()
        
        st.markdown("---")
        
        if st.button("🚪 Abandonar Prova e Voltar", key=f"btn_abandonar_ativo_{tipo_key}"):
            st.session_state[ativo_key] = False
            st.session_state[finalizado_key] = False
            st.session_state.simulado_em_andamento = None
            st.rerun()
        st.markdown("---")

        if st.session_state.erro_finalizacao:
            st.error(st.session_state.erro_finalizacao)
            if "50%" in st.session_state.erro_finalizacao:
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Limpar Respostas", key=f"btn_limpar_topo_{tipo_key}"):
                        st.session_state[respostas_key] = {}
                        st.session_state.erro_finalizacao = None
                        st.rerun()
                with c2:
                    if st.button("Sortear Novas Questões", key=f"btn_sortear_topo_{tipo_key}"):
                        st.session_state[simulado_ativo_key] = random.sample(banco_questoes_ref, k=min(qtd_questoes, len(banco_questoes_ref)))
                        st.session_state[respostas_key] = {}
                        st.session_state.erro_finalizacao = None
                        st.session_state[inicio_key] = time.time()
                        st.rerun()
            st.markdown("---")

        if st.button("Finalizar Simulado e Ver Gabarito", key=f"btn_fin_topo_{tipo_key}"):
            processar_finalizacao(tipo_key, tempo_decorrido)

        st.markdown("---")
            
        for i, q in enumerate(st.session_state[simulado_ativo_key]):
            st.markdown(f"**{i+1}. {q['pergunta']}**")
                
            opcoes = q['opcoes_fixas']
            resp_atual = st.session_state[respostas_key].get(i)
            idx_default = opcoes.index(resp_atual) if resp_atual in opcoes else None
            
            # 🌟 ALTERNATIVAS NUMERADAS/FORMATADAS COM LETRAS (A, B, C, D)
            opcoes_formatadas = [f"{chr(65+j)}) {op}" for j, op in enumerate(opcoes)]
            mapa_opcoes = {f"{chr(65+j)}) {op}": op for j, op in enumerate(opcoes)}
            
            val_atual_fmt = None
            if resp_atual in opcoes:
                for k_f, v_o in mapa_opcoes.items():
                    if v_o == resp_atual:
                        val_atual_fmt = k_f
                        break
            
            escolha_fmt = st.radio(f"radio_{tipo_key}_{i}_{q['id']}", opcoes_formatadas, index=opcoes_formatadas.index(val_atual_fmt) if val_atual_fmt in opcoes_formatadas else None, key=f"val_{tipo_key}_{i}", label_visibility="collapsed")
            if escolha_fmt is not None:
                st.session_state[respostas_key][i] = mapa_opcoes[escolha_fmt]
            st.divider()

        if st.session_state.erro_finalizacao:
            st.error(st.session_state.erro_finalizacao)
            if "50%" in st.session_state.erro_finalizacao:
                cb1, cb2 = st.columns(2)
                with cb1:
                    if st.button("Limpar Respostas", key=f"btn_limpar_base_{tipo_key}"):
                        st.session_state[respostas_key] = {}
                        st.session_state.erro_finalizacao = None
                        st.rerun()
                with cb2:
                    if st.button("Sortear Novas Questões", key=f"btn_sortear_base_{tipo_key}"):
                        st.session_state[simulado_ativo_key] = random.sample(banco_questoes_ref, k=min(qtd_questoes, len(banco_questoes_ref)))
                        st.session_state[respostas_key] = {}
                        st.session_state.erro_finalizacao = None
                        st.session_state[inicio_key] = time.time()
                        st.rerun()
            st.markdown("---")

        if st.button("Finalizar Simulado e Ver Gabarito", key=f"btn_fin_base_{tipo_key}"):
            processar_finalizacao(tipo_key, tempo_decorrido)
            
    elif st.session_state[finalizado_key]:
        st.success(f"{titulo_pagina} Concluído com Sucesso!")
        
        acertos = 0
        for i, q in enumerate(st.session_state[simulado_ativo_key]):
            resp_user = st.session_state[respostas_key].get(i)
            resp_certa = q.get('resposta_oficial')
            if verificar_acerto(resp_user, resp_certa):
                acertos += 1
                    
        total_questoes = len(st.session_state[simulado_ativo_key])
        nota_final = (acertos / total_questoes) * 10 if total_questoes > 0 else 0
        
        tag_ranking = {"essentials": "Essentials", "lpic1": "LPIC-1", "lpic2": "LPIC-2", "misto12": "Misto 1+2", "geral": "Geral"}[tipo_key]

        if not st.session_state[nick_salvo_key]:
            st.info("Desempenho aprovado! Registre sua credencial no Ranking Global:")
            col_n1, col_n2 = st.columns([3, 1])
            with col_n1:
                nick_input = st.text_input("Nome / Nickname:", value="Samico", key=f"nick_{tipo_key}")
            with col_n2:
                st.write("")
                st.write("")
                if st.button("Salvar no Ranking", key=f"btn_salvar_{tipo_key}"):
                    st.session_state.ranking.append({
                        "nick": nick_input, 
                        "nota": nota_final, 
                        "tempo": st.session_state.tempo_gasto, 
                        "prova": tag_ranking,
                        "data_hora": datetime.now().strftime("%d/%m/%Y às %H:%M")
                    })
                    st.session_state.ranking = sorted(st.session_state.ranking, key=lambda x: (-x['nota'], x['tempo']))
                    st.session_state[nick_salvo_key] = True
                    st.rerun()
        else:
            st.success("Credencial registrada com sucesso no Ranking!")
        
        st.markdown("---")
        st.metric("Sua Nota Final", f"{nota_final:.1f} / 10.0", f"{acertos} de {total_questoes} corretas")
        
        if st.button("Sortear Novo Exame", key=f"btn_novo_fim_{tipo_key}"):
            st.session_state[finalizado_key] = False
            st.session_state[ativo_key] = False
            st.session_state.simulado_em_andamento = None
            st.session_state[simulado_ativo_key] = random.sample(banco_questoes_ref, k=min(qtd_questoes, len(banco_questoes_ref)))
            st.session_state[respostas_key] = {}
            st.session_state.erro_finalizacao = None
            st.rerun()

        st.markdown("### Gabarito Analítico com Comentários Técnicos")
        for i, q in enumerate(st.session_state[simulado_ativo_key]):
            resp_user = st.session_state[respostas_key].get(i)
            resp_certa = q.get('resposta_oficial', 'Não informada')
            st.markdown(f"**{i+1}. {q['pergunta']}**")
            
            if verificar_acerto(resp_user, resp_certa):
                st.success(f"Sua resposta: {resp_user} (Correta!)")
            else:
                if not resp_user:
                    st.warning(f"Sua resposta: Não respondida | Resposta Correta: {resp_certa}")
                else:
                    st.error(f"Sua resposta: {resp_user} | Resposta Correta: {resp_certa}")
            
            comentario = obter_comentario(q['pergunta'], resp_certa)
            st.info(comentario)
            st.divider()

def main():
    st.set_page_config(page_title="LinuxPro Academy | SAMICOIOT", layout="wide")

    if 'banco_essentials' not in st.session_state:
        st.session_state.banco_essentials = carregar_banco_essentials()
    if 'banco_lpic1' not in st.session_state:
        st.session_state.banco_lpic1 = carregar_banco_lpic1()
    if 'banco_lpic2' not in st.session_state:
        st.session_state.banco_lpic2 = carregar_banco_lpic2()
    if 'banco_misto12' not in st.session_state:
        st.session_state.banco_misto12 = st.session_state.banco_lpic1 + st.session_state.banco_lpic2
    if 'banco_geral' not in st.session_state:
        st.session_state.banco_geral = st.session_state.banco_essentials + st.session_state.banco_lpic1 + st.session_state.banco_lpic2

    if 'acesso_vip' not in st.session_state: st.session_state.acesso_vip = False
    if 'senha_aleatoria' not in st.session_state:
        st.session_state.senha_aleatoria = ''.join(random.choices(string.digits, k=6))
        
    if 'tempo_gasto' not in st.session_state: st.session_state.tempo_gasto = 0
    if 'erro_finalizacao' not in st.session_state: st.session_state.erro_finalizacao = None
    if 'simulado_em_andamento' not in st.session_state: st.session_state.simulado_em_andamento = None
    
    if 'ranking' not in st.session_state:
        st.session_state.ranking = [
            {"nick": "Samico", "nota": 9.5, "tempo": 1200, "prova": "Essentials", "data_hora": "21/07/2026 às 08:30"},
            {"nick": "LinuxPro", "nota": 8.8, "tempo": 1450, "prova": "LPIC-1", "data_hora": "21/07/2026 às 08:40"},
            {"nick": "SysAdmin", "nota": 8.2, "tempo": 1300, "prova": "LPIC-2", "data_hora": "21/07/2026 às 08:50"},
            {"nick": "DevOpsBR", "nota": 7.9, "tempo": 1350, "prova": "Misto 1+2", "data_hora": "21/07/2026 às 08:55"},
            {"nick": "TerminalMaster", "nota": 8.0, "tempo": 1100, "prova": "Geral", "data_hora": "21/07/2026 às 09:00"}
        ]

    # Inicializa o estado do menu
    if 'menu_ativo' not in st.session_state:
        st.session_state.menu_ativo = "Treino Geral"

    # Configurações na Barra Lateral (Apenas Zoom e Modo Escuro)
    st.sidebar.markdown("## LinuxPro Academy")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👁️ Acessibilidade Visual")
    nivel_zoom = st.sidebar.radio("Tamanho do Texto:", ["Padrão (100%)", "Ampliado (115%)", "Grande (130%)"], key="zoom_sb", label_visibility="collapsed")
    modo_escuro = st.sidebar.checkbox("🌙 Ativar Tela Escura (Modo Noturno)", key="dark_sb")

    aplicar_estilo_acessivel(nivel_zoom, modo_escuro)

    opcoes_menu = [
        "Treino Geral", 
        "Treino por Tópico", 
        "Simulado Linux Essentials (60 Q)",
        "Simulado LPIC-1 (40 Q)",
        "Simulado LPIC-2 (40 Q)",
        "Simulado Misto LPIC-1 + LPIC-2 (40 Q)",
        "Simulado Geral (Misto 60 Q)",
        "Ranking de Notas",
        "Materiais VIP",
        "Créditos"
    ]

    # 🌟 MENU DE NAVEGAÇÃO SUPERIOR COMPLETO E FUNCIONAL EM DUAS LINHAS DE BOTÕES
    st.markdown("### 🧭 Painel de Navegação Rápida")
    
    col_n1, col_n2, col_n3, col_n4, col_n5 = st.columns(5)
    with col_n1:
        if st.button("📚 Treino Geral", use_container_width=True, key="top_tg"):
            st.session_state.menu_ativo = "Treino Geral"
            st.rerun()
    with col_n2:
        if st.button("🔍 Por Tópico", use_container_width=True, key="top_tp"):
            st.session_state.menu_ativo = "Treino por Tópico"
            st.rerun()
    with col_n3:
        if st.button("📝 Essentials", use_container_width=True, key="top_se"):
            st.session_state.menu_ativo = "Simulado Linux Essentials (60 Q)"
            st.rerun()
    with col_n4:
        if st.button("⚡ LPIC-1", use_container_width=True, key="top_s1"):
            st.session_state.menu_ativo = "Simulado LPIC-1 (40 Q)"
            st.rerun()
    with col_n5:
        if st.button("🚀 LPIC-2", use_container_width=True, key="top_s2"):
            st.session_state.menu_ativo = "Simulado LPIC-2 (40 Q)"
            st.rerun()

    col_n6, col_n7, col_n8, col_n9, col_n10 = st.columns(5)
    with col_n6:
        if st.button("🔥 Misto 1+2", use_container_width=True, key="top_sm"):
            st.session_state.menu_ativo = "Simulado Misto LPIC-1 + LPIC-2 (40 Q)"
            st.rerun()
    with col_n7:
        if st.button("🎯 Sim. Geral", use_container_width=True, key="top_sg"):
            st.session_state.menu_ativo = "Simulado Geral (Misto 60 Q)"
            st.rerun()
    with col_n8:
        if st.button("🏆 Ranking", use_container_width=True, key="top_rk"):
            st.session_state.menu_ativo = "Ranking de Notas"
            st.rerun()
    with col_n9:
        if st.button("🔓 Materiais VIP", use_container_width=True, key="top_vip"):
            st.session_state.menu_ativo = "Materiais VIP"
            st.rerun()
    with col_n10:
        if st.button("ℹ️ Créditos", use_container_width=True, key="top_cred"):
            st.session_state.menu_ativo = "Créditos"
            st.rerun()
            
    st.markdown("---")

    modo = st.session_state.menu_ativo

    if modo == "Treino Geral":
        st.markdown("## Área de Treino Geral")
        st.markdown("Ambiente de estudo contínuo com feedback e gabarito comentado instantâneo.")
        st.markdown("---")
        for i, q in enumerate(st.session_state.banco_essentials, 1):
            st.markdown(f"**Questão {i}: {q['pergunta']}**")
            opcoes_q = q['opcoes_fixas']
            opcoes_fmt = [f"{chr(65+j)}) {op}" for j, op in enumerate(opcoes_q)]
            mapa_fmt = {f"{chr(65+j)}) {op}": op for j, op in enumerate(opcoes_q)}
            
            resp_t = st.radio(f"tg_{i}_{q['id']}", opcoes_fmt, index=None, label_visibility="collapsed", key=f"radio_tg_{i}")
            
            if resp_t:
                resp_escolhida = mapa_fmt[resp_t]
                resp_certa = q.get('resposta_oficial', 'Não informada')
                if verificar_acerto(resp_escolhida, resp_certa):
                    st.success(f"Resposta Correta: {resp_t}")
                else:
                    # Acha a letra da resposta certa para exibir bonitinho
                    letra_certa = ""
                    for k_f, v_o in mapa_fmt.items():
                        if verificar_acerto(v_o, resp_certa):
                            letra_certa = k_f
                            break
                    st.error(f"Sua resposta: {resp_t} | Correta: {letra_certa if letra_certa else resp_certa}")
                
                st.info(obter_comentario(q['pergunta'], resp_certa))
            st.divider()

    elif modo == "Treino por Tópico":
        st.markdown("## Treino Focado por Tópico")
        topicos = sorted(list(set(q.get('topico', 'Geral Essentials') for q in st.session_state.banco_essentials if 'topico' in q)))
        if not topicos:
            topicos = ["Geral Essentials"]
        t = st.selectbox("Selecione o Módulo de Estudo:", topicos)
        st.markdown("---")
        
        questoes_filtradas = [q for q in st.session_state.banco_essentials if q.get('topico', 'Geral Essentials') == t]
        for i, q in enumerate(questoes_filtradas, 1):
            st.markdown(f"**Questão {i}: {q['pergunta']}**")
            opcoes_q = q['opcoes_fixas']
            opcoes_fmt = [f"{chr(65+j)}) {op}" for j, op in enumerate(opcoes_q)]
            mapa_fmt = {f"{chr(65+j)}) {op}": op for j, op in enumerate(opcoes_q)}
            
            resp_top = st.radio(f"tp_{i}_{q['id']}_{t}", opcoes_fmt, index=None, label_visibility="collapsed", key=f"radio_tp_{i}")
            
            if resp_top:
                resp_escolhida = mapa_fmt[resp_top]
                resp_certa = q.get('resposta_oficial', 'Não informada')
                if verificar_acerto(resp_escolhida, resp_certa):
                    st.success(f"Resposta Correta: {resp_top}")
                else:
                    letra_certa = ""
                    for k_f, v_o in mapa_fmt.items():
                        if verificar_acerto(v_o, resp_certa):
                            letra_certa = k_f
                            break
                    st.error(f"Sua resposta: {resp_top} | Correta: {letra_certa if letra_certa else resp_certa}")
                
                st.info(obter_comentario(q['pergunta'], resp_certa))
            st.divider()

    elif modo == "Simulado Linux Essentials (60 Q)":
        renderizar_modulo_simulado("Simulado Linux Essentials (60 Questões)", "essentials", st.session_state.banco_essentials, qtd_questoes=60, tempo_minutos=60)

    elif modo == "Simulado LPIC-1 (40 Q)":
        renderizar_modulo_simulado("Simulado LPIC-1 (Prova Real Avançada 40 Q)", "lpic1", st.session_state.banco_lpic1, qtd_questoes=40, tempo_minutos=60)

    elif modo == "Simulado LPIC-2 (40 Q)":
        renderizar_modulo_simulado("Simulado LPIC-2 (Administração de Redes e Servidores)", "lpic2", st.session_state.banco_lpic2, qtd_questoes=40, tempo_minutos=60)

    elif modo == "Simulado Misto LPIC-1 + LPIC-2 (40 Q)":
        renderizar_modulo_simulado("Simulado Misto LPIC-1 + LPIC-2 (40 Q)", "misto12", st.session_state.banco_misto12, qtd_questoes=40, tempo_minutos=60)

    elif modo == "Simulado Geral (Misto 60 Q)":
        renderizar_modulo_simulado("Simulado Geral Misto (Essentials + LPIC-1 + LPIC-2)", "geral", st.session_state.banco_geral, qtd_questoes=60, tempo_minutos=90)

    elif modo == "Ranking de Notas":
        st.markdown("## Hall da Fama - Rankings Globais")
        st.markdown("Painel executivo de certificações e melhores desempenhos com registro de data e horário.")
        st.markdown("---")
        
        categorias = [
            ("Linux Essentials", "Essentials"),
            ("LPIC-1", "LPIC-1"),
            ("LPIC-2", "LPIC-2"),
            ("Misto LPIC-1 + LPIC-2", "Misto 1+2"),
            ("Simulado Geral Misto", "Geral")
        ]
        
        for nome_cat, tag_cat in categorias:
            st.markdown(f"### Categoria: {nome_cat}")
            ranking_filtrado = [r for r in st.session_state.ranking if r.get('prova') == tag_cat]
            ranking_ordenado = sorted(ranking_filtrado, key=lambda x: (-x['nota'], x['tempo']))[:10]
            
            if not ranking_ordenado:
                st.info(f"Nenhum registro no ranking de {nome_cat} ainda.")
            else:
                for idx, item in enumerate(ranking_ordenado, 1):
                    m_t = item['tempo'] // 60
                    s_t = item['tempo'] % 60
                    tempo_str = f"{m_t:02d}:{s_t:02d}"
                    dh_str = item.get('data_hora', '21/07/2026 às 09:00')
                    
                    if idx == 1:
                        st.markdown(f"**1º Lugar:** `{item['nick']}` — **Nota: {item['nota']:.1f}** *(Tempo: {tempo_str})* | `{dh_str}`")
                    elif idx == 2:
                        st.markdown(f"**2º Lugar:** `{item['nick']}` — **Nota: {item['nota']:.1f}** *(Tempo: {tempo_str})* | `{dh_str}`")
                    elif idx == 3:
                        st.markdown(f"**3º Lugar:** `{item['nick']}` — **Nota: {item['nota']:.1f}** *(Tempo: {tempo_str})* | `{dh_str}`")
                    else:
                        st.markdown(f"**{idx}º Lugar:** `{item['nick']}` — **Nota: {item['nota']:.1f}** *(Tempo: {tempo_str})* | `{dh_str}`")
            st.markdown("---")
            
    elif modo == "Materiais VIP":
        st.markdown("## Central de Recursos VIP")
        st.markdown("---")
        if not st.session_state.acesso_vip:
            st.info("🔓 **Área de Apoio e Doação Voluntária**\n\nApoie o projeto com qualquer contribuição via Pix e tenha acesso imediato a materiais exclusivos de estudo.")
            
            st.markdown("### Passo 1: Inscreva-se no Canal Oficial")
            st.markdown("""
                <a href="https://www.youtube.com/@EdielsonSamico?sub_confirmation=1" target="_blank" class="custom-link-btn">
                    👉 INSCREVA-SE NO CANAL DO YOUTUBE
                </a>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### Passo 2: Contribuição Voluntária via Pix")
            st.markdown("Faça uma doação/contribuição para a chave Pix abaixo:")
            st.code("samicoiot@gmail.com", language="text")
            
            st.markdown("Ou escaneie o QR Code abaixo com o aplicativo do seu banco:")
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=samicoiot@gmail.com"
            st.image(qr_url, width=200)
            
            st.markdown("---")
            st.markdown("### Passo 3: Validar Acesso")
            comprovante_input = st.text_input("Insira o código de liberação ou ID da transação:", type="password")
            
            if st.button("Validar Acesso VIP"):
                if comprovante_input == st.session_state.senha_aleatoria or comprovante_input == "vip2026":
                    st.session_state.acesso_vip = True
                    st.success("✅ Acesso liberado com sucesso! Obrigado pelo apoio.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Código inválido. Verifique o código ou gere uma chave de teste.")
            
            if st.button("Gerar Chave de Teste (Admin)"):
                st.info(f"Chave gerada para teste: **{st.session_state.senha_aleatoria}**")
        else:
            st.success("🎉 **Bem-vindo à Área VIP Corporativa!** Acesso total liberado.")
            materiais = {
                "Apostila Master Linux Completa": "Apostila_Premium_de_Certificacao.pdf", 
                "Guia Definitivo LPIC-1 Terminal": "LPIC-1_Terminal_2026.pdf",
                "Banco de Questões Comentadas Avançadas": "Banco_Questoes_VIP.pdf"
            }
            for n, l in materiais.items(): 
                st.markdown(f"- 📥 [{n}]({l})")
                
            st.markdown("---")
            if st.button("Encerrar Sessão VIP"):
                st.session_state.acesso_vip = False
                st.rerun()
    
    elif modo == "Créditos":
        st.markdown("## Sobre a Plataforma & Apoio")
        st.markdown("**LinuxPro Academy** — Desenvolvido por Edielson Samico.")
        st.markdown("---")
        st.markdown("### 💡 Apoie este Projeto")
        st.markdown("Se esta plataforma te ajudou nos estudos para as certificações Linux e você deseja apoiar a manutenção e criação de novos conteúdos gratuitos para o canal, considere fazer uma contribuição voluntária via Pix:")
        st.code("samicoiot@gmail.com", language="text")
        
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data=samicoiot@gmail.com"
        st.image(qr_url, width=180)
        
        st.markdown("🚀 *Muito obrigado por fazer parte da nossa comunidade!*")

if __name__ == "__main__":
    main()
