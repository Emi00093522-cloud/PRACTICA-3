import streamlit as st
from config.conexion import get_connection

def show_clientes():
    """
    Módulo de gestión de clientes
    """
    st.header("👥 Gestión de Clientes")
    
    # Pestañas para diferentes acciones
    tab1, tab2 = st.tabs(["📋 Ver Clientes", "➕ Agregar Cliente"])
    
    with tab1:
        ver_clientes()
    
    with tab2:
        agregar_cliente()

def ver_clientes():
    """
    Muestra la lista de clientes existentes
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM clientes ORDER BY fecha_registro DESC")
            clientes = cursor.fetchall()
            
            if clientes:
                st.subheader(f"Total de clientes registrados: {len(clientes)}")
                
                # Mostrar en forma de tarjetas
                for cliente in clientes:
                    with st.expander(f"👤 {cliente['nombre']} - ID: {cliente['id_cliente']}", expanded=False):
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            st.write(f"**Email:** {cliente['email'] or 'No especificado'}")
                            st.write(f"**Teléfono:** {cliente['telefono'] or 'No especificado'}")
                            if cliente['direccion']:
                                st.write(f"**Dirección:** {cliente['direccion']}")
                        
                        with col2:
                            st.write(f"**ID:** {cliente['id_cliente']}")
                            if cliente['fecha_registro']:
                                st.write(f"**Registro:** {cliente['fecha_registro'].strftime('%d/%m/%Y')}")
                        
                        with col3:
                            if st.button("🗑️ Eliminar", key=f"del_{cliente['id_cliente']}"):
                                eliminar_cliente(cliente['id_cliente'])
            else:
                st.info("📝 No hay clientes registrados en el sistema")
                
        except Exception as e:
            st.error(f"❌ Error cargando clientes: {e}")
        finally:
            cursor.close()
            conn.close()

def agregar_cliente():
    """
    Formulario para agregar nuevo cliente
    """
    st.subheader("Agregar Nuevo Cliente")
    
    # ✅ USAR st.form CON clear_on_submit=True
    with st.form("cliente_form", clear_on_submit=True):
        nombre = st.text_input("Nombre completo *", placeholder="Ej: Juan Pérez")
        email = st.text_input("Email", placeholder="Ej: juan@email.com")
        telefono = st.text_input("Teléfono", placeholder="Ej: +1234567890")
        direccion = st.text_area("Dirección", placeholder="Ej: Av. Principal #123")
        
        submitted = st.form_submit_button("💾 Guardar Cliente")
        
        if submitted:
            if not nombre.strip():
                st.error("❌ El nombre es obligatorio")
                return
                
            conn = get_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    
                    # ✅ VERIFICAR SI EL CLIENTE YA EXISTE (por email)
                    if email.strip():
                        cursor.execute("SELECT id_cliente FROM clientes WHERE email = %s", (email.strip(),))
                        if cursor.fetchone():
                            st.error("❌ Ya existe un cliente con ese email")
                            return
                    
                    # ✅ INSERTAR NUEVO CLIENTE
                    cursor.execute(
                        "INSERT INTO clientes (nombre, email, telefono, direccion, fecha_registro) VALUES (%s, %s, %s, %s, NOW())",
                        (nombre.strip(), email.strip() if email else None, telefono.strip() if telefono else None, direccion.strip() if direccion else None)
                    )
                    conn.commit()
                    st.success("✅ Cliente agregado correctamente")
                    st.balloons()
                    
                    # ✅ REDIRECCIÓN CON DELAY PARA EVITAR DUPLICADOS
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error guardando cliente: {e}")
                finally:
                    cursor.close()
                    conn.close()

def eliminar_cliente(cliente_id):
    """
    Elimina un cliente de la base de datos
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (cliente_id,))
            conn.commit()
            st.success("✅ Cliente eliminado correctamente")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error eliminando cliente: {e}")
        finally:
            cursor.close()
            conn.close()
