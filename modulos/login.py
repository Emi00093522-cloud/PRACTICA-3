import streamlit as st

def show_login():
    """
    Muestra el formulario de login SIMPLIFICADO para testing
    """
    st.title("🔐 Sistema de Gestión - Login")
    
    # 🔥 LOGIN SIMPLIFICADO PARA TESTING - ELIMINAR LUEGO
    with st.form("login_form"):
        username = st.text_input("Usuario", value="admin", placeholder="Ingrese 'admin'")
        password = st.text_input("Contraseña", type="password", value="admin123", placeholder="Ingrese 'admin123'")
        submit = st.form_submit_button("Iniciar Sesión")
        
        if submit:
            # Credenciales hardcodeadas para testing
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.user = {
                    "usuario": "admin", 
                    "email": "admin@example.com",
                    "id": 1
                }
                st.success("✅ ¡Login exitoso! (Modo testing)")
                st.rerun()
            else:
                st.error("❌ Use: Usuario: 'admin' / Contraseña: 'admin123'")
                
    return st.session_state.get('logged_in', False)
