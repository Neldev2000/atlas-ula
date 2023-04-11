import streamlit as st
from utils.utils import franchise_map, lista_sucursales, update_database

st.write(""" # BIENVENIDOS """)

sucursal = st.sidebar.selectbox("Selecciona tu sucursal", lista_sucursales)
st.session_state['franchise_id'] = (franchise_map[sucursal], sucursal)

st.write("## Esta es la pagina oficial para ver las estadisticas de tu sucursal")