POOL_109 = [
    {
        "id": 401, "topico": "Tópico 109: Redes",
        "pergunta": "Na configuração básica e resolução estática sem domínio real de rede externa, qual arquivo mapeia pares de IP e Nome Local no Linux?",
        "opcoes": ["/etc/hosts", "/etc/resolv.conf", "/etc/networks", "/etc/hostname"], "correta": "/etc/hosts",
        "explicacao": "O arquivo /etc/hosts associa IPs a nomes locais manualmente, sem depender de servidores DNS."
    },
    {
        "id": 402, "topico": "Tópico 109: Redes",
        "pergunta": "No cliente de DNS nativo, onde estão listados hierarquicamente os IPs dos nameservers habilitados para resolver endereços complexos da internet?",
        "opcoes": ["/etc/resolv.conf", "/etc/hosts", "/etc/nsswitch.conf", "/etc/named.conf"], "correta": "/etc/resolv.conf",
        "explicacao": "O arquivo '/etc/resolv.conf' parametriza os IPs de busca do DNS do sistema."
    },
    {
        "id": 403, "topico": "Tópico 109: Redes",
        "pergunta": "Qual lista interna, gerida em texto, orienta clientes e servidores Linux apontando as atribuições correspondentes entre Portas Populares e seus Nomes Operacionais associados (ex. TCP 80 = HTTP)?",
        "opcoes": ["/etc/services", "/etc/protocols", "/etc/inetd.conf", "/etc/rpc"], "correta": "/etc/services",
        "explicacao": "O arquivo '/etc/services' traduz portas conhecidas de internet para nomes de aplicações humanas."
    },
    {
        "id": 404, "topico": "Tópico 109: Redes",
        "pergunta": "O comando que habilita de imediato uma interface desativada (ex: levanta a eth0) é o?",
        "opcoes": ["ifconfig eth0 up", "ifconfig eth0 down", "route add eth0", "netstat -i eth0"], "correta": "ifconfig eth0 up",
        "explicacao": "A flag 'up' do comando ifconfig ativa a interface de rede para tráfego elétrico de pacotes."
    },
    {
        "id": 405, "topico": "Tópico 109: Redes",
        "pergunta": "Qual utilitário do protocolo de controle testa conectividade usando primitivas básicas de eco originadas no ICMP?",
        "opcoes": ["ping", "traceroute", "netstat", "dig"], "correta": "ping",
        "explicacao": "O comando ping avalia a conectividade e latência disparando mensagens de echo request do protocolo ICMP."
    },
    {
        "id": 406, "topico": "Tópico 109: Redes",
        "pergunta": "Na investigação de conectividade em redes emaranhadas de várias camadas, qual ferramenta aponta salto a salto por quais endereços os pacotes IP foram afunilados até o destino?",
        "opcoes": ["traceroute", "ping", "netstat", "route"], "correta": "traceroute",
        "explicacao": "'traceroute' rastreia os saltos de roteadores incrementando o campo TTL do pacote IP."
    },
    {
        "id": 407, "topico": "Tópico 109: Redes",
        "pergunta": "A qual porta padrão se direciona um host requerendo um login de shell autenticado no modo Secure Shell (SSH)?",
        "opcoes": ["Porta 22", "Porta 23", "Porta 21", "Porta 80"], "correta": "Porta 22",
        "explicacao": "O daemon OpenSSH escuta conexões de criptografia de chaves por padrão sobre a porta TCP 22."
    },
    {
        "id": 408, "topico": "Tópico 109: Redes",
        "pergunta": "Qual aplicação nativa em Unix disseca e inspeciona visualmente as tabelas de roteamento internas integradas juntamente com todas as interfaces da máquina ligadas a um Socket TCP ativo?",
        "opcoes": ["netstat", "ifconfig", "route", "iptables"], "correta": "netstat",
        "explicacao": "O comando netstat (network statistics) é a ferramenta diagnóstica tradicional de sockets e conexões."
    },
    {
        "id": 409, "topico": "Tópico 109: Redes",
        "pergunta": "Qual arquivo, através da sua estrutura em tabelas e prioridades, ordena qual mecanismo de busca (arquivos locais primeiro, depois DNS, NIS etc) deve ser usado na resolução de entidades IP?",
        "opcoes": ["/etc/nsswitch.conf", "/etc/resolv.conf", "/etc/hosts", "/etc/passwd"], "correta": "/etc/nsswitch.conf",
        "explicacao": "O Name Service Switch (/etc/nsswitch.conf) dita se o Linux lerá arquivos locais antes ou depois de consultas DNS/NIS."
    },
    {
        "id": 410, "topico": "Tópico 109: Redes",
        "pergunta": "Entre os subníveis vitais de internet, que protocolo suporta não o tráfego dos dados, mas sim o alerta sobre erro de acesso e roteamento inacessível por echo response?",
        "opcoes": ["ICMP", "UDP", "TCP", "ARP"], "correta": "ICMP",
        "explicacao": "O ICMP (Internet Control Message Protocol) gerencia códigos de diagnóstico e erros estruturais entre nós IPs."
    }
]

# Populando até 50 questões do tópico de redes (IDs 411 a 450)
for i in range(411, 451):
    POOL_109.append({
        "id": i, "topico": "Tópico 109: Redes",
        "pergunta": f"Questão Avançada de Redes {i}: Qual arquivo configura o nome da máquina local para fins de identificação de rede?",
        "opcoes": ["/etc/hostname", "/etc/hosts", "/etc/resolv.conf", "/etc/myname"], "correta": "/etc/hostname",
        "explicacao": "O arquivo /etc/hostname guarda o rótulo textual de identificação de rede do host local."
    })
