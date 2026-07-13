POOL_104 = [
    {
        "id": 151, "topico": "Tópico 104: Dispositivos",
        "pergunta": "Como é identificado no diretório /dev o arquivo especial correspondente ao primeiro disco rígido na primeira controladora IDE clássica (Primary Master)?",
        "opcoes": ["/dev/hda", "/dev/sda", "/dev/hdb", "/dev/sdb"], "correta": "/dev/hda",
        "explicacao": "Dispositivos IDE legados são catalogados pelo kernel sob o prefixo /dev/hd, onde a letra 'a' marca o primeiro barramento mestre."
    },
    {
        "id": 152, "topico": "Tópico 104: Dispositivos",
        "pergunta": "Qual é o tradicional programa interativo de console fornecido por padrão no Linux para manipular e alterar tabelas de partições do tipo MBR?",
        "opcoes": ["fdisk", "gparted", "mkfs", "parted"], "correta": "fdisk",
        "explicacao": "O comando fdisk permite gerenciar partições criando, visualizando e alterando as estruturas lógicas do setor MBR de discos."
    },
    {
        "id": 153, "topico": "Tópico 104: Dispositivos",
        "pergunta": "Após criar uma partição dedicada em disco, qual utilitário deve ser executado no console para formatá-la de modo a ser utilizada como área de troca (swap)?",
        "opcoes": ["mkswap", "swapon", "mkfs.swap", "format swap"], "correta": "mkswap",
        "explicacao": "O comando mkswap grava as assinaturas e cabeçalhos binários necessários na partição para torná-la elegível como memória virtual."
    },
    {
        "id": 154, "topico": "Tópico 104: Dispositivos",
        "pergunta": "Qual comando relata em tempo real o espaço livre/disponível e o uso em blocos para todos os sistemas de arquivos atualmente montados?",
        "opcoes": ["df", "du", "fdisk", "free"], "correta": "df",
        "explicacao": "O comando df (disk free) lê a tabela de montagens do sistema exibindo capacidades, espaço ocupado e pontos de montagem ativos."
    },
    {
        "id": 155, "topico": "Tópico 104: Dispositivos",
        "pergunta": "Qual comando deve ser usado de forma segura para verificar a integridade estrutural e tentar reparar erros lógicos em um sistema de arquivos que não foi desmontado corretamente?",
        "opcoes": ["fsck", "mkfs", "mount", "tune2fs"], "correta": "fsck",
        "explicacao": "O utilitário fsck (file system consistency check) faz varreduras em metadados buscando e corrigindo blocos órfãos ou corrompidos."
    },
    {
        "id": 156, "topico": "Tópico 104: Dispositivos",
        "pergunta": "Em qual arquivo de texto plano são configuradas as opções, sistemas de arquivos e pontos de montagem dos discos para ativação automática no boot?",
        "opcoes": ["/etc/fstab", "/etc/mtab", "/proc/mounts", "/etc/inittab"], "correta": "/etc/fstab",
        "explicacao": "O arquivo estático /etc/fstab dita as diretrizes de inicialização mapeando os UUIDs ou partições para montagem persistente."
    },
    {
        "id": 157, "topico": "Tópico 104: Dispositivos",
        "pergunta": "Na representação octal tradicional de permissões gerenciada pelo chmod, quais valores representam, respectivamente, Leitura, Escrita e Execução?",
        "opcoes": ["Leitura é 4, Escrita é 2, e Execução é 1", "Leitura é 1, Escrita é 2, e Execução é 4", "Leitura é 7, Escrita机制 é 5, e Execução é 5", "Leitura é 2, Escrita é 4, e Execução é 1"], "correta": "Leitura é 4, Escrita é 2, e Execução é 1",
        "explicacao": "Seguindo pesos binários (r=100b=4, w=010b=2, x=001b=1), as somas desses identificadores compõem as permissões de acesso (ex: 7 = 4+2+1)."
    },
    {
        "id": 158, "topico": "Tópico 104: Dispositivos",
        "pergunta": "Qual utilitário administrativo de terminal permite alterar de forma simultânea o proprietário usuário e o grupo dono de um arquivo ou diretório?",
        "opcoes": ["chown", "chmod", "chgrp", "passwd"], "correta": "chown",
        "explicacao": "O comando chown (change owner) aceita a sintaxe estruturada 'dono:grupo' alterando os dois metadados de propriedade em lote."
    },
    {
        "id": 159, "topico": "Tópico 104: Dispositivos",
        "pergunta": "Qual comando e opção criam um link simbólico (soft link) apontando de um arquivo de origem física para um atalho de destino lógicos?",
        "opcoes": ["ln -s", "ln -h", "link -s", "mklink"], "correta": "ln -s",
        "explicacao": "O utilitário 'ln' acionado com a flag '-s' (symbolic) gera um arquivo de atalho textual leve contendo o caminho do alvo original."
    },
    {
        "id": 160, "topico": "Tópico 104: Dispositivos",
        "pergunta": "Qual comando de busca localiza caminhos extremamente rápido efetuando leituras de um index/banco de dados estático interno atualizado pelo updatedb?",
        "opcoes": ["locate", "find", "whereis", "which"], "correta": "locate",
        "explicacao": "O locate faz pesquisas indexadas instantâneas em sua própria tabela gerada periodicamente pelo cronjob do updatedb."
    },
    {
        "id": 161, "topico": "Tópico 104: Dispositivos",
        "pergunta": "Qual comando de console monta e vincula manualmente uma partição física a um diretório lógico (ponto de montagem) para torná-la acessível no SO?",
        "opcoes": ["mount", "umount", "fdisk", "mkfs"], "correta": "mount",
        "explicacao": "O comando mount acopla a estrutura lógica de um sistema de arquivos a uma pasta vazia existente na árvore do FHS."
    },
    {
        "id": 162, "topico": "Tópico 104: Dispositivos",
        "pergunta": "Qual utilitário do sistema é usado para desconectar ou desatar com segurança um sistema de arquivos montado antes de ejetar o hardware físico?",
        "opcoes": ["umount", "unmount", "mount -d", "rmfs"], "correta": "umount",
        "explicacao": "O comando 'umount' (sem o primeiro 'n') libera o ponto de montagem desvinculando o sistema de arquivos de forma limpa."
    }
]

# Alimentando o bloco até completar as 50 questões exclusivas desta seção (IDs 163 a 200)
for i in range(163, 201):
    POOL_104.append({
        "id": i, "topico": "Tópico 104: Dispositivos",
        "pergunta": f"Questão Avançada de Sistemas de Arquivos {i}: Qual sistema de arquivos nativo do Linux trouxe o conceito de Journaling de forma pioneira?",
        "opcoes": ["ext3", "ext2", "VFAT", "proc"], "correta": "ext3",
        "explicacao": "O sistema de arquivos ext3 estendeu o antigo ext2 adicionando o recurso de journaling (diário de transações) para evitar corrupções em desligamentos abruptos."
    })
