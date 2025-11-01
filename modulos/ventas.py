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
                LEFT JOIN clientes c ON v.cliente_id = c.id
                LEFT JOIN productos p ON v.producto_id = p.id
                ORDER BY v.fecha_venta DESC
            """)
            ventas = cursor.fetchall()
            
            if ventas:
                st.subheader(f"Total de ventas registradas: {len(ventas)}")
                
                # Métricas
                total_ventas = sum(venta['total'] for venta in ventas)
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("💰 Total Recaudado", f"${total_ventas:,.2f}")
                with col2:
                    st.metric("📈 Número de Ventas", len(ventas))
                
                st.write("---")
                
                # Lista de ventas
                for venta in ventas:
                    with st.expander(f"🛒 Venta #${venta['id']} - ${venta['total']:.2f} - {venta['fecha_venta'].strftime('%d/%m/%Y')}", expanded=False):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Cliente:** {venta['cliente_nombre'] or 'N/A'}")
                            st.write(f"**Producto:** {venta['producto_nombre'] or 'N/A'}")
                        with col2:
                            st.write(f"**Cantidad:** {venta['cantidad']}")
                            st.write(f"**Precio Unitario:** ${venta['precio']:.2f}")
                            st.write(f"**Fecha:** {venta['fecha_venta'].strftime('%d/%m/%Y %H:%M')}")
            else:
                st.info("📝 No hay ventas registradas")
                
        except Exception as e:
            st.error(f"❌ Error cargando ventas: {e}")
        finally:
            cursor.close()
            conn.close()

def nueva_venta():
    """
    Formulario para registrar nueva venta
    """
    st.subheader("Registrar Nueva Venta")
    
    conn = get_connection()
    if conn:
        try:
            # Obtener datos necesarios
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, nombre FROM clientes ORDER BY nombre")
            clientes = cursor.fetchall()
            
            cursor.execute("SELECT id, nombre, precio, stock FROM productos WHERE stock > 0 ORDER BY nombre")
            productos = cursor.fetchall()
            
            if not clientes:
                st.warning("⚠️ No hay clientes registrados. Primero registre al menos un cliente.")
                return
                
            if not productos:
                st.warning("⚠️ No hay productos con stock disponible.")
                return
            
            with st.form("venta_form"):
                # Selector de cliente
                cliente_options = {f"{c['nombre']} (ID: {c['id']})": c['id'] for c in clientes}
                cliente_seleccionado = st.selectbox(
                    "Cliente *",
                    options=list(cliente_options.keys())
                )
                cliente_id = cliente_options[cliente_seleccionado]
                
                # Selector de producto
                producto_options = {f"{p['nombre']} - ${p['precio']:.2f} (Stock: {p['stock']})": p['id'] for p in productos}
                producto_seleccionado = st.selectbox(
                    "Producto *",
                    options=list(producto_options.keys())
                )
                producto_id = producto_options[producto_seleccionado]
                
                # Cantidad
                producto_stock = next(p['stock'] for p in productos if p['id'] == producto_id)
                cantidad = st.number_input("Cantidad *", min_value=1, max_value=producto_stock, step=1)
                
                # Mostrar resumen
                producto_precio = next(p['precio'] for p in productos if p['id'] == producto_id)
                total = cantidad * producto_precio
                
                st.info(f"**Total a pagar:** ${total:.2f}")
                
                submitted = st.form_submit_button("💾 Registrar Venta")
                
                if submitted:
                    # Registrar venta
                    cursor.execute(
                        "INSERT INTO ventas (cliente_id, producto_id, cantidad, total) VALUES (%s, %s, %s, %s)",
                        (cliente_id, producto_id, cantidad, total)
                    )
                    
                    # Actualizar stock
                    cursor.execute(
                        "UPDATE productos SET stock = stock - %s WHERE id = %s",
                        (cantidad, producto_id)
                    )
                    
                    conn.commit()
                    st.success("✅ Venta registrada correctamente")
                    st.rerun()
                    
        except Exception as e:
            st.error(f"❌ Error registrando venta: {e}")
        finally:
            cursor.close()
            conn.close()
