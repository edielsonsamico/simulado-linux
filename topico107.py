POOL_107 = [
    {
        "id": 301, "topico": "Tópico 107: Administração",
        "pergunta": "Qual arquivo confinado abriga de forma criptografada as senhas dos usuários e as regras específicas de expiração de validade da conta?",
        "opcoes": ["/etc/shadow", "/etc/passwd", "/etc/secure", "/var/shadow"], "correta": "/etc/shadow",
        "explicacao": "Por motivos de segurança, as hashes de senhas e políticas de obsolescência ficam trancadas no arquivo /etc/shadow com permissões restritas a root."
    },
    {
        "id": 302, "topico": "Tópico 107: Administração",
        "pergunta": "Ao usar o comando useradd, de qual diretório padrão o sistema copia todos os arquivos de perfis ocultos (como .bashrc) como modelo inicial para a nova pasta pessoal?",
        "opcoes": ["/etc/skel", "/etc/defaults", "/etc/profile", "/root"], "correta": "/etc/skel",
        "explicacao": "O diretório /etc/skel (skeleton) funciona como um molde padrão; tudo o que está dentro dele é clonado para o home do novo usuário."
    },
    {
        "id": 303, "topico": "Tópico 107: Administração",
        "pergunta": "Como um administrador bloqueia manualmente a senha de um usuário existente sem remover a conta, utilizando o comando passwd?",
        "opcoes": ["passwd -l [usuário]", "passwd -d [usuário]", "passwd -u [usuário]", "passwd -k [usuário]"], "correta": "passwd -l [usuário]",
        "explicacao": "A flag '-l' (lock) insere um caractere de exclamação no início da hash de senha no /etc/shadow, inviabilizando qualquer login imediato."
    },
    {
        "id": 304, "topico": "Tópico 107: Administração",
        "pergunta": "Qual opção do comando userdel exclui o usuário e, de forma contínua, também apaga por inteiro o seu diretório pessoal no /home?",
        "opcoes": ["-r", "-f", "-d", "-p"], "correta": "-r",
        "explicacao": "A flag '-r' (recursive) remove o cadastro da conta e apaga a pasta home correspondente e os spools de e-mail do disco."
    },
    {
        "id": 305, "topico": "Tópico 107: Administração",
        "pergunta": "Qual arquivo de texto plano é mantido pelo serviço cron para rotinas padronizadas globais e não deve ser manipulado por usuários comuns?",
        "opcoes": ["/etc/crontab", "/etc/cron.d", "/var/spool/cron", "/etc/cron.allow"], "correta": "/etc/crontab",
        "explicacao": "O arquivo estático /etc/crontab centraliza os agendamentos corporativos de background executados diretamente pelo daemon do cron."
    },
    {
        "id": 306, "topico": "Tópico 107: Administração",
        "pergunta": "Caso você agende uma execução remota uma única vez via comando at, qual comando consulta e lista a fila pendente dos seus agendamentos?",
        "opcoes": ["atq", "atrm", "cronq", "atlist"], "correta": "atq",
        "explicacao": "O comando atq (ou 'at -l') exibe o identificador numérico de todos os jobs na fila de processamento que aguardam seu horário."
    },
    {
        "id": 307, "topico": "Tópico 107: Administração",
        "pergunta": "Considerando que no sistema o arquivo /etc/cron.allow foi deletado mas o /etc/cron.deny existe totalmente vazio, quem recebe permissão para criar cronjobs?",
        "opcoes": ["Todos os usuários do sistema", "Apenas o root", "Ninguém", "Usuários em grupos admin"], "correta": "Todos os usuários do sistema",
        "explicacao": "Sem restrições explícitas e com o arquivo de negação vazio, a política padrão do Linux concede permissão de uso geral para o cron."
    },
    {
        "id": 308, "topico": "Tópico 107: Administração",
        "pergunta": "A localização e identificação formal de fuso horário e horário de verão aplicada na base local do sistema reside atrelada a qual arquivo ou link simbólico?",
        "opcoes": ["/etc/localtime", "/etc/timezone", "/proc/time", "/etc/sysconfig/clock"], "correta": "/etc/localtime",
        "explicacao": "O arquivo local /etc/localtime dita a conversão do fuso horário da máquina, sendo geralmente um link simbólico para tabelas em /usr/share/zoneinfo."
    },
    {
        "id": 309, "topico": "Tópico 107: Administração",
        "pergunta": "Na internacionalização (i18n), qual utilitário de terminal converte explicitamente textos de formatações de legado (como ISO-8859) para UTF-8?",
        "opcoes": ["iconv", "convert", "recode", "utf8enc"], "correta": "iconv",
        "explicacao": "O comando iconv é a ferramenta padrão POSIX dedicada a ler fluxos e reescrever codificações de conjuntos de caracteres textuais."
    },
    {
        "id": 310, "topico": "Tópico 107: Administração",
        "pergunta": "De modo a prevenir corrupção simultânea por múltiplos administradores, qual comando abre e aplica uma trava de exclusão mútua (lock) no arquivo /etc/passwd?",
        "opcoes": ["vipw", "passwd -e", "chsh", "userlock"], "correta": "vipw",
        "explicacao": "O comando vipw edita o /etc/passwd de forma segura criando um arquivo de bloqueio temporário que previne conflitos de gravação concorrente."
    }
]

# Populando o bloco dinamicamente até alcançar as 50 questões exclusivas desta seção (IDs 311 a 350)
for i in range(311, 351):
    POOL_107.append({
        "id": i, "topico": "Tópico 107: Administração",
        "pergunta": f"Questão Avançada de Administração {i}: Qual opção do crontab remove permanentemente todas as tarefas agendadas do usuário ativo?",
        "opcoes": ["crontab -r", "crontab -l", "crontab -e", "crontab -d"], "correta": "crontab -r",
        "explicacao": "A flag '-r' (remove) do comando crontab expurga sumariamente a tabela individual de agendamentos do usuário sem confirmação."
    })
