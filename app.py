# --- MODO 1: ÁREA DE TREINAMENTO GERAL (CONTINUAÇÃO) ---
if modo_selecionado == "📖 Área de Treino (Geral)":
    st.title("📖 Área de Treino e Fixação Técnica")
    st.write("Responda às questões abaixo. O feedback é exibido em tempo real para cada questão.")

    questoes_treino = st.session_state.questoes_treino
    total_acertos_treino = 0

    for idx, q in enumerate(questoes_treino):
        st.markdown(f"### Questão {idx + 1} | `{q['topico']}`")
        st.markdown(f"**{q['pergunta']}**")
        
        # Recupera resposta anterior se houver
        chave_resposta = f"treino_{q['id']}"
        indice_padrao = None
        if chave_resposta in st.session_state.respostas_treino_salvas:
            if st.session_state.respostas_treino_salvas[chave_resposta] in q['opcoes']:
                indice_padrao = q['opcoes'].index(st.session_state.respostas_treino_salvas[chave_resposta])

        resposta = st.radio(
            f"Selecione a opção da Questão {idx + 1}:",
            q['opcoes'],
            index=indice_padrao,
            key=f"radio_treino_{q['id']}"
        )
        
        st.session_state.respostas_treino_salvas[chave_resposta] = item_selecionado = resposta

        # Validação imediata (Modo Treino)
        if item_selecionado:
            if item_selecionado == q['correta']:
                st.success("🎯 Resposta Correta!")
                total_acertos_treino += 1
            else:
                st.error(f"❌ Resposta Incorreta. A alternativa certa é: **{q['correta']}**")
            
            with st.expander("📚 Ver Explicação Técnica"):
                st.info(q['explicacao'])
        
        st.divider()

    # Atualiza ranking de treino se o nome do usuário estiver preenchido
    if nome_usuario:
        st.session_state.ranking_treino[nome_usuario] = f"{total_acertos_treino}/{len(questoes_treino)}"

# --- MODO 2: TREINO POR TÓPICO ---
elif modo_selecionado == "🎯 Treino por Tópico (Focado)":
    st.title("🎯 Treino Direcionado por Tópicos")
    
    # Extrai os tópicos únicos disponíveis no pool
    topicos_disponiveis = sorted(list(set([q['topico'] for q in QUESTOES_POOL])))
    topico_escolhido = st.selectbox("Escolha o tópico que deseja dominar:", topicos_disponiveis)
    
    questoes_filtradas = [q for q in QUESTOES_POOL if q['topico'] == topico_escolhido]
    st.write(f"Encontradas **{len(questoes_filtradas)}** questões para este tópico.")
    
    total_acertos_topico = 0
    
    for idx, q in enumerate(questoes_filtradas):
        st.markdown(f"### Questão {idx + 1}")
        st.markdown(f"**{q['pergunta']}**")
        
        resposta = st.radio(
            f"Opções para a Questão {idx + 1}:",
            q['opcoes'],
            index=None,
            key=f"radio_topico_{q['id']}"
        )
        
        if resposta:
            if resposta == q['correta']:
                st.success("🎯 Correto!")
                total_acertos_topico += 1
            else:
                st.error(f"❌ Erro! Alternativa correta: **{q['correta']}**")
            
            with st.expander("📚 Detalhes do Conceito"):
                st.info(q['explicacao'])
        st.divider()

    if nome_usuario and len(questoes_filtradas) > 0:
        st.session_state.ranking_topico[nome_usuario] = f"{total_acertos_topico}/{len(questoes_filtradas)}"

# --- MODO 3: SIMULADO LPI ---
elif modo_selecionado == "⏱️ Simulado LPI (Prova Real 40 Q)":
    st.title("⏱️ Simulado Preparatório LPI")
    st.write("Regras da Prova: O gabarito e as explicações só aparecem após o envio definitivo.")

    if not st.session_state.tempo_inicio_simulado:
        st.session_state.tempo_inicio_simulado = time.time()

    questoes_simulado = st.session_state.questoes_simulado
    
    # Renderização do caderno de prova
    for idx, q in enumerate(questoes_simulado):
        st.markdown(f"##### {idx + 1}. {q['pergunta']}")
        
        resposta =
