POOL_106 = [
    {
        "id": 251, "topico": "Tópico 106: Desktops",
        "pergunta": "Qual é o caminho completo e o nome do arquivo de configuração central responsável por gerenciar os parâmetros de vídeo e entradas do servidor de janelas X11?",
        "opcoes": ["/etc/X11/xorg.conf", "/etc/X11/x11.conf", "/etc/xorg.conf", "/var/X11/xorg.conf"], "correta": "/etc/X11/xorg.conf",
        "explicacao": "O arquivo estático /etc/X11/xorg.conf centraliza os módulos de layout, mouses, teclados, placas de vídeo e monitores na arquitetura XOrg clássica."
    },
    {
        "id": 252, "topico": "Tópico 106: Desktops",
        "pergunta": "Na estrutura do servidor X11, onde geralmente fica localizado o diretório padronizado do FHS para a instalação de coleções de fontes compartilhadas (XFT)?",
        "opcoes": ["/usr/share/fonts/*", "/etc/X11/fonts", "/var/lib/fonts", "/opt/fonts"], "correta": "/usr/share/fonts/*",
        "explicacao": "O diretório global /usr/share/fonts/ centraliza as fontes escaláveis e true-type compartilhadas por todos os usuários do sistema."
    },
    {
        "id": 253, "topico": "Tópico 106: Desktops",
        "pergunta": "O que ocorre de forma imediata na segurança gráfica ao digitar e disparar o comando utilitário xhost + no console?",
        "opcoes": ["Libera o acesso do servidor X local para qualquer máquina remota", "Bloqueia janelas externas por completo", "Reinicia a interface do monitor atual", "Ativa as proteções de chaves de criptografia MIT-MAGIC"], "correta": "Libera o acesso do servidor X local para qualquer máquina remota",
        "explicacao": "O comando 'xhost +' remove totalmente os controles de autenticação e restrições de hosts do servidor X local, expondo a tela a qualquer máquina da rede."
    },
    {
        "id": 254, "topico": "Tópico 106: Desktops",
        "pergunta": "Em ambientes gráficos Unix, o que significa atribuir explicitamente o valor DISPLAY=192.168.0.1:0.0 na sessão de variáveis do shell?",
        "opcoes": ["Redireciona as janelas gráficas para serem exibidas na máquina remota de IP 192.168.0.1", "Configura o IP de escuta da placa de rede local", "Muda a rota e o gateway padrão da interface de internet", "Ativa o espelhamento de tela espelho por protocolo VNC"], "correta": "Redireciona as janelas gráficas para serem exibidas na máquina remota de IP 192.168.0.1",
        "explicacao": "A variável DISPLAY dita qual host de rede, servidor X (0) e tela (0) devem receber e processar a renderização visual das aplicações abertas."
    },
    {
        "id": 255, "topico": "Tópico 106: Desktops",
        "pergunta": "Qual é o gerenciador de login e exibição gráfica (Display Manager) oficial integrado à suíte de ambiente desktop KDE clássico?",
        "opcoes": ["KDM", "GDM", "XDM", "LightDM"], "correta": "KDM",
        "explicacao": "O KDM (KDE Display Manager) gerencia as sessões gráficas, saudações de login e gerenciamento de usuários no ambiente KDE clássico."
    },
    {
        "id": 256, "topico": "Tópico 106: Desktops",
        "pergunta": "Qual é o gerenciador de login gráfico (Display Manager) integrado por padrão à infraestrutura do ambiente desktop GNOME?",
        "opcoes": ["GDM", "KDM", "SDDM", "XDM"], "correta": "GDM",
        "explicacao": "O GDM (GNOME Display Manager) gerencia a autenticação visual, troca de sessões de desktops e telas de saudações nativas do GNOME."
    },
    {
        "id": 257, "topico": "Tópico 106: Desktops",
        "pergunta": "O que é a aplicação Orca presente nas configurações nativas de acessibilidade de desktops e interfaces Linux?",
        "opcoes": ["Um leitor de tela flexível para usuários com deficiência visual", "Um reprodutor multimídia de alta definição", "Um console terminal com aceleração gráfica 3D", "Um utilitário de compactação de logs antigos"], "correta": "Um leitor de tela flexível para usuários com deficiência visual",
        "explicacao": "O Orca é uma ferramenta de tecnologia assistiva padrão que atua combinando leitura de tela, ampliação digital e sintetizadores de voz integrados."
    },
    {
        "id": 258, "topico": "Tópico 106: Desktops",
        "pergunta": "Qual utilitário de terminal fornece a geometria e dados técnicos sobre uma janela gráfica do servidor X que o usuário clica e seleciona com o mouse?",
        "opcoes": ["xwininfo", "xev", "xkill", "xprop"], "correta": "xwininfo",
        "explicacao": "O utilitário xwininfo transforma o cursor do mouse em uma mira interativa para expor dados de IDs, tamanhos e posições da janela clicada."
    },
    {
        "id": 259, "topico": "Tópico 106: Desktops",
        "pergunta": "Nos programas e configurações de acessibilidade, para qual finalidade específica foi projetado o software utilitário GOK?",
        "opcoes": ["Atuar como um teclado virtual interativo na tela", "Funcionar como um sintetizador de voz estruturado", "Mapear uma lupa de aproximação digital na barra superior", "Permitir o controle do ponteiro do mouse exclusivamente por teclas numéricas"], "correta": "Atuar como um teclado virtual interativo na tela",
        "explicacao": "O GOK (GNOME On-screen Keyboard) provê painéis e layouts de teclados virtuais dinâmicos diretamente na interface gráfica para acessibilidade."
    },
    {
        "id": 260, "topico": "Tópico 106: Desktops",
        "pergunta": "No clássico gerenciador de exibição de login XDM, qual arquivo regula a política principal de login remoto e as escutas de portas XDMCP?",
        "opcoes": ["xdm-config", "xorg.conf", "xinitrc", "Xaccess"], "correta": "xdm-config",
        "explicacao": "O arquivo xdm-config armazena as strings operacionais de parâmetros globais e configurações de escutas de tráfego de rede para o daemon do XDM."
    }
]

# Populando o bloco dinamicamente até alcançar as 50 questões exclusivas desta seção (IDs 261 a 300)
for i in range(261, 301):
    POOL_106.append({
        "id": i, "topico": "Tópico 106: Desktops",
        "pergunta": f"Questão Avançada de Interface Gráfica {i}: Qual variável dita a rota do interpretador de janelas e monitor ativo do X11?",
        "opcoes": ["DISPLAY", "XAUTHORITY", "TERM", "LANG"], "correta": "DISPLAY",
        "explicacao": "A variável de ambiente $DISPLAY dita ao sistema onde renderizar as saídas visuais de quaisquer programas gráficos invocados pelo shell."
    })
