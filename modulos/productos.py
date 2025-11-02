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
                            st.write(f"**Stock actual:** {producto['stock']} unidades")
                            
                            # 🔹 NUEVO: formulario para agregar stock
                            with st.form(f"form_stock_{producto['id_producto']}", clear_on_submit=True):
                                cantidad_agregar = st.number_input(
                                    "Cantidad a agregar",
                                    min_value=1,
                                    step=1,
                                    key=f"stock_input_{producto['id_producto']}"
                                )
                                submitted_stock = st.form_submit_button("➕ Agregar Stock")
                                
                                if submitted_stock:
                                    agregar_stock(producto['id_producto'], cantidad_agregar)
                        
                        with col3:
                            st.write(f"**ID:** {producto['id_producto']}")
                            if producto['fecha_creacion']:
                                st.write(f"**Creado:** {producto['fecha_creacion'].strftime('%d/%m/%Y')}")
                            
                            # Botón eliminar
                            if st.button("🗑️ Eliminar", key=f"del_prod_{producto['id_producto']}"):
                                eliminar_producto(producto['id_producto'])
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
    
    with st.form("producto_form", clear_on_submit=True):
        nombre = st.text_input("Nombre del producto *", placeholder="Ej: Laptop Gaming")
        descripcion = st.text_area("Descripción", placeholder="Ej: Laptop para gaming con 16GB RAM")
        precio = st.number_input("Precio *", min_value=0.0, step=0.1, format="%.2f")
        stock = st.number_input("Stock *", min_value=0, step=1)
        categoria = st.selectbox("Categoría", ["", "Electrónicos", "Ropa", "Hogar", "Deportes", "Otros"])
        
        submitted = st.form_submit_button("💾 Guardar Producto")
        
        if submitted:
            if not nombre.strip() or precio <= 0:
                st.error("❌ Nombre y precio son obligatorios (precio debe ser mayor a 0)")
                return
                
            conn = get_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    
                    # Verificar si el producto ya existe
                    cursor.execute("SELECT id_producto FROM productos WHERE nombre = %s", (nombre.strip(),))
                    if cursor.fetchone():
                        st.error("❌ Ya existe un producto con ese nombre")
                        return
                    
                    # Insertar nuevo producto
                    cursor.execute(
                        "INSERT INTO productos (nombre, descripcion, precio, stock, categoria) VALUES (%s, %s, %s, %s, %s)",
                        (nombre.strip(), descripcion.strip() if descripcion else None, precio, stock, categoria if categoria else None)
                    )
                    conn.commit()
                    st.success("✅ Producto agregado correctamente")
                    st.balloons()
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error guardando producto: {e}")
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
            cursor.execute("DELETE FROM productos WHERE id_producto = %s", (producto_id,))
            conn.commit()
            st.success("✅ Producto eliminado correctamente")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error eliminando producto: {e}")
        finally:
            cursor.close()
            conn.close()

def agregar_stock(producto_id, cantidad):
    """
    Incrementa el stock de un producto existente
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Actualizar stock sumando la cantidad
            cursor.execute(
                "UPDATE productos SET stock = stock + %s WHERE id_producto = %s",
                (cantidad, producto_id)
            )
            conn.commit()
            st.success(f"✅ Se agregaron {cantidad} unidades al stock")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error al agregar stock: {e}")
        finally:
            cursor.close()
            conn.close()
