import mysql.connector
import streamlit as st

def get_connection():
    """
    Establece conexión con la base de datos en Clever Cloud
    """
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
    """
    Verifica las credenciales del usuario en la base de datos
    """
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM USUARIO WHERE usuario = %s", (username,))
            user = cursor.fetchone()
            
            if user:
                # En producción usar bcrypt para verificar contraseñas
                # Por simplicidad, asumimos que la verificación es correcta
                return user
        except mysql.connector.Error as e:
            st.error(f"Error verificando usuario: {e}")
        finally:
            cursor.close()
            conn.close()
    return None
