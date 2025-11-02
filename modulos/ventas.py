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
    Formulario para registrar nueva venta - SOLUCIÓN DEFINITIVA
    """
    st.subheader("Registrar Nueva Venta")

    # ✅ SOLUCIÓN: Usar un estado único para controlar la venta
    if 'venta_procesada' not in st.session_state:
        st.session_state.venta_procesada = False
    
    # ✅ Si ya se procesó una venta en esta ejecución, no hacer nada
    if st.session_state.venta_procesada:
        st.success("✅ Venta registrada exitosamente!")
        if st.button("🔄 Registrar otra venta"):
            st.session_state.venta_procesada = False
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
    
    # ✅ FORMULARIO CON clear_on_submit=True
    with st.form("venta_form", clear_on_submit=True):
        cliente_options = {f"{c['nombre']}": c['id_cliente'] for c in clientes}
        cliente_seleccionado = st.selectbox("Cliente *", options=list(cliente_options.keys()))
        cliente_id = cliente_options[cliente_seleccionado]
        
        producto_options = {f"{p['nombre']} - ${p['precio']:.2f} (Stock: {p['stock']})": p['id_producto'] for p in productos}
        producto_seleccionado = st.selectbox("Producto *", options=list(producto_options.keys()))
        producto_id = producto_options[producto_seleccionado]
        
        producto_stock = next(p['stock'] for p in productos if p['id_producto'] == producto_id)
        cantidad = st.number_input("Cantidad *", min_value=1, max_value=producto_stock, step=1)
        
        producto_precio = next(p['precio'] for p in productos if p['id_producto'] == producto_id)
        total = cantidad * producto_precio
        
        st.info(f"**Total a pagar:** ${total:.2f}")
        
        submitted = st.form_submit_button("💾 Registrar Venta")
        
        if submitted:
            # ✅ MARCAR INMEDIATAMENTE que se está procesando
            st.session_state.venta_procesada = True
            
            conn_venta = get_connection()
            if not conn_venta:
                st.error("❌ No se pudo conectar para registrar la venta")
                st.session_state.venta_procesada = False
                return
            
            try:
                cursor_venta = conn_venta.cursor()
                
                # ✅ INSERTAR VENTA
                cursor_venta.execute(
                    "INSERT INTO ventas (id_cliente, id_producto, cantidad, total) VALUES (%s, %s, %s, %s)",
                    (cliente_id, producto_id, cantidad, total)
                )
                
                # ✅ ACTUALIZAR STOCK
                cursor_venta.execute(
                    "UPDATE productos SET stock = stock - %s WHERE id_producto = %s",
                    (cantidad, producto_id)
                )
                
                conn_venta.commit()
                
                st.success("✅ Venta registrada correctamente")
                # ❌ ELIMINADO: st.balloons() - Los globos ya no aparecerán
                
                # ✅ NO HACER rerun() AUTOMÁTICO - Mostrar mensaje y botón
                st.info("💡 La venta se ha registrado. Puedes verla en la pestaña 'Ver Ventas'")
                
            except Exception as e:
                st.error(f"❌ Error registrando venta: {e}")
                st.session_state.venta_procesada = False
            finally:
                cursor_venta.close()
                conn_venta.close()

def eliminar_venta(venta_id):
    """
    Elimina una venta de la base de datos y restaura el stock
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id_producto, cantidad FROM ventas WHERE id_venta = %s", (venta_id,))
            venta_info = cursor.fetchone()
            
            if venta_info:
                cursor.execute(
                    "UPDATE productos SET stock = stock + %s WHERE id_producto = %s",
                    (venta_info[1], venta_info[0])
                )
            
            cursor.execute("DELETE FROM ventas WHERE id_venta = %s", (venta_id,))
            conn.commit()
            st.success("✅ Venta eliminada correctamente")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error eliminando venta: {e}")
        finally:
            cursor.close()
            conn.close()
