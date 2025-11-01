import streamlit as st
import sys
import os

# Configurar el path de manera absoluta
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Verificar que los archivos existen
def verificar_archivos():
    archivos_requeridos = [
        'modules/login.py',
        'modules/menu.py', 
        'modules/clientes.py',
        'modules/productos.py',
        'modules/ventas.py',
        'config/conexion.py'
    ]
    
    for archivo in archivos_requeridos:
        ruta_completa = os.path.join(current_dir, archivo)
        if os.path.exists(ruta_completa):
            st.success(f"✅ {archivo} - EXISTE")
        else:
            st.error(f"❌ {archivo} - NO EXISTE")
            return False
    return True

# Verificar archivos primero
if not verificar_archivos():
    st.error("❌ Faltan archivos críticos. No se puede continuar.")
    st.stop()

# IMPORTACIÓN ABSOLUTA - Método más confiable
try:
    # Crear un sistema de importación manual
    import importlib.util
    
    def importar_modulo(nombre, ruta):
        spec = importlib.util.spec_from_file_location(nombre, ruta)
        modulo = importlib.util.module_from_spec(spec)
        
        # Ejecutar el módulo en un namespace específico
        spec.loader.exec_module(modulo)
        return modulo
    
    # Cargar conexión primero
    conexion_path = os.path.join(current_dir, 'config', 'conexion.py')
    conexion_mod = importar_modulo('conexion', conexion_path)
    
    # Cargar módulos de la carpeta modules
    login_mod = importar_modulo('login', os.path.join(current_dir, 'modules', 'login.py'))
    menu_mod = importar_modulo('menu', os.path.join(current_dir, 'modules', 'menu.py'))
    clientes_mod = importar_modulo('clientes', os.path.join(current_dir, 'modules', 'clientes.py'))
    productos_mod = importar_modulo('productos', os.path.join(current_dir, 'modules', 'productos.py'))
    ventas_mod = importar_modulo('ventas', os.path.join(current_dir, 'modules', 'ventas.py'))
    
    # Asignar las funciones
    show_login = login_mod.show_login
    show_menu = menu_mod.show_menu
    show_clientes = clientes_mod.show_clientes
    show_productos = productos_mod.show_productos
    show_ventas = ventas_mod.show_ventas
    get_connection = conexion_mod.get_connection
    verify_user = conexion_mod.verify_user
    
    st.success("✅ Todos los módulos importados correctamente!")
    
except Exception as e:
    st.error(f"❌ Error en la importación: {str(e)}")
    import traceback
    st.code(traceback.format_exc())
    st.stop()

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Gestión",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
