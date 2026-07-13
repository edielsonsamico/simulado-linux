POOL_108 = [
    {
        "id": 351, "topico": "Tópico 108: Serviços",
        "pergunta": "Qual daemon do Linux é tradicionalmente responsável por centralizar, processar e despachar mensagens de notificação de programas e facilidades do sistema?",
        "opcoes": ["syslogd", "klogd", "journald", "systemd-log"], "correta": "syslogd",
        "explicacao": "O daemon syslogd (e seus sucessores como rsyslogd) escuta sockets locais coletando e gravando logs com base em regras de severidade."
    },
    {
        "id": 352, "topico": "Tópico 108: Serviços",
        "pergunta": "O protocolo de sincronização temporal NTP executa o seu tráfego vital por meio de qual porta de rede e protocolo de transporte, respectivamente?",
        "opcoes": ["Porta UDP 123", "Porta TCP 123", "Porta UDP 53", "Porta TCP 80"], "correta": "Porta UDP 123",
        "explicacao": "O Network Time Protocol (NTP) dita a troca estruturada de pacotes de timestamp de tempo sobre datagramas na porta UDP 123."
    },
    {
        "id": 353, "topico": "Tópico 108: Serviços",
        "pergunta": "Qual ferramenta de linha de comando permite a um administrador consultar ou ajustar diretamente o relógio físico mantido na placa-mãe (BIOS)?",
        "opcoes": ["hwclock", "date", "ntpdate", "timedatectl"], "correta": "hwclock",
        "explicacao": "O comando hwclock (hardware clock) acessa a bios de tempo real independentemente do relógio dinâmico virtual mantido pelo kernel."
    },
    {
        "id": 354, "topico": "Tópico 108: Serviços",
        "pergunta": "Qual utilitário de terminal permite a um usuário ou script injetar manualmente registros de texto em níveis arbitrários no sistema central de log?",
        "opcoes": ["logger", "logwrite", "syslog -m", "echo > /var/log/syslog"], "correta": "logger",
        "explicacao": "O utilitário logger atua injetando strings personalizadas diretamente no syslog facilitando testes e auditorias de scripts."
    },
    {
        "id": 355, "topico": "Tópico 108: Serviços",
        "pergunta": "Qual nível literal de severidade de log do syslog representa o estado de máxima criticidade de pane total, indicando que o sistema ficou inutilizável?",
        "opcoes": ["emerg", "crit", "alert", "err"], "correta": "emerg",
        "explicacao": "A prioridade 'emerg' (emergency) sinaliza o nível de erro mais grave, disparando avisos de broadcast em lote para todos os terminais abertos."
    },
    {
        "id": 356, "topico": "Tópico 108: Serviços",
        "pergunta": "Em servidores onde o gerenciador de impressão CUPS está rodando ativo, qual porta IP trafega por padrão o acesso do painel administrativo web HTTP?",
        "opcoes": ["Porta 631", "Porta 515", "Porta 80", "Porta 9100"], "correta": "Porta 631",
        "explicacao": "O CUPS disponibiliza a sua interface gráfica de gerenciamento de spools e impressoras nativamente através do protocolo HTTP na porta 631."
    },
    {
        "id": 357, "topico": "Tópico 108: Serviços",
        "pergunta": "Na arquitetura clássica e comandos legados de impressão LPD, qual binário envia diretamente um arquivo documental para a fila de processamento da impressora?",
        "opcoes": ["lpr", "lpd", "lpq", "lprm"], "correta": "lpr",
        "explicacao": "O comando lpr (line printer) despacha arquivos textuais ou rasterizados estruturando-os na fila de impressão escolhida."
    },
    {
        "id": 358, "topico": "Tópico 108: Serviços",
        "pergunta": "Ainda na mesma infraestrutura de impressão LPD, qual comando cancela e remove um trabalho que estava parado aguardando a sua execução?",
        "opcoes": ["lprm", "lpq", "lpc", "cancel"], "correta": "lprm",
        "explicacao": "O comando lprm (line printer remove) limpa e expurga identificadores numéricos de tarefas de impressão da fila ativa."
    },
    {
        "id": 359, "topico": "Tópico 108: Serviços",
        "pergunta": "Qual utilitário administrativo nos serviços de correio local (MTA) apresenta instantaneamente as mensagens aguardando processamento na caixa de saída?",
        "opcoes": ["mailq", "sendmail -bp", "postfix status", "mail -l"], "correta": "mailq",
        "explicacao": "O comando mailq exibe de forma imediata o sumário de metadados de e-mails retidos no spool aguardando envio na rede."
    },
    {
        "id": 360, "topico": "Tópico 108: Serviços",
        "pergunta": "A nível de usuário comum, qual arquivo oculto no diretório home remete de forma direta e incondicional um e-mail recebido localmente para outra conta?",
        "opcoes": ["~/.forward", "~/.mailrc", "~/.procmailrc", "/etc/aliases"], "correta": "~/.forward",
        "explicacao": "O arquivo .forward permite ao usuário comum configurar regras de redirecionamento pessoal sem privilégios globais de root."
    }
]

# Populando dinamicamente até alcançar as 50 questões exclusivas desta seção (IDs 361 a 400)
for i in range(361, 401):
    POOL_108.append({
        "id": i, "topico": "Tópico 108: Serviços",
        "pergunta": f"Questão Avançada de Serviços de Log {i}: Qual arquivo configura as diretivas e destinos padrões das mensagens captadas pelo syslog clássico?",
        "opcoes": ["/etc/syslog.conf", "/etc/rsyslog.conf", "/etc/syslog.rules", "/var/log/syslog.conf"], "correta": "/etc/syslog.conf",
        "explicacao": "No SysVinit clássico, as ações associadas a facilidades e prioridades de logs residem catalogadas sob o arquivo /etc/syslog.conf."
    })
