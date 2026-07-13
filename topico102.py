POOL_102 = [
    {
        "id": 11, "topico": "Tópico 102: Pacotes",
        "pergunta": "Qual o nome da partição utilizada para oferecer suporte à memória virtual no Linux, geralmente identificada pelo ID de tipo 82?",
        "opcoes": ["swap", "ext4", "root", "home"], "correta": "swap",
        "explicacao": "A partição swap funciona como uma extensão física em disco para a memória RAM, permitindo paginação de dados virtuais."
    },
    {
        "id": 12, "topico": "Tópico 102: Pacotes",
        "pergunta": "De acordo com a hierarquia do FHS, qual diretório é destinado a guardar exclusivamente os arquivos de configuração específicos da máquina local?",
        "opcoes": ["/etc", "/var", "/usr", "/opt"], "correta": "/etc",
        "explicacao": "O diretório /etc é o local padronizado pelo FHS para armazenar scripts e arquivos de configuração de texto do sistema."
    },
    {
        "id": 13, "topico": "Tópico 102: Pacotes",
        "pergunta": "Qual gerenciador de boot alternativo ao antigo LILO lê suas configurações clássicas a partir do arquivo /boot/grub/grub.conf ou menu.lst?",
        "opcoes": ["GRUB Legacy", "systemd-boot", "ELILO", "Syslinux"], "correta": "GRUB Legacy",
        "explicacao": "O GRUB Legacy (versão 0.97) utilizava os arquivos grub.conf ou menu.lst para mapear os kernels do menu de boot."
    },
    {
        "id": 14, "topico": "Tópico 102: Pacotes",
        "pergunta": "Qual comando você deve executar no terminal para descobrir quais bibliotecas compartilhadas (.so) são requeridas por um arquivo executável?",
        "opcoes": ["ldd", "ldconfig", "strings", "file"], "correta": "ldd",
        "explicacao": "O comando ldd (list dynamic dependencies) imprime na tela de forma tabular todas as bibliotecas dinâmicas vinculadas ao binário."
    },
    {
        "id": 15, "topico": "Tópico 102: Pacotes",
        "pergunta": "Qual é o arquivo de configuração central que contém os caminhos das bibliotecas compartilhadas e é lido pelo comando ldconfig?",
        "opcoes": ["/etc/ld.so.conf", "/etc/libs.conf", "/etc/modules", "/etc/profile"], "correta": "/etc/ld.so.conf",
        "explicacao": "O arquivo /etc/ld.so.conf dita em quais diretórios adicionais o sistema deve mapear e indexar bibliotecas compartilhadas."
    },
    {
        "id": 16, "topico": "Tópico 102: Pacotes",
        "pergunta": "Na gerência de pacotes de distribuições baseadas em Debian, qual comando e opção são usados para instalar um arquivo .deb localmente?",
        "opcoes": ["dpkg -i", "apt-get install", "dpkg -r", "aptitude local"], "correta": "dpkg -i",
        "explicacao": "A flag '-i' (ou --install) do utilitário dpkg descompacta e registra pacotes binários locais de formato Debian."
    },
    {
        "id": 17, "topico": "Tópico 102: Pacotes",
        "pergunta": "Como você obtém a lista e os índices mais atualizados de pacotes a partir dos repositórios remotos configurados no gerenciador APT?",
        "opcoes": ["apt-get update", "apt-get upgrade", "apt-get check", "apt-get clean"], "correta": "apt-get update",
        "explicacao": "O comando 'apt-get update' sincroniza as tabelas locais de metadados com os arquivos descritos na sources.list."
    },
    {
        "id": 18, "topico": "Tópico 102: Pacotes",
        "pergunta": "No ecossistema Red Hat Package Manager (RPM), qual comando exibe uma lista de todos os pacotes atualmente instalados no sistema?",
        "opcoes": ["rpm -qa", "rpm -ivh", "rpm -ql", "rpm -qf"], "correta": "rpm -qa",
        "explicacao": "A flag '-q' (query) combinada com '-a' (all) faz uma busca e listagem em lote de todos os pacotes RPM registrados localmente."
    },
    {
        "id": 19, "topico": "Tópico 102: Pacotes",
        "pergunta": "Qual ferramenta de pacotes em plataformas Red Hat/RPM funciona de maneira semelhante ao APT, resolvendo dependências automaticamente via rede?",
        "opcoes": ["yum", "rpm", "dnf", "zypper"], "correta": "yum",
        "explicacao": "O YUM (Yellowdog Updater, Modified) foi o gerenciador automatizado de alta camada tradicional das distribuições Red Hat/CentOS."
    },
    {
        "id": 20, "topico": "Tópico 102: Pacotes",
        "pergunta": "Como extrair ou converter o formato de um pacote RPM para um formato de fluxo de arquivo de arquivador cpio padrão?",
        "opcoes": ["rpm2cpio", "rpm -extract", "cpio -rpm", "tar -rpm"], "correta": "rpm2cpio",
        "explicacao": "O comando rpm2cpio converte um arquivo .rpm em um fluxo de dados cpio na saída padrão, permitindo extrair arquivos isolados."
    }
]
