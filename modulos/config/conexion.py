import mysql.connector
import streamlit as st

def get_connection():
    """
    Función de conexión - COMENTADA TEMPORALMENTE PARA TESTING
    """
    try:
        # 🔥 COMENTADO TEMPORALMENTE - USAR MODO TESTING
        return None
        """
        connection = mysql.connector.connect(
            host='be5bmntqvmjb45dbc68h-mysql.services.clever-cloud.com',
            user='ufr:seuvahgrdaghy',
            password='UXDn3bPXibZaLwBC6Xt1',
            database='be5bmntqvmjb45dbc68h',
            port=3306
        )
        return connection
        """
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
