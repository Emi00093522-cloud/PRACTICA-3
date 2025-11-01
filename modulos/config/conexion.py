import mysql.connector
import streamlit as st

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='bamwzuzf0b3jk0jwtius-mysql.services.clever-cloud.com',
            user='uuji5eicsayhs6o0',
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
            # 🔥 CAMBIO: Usar 'Usuario' en lugar de 'USUARIO'
            cursor.execute("SELECT * FROM Usuario WHERE usuario = %s", (username,))
            user = cursor.fetchone()
            
            if user:
                # Verificación simple de contraseña (para testing)
                if user['Password'] == password:  # 🔥 CAMBIO: 'Password' con P mayúscula
                    return user
            return None
            
        except mysql.connector.Error as e:
            st.error(f"Error verificando usuario: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None
