def agregar_producto():
    st.subheader("Agregar Nuevo Producto")

    # Inicializar bandera
    if "producto_guardado" not in st.session_state:
        st.session_state.producto_guardado = False

    with st.form("producto_form", clear_on_submit=True):
        nombre = st.text_input("Nombre del producto *", placeholder="Ej: Laptop Gaming")
        descripcion = st.text_area("Descripción", placeholder="Ej: Laptop para gaming con 16GB RAM")
        precio = st.number_input("Precio *", min_value=0.0, step=0.1, format="%.2f")
        stock = st.number_input("Stock *", min_value=0, step=1)
        categoria = st.selectbox("Categoría", ["", "Electrónicos", "Ropa", "Hogar", "Deportes", "Otros"])
        
        submitted = st.form_submit_button("💾 Guardar Producto")

        if submitted and not st.session_state.producto_guardado:
            if not nombre.strip() or precio <= 0:
                st.error("❌ Nombre y precio son obligatorios (precio debe ser mayor a 0)")
                return

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
                    
                    # Marcar como guardado
                    st.session_state.producto_guardado = True
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Error guardando producto: {e}")
                finally:
                    cursor.close()
                    conn.close()
