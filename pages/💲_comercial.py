import pandas as pd
import psycopg2 as pg
import os
import subprocess
import streamlit as st

import plotly.graph_objects as go
######################################################
######################################################
import streamlit_authenticator as stauth
import sys
sys.path.append('../database')
from database import database as db
sys.path.append('../utils')
from utils import utils
users = db.fecth_all_users()

usernames = [user['key'] for user in users ]
names = [user['name'] for user in users]
hashed_passwords = [user['password'] for user in users]
authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "home_page", "abcdef", cookie_expiry_days=1)

name, auth_status, username = authenticator.login("Login", "main")

role = utils.get_roles(users, username)
role_list = ['full', 'comercial']
if not (role in role_list):
    st.error('You don\'t have access to this module')

if auth_status == False:
    st.error("/username/password incorrect")
if auth_status == None:
    st.warning("Please enter your username and password")
if auth_status and (role in role_list):
    authenticator.logout("Logout", "sidebar")
#######################################################
    lista_sucursales = utils.lista_sucursales
    franchise_map   = utils.franchise_map
    time_translate = utils.time_translate
    sucursal = st.sidebar.selectbox("Selecciona tu sucursal", lista_sucursales)
    st.session_state['franchise_id'] = (franchise_map[sucursal], sucursal)

    #######################################################

    #######################################################


    #######################################################

    st.write("# 💲Comercial")
    st.write(f" ## Ventas de {st.session_state['franchise_id'][1]}")

    


    tiempo = st.radio('Selecciona el tiempo a visualiazar para las ventas', ['Diario', 'Semanal', 'Mensual'], horizontal=True)

    ventas = utils.obtener_data(file_path='./queries/comercial/ventas.sql',
                        columns=['fecha_venta', 'ventas'],
                        franchise_id=  st.session_state['franchise_id'][0],
                        tiempo = time_translate[tiempo][0])

    st.write("### Ventas {t}: {val: .2f}".format(t = time_translate[tiempo][1],val = ventas.loc[0, ['ventas']].values[0]))

    st.bar_chart(ventas, x='fecha_venta', y ='ventas')

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"## Ventas de este mes ya instaladas")
        ventas_actual = utils.obtener_data(file_path='./queries/comercial/clientes_instalados_este_mes.sql',
                        columns=['ventas'],
                        franchise_id=  st.session_state['franchise_id'][0]) 
        st.write(f"## {ventas_actual.loc[0, ['ventas']].values[0]}")
    with col2:
        st.write(f"## Ventas del mes pasado ya instaladas")
        ventas_pasadas = utils.obtener_data(file_path='./queries/comercial/clientes_del_mes_pasado.sql',
                        columns=['ventas'],
                        franchise_id=  st.session_state['franchise_id'][0]) 
        st.write(f"## {ventas_pasadas.loc[0, ['ventas']].values[0]}")
    st.write("# Distribucion de pagos en moneda")
    tiempo = st.radio('Selecciona el tiempo a visualiazar para la distribucion de pagos', ['Diario', 'Semanal', 'Mensual'], horizontal=True)
    metodo_ventas = utils.obtener_data(file_path='./queries/comercial/distribucion_pago_ventas.sql',
                        columns=['fecha', 'moneda'],
                        franchise_id=  st.session_state['franchise_id'][0],
                        tiempo = time_translate[tiempo][0])

    cross_tab_prop = pd.crosstab(index=metodo_ventas['fecha'],
                                columns=metodo_ventas['moneda'],
                                normalize="index")
    cross_tab_prop = cross_tab_prop.sort_index(ascending=True)
    plot = go.Figure()
    
    plot.add_trace(go.Scatter(
        name = 'USD',
        x = cross_tab_prop.index,
        y = cross_tab_prop['USD'],
        stackgroup='one'
    ))
    
    plot.add_trace(go.Scatter(
        name = 'VES',
        x = cross_tab_prop.index,
        y = cross_tab_prop['VES'],
        stackgroup='one'
    )
    )
    st.plotly_chart(plot, theme=None, use_container_width=True)