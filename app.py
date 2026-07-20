import streamlit as st
import random
import time
import os

# ==========================================
# 1. FUNÇÕES DE APOIO E EMBARALHAMENTO
# ==========================================
def embaralhar_opcoes(questao):
    """Cria uma cópia da questão com as opções embaralhadas."""
    opcoes = questao['opcoes'].copy()
    correta = questao['correta']
    random.shuffle(opcoes)
    return {**questao, 'opcoes': opcoes, 'correta': correta}

# (Mantenha aqui as funções gerenciar_acesso_e_obter_metricas, normalizar_texto, desduplicar_questoes do código anterior)

# ==========================================
# 2. LOGIC DE QUIZ (APLICADA EM TODOS OS MODOS)
# ==========================================
# Sempre que for exibir uma questão, use:
# q = embaralhar_opcoes(q_original)
# st.radio("Alternativas:", q['opcoes'], ...)

# ==========================================
# 3. EXEMPLO DE APLICAÇÃO NO TREINO POR TÓPICO
# ==========================================
# Substitua o bloco do "Treino por Tópico (Focado)" no seu código por este:

elif modo_selecionado == "🎯 Treino por Tópico (Focado)":
    st.title("🎯 Treino Direcionado por Tópicos")
    topicos_disponiveis = sorted(list(set([q['topico'] for q in QUESTOES_POOL])))
    topico_escolhido = st.selectbox("Escolha o tópico desejado:", topicos_disponiveis)
    questoes_filtradas = [q for q in QUESTOES_POOL if q['topico'] == topico_escolhido]
    
    for idx, q_orig in enumerate(questoes_filtradas):
        # EMBARALHA AS OPÇÕES A CADA RENDERIZAÇÃO
        q = embaralhar_opcoes(q_orig) 
        
        st.markdown(f"### Questão {idx + 1}")
        st.markdown(f"**{q['pergunta']}**")
        
        resposta = st.radio("Selecione a alternativa:", q['opcoes'], index=None, key=f"f_{idx}")
        if resposta:
            if resposta == q['correta']:
                st.success("🎯 Correto!")
            else:
                st.error(f"❌ Errado. Correto: **{q['correta']}**")
        st.divider()

# ==========================================
# APLIQUE O MESMO PADRÃO (q = embaralhar_opcoes(q_orig)) 
# EM TODAS AS ABAS DE TREINO E SIMULADO DO SEU CÓDIGO
# ==========================================
