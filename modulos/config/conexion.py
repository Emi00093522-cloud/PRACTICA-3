import mysql.connector
from mysql.connector import Error
import streamlit as st

def get_connection():
    """
    Establece conexión con la base de datos Clever Cloud
    """
    try:
        connection = mysql.connector.connect(
            host='bamwzuzf0b3jk0jwtius-mysql.services.clever-cloud.com',
            database='bamwzuzf0b3jk0jwtius',
            user='uuji5eicsayhs6o0',
            password='IoZiOb8QZZ3HeaxfFBEJ'
        )
        
        if connection.is_connected():
            return connection
            
    except Error as e:
        st.error(f"❌ Error de conexión: {e}")
        return None

def verify_user(username, password):
    """
    Verifica las credenciales del usuario en la tabla Usuario
    """
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            
            query = "SELECT Id_usuario, Usuario, email FROM Usuario WHERE Usuario = %s AND Password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if user:
                return {
                    'id': user['Id_usuario'],
                    'usuario': user['Usuario'],
                    'email': user['email']
                }
            return None
            
        return None
        
    except Exception as e:
        st.error(f"❌ Error verificando usuario: {e}")
        return None
