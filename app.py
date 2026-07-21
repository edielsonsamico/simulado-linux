import streamlit as st
import random
import re
import importlib
import hashlib
import string
import time

def gerar_hash_conteudo(pergunta):
    texto_limpo = re.sub(r'^(quest[ãa]o.*?\d+|q\d+|\d+)\s*[\.\:\-]?\s*', '', pergunta.strip(), flags=re.IGNORECASE)
    texto_limpo = " ".join(texto_limpo.lower().split())
    return hashlib.md5(texto_limpo.encode('utf-8')).hexdigest()

def inferir_resposta_correta(pergunta, opcoes):
    """Fallback inteligente para associar a resposta caso a chave do tópico venha vazia."""
    p = pergunta.lower()
    termos_chave = {
        "geometria e dados técnicos sobre uma janela gráfica": "xwininfo",
        "representação octal tradicional de permissões": "leitura é 4",
        "lsof utilizando especificamente a flag -i": "processos atrelados a conexões de rede e portas abertas",
        "protocolo de sincronização temporal ntp": "porta udp 123",
        "hotplug": "permitir conexão e desconexão de dispositivos com a máquina ligada",
        "desligar ou reiniciar a máquina de forma segura, permitindo alertar": "shutdown",
        "variável especial de shell identificada pelo token": "código de retorno",
        "opção do comando ls deve ser usada": "-l",
        "abriga de forma criptografada as senhas": "/etc/shadow",
        "centralizar, processar e despachar mensagens": "syslogd",
        "cotas virtuais": "quota",
        "pausa a execução": "read",
        "configura o nome da máquina local": "/etc/hostname",
        "display=192.168": "direcionar a saída gráfica",
        "suid": "-perm",
        "conectividad": "ping",
        "cron.allow": "todos",
        "linha inteira": "dd",
        "pacotes atualmente instalados": "rpm -qa",
        "máxima criticidade": "emerg",
        "syslog": "emerg",
        "árvore genealógica": "pstree",
        "bibliotecas compartilhadas": "/etc/ld.so.conf",
        "redirecionamento envia a saída padrão": ">>",
        "protocolo de sincronização temporal": "123",
        "ordenada de forma alfabética": "order by",
        "inserção de novos dados": "insert into",
        "cláusula é usada para especificar uma condição": "where",
        "proprietário usuário e o grupo": "chown",
        "primeiro processo": "init",
        "diretório padrão o sistema copia": "/etc/skel",
        "compactação": "gzip",
        "reiniciar a máquina": "reboot",
        "variável já carregada": "unset",
        "servidor x11": "/etc/x11/xorg.conf",
        "i18n": "iconv",
        "arquivo regular existe": "-f",
        "detalhes como modelo de fábrica": "/proc/cpuinfo",
        "variáveis de ambiente que foram exportadas": "export",
        "localiza caminhos": "locate",
        "intervalo regulamentado": "-20 a +19"
    }
    for chave, termo in termos_chave.items():
        if chave in p:
            for op in opcoes:
                if termo in op.lower():
                    return op
    return opcoes[0] if opcoes else "Não informada"

def carregar_banco_unico():
    pool_total = []
    for i in range(101, 111):
        try:
            modulo = importlib.import_module(f"topico{i}")
            if hasattr(modulo, f"POOL_{i}"):
                pool_total.extend(getattr(modulo, f"POOL_{i}"))
        except: continue
    
    banco_final = {}
    for q in pool_total:
        h = gerar_hash_conteudo(q["pergunta"])
        if h not in banco_final:
            q_copia = q.copy()
            opcoes_originais = q.get('opcoes', [])
            q_copia['opcoes_fixas'] = opcoes_originais.copy()
            random.shuffle(q_copia['opcoes_fixas'])
            
            resp_oficial = None
            
            if 'correta' in q and q['correta'] is not None:
                val = q['correta']
                try:
                    idx = int(val)
                    if 0 <= idx < len(opcoes_originais):
                        resp_oficial = str(opcoes_originais[idx]).strip()
                except ValueError:
                    resp_oficial = str(val).strip()
            
            if not resp_oficial or resp_oficial == "":
                resp_oficial = inferir_resposta_correta(q['pergunta'], q_copia['opcoes_fixas'])
                
            q_copia['resposta_oficial'] = resp_oficial
            banco_final[h] = q_copia
            
    return list(banco_final.values())

def processar_finalizacao(tempo_decorrido):
    total_questoes = len(st.session_state.simulado_ativo)
    questoes_respondidas = len(st.session_state.respostas_usuario)
    
    if questoes_respondidas < total_questoes:
        st.session_state.erro_finalizacao = f"❌ Você respondeu apenas {questoes_respondidas} de {total_questoes} questões. É obrigatório responder TODAS as questões antes de finalizar!"
        st.rerun()
        return

    acertos = 0
    for i, q in enumerate(st.session_state.simulado_ativo):
        resp_user = st.session_state.respostas_usuario.get(i)
        resp_certa = q.get('resposta_oficial')
        if resp_user and resp_certa and (str(resp_user).strip().lower() == str(resp_certa).strip().lower()):
            acertos += 1
            
    minimo_acertos = total_questoes * 0.5
    
    if acertos < minimo_acertos:
        st.session_state.erro_finalizacao = f"❌ Você concluiu a prova, mas acertou {acertos} de {total_questoes} questões ({(acertos/total_questoes)*100:.1f}%). Para liberar o gabarito e entrar no Ranking Top 10, é necessário atingir no mínimo 50% de acertos ({int(minimo_acertos)} acertos). Escolha uma das opções abaixo para continuar treinando!"
    else:
        st.session_state.erro_finalizacao = None
        st.session_state.tempo_gasto = tempo_decorrido
        st.session_state.simulado_finalizado = True
        st.session_state.nick_salvo = False # Prepara para o ranking
    st.rerun()

def main():
    st.set_page_config(page_title="Ambiente SAMICOIOT", layout="wide")

    # Inicialização de Estados da Sessão
    if 'banco_questoes' not in st.session_state:
        st.session_state.banco_questoes = carregar_banco_unico()
        st.session_state.simulado_ativo = random.sample(st.session_state.banco_questoes, k=min(40, len(st.session_state.banco_questoes)))
    
    if 'acesso_vip' not in st.session_state: st.session_state.acesso_vip = False
    if 'clicou_no_cadastro' not in st.session_state: st.session_state.clicou_no_cadastro = False
    if 'senha_aleatoria' not in st.session_state:
        st.session_state.senha_aleatoria = ''.join(random.choices(string.digits, k=6))
    if 'inicio_simulado' not in st.session_state:
        st.session_state.inicio_simulado = time.time()
    if 'tempo_gasto' not in st.session_state:
        st.session_state.tempo_gasto = 0
    if 'simulado_finalizado' not in st.session_state:
        st.session_state.simulado_finalizado = False
    if 'erro_finalizacao' not in st.session_state:
        st.session_state.erro_finalizacao = None
    if 'nick_salvo' not in st.session_state:
        st.session_state.nick_salvo = False
    if 'respostas_usuario' not in st.session_state:
        st.session_state.respostas_usuario = {}
    if 'ranking' not in st.session_state:
        st.session_state.ranking = [
            {"nick": "Samico", "nota": 9.5, "tempo": 1200},
            {"nick": "LinuxPro", "nota": 8.8, "tempo": 1450},
            {"nick": "TerminalMaster", "nota": 8.0, "tempo": 1100},
            {"nick": "SysAdmin", "nota": 7.5, "tempo": 1600},
            {"nick": "DevOpsBR", "nota": 7.0, "tempo": 1800}
        ]

    st.sidebar.title("Ambiente SAMICOIOT")
    modo = st.sidebar.radio("Navegação:", [
        "Treino Geral", 
        "Treino por Tópico", 
        "Simulado LPI Oficial",
        "Ranking de Notas",
        "Materiais VIP",
        "Créditos"
    ])

    if modo == "Treino Geral":
        st.title("📖 Área de Treino Geral")
        for q in st.session_state.banco_questoes:
            st.markdown(f"**{q['pergunta']}**")
            st.radio(f"t_{q['id']}", q['opcoes_fixas'], index=None, label_visibility="collapsed")
            st.divider()

    elif modo == "Treino por Tópico":
        st.title("🎯 Treino por Tópico")
        topicos = sorted(list(set(q.get('topico', 'Geral') for q in st.session_state.banco_questoes)))
        t = st.selectbox("Escolha:", topicos)
        for q in [q for q in st.session_state.banco_questoes if q.get('topico') == t]:
            st.markdown(f"**{q['pergunta']}**")
            st.radio(f"radio_{q['id']}_{t}", q['opcoes_fixas'], index=None, label_visibility="collapsed")
            st.divider()

    elif modo == "Simulado LPI Oficial":
        st.title("⏱️ Simulado LPI (Prova Real 40 Q)")
        TEMPO_OFICIAL = 60 * 60 

        # Estado da Prova Ativa
        if not st.session_state.simulado_finalizado:
            tempo_decorrido = int(time.time() - st.session_state.inicio_simulado)
            tempo_restante = TEMPO_OFICIAL - tempo_decorrido
            
            if tempo_restante > 0:
                st.metric("⏱️ Tempo Restante", f"{tempo_restante // 60:02d}:{tempo_restante % 60:02d}")
            else:
                st.error("TEMPO ESGOTADO!")
                st.session_state.tempo_gasto = TEMPO_OFICIAL
                st.session_state.simulado_finalizado = True
                st.rerun()
            
            st.markdown("---")
            
            # EXIBIÇÃO DE ERRO E BOTÕES DE RETENTATIVA NO TOPO
            if st.session_state.erro_finalizacao:
                st.error(st.session_state.erro_finalizacao)
                if "50%" in st.session_state.erro_finalizacao:
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("🧹 Limpar Respostas (Refazer as mesmas)", key="btn_limpar_topo"):
                            st.session_state.respostas_usuario = {}
                            st.session_state.erro_finalizacao = None
                            st.rerun()
                    with c2:
                        if st.button("🔄 Sortear Novas Questões", key="btn_sortear_topo"):
                            st.session_state.simulado_ativo = random.sample(st.session_state.banco_questoes, k=min(40, len(st.session_state.banco_questoes)))
                            st.session_state.respostas_usuario = {}
                            st.session_state.erro_finalizacao = None
                            st.session_state.inicio_simulado = time.time()
                            st.rerun()
                st.markdown("---")

            # BOTÃO DE FINALIZAR TOPO
            if st.button("Finalizar Simulado e Ver Gabarito", key="btn_fin_topo"):
                processar_finalizacao(tempo_decorrido)

            st.markdown("---")
                
            for i, q in enumerate(st.session_state.simulado_ativo):
                st.markdown(f"**{i+1}. {q['pergunta']}**")
                
                opcoes = q['opcoes_fixas']
                resp_atual = st.session_state.respostas_usuario.get(i)
                idx_default = opcoes.index(resp_current) if (resp_current := resp_atual) in opcoes else None
                
                escolha = st.radio(f"sim_{i}_{q['id']}", opcoes, index=idx_default, label_visibility="collapsed")
                if escolha:
                    st.session_state.respostas_usuario[i] = escolha
                    
                st.divider()

            # EXIBIÇÃO DE ERRO E BOTÕES DE RETENTATIVA NA BASE
            if st.session_state.erro_finalizacao:
                st.error(st.session_state.erro_finalizacao)
                if "50%" in st.session_state.erro_finalizacao:
                    cb1, cb2 = st.columns(2)
                    with cb1:
                        if st.button("🧹 Limpar Respostas (Refazer as mesmas)", key="btn_limpar_base"):
                            st.session_state.respostas_usuario = {}
                            st.session_state.erro_finalizacao = None
                            st.rerun()
                    with cb2:
                        if st.button("🔄 Sortear Novas Questões", key="btn_sortear_base"):
                            st.session_state.simulado_ativo = random.sample(st.session_state.banco_questoes, k=min(40, len(st.session_state.banco_questoes)))
                            st.session_state.respostas_usuario = {}
                            st.session_state.erro_finalizacao = None
                            st.session_state.inicio_simulado = time.time()
                            st.rerun()
                st.markdown("---")

            # BOTÃO DE FINALIZAR BASE
            if st.button("Finalizar Simulado e Ver Gabarito", key="btn_fin_base"):
                processar_finalizacao(tempo_decorrido)
                
        # Estado de Prova Finalizada com Sucesso
        else:
            st.success("🏁 Simulado Finalizado com Sucesso! Desempenho aprovado para liberação do gabarito.")
            
            acertos = 0
            total_questoes = len(st.session_state.simulado_ativo)
            
            for i, q in enumerate(st.session_state.simulado_ativo):
                resposta_usuario = st.session_state.respostas_usuario.get(i)
                resposta_correta = q.get('resposta_oficial')
                
                if resposta_usuario and resposta_correta and (str(resposta_usuario).strip().lower() == str(resposta_correta).strip().lower()):
                    acertos += 1
            
            nota_final = (acertos / total_questoes) * 10 if total_questoes > 0 else 0
            minutos_usados = st.session_state.tempo_gasto // 60
            segundos_usados = st.session_state.tempo_gasto % 60

            # Sistema de Ranking (Só aparece se a pessoa ainda não salvou o nick)
            if not st.session_state.nick_salvo:
                st.info("🎉 Parabéns! Registre sua nota no Ranking Top 10:")
                col_n1, col_n2 = st.columns([3, 1])
                with col_n1:
                    nick_input = st.text_input("Digite seu Nickname:", value="Samico")
                with col_n2:
                    st.write("")
                    st.write("")
                    if st.button("Salvar no Ranking", key="btn_salvar_ranking"):
                        st.session_state.ranking.append({"nick": nick_input, "nota": nota_final, "tempo": st.session_state.tempo_gasto})
                        st.session_state.ranking = sorted(st.session_state.ranking, key=lambda x: (-x['nota'], x['tempo']))
                        st.session_state.nick_salvo = True
                        st.rerun()
            else:
                st.success("✅ Sua nota foi salva no Ranking!")
            
            st.markdown("---")

            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("Sua Nota Final", f"{nota_final:.1f} / 10.0", f"{acertos} de {total_questoes} corretas")
            with col_m2:
                st.metric("Tempo de Prova", f"{minutos_usados:02d}:{segundos_usados:02d}")
            
            st.markdown("---")
            
            if st.button("🔄 Sortear Novas Questões (Iniciar Novo Simulado)", key="btn_novo_fim_topo"):
                st.session_state.simulado_finalizado = False
                st.session_state.inicio_simulado = time.time()
                st.session_state.simulado_ativo = random.sample(st.session_state.banco_questoes, k=min(40, len(st.session_state.banco_questoes)))
                st.session_state.respostas_usuario = {}
                st.session_state.erro_finalizacao = None
                st.rerun()

            st.subheader("📋 Gabarito Detalhado")
            
            for i, q in enumerate(st.session_state.simulado_ativo):
                resp_user = st.session_state.respostas_usuario.get(i)
                resp_certa = q.get('resposta_oficial', 'Não informada')
                
                st.markdown(f"**{i+1}. {q['pergunta']}**")
                
                if not resp_user:
                    st.warning(f"Sua resposta: Não respondida | Resposta Correta: {resp_certa}")
                elif resp_certa and str(resp_user).strip().lower() == str(resp_certa).strip().lower():
                    st.success(f"Sua resposta: {resp_user} (Correta!)")
                else:
                    st.error(f"Sua resposta: {resp_user} | Resposta Correta: {resp_certa}")
                st.divider()

            if st.button("🔄 Sortear Novas Questões (Iniciar Novo Simulado)", key="btn_novo_fim_base"):
                st.session_state.simulado_finalizado = False
                st.session_state.inicio_simulado = time.time()
                st.session_state.simulado_ativo = random.sample(st.session_state.banco_questoes, k=min(40, len(st.session_state.banco_questoes)))
                st.session_state.respostas_usuario = {}
                st.session_state.erro_finalizacao = None
                st.rerun()

    elif modo == "Ranking de Notas":
        st.title("🏆 Ranking Top 10 (Maiores Notas & Agilidade)")
        st.markdown("Os 10 melhores operadores do ambiente. *Critério de desempate: menor tempo de conclusão.*")
        
        ranking_ordenado = sorted(st.session_state.ranking, key=lambda x: (-x['nota'], x['tempo']))[:10]
        
        for idx, item in enumerate(ranking_ordenado, 1):
            m_t = item['tempo'] // 60
            s_t = item['tempo'] % 60
            tempo_str = f"{m_t:02d}:{s_t:02d}"
            
            if idx == 1:
                st.markdown(f"🥇 **1º Lugar:** `{item['nick']}` — **Nota: {item['nota']:.1f}** *(Tempo: {tempo_str})*")
            elif idx == 2:
                st.markdown(f"🥈 **2º Lugar:** `{item['nick']}` — **Nota: {item['nota']:.1f}** *(Tempo: {tempo_str})*")
            elif idx == 3:
                st.markdown(f"🥉 **3º Lugar:** `{item['nick']}` — **Nota: {item['nota']:.1f}** *(Tempo: {tempo_str})*")
            else:
                st.markdown(f"▫️ **{idx}º Lugar:** `{item['nick']}` — **Nota: {item['nota']:.1f}** *(Tempo: {tempo_str})*")
            
    elif modo == "Materiais VIP":
        st.title("🎁 Materiais VIP")
        if not st.session_state.acesso_vip:
            if st.link_button("👉 INSCREVA-SE NO CANAL", "https://www.youtube.com/@EdielsonSamico?sub_confirmation=1"):
                st.session_state.clicou_no_cadastro = True
            if st.session_state.clicou_no_cadastro:
                if st.button("Gerar Senha"): st.info(f"Senha: **{st.session_state.senha_aleatoria}**")
                codigo = st.text_input("Senha:", type="password")
                if st.button("Validar"):
                    if codigo == st.session_state.senha_aleatoria:
                        st.session_state.acesso_vip = True
                        st.rerun()
        else:
            st.success("Acesso VIP Liberado!")
            materiais = {"Apostila": "Apostila_Premium_de_Certificacao.pdf", "LPIC-1": "LPIC-1_Terminal_2026.pdf"}
            for n, l in materiais.items(): st.markdown(f"- [{n}]({l})")
            if st.button("Sair"):
                st.session_state.acesso_vip = False
                st.rerun()
    
    elif modo == "Créditos":
        st.write("Desenvolvido por Edielson Samico.")

if __name__ == "__main__":
    main()
