import streamlit as st
import sys
import os
import importlib.util

# 🔥 CONFIGURACIÓN DE PÁGINA DEBE SER PRIMERO
st.set_page_config(
    page_title="Sistema de Gestión",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración de paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

st.success("✅ Cargando desde estructura real: modulos/")

# Función para cargar módulos manualmente
def load_module(module_name, file_path):
    """Carga un módulo desde una ruta específica"""
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        
        # 🔥 SOLUCIÓN: Hacer que 'config' esté disponible antes de ejecutar
        if 'config' not in sys.modules:
            # Crear un módulo config ficticio
            import types
            config_module = types.ModuleType('config')
            sys.modules['config'] = config_module
        
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        st.error(f"❌ Error cargando {module_name}: {e}")
        return None

# 🔥 CARGAR CONEXIÓN PRIMERO
try:
    st.info("🔄 Cargando módulo de conexión...")
    conexion_module = load_module('conexion', os.path.join(current_dir, 'modulos', 'config', 'conexion.py'))
    
    # Hacer que conexion esté disponible como config.conexion
    if 'config' not in sys.modules:
        import types
        sys.modules['config'] = types.ModuleType('config')
    
    sys.modules['config.conexion'] = conexion_module
    get_connection = conexion_module.get_connection
    verify_user = conexion_module.verify_user
    
    st.success("✅ Módulo de conexión cargado")
    
except Exception as e:
    st.error(f"❌ Error cargando conexión: {e}")
    st.stop()

# 🔥 CARGAR MÓDULOS DE modulos/
try:
    st.info("🔄 Cargando módulos de la aplicación...")
    
    # Función especial para cargar módulos que necesitan config
    def load_app_module(module_name, file_path):
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        
        # Inyectar config.conexion en el namespace del módulo
        module.__dict__['config'] = sys.modules['config']
        module.__dict__['get_connection'] = get_connection
        module.__dict__['verify_user'] = verify_user
        
        spec.loader.exec_module(module)
        return module
    
    # Cargar módulos de la aplicación
    login_module = load_app_module('login', os.path.join(current_dir, 'modulos', 'login.py'))
    menu_module = load_app_module('menu', os.path.join(current_dir, 'modulos', 'menu.py'))
    clientes_module = load_app_module('clientes', os.path.join(current_dir, 'modulos', 'clientes.py'))
    productos_module = load_app_module('productos', os.path.join(current_dir, 'modulos', 'productos.py'))
    ventas_module = load_app_module('ventas', os.path.join(current_dir, 'modulos', 'ventas.py'))
    
    # Asignar funciones
    show_login = login_module.show_login
    show_menu = menu_module.show_menu
    show_clientes = clientes_module.show_clientes
    show_productos = productos_module.show_productos
    show_ventas = ventas_module.show_ventas
    
    st.success("✅ Todos los módulos cargados correctamente")
    
except Exception as e:
    st.error(f"❌ Error cargando módulos: {e}")
    st.stop()

def show_dashboard():
    """
    Muestra el dashboard principal
    """
    st.title("📊 Dashboard Principal")
    
    try:
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Obtener estadísticas
                cursor.execute("SELECT COUNT(*) FROM clientes")
                total_clientes = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM productos")
                total_productos = cursor.fetchone()[0]
                
                cursor.execute("SELECT SUM(total) FROM ventas")
                total_ventas = cursor.fetchone()[0] or 0
                
                cursor.execute("SELECT COUNT(*) FROM ventas")
                numero_ventas = cursor.fetchone()[0]
                
                # Mostrar métricas
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("👥 Total Clientes", total_clientes)
                with col2:
                    st.metric("📦 Total Productos", total_productos)
                with col3:
                    st.metric("💰 Total Ventas", f"${total_ventas:,.2f}")
                with col4:
                    st.metric("🛒 N° de Ventas", numero_ventas)
                    
            except Exception as e:
                st.error(f"❌ Error cargando dashboard: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            st.warning("⚠️ No se pudo conectar a la base de datos")
                
    except Exception as e:
        st.error(f"❌ Error con la conexión: {e}")
    
    st.write("---")
    st.subheader("Bienvenido al Sistema de Gestión")
    st.write("""
    Utilice el menú lateral para navegar entre las diferentes secciones del sistema:
    
    - **👥 Gestión de Clientes**: Administre la información de sus clientes
    - **📦 Gestión de Productos**: Controle su inventario de productos
    - **💰 Gestión de Ventas**: Registre y consulte las ventas realizadas
    """)

def show_config():
    """
    Muestra la configuración del sistema
    """
    st.title("⚙️ Configuración del Sistema")
    
    if 'user' in st.session_state and st.session_state.user:
        st.info(f"**Usuario conectado:** {st.session_state.user['usuario']}")
    else:
        st.info("**Usuario conectado:** No disponible")
    
    st.info(f"**Base de datos:** Clever Cloud MySQL")
    
    st.write("---")
    st.subheader("Información del Sistema")
    st.write("""
    Esta aplicación fue desarrollada como parte de la Tarea #3 y incluye:
    
    - ✅ Autenticación de usuarios
    - ✅ Gestión de clientes, productos y ventas
    - ✅ Base de datos MySQL en Clever Cloud
    - ✅ Interfaz amigable con Streamlit
    """)

def main():
    """
    Función principal de la aplicación
    """
    # Inicializar estado de sesión
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Mostrar login si no está autenticado
    if not st.session_state.logged_in:
        show_login()
    else:
        # Mostrar menú y contenido principal
        selected_section = show_menu()
        
        # Navegación entre módulos
        if selected_section == "dashboard":
            show_dashboard()
        elif selected_section == "clientes":
            show_clientes()
        elif selected_section == "productos":
            show_productos()
        elif selected_section == "ventas":
            show_ventas()
        elif selected_section == "config":
            show_config()

if __name__ == "__main__":
    main()
