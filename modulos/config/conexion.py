import mysql.connector
import streamlit as st

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='bamwzuzf0b3jk0jwtius-mysql.services.clever-cloud.com',
            user=' uuji5eicsayhs6o0',
            password='IoZiOb8QZZ3HeaxfFBEJ',
            database='bamwzuzf0b3jk0jwtius',
            port=3306
        )
        return connection
    except mysql.connector.Error as e:
        st.error(f"Error conectando a la base de datos: {e}")
        return None

def verify_user(username, password):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            
            # 🔥 DEBUG: Mostrar estructura de la tabla
            cursor.execute("DESCRIBE Usuario")
            estructura = cursor.fetchall()
            st.info("🔍 Estructura de la tabla Usuario:")
            for columna in estructura:
                st.write(f"   - {columna['Field']} ({columna['Type']})")
            
            # Buscar usuario
            cursor.execute("SELECT * FROM Usuario WHERE usuario = %s OR Usuario = %s", (username, username))
            user = cursor.fetchone()
            
            if user:
                st.success("🔍 DEBUG - Usuario encontrado en BD")
                st.write("🔍 DEBUG - Datos del usuario:", user)
                
                # Verificar contraseña (simple para testing)
                if 'password' in user and user['password'] == password:
                    return user
                elif 'Password' in user and user['Password'] == password:
                    return user
                elif 'contrasena' in user and user['contrasena'] == password:
                    return user
                else:
                    st.error("❌ Contraseña incorrecta")
                    return None
            else:
                st.error("❌ Usuario no encontrado en la base de datos")
                return None
                
        except mysql.connector.Error as e:
            st.error(f"Error verificando usuario: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None
