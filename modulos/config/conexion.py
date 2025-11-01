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
    """
    Función de verificación - COMENTADA TEMPORALMENTE
    """
    # 🔥 MODO TESTING ACTIVADO
    st.info("🔧 Modo testing activado - Base de datos deshabilitada")
    return None
