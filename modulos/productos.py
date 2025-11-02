import streamlit as st
from config.conexion import get_connection

def show_productos():
    st.header("📦 Gestión de Productos")
    
    tab1, tab2 = st.tabs(["📋 Ver Productos", "➕ Agregar Producto"])
    
    with tab1:
        ver_productos()
    with tab2:
        agregar_producto_simple()

def agregar_producto_simple():
    """
    Versión SUPER simple que garantiza un solo INSERT
    """
    st.subheader("Agregar Nuevo Producto")
    
    # Usar un key único en el formulario
    with st.form("form_producto_unico", clear_on_submit=True):
        nombre = st.text_input("Nombre *")
        descripcion = st.text_area("Descripción")
        precio = st.number_input("Precio *", min_value=0.1, step=0.1)
        stock = st.number_input("Stock *", min_value=0, value=1)
        categoria = st.selectbox("Categoría", ["Electrónicos", "Ropa", "Hogar", "Deportes", "Otros"])
        
        guardar = st.form_submit_button("💾 Guardar Producto")
        
        if guardar:
            # Validar
            if not nombre.strip():
                st.error("❌ Nombre requerido")
                return
                
            # CONEXIÓN Y INSERT ÚNICO
            conn = get_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    sql = """
                        INSERT INTO productos (nombre, descripcion, precio, stock, categoria) 
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        nombre.strip(), 
                        descripcion.strip() or None, 
                        precio, 
                        stock, 
                        categoria
                    ))
                    conn.commit()
                    
                    st.success("✅ ¡Producto guardado exitosamente!")
                    st.info("🔃 Recargando página...")
                    
                    # Esperar un momento y recargar
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                finally:
                    cursor.close()
                    conn.close()

def ver_productos():
    """ (Mismo código que arriba) """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM productos ORDER BY fecha_creacion DESC")
            productos = cursor.fetchall()
            
            if productos:
                st.subheader(f"Total de productos: {len(productos)}")
                for producto in productos:
                    with st.expander(f"📦 {producto['nombre']} - ${producto['precio']:.2f}"):
                        st.write(f"**Descripción:** {producto['descripcion']}")
                        st.write(f"**Precio:** ${producto['precio']:.2f}")
                        st.write(f"**Stock:** {producto['stock']} unidades")
                        st.write(f"**Categoría:** {producto['categoria']}")
                        
                        if st.button("Eliminar", key=f"delete_{producto['id']}"):
                            eliminar_producto(producto['id'])
            else:
                st.info("No hay productos")
                
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

def eliminar_producto(producto_id):
    """ (Mismo código que arriba) """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
            conn.commit()
            st.success("✅ Producto eliminado")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()
