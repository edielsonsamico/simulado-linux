import streamlit as st
import random
import re
import importlib
import hashlib
import string
import time

# Função de Limpeza de Questões
def gerar_hash_conteudo(pergunta):
    texto_limpo = re.sub(r'^(quest[ãa]o.*?\d+|q\d+|\d+)\s*[\.\:\-]?\s*', '', pergunta.strip(), flags=re.IGNORECASE)
    texto_limpo = " ".join(texto_limpo.lower().split())
    return hashlib.md5(texto_limpo.encode('utf-8')).hexdigest()

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
            banco_final[h] = q_copia
    return list(banco_final.values())

# App Principal
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
                st.metric("Tempo Restante", f"{tempo_restante // 60:02d}:{tempo_restante % 60:02d}")
            else:
                st.error("TEMPO ESGOTADO!")
                st.session_state.simulado_finalizado = True
            
            if st.button("Gerar novo simulado"):
                st.session_state.inicio_simulado = time.time()
                st.session_state.simulado_ativo = random.sample(st.session_state.banco_questoes, k=min(40, len(st.session_state.banco_questoes)))
                st.rerun()
                
            for i, q in enumerate(st.session_state.simulado_ativo):
                st.markdown(f"**{i+1}. {q['pergunta']}**")
                st.radio(f"sim_{q['id']}", q['opcoes_fixas'], key=f"ans_{i}", index=None, label_visibility="collapsed")
                st.divider()
            
            if st.button("Finalizar Simulado"):
                st.session_state.simulado_finalizado = True
                st.rerun()
        else:
            st.success("Simulado finalizado!")
            if st.button("Reiniciar"):
                st.session_state.simulado_finalizado = False
                st.session_state.inicio_simulado = time.time()
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
