import streamlit as st
import random
import re
import importlib
import hashlib
import string

# 1. FUNÇÃO DE LIMPEZA E HASH
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

# 2. APP PRINCIPAL
def main():
    st.set_page_config(page_title="Ambiente SAMICOIOT", layout="wide")

    # Inicialização de Estados
    if 'banco_questoes' not in st.session_state:
        st.session_state.banco_questoes = carregar_banco_unico()
        st.session_state.simulado_ativo = random.sample(st.session_state.banco_questoes, k=min(40, len(st.session_state.banco_questoes)))
    
    if 'acesso_vip' not in st.session_state:
        st.session_state.acesso_vip = False
    
    if 'senha_aleatoria' not in st.session_state:
        # Gera uma senha aleatória de 6 dígitos
        st.session_state.senha_aleatoria = ''.join(random.choices(string.digits, k=6))

    # MENU
    st.sidebar.title("Ambiente SAMICOIOT")
    modo = st.sidebar.radio("Selecione:", [
        "📖 Área de Treino (Geral)", 
        "🎯 Treino por Tópico (Focado)", 
        "⏱️ Simulado LPI (Prova Real 40 Q)",
        "🎁 Materiais VIP & Simulados",
        "ℹ️ Créditos & Desenvolvimento"
    ])

    # LÓGICA DE EXIBIÇÃO (Treinos iguais aos anteriores)
    if modo == "📖 Área de Treino (Geral)":
        st.title("📖 Área de Treino Geral")
        for q in st.session_state.banco_questoes:
            st.markdown(f"**{q['pergunta']}**")
            st.radio(f"t_{q['id']}", q['opcoes_fixas'], index=None, label_visibility="collapsed")
            st.divider()

    elif modo == "🎯 Treino por Tópico (Focado)":
        st.title("🎯 Treino por Tópico (Focado)")
        topicos = sorted(list(set(q.get('topico', 'Geral') for q in st.session_state.banco_questoes)))
        t = st.selectbox("Escolha o tópico:", topicos)
        for q in [q for q in st.session_state.banco_questoes if q.get('topico') == t]:
            st.markdown(f"**{q['pergunta']}**")
            st.radio(f"radio_{q['id']}_{t}", q['opcoes_fixas'], index=None, label_visibility="collapsed")
            st.divider()

    elif modo == "⏱️ Simulado LPI (Prova Real 40 Q)":
        st.title("⏱️ Simulado LPI (Prova Real 40 Q)")
        if st.button("Gerar novo simulado"):
            st.session_state.simulado_ativo = random.sample(st.session_state.banco_questoes, k=min(40, len(st.session_state.banco_questoes)))
            st.rerun()
        for i, q in enumerate(st.session_state.simulado_ativo):
            st.markdown(f"**{i+1}. {q['pergunta']}**")
            st.radio(f"sim_{q['id']}", q['opcoes_fixas'], key=f"ans_{i}", index=None, label_visibility="collapsed")
            st.divider()
            
    elif modo == "🎁 Materiais VIP & Simulados":
        st.title("🎁 Materiais VIP & Simulados")
        
        if not st.session_state.acesso_vip:
            st.subheader("Conteúdo Exclusivo")
            st.link_button("👉 INSCREVA-SE NO CANAL EDILSON SAMICO", "https://www.youtube.com/@EdielsonSamico?sub_confirmation=1")
            
            # Gerador de Senha Privado
            with st.expander("Sou inscrito, como obtenho a senha?"):
                st.write("Clique abaixo para gerar a senha de acesso atual:")
                if st.button("Gerar/Ver Senha do Dia"):
                    st.info(f"A senha atual é: **{st.session_state.senha_aleatoria}**")
            
            codigo = st.text_input("Insira o código gerado:", type="password")
            if st.button("Validar Acesso"):
                if codigo == st.session_state.senha_aleatoria:
                    st.session_state.acesso_vip = True
                    st.rerun()
                else:
                    st.error("Código incorreto.")
        else:
            st.success("Acesso VIP Liberado!")
            materiais = {"Guia LPI": "#", "Simulado Avançado": "#"}
            for nome, link in materiais.items():
                st.markdown(f"- [{nome}]({link})")
            if st.button("Sair da área VIP"):
                st.session_state.acesso_vip = False
                st.rerun()
        
    elif modo == "ℹ️ Créditos & Desenvolvimento":
        st.title("ℹ️ Créditos & Desenvolvimento")
        st.write("Desenvolvido por Edielson Samico - SAMICOIOT.")

if __name__ == "__main__":
    main()
