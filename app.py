elif modo == "⏱️ Simulado LPI (Prova Real 40 Q)":
        st.title("⏱️ Simulado LPI (Prova Real 40 Q)")
        
        # Define tempo oficial em segundos (60 minutos)
        TEMPO_OFICIAL = 60 * 60 
        
        if not st.session_state.simulado_finalizado:
            # Lógica de cronômetro regressivo
            tempo_decorrido = int(time.time() - st.session_state.inicio_simulado)
            tempo_restante = TEMPO_OFICIAL - tempo_decorrido
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if tempo_restante > 0:
                    minutos = tempo_restante // 60
                    segundos = tempo_restante % 60
                    st.metric("Tempo Restante", f"{minutos:02d}:{segundos:02d}")
                else:
                    st.error("TEMPO ESGOTADO!")
                    st.session_state.simulado_finalizado = True
                    st.rerun()
            
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
            if st.button("Reiniciar Simulado"):
                st.session_state.simulado_finalizado = False
                st.session_state.inicio_simulado = time.time()
                st.rerun()
