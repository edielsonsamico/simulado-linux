# --- NOVO MODO: CRÉDITOS & DESENVOLVIMENTO ---
if modo_selecionado == "ℹ️ Créditos & Desenvolvimento":
    st.title("ℹ️ Créditos & Desenvolvimento")
    st.write("Conheça o desenvolvedor responsável por esta plataforma de estudos e simulados.")
    
    # Renderização correta forçando a interpretação do HTML
    st.markdown("""
    <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; padding: 30px; border-radius: 12px; margin-top: 20px;">
        <h2 style="color: #1E3A8A; margin-top: 0px;">Edielson Samico</h2>
        <p style="font-size: 16px; color: #475569;">
            Desenvolvedor e entusiasta de tecnologia Linux, infraestrutura e criação de sistemas web interativos.
        </p>
        <hr style="border: 0; border-top: 1px dashed #CBD5E1; margin: 20px 0;">
        <h4 style="color: #0F172A; margin-bottom: 15px;">Entre em contacto:</h4>
        
        <div style="display: flex; flex-direction: column; gap: 12px; font-size: 16px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 20px;">💬</span>
                <a href="https://wa.me/5581987316454" target="_blank" style="color: #25D366; font-weight: bold; text-decoration: none;">
                    WhatsApp (81 98731-6454)
                </a>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 20px;">📸</span>
                <a href="https://instagram.com/edielsonsamico" target="_blank" style="color: #E1306C; font-weight: bold; text-decoration: none;">
                    Instagram (@edielsonsamico)
                </a>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 20px;">🎥</span>
                <a href="https://youtube.com/@EdielsonSamico" target="_blank" style="color: #FF0000; font-weight: bold; text-decoration: none;">
                    YouTube (@EdielsonSamico)
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)  # <--- O segredo para renderizar o código está aqui!
