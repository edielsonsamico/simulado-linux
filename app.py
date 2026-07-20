elif modo == "🎁 Materiais VIP & Simulados":
        st.title("🎁 Materiais VIP & Simulados")
        
        if not st.session_state.acesso_vip:
            st.subheader("Conteúdo Exclusivo para Inscritos")
            st.write("Para acessar nossos simulados e materiais, inscreva-se em nosso canal e valide seu acesso.")
            
            # Botão com sub_confirmation=1 para abrir o popup de inscrição automaticamente
            st.link_button(
                "👉 INSCREVA-SE NO CANAL EDILSON SAMICO", 
                "https://www.youtube.com/@EdielsonSamico?sub_confirmation=1"
            )
            
            st.write("---")
            codigo = st.text_input("Insira o código de validação recebido após a inscrição:", type="password")
            if st.button("Validar Acesso"):
                if codigo == "SAMICO123": # Altere este código conforme sua preferência
                    st.session_state.acesso_vip = True
                    st.rerun()
                else:
                    st.error("Código incorreto. Certifique-se de estar inscrito!")
        else:
            st.success("Acesso VIP Liberado!")
            materiais = {
                "Guia de Comandos LPI": "#",
                "Simulado LPI - Módulos Avançados": "#",
                "Área de Membros": "#"
            }
            for nome, link in materiais.items():
                st.markdown(f"- [{nome}]({link})")
            if st.button("Sair da área VIP"):
                st.session_state.acesso_vip = False
                st.rerun()
