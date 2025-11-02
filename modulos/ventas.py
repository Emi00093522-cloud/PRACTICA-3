import streamlit as st
from config.conexion import get_connection

def show_ventas():
    """
    Módulo de gestión de ventas
    """
    st.header("💰 Gestión de Ventas")
    
    tab1, tab2 = st.tabs(["📋 Ver Ventas", "➕ Nueva Venta"])
    
    with tab1:
        ver_ventas()
    
    with tab2:
        nueva_venta()

def ver_ventas():
    """
    Muestra el historial de ventas
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT v.*, c.nombre as cliente_nombre, p.nombre as producto_nombre, p.precio
                FROM ventas v
                LEFT JOIN clientes c ON v.id_cliente = c.id_cliente
                LEFT JOIN productos p ON v.id_producto = p.id_producto
                ORDER BY v.fecha_venta DESC
            """)
            ventas = cursor.fetchall()
            
            if ventas:
                st.subheader(f"Total de ventas registradas: {len(ventas)}")
                
                total_ventas = sum(venta['total'] for venta in ventas)
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("💰 Total Recaudado", f"${total_ventas:,.2f}")
                with col2:
                    st.metric("📈 Número de Ventas", len(ventas))
                
                st.write("---")
                
                for venta in ventas:
                    with st.expander(f"🛒 Venta #{venta['id_venta']} - ${venta['total']:.2f} - {venta['fecha_venta'].strftime('%d/%m/%Y')}", expanded=False):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Cliente:** {venta['cliente_nombre'] or 'N/A'}")
                            st.write(f"**Producto:** {venta['producto_nombre'] or 'N/A'}")
                        with col2:
                            st.write(f"**Cantidad:** {venta['cantidad']}")
                            st.write(f"**Precio Unitario:** ${venta['precio']:.2f}")
                            st.write(f"**Fecha:** {venta['fecha_venta'].strftime('%d/%m/%Y %H:%M')}")
                            
                        if st.button("🗑️ Eliminar", key=f"del_venta_{venta['id_venta']}"):
                            eliminar_venta(venta['id_venta'])
            else:
                st.info("📝 No hay ventas registradas")
                
        except Exception as e:
            st.error(f"❌ Error cargando ventas: {e}")
        finally:
            cursor.close()
            conn.close()

def nueva_venta():
    """
    Formulario para registrar nueva venta (sin duplicaciones)
    """
    st.subheader("Registrar Nueva Venta")

    # 🚫 Evitar que se repita tras recargar
    if st.session_state.get("venta_registrada", False):
        st.session_state["venta_registrada"] = False
        st.rerun()
        return
    
    conn = get_connection()
    if not conn:
        st.error("❌ No se pudo conectar a la base de datos")
        return
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_cliente, nombre FROM clientes ORDER BY nombre")
        clientes = cursor.fetchall()
        
        cursor.execute("SELECT id_producto, nombre, precio, stock FROM productos WHERE stock > 0 ORDER BY nombre")
        productos = cursor.fetchall()
        
    except Exception as e:
        st.error(f"❌ Error cargando datos: {e}")
        return
    finally:
        cursor.close()
        conn.close()
    
    if not clientes:
        st.warning("⚠️ No hay clientes registrados. Primero registre al menos un cliente.")
        return
        
    if not productos:
        st.warning("⚠️ No hay productos con stock disponible.")
        return
    
    with st.form("venta_form", clear_on_submit=True):
        cliente_options = {f"{c['nombre']}": c['id_cliente'] for c in clientes}
        cliente_seleccionado = st.selectbox("Cliente *", options=list(cliente_options.keys()))
        cliente_id = cliente_options[cliente_seleccionado]
        
        producto_options = {f"{p['nombre']} - ${p['precio']:.2f} (Stock: {p['stock']})": p['id_producto'] for p in productos}
        producto_seleccionado = st.selectbox("Producto *", options=list(producto_options.keys()))
        producto_id = producto_options[producto_seleccionado]
        
        producto_stock = next(p['stock'] fo_

