import streamlit as st
from config.conexion import get_connection

def show_productos():
    """
    Módulo de gestión de productos
    """
    st.header("📦 Gestión de Productos")
    
    tab1, tab2 = st.tabs(["📋 Ver Productos", "➕ Agregar Producto"])
    
    with tab1:
        ver_productos()
    
    with tab2:
        agregar_producto()

def ver_productos():
    """
    Muestra la lista de productos existentes
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM productos ORDER BY fecha_creacion DESC")
            productos = cursor.fetchall()
            
            if productos:
                st.subheader(f"Total de productos: {len(productos)}")
                
                for producto in productos:
                    with st.expander(f"📦 {producto['nombre']} - ${producto['precio']:.2f}", expanded=False):
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            st.write(f"**Descripción:** {producto['descripcion'] or 'Sin descripción'}")
                            st.write(f"**Categoría:** {producto['categoria'] or 'Sin categoría'}")
                        
                        with col2:
                            st.write(f"**Precio:** ${producto['precio']:.2f}")
                            st.write(f"**Stock:** {producto['stock']} unidades")
                        
                        with col3:
                            st.write(f"**ID:** {producto['id']}")
                            st.write(f"**Creado:** {producto['fecha_creacion'].strftime('%d/%m/%Y')}")
                            
                            # Usar estado de sesión para evitar múltiples ejecuciones
                            if st.button("🗑️ Eliminar", key=f"del_prod_{producto['id']}"):
                                if f"deleting_{producto['id']}" not in st.session_state:
                                    st.session_state[f"deleting_{producto['id']}"] = True
                                    eliminar_producto(producto['id'])
            else:
                st.info("📝 No hay productos registrados")
                
        except Exception as e:
            st.error(f"❌ Error cargando productos: {e}")
        finally:
            cursor.close()
            conn.close()

def agregar_producto():
    """
    Formulario para agregar nuevo producto
    """
    st.subheader("Agregar Nuevo Producto")
    
    # Inicializar estado del formulario
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False
    
    with st.form("producto_form", clear_on_submit=True):
        nombre = st.text_input("Nombre del producto *", placeholder="Ej: Laptop Gaming")
        descripcion = st.text_area("Descripción", placeholder="Ej: Laptop para gaming con 16GB RAM")
        precio = st.number_input("Precio *", min_value=0.0, step=0.1, format="%.2f")
        stock = st.number_input("Stock *", min_value=0, step=1)
        categoria = st.selectbox("Categoría", ["", "Electrónicos", "Ropa", "Hogar", "Deportes", "Otros"])
        
        submitted = st.form_submit_button("💾 Guardar Producto")
        
        if submitted:
            # Verificar si ya fue enviado
            if st.session_state.form_submitted:
                st.warning("⏳ El producto ya está siendo guardado...")
                return
                
            if not nombre.strip() or precio <= 0:
                st.error("❌ Nombre y precio son obligatorios (precio debe ser mayor a 0)")
                return
                
            # Marcar como enviado
            st.session_state.form_submitted = True
            
            conn = get_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO productos (nombre, descripcion, precio, stock, categoria) VALUES (%s, %s, %s, %s, %s)",
                        (nombre.strip(), descripcion.strip() if descripcion else None, precio, stock, categoria if categoria else None)
                    )
                    conn.commit()
                    st.success("✅ Producto agregado correctamente")
                    
                    # Limpiar el estado después de un éxito
                    st.session_state.form_submitted = False
                    
                    # Forzar rerun después de un breve delay
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error guardando producto: {e}")
                    # Resetear el estado en caso de error
                    st.session_state.form_submitted = False
                finally:
                    cursor.close()
                    conn.close()

def eliminar_producto(producto_id):
    """
    Elimina un producto de la base de datos
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
            conn.commit()
            st.success("✅ Producto eliminado correctamente")
            
            # Limpiar el estado de eliminación
            if f"deleting_{producto_id}" in st.session_state:
                del st.session_state[f"deleting_{producto_id}"]
                
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error eliminando producto: {e}")
            # Limpiar el estado en caso de error
            if f"deleting_{producto_id}" in st.session_state:
                del st.session_state[f"deleting_{producto_id}"]
        finally:
            cursor.close()
            conn.close()
