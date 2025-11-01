import streamlit as st
from config.conexion import verify_user

def show_login():
    """
    Muestra el formulario de login y maneja la autenticación
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
            
            # 🔥 DEBUG: Mostrar información del usuario
            if user:
                st.write("🔍 DEBUG - Estructura del usuario:", user)
                
                # 🔥 SOLUCIÓN: Usar la clave correcta basada en la estructura real
                if 'usuario' in user:
                    nombre_usuario = user['usuario']
                elif 'Usuario' in user:
                    nombre_usuario = user['Usuario']
                elif 'user' in user:
                    nombre_usuario = user['user']
                else:
                    # Si no encontramos la clave, usar la primera disponible
                    claves_disponibles = list(user.keys())
                    nombre_usuario = user[claves_disponibles[1]] if len(claves_disponibles) > 1 else username
                
                st.session_state.logged_in = True
                st.session_state.user = user
                st.success(f"✅ Bienvenido {nombre_usuario}!")
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")
                
    return st.session_state.get('logged_in', False)
