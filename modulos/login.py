import streamlit as st
from config.conexion import verify_user

def show_login():
    """
    Muestra el formulario de login CONECTADO A BD REAL
    """
    st.title("🔐 Sistema de Gestión - Login")
    
    with st.form("login_form"):
        username = st.text_input("Usuario", placeholder="Ingrese su usuario")
        password = st.text_input("Contraseña", type="password", placeholder="Ingrese su contraseña")
        submit = st.form_submit_button("Iniciar Sesión")
        
        if submit:
            if not username or not password:
                st.error("❌ Por favor ingrese usuario y contraseña")
                return False
                
            user = verify_user(username, password)
            
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.success(f"✅ Bienvenido {user['usuario']}!")
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")
                
    return st.session_state.get('logged_in', False)
