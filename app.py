# --- MODO 2: TREINO POR TÓPICO E QTD PERSONALIZADA (CORRIGIDO) ---
elif modo_selecionado == "🎯 Treino por Tópico (Focado)":
    st.title("🎯 Bateria de Exercícios por Assunto")
    st.write("Foque seus estudos! Escolha o assunto específico e a quantidade exata de questões.")

    aba_filtro, aba_rank_filtro = st.tabs(["⚡ Configurar e Responder", "🏆 Líderes (Treino Focado)"])

    with aba_filtro:
        topicos_disponiveis = sorted(list(set(q['topico'] for q in QUESTOES_POOL)))
        topicos_disponiveis.insert(0, "Todos os Assuntos")
        
        col1, col2 = st.columns(2)
        with col1:
            assunto_escolhido = st.selectbox("📚 Escolha o Assunto:", topicos_disponiveis)
        with col2:
            qtd_escolhida = st.selectbox("🔢 Quantidade de Questões:", [10, 20, 30, 40])

        # Cria chaves de controle na memória de sessão para travar o sorteio
        chave_bateria = f"bateria_{assunto_escolhido}_{qtd_escolhida}"
        
        if "chave_atual_bateria" not in st.session_state or st.session_state.chave_atual_bateria != chave_bateria:
            if assunto_escolhido == "Todos os Assuntos":
                pool_filtrado = list(QUESTOES_POOL)
            else:
                pool_filtrado = [q for q in QUESTOES_POOL if q['topico'] == assunto_escolhido]
            
            random.shuffle(pool_filtrado)
            st.session_state.questoes_bateria_fixas = pool_filtrado[:min(qtd_escolhida, len(pool_filtrado))]
            st.session_state.chave_atual_bateria = chave_bateria

        questoes_bateria = st.session_state.questoes_bateria_fixas

        st.caption(f"Exibindo {len(questoes_bateria)} questões exclusivas sobre '{assunto_escolhido}'.")
        st.divider()

        acertos_focados = 0
        for idx, q in enumerate(questoes_bateria):
            st.markdown(f"**Questão {idx+1} [{q['topico']}]:** {q['pergunta']}")
            
            # Chave única para o rádio não perder o estado
            chave_radio = f"foco_{q['id']}_{assunto_escolhido}_{idx}"
            resp_focada = st.radio("Sua resposta:", q['opcoes'], key=chave_radio, index=None)
            
            if st.checkbox("💡 Corrigir e Ver Comentário", key=f"fococheck_{q['id']}_{assunto_escolhido}_{idx}"):
                if resp_focada == q['correta']:
                    st.success(f"✅ Correto! Resposta: {q['correta']}")
                    acertos_focados += 1
                else:
                    st.error(f"❌ Incorreto. Resposta certa: {q['correta']}")
                st.info(f"📘 **Comentário Técnico:** {q['explicacao']}")
            st.divider()

        col_btn1, col_col_btn2 = st.columns([1, 4])
        with col_btn1:
            if st.button("🏁 Registrar Bateria", type="primary"):
                if not nome_usuario:
                    st.warning("⚠️ Insira seu nome na barra lateral para registrar no placar!")
                elif len(questoes_bateria) == 0:
                    st.error("Nenhuma questão resolvida.")
                else:
                    score_focado = (acertos_focados / len(questoes_bateria)) * 100
                    st.session_state.ranking_topico[nome_usuario] = max(score_focado, st.session_state.ranking_topico.get(nome_usuario, 0))
                    st.success("Nota salva!")
                    time.sleep(0.5)
                    st.rerun()
        with col_col_btn2:
            if st.button("🔄 Sortear Novas Questões Deste Tópico"):
                # Força o sistema a limpar o cache antigo e sortear perguntas novas
                if "chave_atual_bateria" in st.session_state:
                    del st.session_state.chave_atual_bateria
                st.rerun()
