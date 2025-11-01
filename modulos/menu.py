import streamlit as st

def show_menu():
    """
    Muestra el menú lateral de navegación
    """
    st.sidebar.title("🏢 Sistema de Gestión")
    st.sidebar.write(f"Usuario: **{st.session_state.user['usuario']}**")
    st.sidebar.write("---")
    
    # Opciones del menú
    menu_options = {
        "📊 Dashboard": "dashboard",
        "👥 Gestión de Clientes": "clientes", 
        "📦 Gestión de Productos": "productos",
        "💰 Gestión de Ventas": "ventas",
        "⚙️ Configuración": "config"
    }
    
    selected = st.sidebar.radio("Navegación", list(menu_options.keys()))
    
    # Botón de cerrar sesión
    st.sidebar.write("---")
    if st.sidebar.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()
    
    return menu_options[selected]
