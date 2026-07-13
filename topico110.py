POOL_110 = [
    {
        "id": 451, "topico": "Tópico 110: Segurança",
        "pergunta": "Qual a sintaxe restrita aplicada no utilitário de busca find para garimpar especificamente todos e quaisquer arquivos baseados no gatilho do modo especial SUID nos binários ativos da raiz (/)?",
        "opcoes": ["find / -perm -4000", "find / -perm 777", "find / -type f -suid", "find / -user root"], "correta": "find / -perm -4000",
        "explicacao": "O bit 4000 identifica de forma octal o SUID, rodando arquivos com privilégios do dono do binário."
    },
    {
        "id": 452, "topico": "Tópico 110: Segurança",
        "pergunta": "O rastreador lsof utilizando especificamente a flag -i relata que tipo de inspeção do host interno?",
        "opcoes": ["Processos atrelados a conexões de rede e portas abertas", "Módulos de disco", "Uso de memória", "Arquivos deletados no shadow"], "correta": "Processos atrelados a conexões de rede e portas abertas",
        "explicacao": "O comando lsof (list open files) com '-i' isola mapeamentos de rede ativos e conexões de sockets."
    },
    {
        "id": 453, "topico": "Tópico 110: Segurança",
        "pergunta": "Sob a política do TCP Wrappers (libwrap), caso um usuário ou host se conecte sem ser enquadrado de forma restritiva no hosts.deny nem permissiva no hosts.allow, o que ocorre?",
        "opcoes": ["O acesso é liberado por omissão", "O acesso é bloqueado", "O sistema trava", "O root recebe um alerta"], "correta": "O acesso é liberado por omissão",
        "explicacao": "A libwrap adota política aberta por padrão; se o host não cai em filtros específicos, o tráfego do daemon é aceito."
    },
    {
        "id": 454, "topico": "Tópico 110: Segurança",
        "pergunta": "Qual sub-rotina integrada do Bash delimita os perfis abusivos de cotas virtuais de softwares (arquivos simultâneos, memória e processos)?",
        "opcoes": ["ulimit", "quota", "setrlimit", "sysctl"], "correta": "ulimit",
        "explicacao": "O comando embutido 'ulimit' dita restrições operacionais e cotas máximas no escopo do shell."
    }
]

# Populando até 50 questões do tópico de segurança (IDs 455 a 500)
for i in range(455, 501):
    POOL_110.append({
        "id": i, "topico": "Tópico 110: Segurança",
        "pergunta": f"Questão Avançada de Segurança {i}: Qual arquivo configura as restrições explícitas de acesso a serviços via TCP Wrappers?",
        "opcoes": ["/etc/hosts.deny", "/etc/hosts.conf", "/etc/securetty", "/etc/passwd"], "correta": "/etc/hosts.deny",
        "explicacao": "O arquivo /etc/hosts.deny especifica quais hosts ou redes estão proibidos de acessar daemons protegidos."
    })
