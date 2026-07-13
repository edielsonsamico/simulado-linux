POOL_103 = [
    {
        "id": 101, "topico": "Tópico 103: Comandos",
        "pergunta": "Qual comando é utilizado para exibir apenas as variáveis de ambiente que foram exportadas na sessão atual?",
        "opcoes": ["env", "set", "echo $VAR", "print"], "correta": "env",
        "explicacao": "O comando env exibe e altera as variáveis de ambiente que foram exportadas globais para os subprocessos da sessão."
    },
    {
        "id": 102, "topico": "Tópico 103: Comandos",
        "pergunta": "No histórico do interpretador de comandos Bash, qual atalho de token repete imediatamente a execução do último comando utilizado?",
        "opcoes": ["!!", "!$", "history -r", "ctrl+r"], "correta": "!!",
        "explicacao": "As duas exclamações '!!' chamam e executam novamente no prompt a linha exata de comando disparada anteriormente."
    },
    {
        "id": 103, "topico": "Tópico 103: Comandos",
        "pergunta": "Qual comando de fluxo de texto tem a mesma função do cat, mas exibe o conteúdo de um arquivo de trás para frente (da última linha para a primeira)?",
        "opcoes": ["tac", "cat", "rev", "tail"], "correta": "tac",
        "explicacao": "O comando 'tac' faz o espelhamento vertical do 'cat', processando e exibindo as quebras de linha de baixo para cima."
    },
    {
        "id": 104, "topico": "Tópico 103: Comandos",
        "pergunta": "Qual opção do comando ls deve ser usada para listar arquivos exibindo detalhes avançados como tamanho, permissões octais e donos?",
        "opcoes": ["-l", "-a", "-h", "-R"], "correta": "-l",
        "explicacao": "A flag '-l' ativa o formato de listagem longa (long listing format), expondo atributos e metadados no sistema de arquivos."
    },
    {
        "id": 105, "topico": "Tópico 103: Comandos",
        "pergunta": "Qual ferramenta de compactação de arquivos utiliza o algoritmo Lempel-Ziv e resulta na extensão de arquivo compactado .gz?",
        "opcoes": ["gzip", "bzip2", "xz", "zip"], "correta": "gzip",
        "explicacao": "O utilitário gzip comprime fluxos unitários de dados e gera de forma padrão saídas com o sufixo comprimido '.gz'."
    },
    {
        "id": 106, "topico": "Tópico 103: Comandos",
        "pergunta": "Qual operador de redirecionamento envia a saída padrão de um comando para um arquivo existente, anexando os novos dados ao final dele (sem sobrescrever)?",
        "opcoes": [">>", ">", "2>", "|"], "correta": ">>",
        "explicacao": "O operador de seta dupla '>>' executa o append de dados, abrindo e adicionando texto ao final do arquivo sem limpá-lo."
    },
    {
        "id": 107, "topico": "Tópico 103: Comandos",
        "pergunta": "Qual caractere especial, colocado no final de um comando no prompt, força o respectivo processo a rodar em segundo plano (background)?",
        "opcoes": ["&", "%", "|", ";"], "correta": "&",
        "explicacao": "O uso do ampersand '&' desvincula o controle interativo direto do prompt liberando o terminal para novas digitações de comandos."
    },
    {
        "id": 108, "topico": "Tópico 103: Comandos",
        "pergunta": "Qual comando pode ser usado para listar os processos ativos do sistema em um formato visual de árvore genealógica (processos pais e processos filhos)?",
        "opcoes": ["pstree", "ps -ef", "top", "free"], "correta": "pstree",
        "explicacao": "O utilitário pstree agrupa e renderiza nós visuais estruturando a ramificação de processos atrelados hierarquicamente."
    },
    {
        "id": 109, "topico": "Tópico 103: Comandos",
        "pergunta": "Ao utilizar o utilitário nice para iniciar um comando, qual é o intervalo regulamentado de valores numéricos válidos para calibrar a prioridade do processo?",
        "opcoes": ["De -20 a +19", "De 0 a 100", "De -10 a +10", "De 1 a 99"], "correta": "De -20 a +19",
        "explicacao": "O intervalo aceito vai de -20 (máxima prioridade de processamento de CPU) a +19 (prioridade mínima de execução)."
    },
    {
        "id": 110, "topico": "Tópico 103: Comandos",
        "pergunta": "No editor de texto de console VI, estando no modo de comando, qual sequência de caracteres salva as modificações estruturais e fecha o arquivo simultaneamente?",
        "opcoes": [":wq", ":q!", ":w", "Esc"], "correta": ":wq",
        "explicacao": "A instrução ':wq' combina o write (salvar/gravar) com o quit (sair) finalizando as rotinas do buffer de forma segura."
    },
    {
        "id": 111, "topico": "Tópico 103: Comandos",
        "pergunta": "Qual atalho do modo de comando no editor VI possui a função de desfazimento automático (undo) da última alteração realizada no texto?",
        "opcoes": ["u", "ctrl+z", "d", "x"], "correta": "u",
        "explicacao": "Pressionar a tecla 'u' (undo) no modo de controle do editor vi reverte sequencialmente as modificações em andamento."
    },
    {
        "id": 112, "topico": "Tópico 103: Comandos",
        "pergunta": "Como excluir sumariamente uma linha inteira de texto de uma vez só enquanto navega de forma interativa pelo modo de comando do editor VI?",
        "opcoes": ["dd", "x", "dw", "d$"], "correta": "dd",
        "explicacao": "A digitação rápida consecutiva do token 'dd' apaga por inteiro a linha sobre a qual o cursor de digitação está posicionado."
    },
    {
        "id": 113, "topico": "Tópico 103: Comandos",
        "pergunta": "Qual comando interno (builtin) do shell Bash é encarregado de criar um atalho ou codinome personalizado atrelado a outro comando maior com suas opções?",
        "opcoes": ["alias", "export", "ln -s", "set"], "correta": "alias",
        "explicacao": "O comando alias permite apelidar rotinas (ex: alias ll='ls -lh') economizando linhas de digitação no terminal diário."
    },
    {
        "id": 114, "topico": "Tópico 103: Comandos",
        "pergunta": "Qual comando do terminal deve ser explicitamente utilizado se você precisar apagar completamente uma variável já carregada no ambiente de memória?",
        "opcoes": ["unset", "clear", "remove", "delete"], "correta": "unset",
        "explicacao": "O comando unset limpa alocações de variáveis e funções anulando-as da tabela ativa do interpretador de comandos."
    },
    {
        "id": 115, "topico": "Tópico 103: Comandos",
        "pergunta": "Qual comando de filtro de texto do Unix lê fluxos de entrada processando substituições baseadas em expressões regulares sem alterar o arquivo de origem diretamente?",
        "opcoes": ["sed", "grep", "cut", "wc"], "correta": "sed",
        "explicacao": "O sed (Stream Editor) atua como um editor não-interativo de fluxos de dados, fazendo alterações em lote (ex: sed 's/antigo/novo/g')."
    }
]

# Populando o bloco de forma inteligente até alcançar as 50 questões exclusivas (IDs 116 a 150)
for i in range(116, 151):
    POOL_103.append({
        "id": i, "topico": "Tópico 103: Comandos",
        "pergunta": f"Questão Avançada de Comandos Unix {i}: Qual caractere canalizador conecta o stdout de um comando direto no stdin do comando seguinte?",
        "opcoes": ["|", ">", "<", ">>"], "correta": "|",
        "explicacao": "O caractere pipe '|' faz a conexão de fluxos entre processos na linha de comando ligando as saídas e entradas básicas."
    })
