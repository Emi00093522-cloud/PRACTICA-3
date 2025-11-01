import streamlit as st
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

st.title("🔍 DIAGNÓSTICO COMPLETO - ESTRUCTURA REAL")

st.subheader("📁 CONTENIDO de CADA CARPETA:")

# Verificar carpeta modules
modules_path = os.path.join(current_dir, 'modules')
st.write(f"**Ruta modules:** {modules_path}")
if os.path.exists(modules_path):
    st.success("✅ Carpeta 'modules' EXISTE")
    archivos = os.listdir(modules_path)
    if archivos:
        st.write("**Archivos en modules/:**")
        for archivo in archivos:
            st.write(f"   📄 {archivo}")
    else:
        st.error("❌ Carpeta 'modules' está VACÍA")
else:
    st.error("❌ Carpeta 'modules' NO EXISTE")

# Verificar carpeta config
config_path = os.path.join(current_dir, 'config')
st.write(f"**Ruta config:** {config_path}")
if os.path.exists(config_path):
    st.success("✅ Carpeta 'config' EXISTE")
    archivos = os.listdir(config_path)
    if archivos:
        st.write("**Archivos en config/:**")
        for archivo in archivos:
            st.write(f"   📄 {archivo}")
    else:
        st.error("❌ Carpeta 'config' está VACÍA")
else:
    st.error("❌ Carpeta 'config' NO EXISTE")

st.subheader("🔍 BUSCAR archivos en TODO el proyecto:")
archivos_buscar = ['login.py', 'menu.py', 'clientes.py', 'productos.py', 'ventas.py', 'conexion.py']

for archivo in archivos_buscar:
    encontrado = False
    for root, dirs, files in os.walk(current_dir):
        if archivo in files:
            st.success(f"✅ {archivo} - ENCONTRADO en: {root}")
            encontrado = True
            break
    if not encontrado:
        st.error(f"❌ {archivo} - NO ENCONTRADO")

st.subheader("📋 ESTRUCTURA COMPLETA del proyecto:")
st.code("""
ESTRUCTURA REQUERIDA:
tu_app/
├── modules/
│   ├── login.py
│   ├── menu.py
│   ├── clientes.py
│   ├── productos.py
│   └── ventas.py
├── config/
│   └── conexion.py
├── app.py
└── requirements.txt
""")

st.stop()
