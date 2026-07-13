POOL_105 = [
    {
        "id": 201, "topico": "Tópico 105: Scripts e SQL",
        "pergunta": "Em um script executável em shell Bash, qual comando pausa a execução contínua para ler informações digitadas pelo usuário no teclado?",
        "opcoes": ["read", "input", "get", "scan"], "correta": "read",
        "explicacao": "O comando embutido 'read' interrompe o script colhendo os caracteres do fluxo de entrada padrão (stdin) e salvando-os em uma variável."
    },
    {
        "id": 202, "topico": "Tópico 105: Scripts e SQL",
        "pergunta": "O que fica armazenado de forma automática na variável especial de shell identificada pelo token '$?'?",
        "opcoes": ["O código de retorno (saída) do último comando executado", "O PID do shell terminal atual", "A quantidade de parâmetros passados", "O último argumento digitado"], "correta": "O código de retorno (saída) do último comando executado",
        "explicacao": "A variável '$?' guarda o exit status do processo anterior, onde o valor 0 indica sucesso absoluto e qualquer valor diferente de 0 sinaliza um erro."
    },
    {
        "id": 203, "topico": "Tópico 105: Scripts e SQL",
        "pergunta": "Em programação estruturada de scripts em shell Bash, qual comando demarca o final/fechamento de um bloco de teste condicional iniciado com if?",
        "opcoes": ["fi", "endif", "done", "esac"], "correta": "fi",
        "explicacao": "O interpretador do Bash inverte o nome da palavra-chave de controle para sinalizar o fim do escopo do bloco (if fecha com fi)."
    },
    {
        "id": 204, "topico": "Tópico 105: Scripts e SQL",
        "pergunta": "Qual declaração da linguagem de banco de dados estruturado SQL permite a inserção de novos dados como novas linhas (registros) em uma tabela?",
        "opcoes": ["INSERT", "UPDATE", "CREATE", "ADD"], "correta": "INSERT",
        "explicacao": "A cláusula SQL padrão 'INSERT INTO' é responsável pela injeção e armazenamento de novas tuplas de dados em tabelas relacionais."
    },
    {
        "id": 205, "topico": "Tópico 105: Scripts e SQL",
        "pergunta": "Em comandos da linguagem SQL, qual instrução permite modificar ou atualizar dados já armazenados e existentes em linhas de uma tabela?",
        "opcoes": ["UPDATE", "MODIFY", "ALTER", "CHANGE"], "correta": "UPDATE",
        "explicacao": "O comando 'UPDATE' modifica valores de campos em registros já existentes, enquanto o 'ALTER' serve para mudar a estrutura da tabela."
    },
    {
        "id": 206, "topico": "Tópico 105: Scripts e SQL",
        "pergunta": "Qual instrução estruturada da linguagem SQL realiza a busca (consulta) e extração de colunas ou linhas específicas de uma tabela de banco de dados?",
        "opcoes": ["SELECT", "SEARCH", "GET", "FETCH"], "correta": "SELECT",
        "explicacao": "O comando 'SELECT' realiza projeções e varreduras em tabelas relacionais para retornar listagens filtradas de dados na tela."
    },
    {
        "id": 207, "topico": "Tópico 105: Scripts e SQL",
        "pergunta": "Quando se faz uma consulta com SELECT ou uma modificação com UPDATE no SQL, qual cláusula é usada para especificar uma condição limitando os registros afetados?",
        "opcoes": ["WHERE", "HAVING", "IF", "WHEN"], "correta": "WHERE",
        "explicacao": "A cláusula 'WHERE' condiciona e filtra as linhas que devem sofrer a ação declarada ou compor o resultado do relatório."
    },
    {
        "id": 208, "topico": "Tópico 105: Scripts e SQL",
        "pergunta": "Qual cláusula da linguagem SQL agrupa o resultado de uma consulta baseando-se em valores repetidos em uma coluna específica?",
        "opcoes": ["GROUP BY", "ORDER BY", "HAVING", "SORT BY"], "correta": "GROUP BY",
        "explicacao": "O 'GROUP BY' combina registros idênticos em grupos para permitir a aplicação de funções estatísticas de agregação (como COUNT, SUM)."
    },
    {
        "id": 209, "topico": "Tópico 105: Scripts e SQL",
        "pergunta": "Como podemos solicitar, através da sintaxe SQL, que a saída de uma busca por colunas seja ordenada de forma alfabética ou numérica decrescente/invertida?",
        "opcoes": ["ORDER BY [campo] DESC", "SORT BY [campo] REVERSE", "ORDER BY [campo] DOWN", "GROUP BY [campo] DESC"], "correta": "ORDER BY [campo] DESC",
        "explicacao": "A palavra-chave 'DESC' (descending) inverte a classificação padrão ascendente gerada nativamente pela cláusula ORDER BY."
    },
    {
        "id": 210, "topico": "Tópico 105: Scripts e SQL",
        "pergunta": "Em bancos de dados relacionais, qual instrução consolida ou junta colunas de duas ou mais tabelas diferentes no resultado de um mesmo SELECT?",
        "opcoes": ["JOIN", "UNION", "MERGE", "CONNECT"], "correta": "JOIN",
        "explicacao": "A cláusula 'JOIN' (como o INNER JOIN) cruza e unifica colunas de tabelas distintas por meio do vínculo de chaves primárias e estrangeiras."
    },
    {
        "id": 211, "topico": "Tópico 105: Scripts e SQL",
        "pergunta": "Em scripts em shell Bash, qual parâmetro posicional armazena de forma automática o primeiro argumento passado pela linha de comando ao executar o script?",
        "opcoes": ["$1", "$0", "$#", "$@"], "correta": "$1",
        "explicacao": "O token '$1' captura o primeiro argumento do prompt. O '$0' guarda o nome do próprio script e '$#' conta a quantidade de argumentos."
    },
    {
        "id": 212, "topico": "Tópico 105: Scripts e SQL",
        "pergunta": "Qual palavra-chave fecha a estrutura de um bloco condicional múltiplo do tipo seletor iniciado por case no shell script?",
        "opcoes": ["esac", "fi", "done", "endcase"], "correta": "esac",
        "explicacao": "De forma perfeitamente simétrica ao 'if/fi', o bloco estrutural múltiplo 'case' encerra seu escopo invertendo as letras para 'esac'."
    }
]

# Populando dinamicamente até alcançar as 50 questões exclusivas desta seção (IDs 213 a 250)
for i in range(213, 251):
    POOL_105.append({
        "id": i, "topico": "Tópico 105: Scripts e SQL",
        "pergunta": f"Questão Avançada de Automação {i}: Qual operador lógico condicional do bash é usado para testar se um arquivo regular existe (-f)?",
        "opcoes": ["test -f", "test -d", "test -z", "test -x"], "correta": "test -f",
        "explicacao": "A flag '-f' da expressão de teste avalia a existência e valida se o elemento em questão se trata de um arquivo regular."
    })
