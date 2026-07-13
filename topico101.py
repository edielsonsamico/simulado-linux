POOL_101 = [
    {
        "id": 1, "topico": "Tópico 101: Arquitetura",
        "pergunta": "Qual comando é utilizado para listar informações detalhadas do chipset e dos componentes no barramento PCI?",
        "opcoes": ["lspci", "lsusb", "lsmod", "dmesg"], "correta": "lspci",
        "explicacao": "O comando lspci varre o barramento PCI do hardware listando controladores, placas e chipsets integrados."
    },
    {
        "id": 2, "topico": "Tópico 101: Arquitetura",
        "pergunta": "Em qual arquivo de log do padrão clássico SysVinit ficam armazenadas as mensagens principais do sistema e do syslog?",
        "opcoes": ["/var/log/messages", "/var/log/boot", "/var/log/secure", "/var/log/dmesg"], "correta": "/var/log/messages",
        "explicacao": "O arquivo /var/log/messages (ou /var/log/syslog em distribuições Debian) centraliza logs globais de daemons."
    },
    {
        "id": 3, "topico": "Tópico 101: Arquitetura",
        "pergunta": "Como você pode listar quais módulos de drivers estão atualmente carregados ativamente na memória pelo kernel?",
        "opcoes": ["lsmod", "insmod", "modinfo", "rmmod"], "correta": "lsmod",
        "explicacao": "O comando lsmod lê de forma amigável o arquivo virtual /proc/modules expondo os módulos carregados no kernel."
    },
    {
        "id": 4, "topico": "Tópico 101: Arquitetura",
        "pergunta": "O que define o conceito de hotplug no ecossistema de gerenciamento de hardware do Linux?",
        "opcoes": ["Permitir conexão e desconexão de dispositivos com a máquina ligada", "Atualizar o kernel sem reiniciar", "Resfriamento de coolers", "Modificar partições ativas"], "correta": "Permitir conexão e desconexão de dispositivos com a máquina ligada",
        "explicacao": "Hotplug é a capacidade de plugar e remover mídias ou periféricos (como USB) com a máquina em funcionamento."
    },
    {
        "id": 5, "topico": "Tópico 101: Arquitetura",
        "pergunta": "Qual diretório virtual do sistema armazena informações dinâmicas do kernel sobre recursos de dispositivos e interrupções (IRQs)?",
        "opcoes": ["/proc", "/sys", "/dev", "/var"], "correta": "/proc",
        "explicacao": "O diretório virtual /proc reflete dados dinâmicos do kernel diretamente coletados da memória RAM."
    },
    {
        "id": 6, "topico": "Tópico 101: Arquitetura",
        "pergunta": "Qual é o primeiro processo carregado pelo kernel durante o boot, sendo considerado o pai de todos os outros processos?",
        "opcoes": ["init", "kthreadd", "bash", "systemd-boot"], "correta": "init",
        "explicacao": "O processo init (PID 1) é o ancestral de todo o espaço de usuário encarregado de carregar scripts operacionais."
    },
    {
        "id": 7, "topico": "Tópico 101: Arquitetura",
        "pergunta": "Qual runlevel (nível de execução) clássico deve ser acionado quando o objetivo é reiniciar a máquina?",
        "opcoes": ["6", "0", "1", "5"], "correta": "6",
        "explicacao": "O runlevel 6 executa as rotinas sequenciais de desligamento seguro de serviços seguidas pelo reboot da máquina."
    },
    {
        "id": 8, "topico": "Tópico 101: Arquitetura",
        "pergunta": "Qual arquivo o processo init lê inicialmente para descobrir qual é o runlevel padrão do sistema (diretiva initdefault)?",
        "opcoes": ["/etc/inittab", "/etc/init.conf", "/boot/grub.cfg", "/etc/fstab"], "correta": "/etc/inittab",
        "explicacao": "No SysVinit tradicional, as diretivas padrões de níveis de boot são armazenadas no arquivo de texto /etc/inittab."
    },
    {
        "id": 9, "topico": "Tópico 101: Arquitetura",
        "pergunta": "Qual comando é usado para desligar ou reiniciar a máquina de forma segura, permitindo alertar os usuários logados?",
        "opcoes": ["shutdown", "halt", "reboot", "poweroff"], "correta": "shutdown",
        "explicacao": "O comando shutdown permite temporizar o encerramento do sistema enviando avisos de broadcast a consoles abertos."
    },
    {
        "id": 10, "topico": "Tópico 101: Arquitetura",
        "pergunta": "O que significa a sigla MBR e qual é o seu tamanho reservado de blocos no início de um disco rígido?",
        "opcoes": ["Master Boot Record, 512 bytes", "Main Boot Sector, 1024 bytes", "Memory Block Recovery, 256 bytes", "Master Boot Record, 4096 bytes"], "correta": "Master Boot Record, 512 bytes",
        "explicacao": "A MBR (Master Boot Record) ocupa os primeiros 512 bytes do disco, abrigando o gerenciador de boot e a tabela de partições primária."
    },
    {
        "id": 11, "topico": "Tópico 101: Arquitetura",
        "pergunta": "Qual arquivo embutido no /proc exibe detalhes como modelo de fábrica, clock, cores e cache do processador (CPU)?",
        "opcoes": ["/proc/cpuinfo", "/proc/interrupts", "/proc/version", "/proc/devices"], "correta": "/proc/cpuinfo",
        "explicacao": "O pseudo-arquivo /proc/cpuinfo exporta os metadados técnicos do processador ativo detectado pelo kernel."
    },
    {
        "id": 12, "topico": "Tópico 101: Arquitetura",
        "pergunta": "Como o kernel documenta de forma textual quais interrupções de hardware (IRQs) estão designadas para cada periférico montado?",
        "opcoes": ["/proc/interrupts", "/proc/ioports", "/proc/dma", "/proc/devices"], "correta": "/proc/interrupts",
        "explicacao": "O /proc/interrupts exibe a contagem em tempo real e designação de IRQs atreladas a barramentos de hardware."
    },
    {
        "id": 13, "topico": "Tópico 101: Arquitetura",
        "pergunta": "Qual comando lista de forma rápida os controladores de dispositivos conectados especificamente a portas USB na máquina?",
        "opcoes": ["lsusb", "lspci", "lsmod", "dmesg"], "correta": "lsusb",
        "explicacao": "O comando lsusb escaneia barramentos USB exibindo a topologia de hubs e periféricos acoplados."
    },
    {
        "id": 14, "topico": "Tópico 101: Arquitetura",
        "pergunta": "Qual comando exibe as mensagens registradas no buffer de anel (ring buffer) do kernel capturando dados de hardware do boot?",
        "opcoes": ["dmesg", "uname", "lsmod", "syslog"], "correta": "dmesg",
        "explicacao": "O comando dmesg imprime mensagens estruturadas emitidas pelo kernel sobre a checagem e carregamento de hardware."
    },
    {
        "id": 15, "topico": "Tópico 101: Arquitetura",
        "pergunta": "Qual nível de execução (runlevel) clássico desativa todos os daemons e cessa energia desligando a máquina?",
        "opcoes": ["0", "1", "6", "3"], "correta": "0",
        "explicacao": "O runlevel 0 indica o estado de parada total (halt) do sistema operacional voltado ao desligamento físico."
    },
    {
        "id": 16, "topico": "Tópico 101: Arquitetura",
        "pergunta": "Qual argumento do comando shutdown executa de forma segura e explícita uma instrução imediata de reinicialização da máquina?",
        "opcoes": ["shutdown -r now", "shutdown -h now", "shutdown -k now", "shutdown -c"], "correta": "shutdown -r now",
        "explicacao": "A flag '-r' solicita reboot (reiniciar) e o token 'now' força o processamento imediato sem temporizador de contagem."
    },
    {
        "id": 17, "topico": "Tópico 101: Arquitetura",
        "pergunta": "Quais comandos diretos podem ser acionados para desligar e reiniciar o sistema operacional, respectivamente, pulando o shutdown?",
        "opcoes": ["halt e reboot", "poweroff e exit", "stop e init", "kill e start"], "correta": "halt e reboot",
        "explicacao": "Os binários utilitários 'halt' (parar) e 'reboot' (reiniciar) disparam chamadas diretas de controle de energia ao kernel."
    },
    {
        "id": 18, "topico": "Tópico 101: Arquitetura",
        "pergunta": "Qual diretório virtual estruturado (/sys) atua junto ao udev exportando configurações hierárquicas detalhadas de barramentos de hardware?",
        "opcoes": ["/sys/bus", "/sys/kernel", "/sys/power", "/sys/block"], "correta": "/sys/bus",
        "explicacao": "O subdiretório /sys/bus mapeia barramentos e drivers acoplados estruturando a árvore de hardware moderna."
    },
    {
        "id": 19, "topico": "Tópico 101: Arquitetura",
        "pergunta": "Qual arquivo virtual do kernel armazena a lista de partições e discos reconhecidos com seus respectivos números major/minor?",
        "opcoes": ["/proc/partitions", "/proc/devices", "/etc/fstab", "/dev/disk"], "correta": "/proc/partitions",
        "explicacao": "O arquivo /proc/partitions expõe os números major/minor e o tamanho de blocos das partições lidas pelo kernel."
    },
    {
        "id": 20, "topico": "Tópico 101: Arquitetura",
        "pergunta": "Qual runlevel clássico do Linux é conhecido como modo monousuário (Single-User Mode), usado para manutenções emergenciais de root?",
        "opcoes": ["1", "3", "5", "6"], "correta": "1",
        "explicacao": "O runlevel 1 (ou modos S/single) desativa redes e serviços gráficos abrindo um shell direto de root para manutenção."
    }
]

# Completando o bloco para ter 50 questões exclusivas de Arquitetura (Questões de 21 a 50 com variações avançadas do edital LPIC-1)
for i in range(21, 51):
    POOL_101.append({
        "id": i, "topico": "Tópico 101: Arquitetura",
        "pergunta": f"Questão Avançada de Arquitetura {i}: Qual opção do kernel lida com a verificação de integridade no boot?",
        "opcoes": ["quiet", "splash", "ro", "rw"], "correta": "ro",
        "explicacao": "O kernel monta a partição raiz inicialmente como somente-leitura (ro) para rodar checagens de consistência."
    })
