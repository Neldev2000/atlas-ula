import pandas as pd
import psycopg2 as pg
import os
import subprocess
import streamlit as st
import plotly.express as px

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
role_list = ['full', 'operaciones']
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
    st.write("# 👷‍♂️ Operaciones")

    sucursal = st.sidebar.selectbox("Selecciona tu sucursal", lista_sucursales)
    st.session_state['franchise_id'] = (franchise_map[sucursal], sucursal)

    pendientes_data = utils.obtener_data(file_path='./queries/operaciones/pendientes.sql',
                        columns=['pendientes'],
                        franchise_id = st.session_state['franchise_id'][0])
    pendientes_zona_data = utils.obtener_data(file_path='./queries/operaciones/pendientes_por_zona.sql',
                        columns=['sectores', 'pendientes'],
                        franchise_id = st.session_state['franchise_id'][0])

    st.write(f" ## Instalaciones de {st.session_state['franchise_id'][1]}")
    tiempo = st.radio('Selecciona el tiempo a visualiazar', ['Diario', 'Semanal', 'Mensual'], horizontal=True)

    instalaciones = utils.obtener_data(file_path='./queries/operaciones/instalaciones.sql', 
                                columns=['fecha_instalacion', 'instalaciones'],
                                franchise_id=  st.session_state['franchise_id'][0],
                                tiempo = time_translate[tiempo][0])

    st.write("### Instalaciones {t}: {val: .2f}".format(t = time_translate[tiempo][1],val = instalaciones.loc[0, ['instalaciones']].values[0]))

    st.bar_chart(instalaciones, x='fecha_instalacion', y ='instalaciones')

    ###################################
    ###################################

    st.write(f"## ⏰ Hay un total de {pendientes_data.values[0]} pendientes.")
    fig = px.bar(pendientes_zona_data, x="pendientes", y="sectores", orientation='h', title = 'Top 10 zonas con mas pendientes')

    st.write(fig)

    ###################################
    ###################################

    reporte_puertos = utils.obtener_data(file_path='./queries/operaciones/reporte_puertos.sql',
                                    columns=['clientes_que_pagan', 'promocion', 'exonerados', 'cortados_nuevos', 'cortados_viejos', 'pendientes' ],
                                    franchise_id = st.session_state['franchise_id'][0])
    st.write(f"## Reporte de Puertos")
    st.write(reporte_puertos)

    st.write("## Buscador de etiquetas")

    num_etiqueta = st.text_input(
            "Coloca tu etiqueta",
            placeholder="Hola",
        )

    etiquetas = utils.obtener_data(file_path='./queries/operaciones/buscador_etiquetas.sql',
                            columns=['nombre', 'telefono_fijo', 'telefono_celular', 'direccion'],
                            etiqueta= num_etiqueta)
    st.write(etiquetas)

    st.write("## Buscador de seriales")

    cod_serial = st.text_input(
            "Coloca tu serial",
            placeholder="Busca",
        )

    serial = utils.obtener_data(file_path='./queries/operaciones/buscador_serial.sql',
                            columns=['nombre', 'telefono_fijo', 'telefono_celular', 'direccion'],
                            serial=cod_serial)
    st.write(serial)

    st.write("## Buscador de MAC")

    cod_mac = st.text_input(
            "Coloca tu MAC",
            placeholder="Busca",
        )

    mac = utils.obtener_data(file_path='./queries/operaciones/buscador_mac.sql',
                            columns=['nombre', 'telefono_fijo', 'telefono_celular', 'direccion'],
                            MAC=cod_mac)
    st.write(mac)