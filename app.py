else:
        # Área VIP Liberada!
        st.success("🎉 Parabéns! Seus conteúdos e recursos VIP estão totalmente desbloqueados.")
        
        col_apostila, col_simulado_vip = st.columns(2)
        
        with col_apostila:
            with st.container(border=True):
                st.subheader("📚 Apostila de Certificação VIP")
                st.write("Material completo cobrando comandos Linux essenciais, mapas mentais de arquitetura de diretórios e guias de redes.")
                # Link para o PDF que foi gerado na mesma pasta
                st.link_button("📥 Baixar Apostila (PDF)", "https://github.com/EdielsonSamico", use_container_width=True)
                st.caption("Dica: Você pode hospedar o PDF no seu Drive/GitHub e colar o link aqui.")
                
        with col_simulado_vip:
            with st.container(border=True):
                st.subheader("🏆 Simulado VIP Avançado")
                st.write("Questões de nível de dificuldade elevado selecionadas e comentadas para testar seus limites reais antes da prova.")
                
                # LINK OFICIAL SOLICITADO INTEGRADO NO BOTÃO VIP
                st.link_button(
                    "🚀 Abrir Simulado VIP", 
                    "https://notebooklm.google.com/notebook/5c438fb6-d069-4b7f-b64c-542d53add525/artifact/f5d7b6b8-9e48-4582-bbe8-e491bb4171c9?utm_source=nlm_web_share&utm_medium=google_oo&utm_campaign=art_share_1&utm_content=&utm_smc=nlm_web_share_google_oo_art_share_1_", 
                    use_container_width=True,
                    type="primary"
                )
                st.caption("Link externo integrado com sucesso na plataforma SAMICOIOT.")
