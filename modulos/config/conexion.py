import mysql.connector
from mysql.connector import Error
import streamlit as st

def get_connection():
    """
    Establece conexión con la base de datos Clever Cloud
    """
    try:
        connection = mysql.connector.connect(
            host=' bamwzuzf0b3jk0jwtius-mysql.services.clever-cloud.com',
            database='bamwzuzf0b3jk0jwtius',
            user='uuji5eicsayhs6o0',
            password='your_password_here'  # Reemplaza con tu password real
        )
        
        if connection.is_connected():
            return connection
            
    except Error as e:
        st.error(f"❌ Error de conexión: {e}")
        return None

def verify_user(username, password):
    """
    Verifica las credenciales del usuario en la tabla Usuario
    ✅ CORREGIDO: Usa los nombres correctos de columnas (Usuario, Password)
    """
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            
            # ✅ CONSULTA CORREGIDA - NOMBRES EXACTOS DE COLUMNAS
            query = "SELECT Id_usuario, Usuario, email FROM Usuario WHERE Usuario = %s AND Password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if user:
                # ✅ RETORNAR OBJETO COMPATIBLE CON TU CÓDIGO
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

# Función de prueba para verificar que todo funciona
def test_connection():
    """
    Función de prueba para verificar la conexión y estructura
    """
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            
            # Verificar datos en la tabla Usuario
            cursor.execute("SELECT * FROM Usuario")
            users = cursor.fetchall()
            
            st.write("### 📊 Usuarios en la base de datos:")
            for user in users:
                st.write(f"- ID: {user['Id_usuario']}, Usuario: {user['Usuario']}, Email: {user['email']}")
            
            cursor.close()
            conn.close()
            return True
        return False
        
    except Exception as e:
        st.error(f"❌ Error en prueba: {e}")
        return False
