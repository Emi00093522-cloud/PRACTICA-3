import streamlit as st
from config.conexion import verify_user

def show_login():
    """
    Muestra el formulario de login CONECTADO A BD REAL
    """
    st.title("🔐 Sistema de Gestión - Login")
    
    # ✅ EVITAR MÚLTIPLES EJECUCIONES
    if st.session_state.get('logged_in', False):
        return True
        
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Usuario", placeholder="Ingrese su usuario")
        password = st.text_input("Contraseña", type="password", placeholder="Ingrese su contraseña")
        submit = st.form_submit_button("Iniciar Sesión")
        
        if submit:
            if not username or not password:
                st.error("❌ Por favor ingrese usuario y contraseña")
                return False
                
            # Mostrar carga mientras verifica
            with st.spinner("Verificando credenciales..."):
                user = verify_user(username, password)
            
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.success(f"✅ Bienvenido {user['usuario']}!")
                # ✅ RETORNAR VERDADERO PERO DEJAR QUE app.py MANEJE EL RERUN
                return True
            else:
                st.error("❌ Usuario o contraseña incorrectos")
                return False
                
    return False
