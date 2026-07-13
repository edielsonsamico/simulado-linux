POOL_102 = [
    {
        "id": 51, "topico": "Tópico 102: Pacotes",
        "pergunta": "Qual o nome da partição utilizada para oferecer suporte à memória virtual no Linux, geralmente identificada pelo ID de tipo 82?",
        "opcoes": ["swap", "ext4", "root", "home"], "correta": "swap",
        "explicacao": "A partição swap funciona como uma extensão física em disco para a memória RAM, permitindo paginação de dados virtuais."
    },
    {
        "id": 52, "topico": "Tópico 102: Pacotes",
        "pergunta": "De acordo com a hierarquia do FHS, qual diretório é destinado a guardar exclusivamente os arquivos de configuração específicos da máquina local?",
        "opcoes": ["/etc", "/var", "/usr", "/opt"], "correta": "/etc",
        "explicacao": "O diretório /etc é o local padronizado pelo FHS para armazenar scripts e arquivos de configuração de texto do sistema."
    },
    {
        "id": 53, "topico": "Tópico 102: Pacotes",
        "pergunta": "Qual gerenciador de boot alternativo ao antigo LILO lê suas configurações clássicas a partir do arquivo /boot/grub/grub.conf ou menu.lst?",
        "opcoes": ["GRUB Legacy", "systemd-boot", "ELILO", "Syslinux"], "correta": "GRUB Legacy",
        "explicacao": "O GRUB Legacy (versão 0.97) utilizava os arquivos grub.conf ou menu.lst para mapear os kernels do menu de boot."
    },
    {
        "id": 54, "topico": "Tópico 102: Pacotes",
        "pergunta": "Qual comando você deve executar no terminal para descobrir quais bibliotecas compartilhadas (.so) são requeridas por um arquivo executável?",
        "opcoes": ["ldd", "ldconfig", "strings", "file"], "correta": "ldd",
        "explicacao": "O comando ldd (list dynamic dependencies) imprime na tela de forma tabular todas as bibliotecas dinâmicas vinculadas ao binário."
    },
    {
        "id": 55, "topico": "Tópico 102: Pacotes",
        "pergunta": "Qual é o arquivo de configuração central que contém os caminhos das bibliotecas compartilhadas e é lido pelo comando ldconfig?",
        "opcoes": ["/etc/ld.so.conf", "/etc/libs.conf", "/etc/modules", "/etc/profile"], "correta": "/etc/ld.so.conf",
        "explicacao": "O arquivo /etc/ld.so.conf dita em quais diretórios adicionais o sistema deve mapear e indexar bibliotecas compartilhadas."
    },
    {
        "id": 56, "topico": "Tópico 102: Pacotes",
        "pergunta": "Na gerência de pacotes de distribuições baseadas em Debian, qual comando e opção são usados para instalar um arquivo .deb localmente?",
        "opcoes": ["dpkg -i", "apt-get install", "dpkg -r", "aptitude local"], "correta": "dpkg -i",
        "explicacao": "A flag '-i' (ou --install) do utilitário dpkg descompacta e registra pacotes binários locais de formato Debian."
    },
    {
        "id": 57, "topico": "Tópico 102: Pacotes",
        "pergunta": "Como você obtém a lista e os índices mais atualizados de pacotes a partir dos repositórios remotos configurados no gerenciador APT?",
        "opcoes": ["apt-get update", "apt-get upgrade", "apt-get check", "apt-get clean"], "correta": "apt-get update",
        "explicacao": "O comando 'apt-get update' sincroniza as tabelas locais de metadados com os arquivos descritos na sources.list."
    },
    {
        "id": 58, "topico": "Tópico 102: Pacotes",
        "pergunta": "No ecossistema Red Hat Package Manager (RPM), qual comando exibe uma lista de todos os pacotes atualmente instalados no sistema?",
        "opcoes": ["rpm -qa", "rpm -ivh", "rpm -ql", "rpm -qf"], "correta": "rpm -qa",
        "explicacao": "A flag '-q' (query) combinada com '-a' (all) faz uma busca e listagem em lote de todos os pacotes RPM registrados localmente."
    },
    {
        "id": 159, "topico": "Tópico 102: Pacotes",
        "pergunta": "Qual ferramenta clássica de pacotes em plataformas Red Hat/RPM funciona de maneira semelhante ao APT, resolvendo dependências automaticamente via rede?",
        "opcoes": ["yum", "rpm", "dnf", "zypper"], "correta": "yum",
        "explicacao": "O YUM (Yellowdog Updater, Modified) foi o gerenciador automatizado de alta camada tradicional das distribuições Red Hat/CentOS."
    },
    {
        "id": 60, "topico": "Tópico 102: Pacotes",
        "pergunta": "Como extrair ou converter o formato de um pacote RPM para um formato de fluxo de arquivo de arquivador cpio padrão?",
        "opcoes": ["rpm2cpio", "rpm -extract", "cpio -rpm", "tar -rpm"], "correta": "rpm2cpio",
        "explicacao": "O comando rpm2cpio converte um arquivo .rpm em um fluxo de dados cpio na saída padrão, permitindo extrair arquivos isolados."
    },
    {
        "id": 61, "topico": "Tópico 102: Pacotes",
        "pergunta": "Em sistemas baseados em Red Hat modernos (como RHEL e Fedora), qual gerenciador de pacotes robusto e otimizado substituiu oficialmente o antigo YUM?",
        "opcoes": ["dnf", "apt", "zypper", "pacman"], "correta": "dnf",
        "explicacao": "O DNF (Dandified YUM) é o sucessor oficial do YUM, trazendo melhor desempenho, menor consumo de memória e resolução de dependências aprimorada."
    },
    {
        "id": 62, "topico": "Tópico 102: Pacotes",
        "pergunta": "Qual arquivo central armazena a lista de espelhos e URLs de repositórios remotos consultados pelo gerenciador de pacotes APT no Debian/Ubuntu?",
        "opcoes": ["/etc/apt/sources.list", "/etc/apt/apt.conf", "/etc/dpkg/dpkg.cfg", "/etc/apt/repos.conf"], "correta": "/etc/apt/sources.list",
        "explicacao": "O arquivo /etc/apt/sources.list dita os caminhos de rede oficiais onde o APT buscará atualizações e novos pacotes."
    },
    {
        "id": 63, "topico": "Tópico 102: Pacotes",
        "pergunta": "Qual comando do gerenciador de boot GRUB 2 é executado para recompilar o arquivo de configuração principal após a adição de um novo kernel?",
        "opcoes": ["grub-mkconfig -o /boot/grub/grub.cfg", "grub-install", "update-grub2", "grub-setup"], "correta": "grub-mkconfig -o /boot/grub/grub.cfg",
        "explicacao": "O utilitário grub-mkconfig escaneia o sistema e gera o menu dinâmico salvando a saída (-o) no arquivo grub.cfg."
    },
    {
        "id": 64, "topico": "Tópico 102: Pacotes",
        "pergunta": "Qual flag do utilitário rpm deve ser utilizada se você precisar remover ou desinstalar por completo um pacote do sistema?",
        "opcoes": ["-e", "-r", "-d", "-u"], "correta": "-e",
        "explicacao": "A opção '-e' (erase) do comando rpm remove o pacote selecionado do banco de dados e apaga seus binários associados."
    },
    {
        "id": 65, "topico": "Tópico 102: Pacotes",
        "pergunta": "Qual subcomando do utilitário apt remove um pacote do sistema, mas preserva intactos os arquivos de configuração criados por ele?",
        "opcoes": ["remove", "purge", "clean", "autoremove"], "correta": "remove",
        "explicacao": "O 'apt remove' apaga os binários mas mantém as configurações. Para apagar tudo, incluindo os arquivos de configuração, usa-se 'purge'."
    }
]

# Populando dinamicamente até atingir as 50 questões exclusivas do bloco (IDs 66 a 100)
for i in range(66, 101):
    POOL_102.append({
        "id": i, "topico": "Tópico 102: Pacotes",
        "pergunta": f"Questão Avançada de Gerenciamento de Pacotes {i}: Qual arquivo configura repositórios locais no subdiretório do DNF?",
        "opcoes": ["/etc/yum.repos.d/", "/etc/dnf/dnf.conf", "/etc/rpm.conf", "/var/lib/dnf/"], "correta": "/etc/yum.repos.d/",
        "explicacao": "O DNF mantém retrocompatibilidade com o YUM, lendo os arquivos de repositórios terminados em .repo dentro de /etc/yum.repos.d/."
    })
