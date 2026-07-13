import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time

# Configuração da página do simulador
st.set_page_config(page_title="Linux Essentials - Treino e Simulado", page_icon="🐧", layout="wide")

# BANCO DE DADOS REVISADO - 30 QUESTÕES DA CERTIFICAÇÃO
QUESTOES_POOL = [
    {
        "id": 1, "topico": "Comandos Básicos", 
        "pergunta": "Qual comando é utilizado para listar os arquivos de um diretório exibindo permissões e donos?", 
        "opcoes": ["ls -l", "ls -a", "list -d", "show files"], "correta": "ls -l", 
        "explicacao": "O comando 'ls -l' ativa o formato de listagem longa, mostrando permissões, proprietário, grupo, tamanho e data."
    },
    {
        "id": 2, "topico": "Licenciamento", 
        "pergunta": "Qual das seguintes licenças garante que o código derivado continue sendo software livre?", 
        "opcoes": ["GPL", "BSD", "MIT", "Apache"], "correta": "GPL", 
        "explicacao": "A licença GPL possui a característica de 'copyleft', exigindo que trabalhos derivados também usem a GPL."
    },
    {
        "id": 3, "topico": "Permissões", 
        "pergunta": "Qual permissão octal corresponde aos acessos 'rwxr-xr-x'?", 
        "opcoes": ["755", "644", "777", "700"], "correta": "755", 
        "explicacao": "rwx = 7, r-x = 5, r-x = 5. Portanto, 755."
    },
    {
        "id": 4, "topico": "Diretórios", 
        "pergunta": "Em qual diretório do padrão FHS ficam armazenados os arquivos de configuração do sistema?", 
        "opcoes": ["/etc", "/var", "/bin", "/usr"], "correta": "/etc", 
        "explicacao": "O diretório /etc é reservado exclusivamente para arquivos de configuração estáticos do sistema operacional."
    },
    {
        "id": 5, "topico": "Processos", 
        "pergunta": "Qual comando envia o sinal padrão SIGTERM (15) para encerrar um processo através do seu PID?", 
        "opcoes": ["kill", "stop", "terminate", "ps -k"], "correta": "kill", 
        "explicacao": "O comando kill, quando executado apenas com o PID (ex: kill 1234), envia por padrão o sinal 15 (SIGTERM)."
    },
    {
        "id": 6, "topico": "FHS", 
        "pergunta": "Qual diretório armazena os arquivos de log do sistema e dados altamente variáveis?", 
        "opcoes": ["/var", "/tmp", "/opt", "/home"], "correta": "/var", 
        "explicacao": "O diretório /var (variable) guarda dados dinâmicos como filas de impressão, spools e logs do sistema (/var/log)."
    },
    {
        "id": 7, "topico": "Comandos de Texto", 
        "pergunta": "Qual comando é usado para exibir as primeiras 10 linhas de um arquivo de texto?", 
        "opcoes": ["head", "tail", "cat", "less"], "correta": "head", 
        "explicacao": "O comando 'head' exibe por padrão as primeiras 10 linhas. O 'tail' exibe as últimas 10."
    },
    {
        "id": 8, "topico": "Usuários e Grupos", 
        "pergunta": "Qual arquivo armazena as senhas criptografadas dos usuários no Linux por questões de segurança?", 
        "opcoes": ["/etc/shadow", "/etc/passwd", "/etc/secure", "/var/shadow"], "correta": "/etc/shadow", 
        "explicacao": "O arquivo /etc/passwd guarda dados públicos (UID, shell), enquanto as senhas cifradas ficam protegidas no /etc/shadow."
    },
    {
        "id": 9, "topico": "Redes", 
        "pergunta": "Qual utilitário envia pacotes ICMP ECHO_REQUEST para verificar a conectividade com um host remoto?", 
        "opcoes": ["ping", "ifconfig", "netstat", "route"], "correta": "ping", 
        "explicacao": "O 'ping' utiliza o protocolo ICMP para testar a comunicação direta e latência entre duas máquinas na rede."
    },
    {
        "id": 10, "topico": "Comandos de Arquivo", 
        "pergunta": "Qual comando cria um diretório vazio no Linux?", 
        "opcoes": ["mkdir", "newdir", "md", "create -d"], "correta": "mkdir", 
        "explicacao": "O comando 'mkdir' (make directory) é a ferramenta padrão POSIX para criação de novas pastas."
    },
    {
        "id": 11, "topico": "Comandos Básicos", 
        "pergunta": "Qual das seguintes opções do comando 'man' é utilizada para buscar páginas de manual contendo uma palavra-chave específica na sua descrição curta?", 
        "opcoes": ["man -k", "man -s", "man -d", "man -w"], "correta": "man -k", 
        "explicacao": "A opção 'man -k' (equivalente ao comando 'apropos') busca por palavras-chave em todas as descrições curtas das páginas de manual."
    },
    {
        "id": 12, "topico": "Diretórios e FHS", 
        "pergunta": "De acordo com o padrão FHS, onde ficam armazenados os arquivos binários essenciais de comando que podem ser utilizados por qualquer usuário do sistema?", 
        "opcoes": ["/bin", "/sbin", "/boot", "/root"], "correta": "/bin", 
        "explicacao": "O diretório '/bin' contém comandos básicos e essenciais executáveis por todos os usuários. Já o '/sbin' guarda executáveis administrativos exclusivos do root."
    },
    {
        "id": 13, "topico": "Permissões", 
        "pergunta": "Se um arquivo possui a permissão octal '640', quais são os acessos concedidos ao dono, ao grupo e aos outros usuários, respectivamente?", 
        "opcoes": ["rw-, r--, ---", "rwx, r--, ---", "rw-, rw-, r--", "r-x, r--, ---"], "correta": "rw-, r--, ---", 
        "explicacao": "6 corresponde a Read+Write (4+2); 4 corresponde a Read (4); 0 corresponde a nenhum acesso (0). Portanto: rw-, r--, ---."
    },
    {
        "id": 14, "topico": "Processos", 
        "pergunta": "Qual utilitário é utilizado para exibir a árvore hierárquica de processos ativos no sistema operacional, mostrando os processos pais e seus respectivos processos filhos?", 
        "opcoes": ["pstree", "ps -A", "top", "free"], "correta": "pstree", 
        "explicacao": "O comando 'pstree' mostra visualmente a estrutura de processos ativos no formato de ramificações ou árvores hierárquicas."
    },
    {
        "id": 15, "topico": "Gerenciamento de Pacotes", 
        "pergunta": "Em distribuições baseadas em Red Hat (como CentOS ou Fedora), qual utilitário moderno de terminal substituiu o antigo 'yum' para instalar pacotes RPM?", 
        "opcoes": ["dnf", "apt-get", "dpkg", "zypper"], "correta": "dnf", 
        "explicacao": "O 'dnf' (Dandified YUM) é o sucessor oficial do 'yum' nas distribuições Linux baseadas na árvore Red Hat."
    },
    {
        "id": 16, "topico": "Filtros de Texto", 
        "pergunta": "Qual comando utiliza expressões regulares para filtrar e exibir apenas as linhas de um arquivo que contenham um determinado padrão de texto?", 
        "opcoes": ["grep", "sed", "wc", "sort"], "correta": "grep", 
        "explicacao": "O comando 'grep' (Global Regular Expression Print) varre arquivos linha por linha procurando correspondências com expressões e padrões informados."
    },
    {
        "id": 17, "topico": "Segurança e Usuários", 
        "pergunta": "Qual é o identificador numérico de usuário (UID) padrão e obrigatório atribuído à conta do superusuário (root) no Linux?", 
        "opcoes": ["0", "1", "1000", "500"], "correta": "0", 
        "explicacao": "O usuário root sempre possui o UID igual a 0 no Linux, sendo este o marcador que concede privilégios totais de sistema."
    },
    {
        "id": 18, "topico": "Compactação de Arquivos", 
        "pergunta": "Qual extensão de arquivo indica que o pacote foi compactado utilizando o algoritmo do utilitário 'bzip2'?", 
        "opcoes": [".bz2", ".gz", ".xz", ".zip"], "correta": ".bz2", 
        "explicacao": "O comando 'bzip2' gera arquivos com a extensão '.bz2'. Ferramentas como o 'gzip' geram '.gz' e 'xz' geram arquivos '.xz'."
    },
    {
        "id": 19, "topico": "Variáveis de Ambiente", 
        "pergunta": "Qual variável de ambiente do Linux armazena a lista de diretórios onde o shell deve procurar pelos comandos executáveis digitados pelo usuário?", 
        "opcoes": ["PATH", "HOME", "SHELL", "USER"], "correta": "PATH", 
        "explicacao": "A variável '$PATH' dita os caminhos do sistema pesquisados em ordem quando um comando sem caminho absoluto é digitado."
    },
    {
        "id": 20, "topico": "Editores de Texto", 
        "pergunta": "No editor de texto 'vi' ou 'vim', qual tecla deve ser Hanna pressionada para alternar do modo de comandos para o modo de inserção de texto?", 
        "opcoes": ["i", "Esc", ":w", "q"], "correta": "i", 
        "explicacao": "A tecla 'i' (de insert) coloca o editor vi/vim no modo de inserção de texto. Para voltar ao modo de comandos, usa-se a tecla 'Esc'."
    },
    {
        "id": 21, "topico": "Redes", 
        "pergunta": "Qual dos seguintes arquivos locais do Linux é consultado primeiro para mapear nomes de domínios ou hosts para endereços IP estáticos?", 
        "opcoes": ["/etc/hosts", "/etc/resolv.conf", "/etc/networks", "/etc/hostname"], "correta": "/etc/hosts", 
        "explicacao": "O arquivo '/etc/hosts' funciona como uma tabela local de resolução de nomes que é consultada antes de servidores DNS externos."
    },
    {
        "id": 22, "topico": "Arquitetura e Hardware", 
        "pergunta": "Qual comando de terminal lê e formata mensagens do buffer de anel do kernel (ring buffer) para listar informações sobre dispositivos detectados na inicialização do sistema?", 
        "opcoes": ["dmesg", "lspci", "lsmod", "uname"], "correta": "dmesg", 
        "explicacao": "O comando 'dmesg' permite visualizar o histórico de eventos de baixo nível emitidos pelo kernel durante e após o carregamento do hardware."
    },
    {
        "id": 23, "topico": "Comandos de Manipulação", 
        "pergunta": "Qual opção do comando 'rm' permite forçar a remoção recursiva de diretórios cheios e seus arquivos sem solicitar confirmação visual ao usuário?", 
        "opcoes": ["rm -rf", "rm -d", "rm -ri", "rm -f"], "correta": "rm -rf", 
