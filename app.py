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
    """Infere a resposta correta com base no conteúdo da pergunta caso o banco não traga a chave."""
    p = pergunta.lower()
    
    # Mapeamento heurístico baseado nos temas comuns de Linux Essentials
    termos_chave = {
        "linha inteira": "dd", # editor vi comando para apagar linha (ex: dd)
        "pacotes atualmente instalados": "rpm -qa",
        "máxima criticidade": "emerg", # ou alert/panic
        "syslog": "emerg",
        "árvore genealógica": "pstree",
        "variável dita a rota": "display",
        "bibliotecas compartilhadas": "/etc/ld.so.conf",
        "redirecionamento envia a saída padrão": ">>",
        "protocolo de sincronização temporal": "123",
        "ordenada de forma alfabética": "order by",
        "inserção de novos dados": "insert into",
        "cláusula é usada para especificar uma condição": "where",
        "pausa a execução": "read",
        "proprietário usuário e o grupo": "chown",
        "primeiro processo": "init",
        "diretório padrão o sistema copia": "/etc/skel",
        "compactação": "gzip",
        "reiniciar a máquina": "reboot", # ou init 6
        "script executável em shell bash, qual parâmetro": "$1",
        "variável já carregada": "unset",
        "servidor x11": "/etc/x11/xorg.conf",
        "i18n": "iconv"
    }
    
    for chave, termo in termos_chave.items():
        if chave in p:
            for op in opcoes:
                if termo in op.lower():
                    return op
                    
    # Fallback padrão caso não encontre correspondência exata
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
            q_copia['opcoes_fixas'] = q.get('opcoes', []).copy()
            random.shuffle(q_copia['opcoes_fixas'])
            
            # Tenta achar a resposta em qualquer chave existente
            resp_encontrada = None
            for chave, valor in q.items():
                if any(termo in chave.lower() for termo in ['corret', 'resp', 'gabarit', 'answer', 'right', 'solucao']):
                    if valor is not None and str(valor).strip() != "":
                        val_str = str(valor).strip()
                        if val_str.isdigit() and 'opcoes' in q:
                            idx = int(val_str)
                            if 0 <= idx < len(q['opcoes']):
                                resp_encontrada = str(q['opcoes'][idx]).strip()
                                break
                        else:
                            resp_encontrada = val_str
                            break
            
            # Se o banco do tópico não tiver a resposta cadastrada, usa a inferência inteligente
            if not resp_encontrada:
                resp_encontrada = inferir_resposta_correta(q['pergunta'], q_copia['opcoes_fixas'])
                
            q_copia['resposta_oficial'] = resp_encontrada
            banco_final[h] = q_copia
            
    return list(banco_final.values())

def main():
    st.set_page_config(page_title="Ambiente SAMICOIOT", layout="wide")

    if 'banco_questoes' not in st.session_state:
        st.session_state.banco_questoes = carregar_banco_unico()
        st.session_state.simulado_ativo = random.sample(st.session_state.banco_questoes, k=min(40, len(st.session_state.banco_questoes)))
    
    if 'acesso_vip' not in st.session_state: st.session_state.acesso_vip = False
    if 'clicou_no_cadastro' not in st.session_state: st.session_state.clicou_no_cadastro = False
    if 'senha_aleatoria' not in st.session_state:
        st.session_state.senha_aleatoria = ''.join(random.choices(string.digits, k=6))
    if 'inicio_simulado' not in st.session_state:
        st.session_state.inicio_simulado = time.time()
    if 'simulado_finalizado' not in st.session_state:
        st.session_state.simulado_finalizado = False
    if 'respostas_usuario' not in st.session_state:
        st.session_state.respostas_usuario = {}

    st.sidebar.title("Ambiente SAMICOIOT")
    modo = st.sidebar.radio("Navegação:", [
        "Treino Geral", 
        "Treino por Tópico", 
        "Simulado LPI Oficial",
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
        
        if not st.session_state.simulado_finalizado:
            tempo_decorrido = int(time.time() - st.session_state.inicio_simulado)
            tempo_restante = TEMPO_OFICIAL - tempo_decorrido
            
            if tempo_restante > 0:
                st.metric("⏱️ Tempo Restante", f"{tempo_restante // 60:02d}:{tempo_restante % 60:02d}")
            else:
                st.error("TEMPO ESGOTADO!")
                st.session_state.simulado_finalizado = True
                st.rerun()
            
            if st.button("Gerar novo simulado"):
                st.session_state.inicio_simulado = time.time()
                st.session_state.simulado_ativo = random.sample(st.session_state.banco_questoes, k=min(40, len(st.session_state.banco_questoes)))
                st.session_state.respostas_usuario = {}
                st.rerun()
                
            for i, q in enumerate(st.session_state.simulado_ativo):
                st.markdown(f"**{i+1}. {q['pergunta']}**")
                
                opcoes = q['opcoes_fixas']
                resp_atual = st.session_state.respostas_usuario.get(i)
                idx_default = opcoes.index(resp_current) if (resp_current := resp_atual) in opcoes else None
                
                escolha = st.radio(f"sim_{i}_{q['id']}", opcoes, index=idx_default, label_visibility="collapsed")
                if escolha:
                    st.session_state.respostas_usuario[i] = escolha
                    
                st.divider()
            
            if st.button("Finalizar Simulado e Ver Gabarito"):
                st.session_state.simulado_finalizado = True
                st.rerun()
        else:
            st.success("🏁 Simulado Finalizado com Sucesso!")
            
            acertos = 0
            total_questoes = len(st.session_state.simulado_ativo)
            
            for i, q in enumerate(st.session_state.simulado_ativo):
                resposta_usuario = st.session_state.respostas_usuario.get(i)
                resposta_correta = q.get('resposta_oficial')
                
                if resposta_usuario and resposta_correta and (str(resposta_usuario).strip().lower() == str(resposta_correta).strip().lower()):
                    acertos += 1
            
            nota_final = (acertos / total_questoes) * 10 if total_questoes > 0 else 0
            
            st.metric("Sua Nota Final", f"{nota_final:.1f} / 10.0", f"{acertos} de {total_questoes} corretas")
            
            st.markdown("---")
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

            if st.button("Reiniciar / Novo Simulado"):
                st.session_state.simulado_finalizado = False
                st.session_state.inicio_simulado = time.time()
                st.session_state.simulado_ativo = random.sample(st.session_state.banco_questoes, k=min(40, len(st.session_state.banco_questoes)))
                st.session_state.respostas_usuario = {}
                st.rerun()
            
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
