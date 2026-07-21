import streamlit as st
import random
import re
import importlib
import hashlib
import string
import time

def gerar_hash_conteudo(pergunta):
    texto_limpo = re.sub(r'^(quest[ãa]o.*?\d+|q\d+|\d+)\s*[\.\:\-]?\s*', '', pergunta.strip(), flags=re.IGNORECASE)
    texto_limpo = " ".join(texto_limpo.lower().split())
    return hashlib.md5(texto_limpo.encode('utf-8')).hexdigest()

def inferir_resposta_correta(pergunta, opcoes):
    """Fallback inteligente para associar a resposta caso a chave venha vazia."""
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
        return "Comentário: A partição/espaço de swap é utilizada pelo kernel como memória virtual quando a RAM física atinge o limite."
    elif "fhs" in p or "usr" in p:
        return "Comentário: Segundo o FHS (Filesystem Hierarchy Standard), o diretório `/usr` armazena dados secundários, utilitários e aplicativos executáveis."
    elif "lilo" in p or "syslinux" in p:
        return "Comentário: O Syslinux é uma família de carregadores de boot leves frequentemente usados para mídias removíveis e sistemas alternativos."
    elif "pci" in p:
        return "Comentário: O comando `lspci` lista detalhadamente todos os dispositivos PCI e o chipset conectado na placa-mãe."
    elif "sysvinit" in p or "messages" in p:
        return "Comentário: O arquivo `/var/log/messages` centraliza logs gerais do sistema e de eventos do syslog no padrão tradicional."
    elif "módulos" in p or "lsmod" in p:
        return "Comentário: O comando `lsmod` lê o arquivo `/proc/modules` para exibir os módulos de driver atualmente carregados na memória."
    else:
        return f"Comentário: A alternativa correta é **'{resposta_certa}'**, pois atende diretamente aos requisitos técnicos descritos no enunciado da questão."

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
    questoes_respondidas = len(respostas_ativas)
    
    if questoes_respondidas < total_questoes:
        st.session_state.erro_finalizacao = f"❌ Você respondeu apenas {questoes_respondidas} de {total_questoes} questões. É obrigatório responder TODAS as questões antes de finalizar!"
        st.rerun()
        return

    acertos = 0
    for i, q in enumerate(banco_ativo):
        resp_user = respostas_ativas.get(i)
        resp_certa = q.get('resposta_oficial')
        if resp_user and resp_certa and (str(resp_user).strip().lower() == str(resp_certa).strip().lower()):
            acertos += 1
            
    minimo_acertos = total_questoes * 0.5  # 50% de acertos
    
    if acertos < minimo_acertos:
        st.session_state.erro_finalizacao = f"❌ Você concluiu a prova, mas acertou {acertos} de {total_questoes} questões ({(acertos/total_questoes)*100:.1f}%). Para liberar o gabarito e entrar no Ranking Top 10, é necessário atingir no mínimo 50% de acertos ({int(minimo_acertos)} acertos). Continue treinando!"
    else:
        st.session_state.erro_finalizacao = None
        st.session_state.tempo_gasto = tempo_decorrido
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
    st.title(f"⏱️ {titulo_pagina}")
    
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

    # 1. TELA DE INICIALIZAÇÃO
    if not st.session_state[ativo_key] and not st.session_state[finalizado_key]:
        st.info(f"📌 **Regras do Simulado Oficial:**\n- {qtd_questoes} Questões de múltipla escolha.\n- Tempo limite: {tempo_minutos} minutos.\n- Obrigatório responder todas as questões.\n- Necessário 50% de acertos para liberar o gabarito e ranking.")
        if st.button("▶️ Iniciar Prova Agora", key=f"btn_iniciar_{tipo_key}"):
            st.session_state[ativo_key] = True
            st.session_state[inicio_key] = time.time()
            st.session_state[respostas_key] = {}
            st.session_state.erro_finalizacao = None
            st.rerun()
        return

    TEMPO_OFICIAL = tempo_minutos * 60 

    # 2. PROVA EM ANDAMENTO
    if st.session_state[ativo_key] and not st.session_state[finalizado_key]:
        tempo_decorrido = int(time.time() - st.session_state[inicio_key])
        tempo_restante = TEMPO_OFICIAL - tempo_decorrido
        
        if tempo_restante > 0:
            st.metric("⏱️ Tempo Restante", f"{tempo_restante // 60:02d}:{tempo_restante % 60:02d}")
        else:
            st.error("TEMPO ESGOTADO!")
            st.session_state.tempo_gasto = TEMPO_OFICIAL
            st.session_state[finalizado_key] = True
            st.session_state[ativo_key] = False
            st.rerun()
        
        st.markdown("---")
        
        if st.session_state.erro_finalizacao:
            st.error(st.session_state.erro_finalizacao)
            if "50%" in st.session_state.erro_finalizacao:
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("🧹 Limpar Respostas", key=f"btn_limpar_topo_{tipo_key}"):
                        st.session_state[respostas_key] = {}
                        st.session_state.erro_finalizacao = None
                        st.rerun()
                with c2:
                    if st.button("🔄 Sortear Novas Questões", key=f"btn_sortear_topo_{tipo_key}"):
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
            idx_default = opcoes.index(resp_current) if (resp_current := resp_atual) in opcoes else None
            
            escolha = st.radio(f"radio_{tipo_key}_{i}_{q['id']}", opcoes, index=idx_default, label_visibility="collapsed")
            if escolha:
                st.session_state[respostas_key][i] = escolha
            st.divider()

        if st.session_state.erro_finalizacao:
            st.error(st.session_state.erro_finalizacao)
            if "50%" in st.session_state.erro_finalizacao:
                cb1, cb2 = st.columns(2)
                with cb1:
                    if st.button("🧹 Limpar Respostas", key=f"btn_limpar_base_{tipo_key}"):
                        st.session_state[respostas_key] = {}
                        st.session_state.erro_finalizacao = None
                        st.rerun()
                with cb2:
                    if st.button("🔄 Sortear Novas Questões", key=f"btn_sortear_base_{tipo_key}"):
                        st.session_state[simulado_ativo_key] = random.sample(banco_questoes_ref, k=min(qtd_questoes, len(banco_questoes_ref)))
                        st.session_state[respostas_key] = {}
                        st.session_state.erro_finalizacao = None
                        st.session_state[inicio_key] = time.time()
                        st.rerun()
            st.markdown("---")

        if st.button("Finalizar Simulado e Ver Gabarito", key=f"btn_fin_base_{tipo_key}"):
            processar_finalizacao(tipo_key, tempo_decorrido)
            
    # 3. PROVA FINALIZADA COM SUCESSO
    elif st.session_state[finalizado_key]:
        st.success(f"🏁 {titulo_pagina} Finalizado com Sucesso!")
        acertos = sum(1 for i, q in enumerate(st.session_state[simulado_ativo_key]) if st.session_state[respostas_key].get(i) and str(st.session_state[respostas_key].get(i)).strip().lower() == str(q.get('resposta_oficial')).strip().lower())
        total_questoes = len(st.session_state[simulado_ativo_key])
        nota_final = (acertos / total_questoes) * 10 if total_questoes > 0 else 0
        
        tag_ranking = {"essentials": "Essentials", "lpic1": "LPIC-1", "lpic2": "LPIC-2", "misto12": "Misto 1+2", "geral": "Geral"}[tipo_key]

        if not st.session_state[nick_salvo_key]:
            st.info("🎉 Registre sua nota no Ranking Top 10:")
            col_n1, col_n2 = st.columns([3, 1])
            with col_n1:
                nick_input = st.text_input("Digite seu Nickname:", value="Samico", key=f"nick_{tipo_key}")
            with col_n2:
                st.write("")
                st.write("")
                if st.button("Salvar no Ranking", key=f"btn_salvar_{tipo_key}"):
                    st.session_state.ranking.append({"nick": nick_input, "nota": nota_final, "tempo": st.session_state.tempo_gasto, "prova": tag_ranking})
                    st.session_state.ranking = sorted(st.session_state.ranking, key=lambda x: (-x['nota'], x['tempo']))
                    st.session_state[nick_salvo_key] = True
                    st.rerun()
        else:
            st.success("✅ Sua nota foi salva no Ranking!")
        
        st.markdown("---")
        st.metric("Sua Nota Final", f"{nota_final:.1f} / 10.0", f"{acertos} de {total_questoes} corretas")
        
        if st.button("🔄 Sortear Novas Questões (Novo Simulado)", key=f"btn_novo_fim_{tipo_key}"):
            st.session_state[finalizado_key] = False
            st.session_state[ativo_key] = False
            st.session_state[simulado_ativo_key] = random.sample(banco_questoes_ref, k=min(qtd_questoes, len(banco_questoes_ref)))
            st.session_state[respostas_key] = {}
            st.session_state.erro_finalizacao = None
            st.rerun()

        st.subheader("📋 Gabarito Detalhado com Respostas Comentadas")
        for i, q in enumerate(st.session_state[simulado_ativo_key]):
            resp_user = st.session_state[respostas_key].get(i)
            resp_certa = q.get('resposta_oficial', 'Não informada')
            st.markdown(f"**{i+1}. {q['pergunta']}**")
            if not resp_user:
                st.warning(f"Sua resposta: Não respondida | Resposta Correta: {resp_certa}")
            elif resp_certa and str(resp_user).strip().lower() == str(resp_certa).strip().lower():
                st.success(f"Sua resposta: {resp_user} (Correta!)")
            else:
                st.error(f"Sua resposta: {resp_user} | Resposta Correta: {resp_certa}")
            
            # Exibe o comentário explicativo detalhado
            comentario = obter_comentario(q['pergunta'], resp_certa)
            st.info(comentario)
            st.divider()

def main():
    st.set_page_config(page_title="Ambiente SAMICOIOT", layout="wide")

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
    if 'clicou_no_cadastro' not in st.session_state: st.session_state.clicou_no_cadastro = False
    if 'senha_aleatoria' not in st.session_state:
        st.session_state.senha_aleatoria = ''.join(random.choices(string.digits, k=6))
        
    if 'tempo_gasto' not in st.session_state: st.session_state.tempo_gasto = 0
    if 'erro_finalizacao' not in st.session_state: st.session_state.erro_finalizacao = None
    
    if 'ranking' not in st.session_state:
        st.session_state.ranking = [
            {"nick": "Samico", "nota": 9.5, "tempo": 1200, "prova": "Essentials"},
            {"nick": "LinuxPro", "nota": 8.8, "tempo": 1450, "prova": "LPIC-1"},
            {"nick": "SysAdmin", "nota": 8.2, "tempo": 1300, "prova": "LPIC-2"},
            {"nick": "DevOpsBR", "nota": 7.9, "tempo": 1350, "prova": "Misto 1+2"},
            {"nick": "TerminalMaster", "nota": 8.0, "tempo": 1100, "prova": "Geral"}
        ]

    st.sidebar.title("Ambiente SAMICOIOT")
    modo = st.sidebar.radio("Navegação:", [
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
    ])

    if modo == "Treino Geral":
        st.title("📖 Área de Treino Geral (Questões Numeradas e Comentadas)")
        st.markdown("Pratique livremente com feedback imediato em cada questão.")
        st.markdown("---")
        for i, q in enumerate(st.session_state.banco_essentials, 1):
            st.markdown(f"**Questão {i}: {q['pergunta']}**")
            resp_t = st.radio(f"tg_{i}_{q['id']}", q['opcoes_fixas'], index=None, label_visibility="collapsed")
            
            if resp_t:
                resp_certa = q.get('resposta_oficial', 'Não informada')
                if str(resp_t).strip().lower() == str(resp_certa).strip().lower():
                    st.success(f"Resposta Correta: {resp_t}")
                else:
                    st.error(f"Sua resposta: {resp_t} | Correta: {resp_certa}")
                
                # Comentário explicativo integrado no Treino Geral
                st.info(obter_comentario(q['pergunta'], resp_certa))
            st.divider()

    elif modo == "Treino por Tópico":
        st.title("🎯 Treino por Tópico (Questões Numeradas e Comentadas)")
        topicos = sorted(list(set(q.get('topico', 'Geral') for q in st.session_state.banco_essentials if 'topico' in q)))
        if not topicos:
            topicos = ["Geral Essentials"]
        t = st.selectbox("Escolha o Tópico:", topicos)
        st.markdown("---")
        
        questoes_filtradas = [q for q in st.session_state.banco_essentials if q.get('topico', 'Geral Essentials') == t]
        for i, q in enumerate(questoes_filtradas, 1):
            st.markdown(f"**Questão {i}: {q['pergunta']}**")
            resp_top = st.radio(f"tp_{i}_{q['id']}_{t}", q['opcoes_fixas'], index=None, label_visibility="collapsed")
            
            if resp_top:
                resp_certa = q.get('resposta_oficial', 'Não informada')
                if str(resp_top).strip().lower() == str(resp_certa).strip().lower():
                    st.success(f"Resposta Correta: {resp_top}")
                else:
                    st.error(f"Sua resposta: {resp_top} | Correta: {resp_certa}")
                
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
        st.title("🏆 Rankings Top 10 por Categoria")
        st.markdown("Confira os melhores desempenhos divididos por cada tipo de simulado. *Critério de desempate: menor tempo de conclusão.*")
        
        categorias = [
            ("Linux Essentials", "Essentials"),
            ("LPIC-1", "LPIC-1"),
            ("LPIC-2", "LPIC-2"),
            ("Misto LPIC-1 + LPIC-2", "Misto 1+2"),
            ("Simulado Geral Misto", "Geral")
        ]
        
        for nome_cat, tag_cat in categorias:
            st.subheader(f"📌 Ranking: {nome_cat}")
            ranking_filtrado = [r for r in st.session_state.ranking if r.get('prova') == tag_cat]
            ranking_ordenado = sorted(ranking_filtrado, key=lambda x: (-x['nota'], x['tempo']))[:10]
            
            if not ranking_ordenado:
                st.info(f"Nenhum registro no ranking de {nome_cat} ainda. Seja o primeiro a concluir!")
            else:
                for idx, item in enumerate(ranking_ordenado, 1):
                    m_t = item['tempo'] // 60
                    s_t = item['tempo'] % 60
                    tempo_str = f"{m_t:02d}:{s_t:02d}"
                    
                    if idx == 1:
                        st.markdown(f"🥇 **1º Lugar:** `{item['nick']}` — **Nota: {item['nota']:.1f}** *(Tempo: {tempo_str})*")
                    elif idx == 2:
                        st.markdown(f"🥈 **2º Lugar:** `{item['nick']}` — **Nota: {item['nota']:.1f}** *(Tempo: {tempo_str})*")
                    elif idx == 3:
                        st.markdown(f"🥉 **3º Lugar:** `{item['nick']}` — **Nota: {item['nota']:.1f}** *(Tempo: {tempo_str})*")
                    else:
                        st.markdown(f"▫️ **{idx}º Lugar:** `{item['nick']}` — **Nota: {item['nota']:.1f}** *(Tempo: {tempo_str})*")
            st.markdown("---")
            
    elif modo == "Materiais VIP":
        st.title("🎁 Materiais VIP")
        if not st.session_state.acesso_vip:
            if st.link_button("👉 INSCREVA-SE NO CANAL", "https://www.youtube.com/@EdielsonSamico?sub_confirmation=1"):
                st.session_state.clicou_no_cadastro = True
            if st.session_state.clicou_no_cadastro:
                if st.button("Gerar Senha"): st.info(f"Senha: **{st.session_state.senha_aleatoria}**")
                codigo = st.text_input("Senha:", type="password")
                if st.button("Validar"):
                    if codigo == st.session_state.senha_aleatoria:
                        st.session_state.acesso_vip = True
                        st.rerun()
        else:
            st.success("Acesso VIP Liberado!")
            materiais = {"Apostila": "Apostila_Premium_de_Certificacao.pdf", "LPIC-1": "LPIC-1_Terminal_2026.pdf"}
            for n, l in materiais.items(): st.markdown(f"- [{n}]({l})")
            if st.button("Sair"):
                st.session_state.acesso_vip = False
                st.rerun()
    
    elif modo == "Créditos":
        st.write("Desenvolvido por Edielson Samico.")

if __name__ == "__main__":
    main()
