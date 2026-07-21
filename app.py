elif modo == "Materiais VIP":
        st.markdown("## Central de Recursos VIP")
        st.markdown("---")
        
        if not st.session_state.acesso_vip:
            st.info("🔓 **Desbloqueie o Acesso VIP Completo!**\n\nTenha acesso a apostilas avançadas, guias de terminal e conteúdos exclusivos.")
            
            # Passo 1: Inscrição no Canal
            st.markdown("### Passo 1: Inscreva-se no Canal Oficial")
            if st.link_button("👉 INSCREVA-SE NO CANAL DO YOUTUBE", "https://www.youtube.com/@EdielsonSamico?sub_confirmation=1"):
                st.session_state.clicou_no_cadastro = True
                
            if st.session_state.clicou_no_cadastro:
                st.markdown("---")
                st.markdown("### Passo 2: Contribuição Simbólica via Pix")
                st.markdown("Faça um Pix no valor simbólico de **R$ 2,00** para apoiar o projeto:")
                st.code("sua-chave-pix-aqui@email.com", language="text") # Substitua pela sua chave Pix real
                
                st.markdown("---")
                st.markdown("### Passo 3: Validar Credencial")
                comprovante_input = st.text_input("Insira o código de liberação ou ID da transação Pix:", type="password")
                
                if st.button("Validar Acesso VIP"):
                    # Aqui você pode aceitar a senha gerada aleatoriamente ou uma senha padrão de confirmação do Pix
                    if comprovante_input == st.session_state.senha_aleatoria or comprovante_input == "vip2026":
                        st.session_state.acesso_vip = True
                        st.success("✅ Pagamento e inscrição confirmados com sucesso!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Código inválido. Verifique o comprovante ou gere uma chave válida.")
                
                # Botão opcional para gerar chave de teste/gerenciamento
                if st.button("Gerar Chave de Teste (Admin)"):
                    st.info(f"Chave gerada para teste: **{st.session_state.senha_aleatoria}**")
        else:
            st.success("🎉 **Bem-vindo à Área VIP Corporativa!** Acesso total liberado.")
            materiais = {
                "Apostila Master Linux Completa": "Apostila_Premium_de_Certificacao.pdf", 
                "Guia Definitivo LPIC-1 Terminal": "LPIC-1_Terminal_2026.pdf",
                "Banco de Questões Comentadas Avançadas": "Banco_Questoes_VIP.pdf"
            }
            for n, l in materiais.items(): 
                st.markdown(f"- 📥 [{n}]({l})")
                
            st.markdown("---")
            if st.button("Encerrar Sessão VIP"):
                st.session_state.acesso_vip = False
                st.rerun()
