import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time

# Configuração da página do simulador
st.set_page_config(page_title="Linux Essentials - Treino e Simulado", page_icon="🐧", layout="wide")

# BANCO DE DADOS COMPLETO E FORMATADO
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
        "pergunta": "No editor de texto 'vi' ou 'vim', qual tecla deve ser pressionada para alternar do modo de comandos para o modo de inserção de texto?", 
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
        "explicacao": "A flag '-r' (recursive) indica a exclusão de subdiretórios e a flag '-f' (force) desativa os alertas interativos de confirmação."
        Esse erro de sintaxe voltou a acontecer porque na hora de copiar o código anterior, houve uma pequena quebra de linha na questão 2 quebrou a estrutura do Python (uma linha ficou dividida incorretamente e o interpretador se perdeu ao fechar os colchetes da lista).
Vamos resolver isso agora mesmo de forma definitiva.
## Passo 1: Limpar o código no GitHub

   1. Vá até o seu repositório no GitHub e abra o arquivo app.py.
   2. Clique no ícone do lápis no canto superior direito para editar.
   3. Apague absolutamente tudo o que estiver escrito dentro do arquivo, deixando-o completamente em branco.

## Passo 2: Colar o Código 100% Corrigido
Copie o bloco de código abaixo e cole no arquivo limpo. As linhas longas foram todas ajustadas e formatadas de maneira padronizada para evitar novos erros de carregamento na nuvem:

import streamlit as stimport smtplibfrom email.mime.text import MIMETextfrom email.mime.multipart import MIMEMultipartimport randomimport time
# Configuração da página do simulador
st.set_page_config(page_title="Linux Essentials - Treino e Simulado", page_icon="🐧", layout="wide")
# BANCO DE DADOS COMPLETO E FORMATADOQUESTOES_POOL = [
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
        "pergunta": "No editor de texto 'vi' ou 'vim', qual tecla deve ser pressionada para alternar do modo de comandos para o modo de inserção de texto?", 
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
        "explicacao": "A flag '-r' (recursive) indica a exclusão de subdiretórios e a flag '-f' (force) desativa os alertas interativos de confirmação."

},
{
"id": 24, "topico": "Redirecionadores",
"pergunta": "Qual operador de redirecionamento de fluxo do terminal deve ser usado para concatenar (adicionar no final) a saída de um comando a um arquivo existente sem apagar o seu conteúdo atual?",
"opcoes": [">>", ">", "<", "|"], "correta": ">>",
"explicacao": "O operador '>>' anexa dados ao final do arquivo, mantendo o histórico anterior. O operador '>' limpa e sobrescreve o arquivo inteiro."
},
{
"id": 25, "topico": "Controle de Tarefas",
"pergunta": "Qual caractere especial deve ser inserido no final de um comando no terminal para executá-lo em segundo plano (background)?",
"opcoes": ["&", "%", "$", "*"], "correta": "&",
"explicacao": "O caractere comercial '&' (e comercial) faz com que o shell execute a tarefa em background, liberando o prompt de digitação na hora."
},
{
"id": 26, "topico": "Filtros de Linhas",
"pergunta": "Qual comando nativo do Linux lê a entrada de dados e remove de forma dinâmica linhas duplicadas consecutivas presentes em um texto ordenado?",
"opcoes": ["uniq", "sort", "cut", "paste"], "correta": "uniq",
"explicacao": "O utilitário 'uniq' remove linhas idênticas adjacentes. Geralmente é utilizado em conjunto com o comando 'sort' via pipe."
},
{
"id": 27, "topico": "Informações do Sistema",
"pergunta": "Qual das seguintes opções do comando 'uname' exibe a arquitetura e o nome completo do kernel do sistema operacional Linux corrente?",
"opcoes": ["uname -a", "uname -v", "uname -p", "uname -n"], "correta": "uname -a",
"explicacao": "A opção '-a' (all) imprime na tela todas as informações consolidadas da máquina: nome do kernel, versão, data e arquitetura de hardware."
},
{
"id": 28, "topico": "Gerenciamento de Links",
"pergunta": "Qual comando e opção criam um link simbólico (soft link) apontando para outro caminho de arquivo no sistema de arquivos?",
"opcoes": ["ln -s", "link -d", "ln -h", "mklink"], "correta": "ln -s",
"explicacao": "O comando 'ln -s' cria links simbólicos (atalhos de ponteiro), enquanto a execução de 'ln' sem flags cria hard links de inodes."
},
{
"id": 29, "topico": "Estatísticas de Disco",
"pergunta": "Qual utilitário de linha de comando exibe o espaço em disco disponível e utilizado em todos os sistemas de arquivos montados, aceitando a flag '-h' para leitura humana?",
"opcoes": ["df", "du", "fdisk", "free"], "correta": "df",
"explicacao": "O comando 'df' (disk free) exibe tabelas de espaço livre de partições montadas. O 'du' (disk usage) monitora o peso de pastas específicas."
},
{
"id": 30, "topico": "Permissões de Diretório",
"pergunta": "Para que um usuário comum do Linux consiga ler e navegar por dentro de uma pasta usando o comando 'cd', qual dupla de permissões mínimas ele precisa ter nesse diretório?",
"opcoes": ["Leitura e Execução (r e x)", "Apenas Leitura (r)", "Leitura e Escrita (r e w)", "Apenas Execução (x)"], "correta": "Leitura e Execução (r e x)",
"explicacao": "Em pastas, a permissão de leitura 'r' permite listar os arquivos (ls), mas a permissão de execução 'x' é mandatória para entrar (cd) e acessar os metadados do diretório."
}
]
## Inicialização e persistência de dados de ranking
if "ranking_treino" not in st.session_state:
st.session_state.ranking_treino = {}
if "ranking_simulado" not in st.session_state:
st.session_state.ranking_simulado = {}
def gerar_40_questoes():
pool_duplicado = QUESTOES_POOL * 2
return random.sample(pool_duplicado, k=40)
if 'questoes_treino' not in st.session_state:
st.session_state.questoes_treino = list(QUESTOES_POOL)
random.shuffle(st.session_state.questoes_treino)
if 'questoes_simulado' not in st.session_state:
st.session_state.questoes_simulado = gerar_40_questoes()
if 'respostas_simulado' not in st.session_state:
st.session_state.respostas_simulado = {}
if 'simulado_entregue' not in st.session_state:
st.session_state.simulado_entregue = False
if 'tempo_inicio_simulado' not in st.session_state:
st.session_state.tempo_inicio_simulado = None
## BARRA LATERAL
st.sidebar.header("👤 Identificação do Aluno")
nome_usuario = st.sidebar.text_input("Seu Nome/Apelido para o Placar:", max_chars=20)
email_usuario = st.sidebar.text_input("Seu E-mail para receber boletins:")
st.sidebar.divider()
st.sidebar.subheader("🕹️ Seleção do Modo")
modo_selecionado = st.sidebar.radio("Escolha o ambiente de estudos:", ["📖 Área de Treino (Fixação)", "⏱️ Simulado LPI (Prova Real 40 Q)"])
def enviar_email_seguro(destinatario, assunto, relatorio):
try:
remetente = st.secrets["email"]["usuario"]
senha = st.secrets["email"]["senha"]
msg = MIMEMultipart()
msg['From'] = remetente
msg['To'] = destinatario
msg['Subject'] = assunto
msg.attach(MIMEText(relatorio, 'plain'))
server = smtplib.SMTP('gmail.com', 587)
server.starttls()
server.login(remetente, senha)
server.sendmail(remetente, destinatario, msg.as_string())
server.quit()
st.sidebar.success("✅ Histórico enviado por e-mail!")
except Exception:
pass
## --- MODO 1: ÁREA DE TREINAMENTO ---
if modo_selecionado == "📖 Área de Treino (Fixação)":
st.title("📖 Área de Treino e Fixação Técnica")
st.write("Aqui você estuda sem pressão. Escolha a resposta e marque o campo para ver a explicação técnica de cada item.")
aba_treino, aba_rank_treino = st.tabs(["🎯 Exercícios", "🏆 Placar de Líderes (Treino)"])
with aba_treino:
acertos_treino = 0
for idx, q in enumerate(st.session_state.questoes_treino):
st.markdown(f"### Questão {idx+1} — {q['topico']}")
st.write(q['pergunta'])
resp = st.radio("Selecione sua alternativa:", q['opcoes'], key=f"treino_{idx}", index=None)
if st.checkbox("💡 Validar e Ver Explicação", key=f"check_{idx}"):
if resp == q['correta']:
st.success(f"🎯 Resposta Correta: {q['correta']}")
acertos_treino += 1
else:
st.error(f"❌ Resposta Incorreta! A alternativa certa é: {q['correta']}")
st.info(f"📘 Explicação: {q['explicacao']}")
st.divider()
if st.button("🏁 Salvar meu Progresso no Ranking de Treino", type="primary"):
if not nome_usuario:
st.warning("⚠️ Digite seu nome na barra lateral antes de registrar os pontos!")
else:
score = (acertos_treino / len(st.session_state.questoes_treino)) * 100
st.session_state.ranking_treino[nome_usuario] = max(score, st.session_state.ranking_treino.get(nome_usuario, 0))
st.success(f"Progresso computado com sucesso no Placar de Treino!")
time.sleep(1)
st.rerun()
with aba_rank_treino:
st.subheader("🏆 Melhores Pontuações na Área de Estudos")
if st.session_state.ranking_treino:
ranking_ordenado = sorted(st.session_state.ranking_treino.items(), key=lambda x: x[1], reverse=True)
for pos, (user, pt) in enumerate(ranking_ordenado, start=1):
st.write(f"{pos}º Lugar: {user} — Aproveitamento de {pt:.1f}%")
else:
st.info("Nenhum registro no placar ainda. Salve seu progresso para iniciar.")
## --- MODO 2: SIMULADO REAL ---
elif modo_selecionado == "⏱️ Simulado LPI (Prova Real 40 Q)":
st.title("⏱️ Simulado Oficial Linux Essentials")
st.write("Simulação do exame real. 40 Questões, tempo limite de 60 minutos e correção apenas após entregar toda a prova.")
aba_simulado, aba_rank_simulado = st.tabs(["📝 Caderno de Prova", "🏆 Placar dos Aprovados (Simulado)"])
if st.session_state.tempo_inicio_simulado is None:
st.session_state.tempo_inicio_simulado = time.time()
tempo_decorrido = time.time() - st.session_state.tempo_inicio_simulado
tempo_restante = max(0, (60 * 60) - tempo_decorrido)
if tempo_restante > 0 and not st.session_state.simulado_entregue:
m, s = divmod(int(tempo_restante), 60)
st.sidebar.subheader(f"⏳ Cronômetro: {m:02d}:{s:02d}")
elif not st.session_state.simulado_entregue:
st.session_state.simulado_entregue = True
st.sidebar.error("🚨 O tempo acabou! Prova finalizada.")
with aba_simulado:
st.subheader("⚠️ Responda todas as perguntas. A nota e o gabarito serão exibidos após clicar no botão de entrega no fim do caderno.")
st.divider()
for idx, q in enumerate(st.session_state.questoes_simulado):
st.markdown(f"Questão {idx+1}: {q['pergunta']}")
resp_sim = st.radio("Escolha uma opção:", q['opcoes'], key=f"sim_{idx}", index=None, disabled=st.session_state.simulado_entregue)
st.session_state.respostas_simulado[f"q_{idx}"] = resp_sim
if st.session_state.simulado_entregue:
if resp_sim == q['correta']:
st.success(f"✅ Correto! Gabarito: {q['correta']}")
else:
st.error(f"❌ Incorreto. Sua resposta: {resp_sim} | Gabarito Oficial: {q['correta']}")
st.info(f"💡 Explicação: {q['explicacao']}")
st.divider()
if st.button("🏁 Entregar Caderno de Questões", type="primary", disabled=st.session_state.simulado_entregue):
if not nome_usuario:
st.error("⚠️ Insira seu nome na barra lateral esquerda antes de submeter a prova!")
else:
st.session_state.simulado_entregue = True
acertos = 0
for idx, q in enumerate(st.session_state.questoes_simulado):
if st.session_state.respostas_simulado.get(f"q_{idx}") == q['correta']:
acertos += 1
porcentagem_acertos = acertos / 40
pontuacao_lpi = int(200 + (porcentagem_acertos * 600))
status = "APROVADO" if pontuacao_lpi >= 500 else "REPROVADO"
st.session_state.ranking_simulado[nome_usuario] = max(pontuacao_lpi, st.session_state.ranking_simulado.get(nome_usuario, 0))
if email_usuario:
rel_corpo = f"Boletim Oficial do Simulado Linux Essentials\nNome do Aluno: {nome_usuario}\nPontuação Final: {pontuacao_lpi} de 800 pontos\nResultado: {status}"
enviar_email_seguro(email_usuario, f"Resultado Simulado Linux - {pontuacao_lpi} Pontos", rel_corpo)
st.rerun()
with aba_rank_simulado:
st.subheader("🏆 Quadro Geral de Notas do Exame Oficial (Escala LPI 200-800)")
st.caption("Aprovação apenas com pontuação mínima de 500 pontos.")
if st.session_state.ranking_simulado:
rank_sim_ordenado = sorted(st.session_state.ranking_simulado.items(), key=lambda x: x[1], reverse=True)
for pos, (user, pontos) in enumerate(rank_sim_ordenado, start=1):
medalha = "🥇" if pos == 1 else "🥈" if pos == 2 else "🥉" if pos == 3 else "🎖️"
sel_status = "🟢 APROVADO" if pontos >= 500 else "🔴 REPROVADO"
st.markdown(f"### {medalha} {pos}º Lugar: {user} — {pontos} pontos ({sel_status})")
else:
st.info("O quadro de notas do simulado oficial está vazio por enquanto.")
if st.button("🔄 Reiniciar e Gerar Nova Prova Oficial"):
st.session_state.questoes_simulado = gerar_40_questoes()
st.session_state.respostas_simulado = {}
st.session_state.simulado_entregue = False
st.session_state.tempo_inicio_simulado = time.time()
st.rerun()


### Passo 3: Concluir
Clique no botão verde **Commit changes...** no GitHub. A plataforma web vai compilar o script limpo e o simulador com os dois modos voltará ao ar imediatamente!

Deseja avançar para mais algum ajuste ou o link carregou perfeitamente no navegador?



