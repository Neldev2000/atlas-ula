import pandas as pd
import psycopg2 as pg
import os
import subprocess
import streamlit as st
import plotly.express as px
import datetime
#######################################################

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
role_list = ['full', 'administracion']
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

########
    ########################################
    ########################################
    st.write("""
        # 💵 Administracion
    """)
   
    if 'franchise_id' in st.session_state:
        st.write(f" ## Facturacion de {st.session_state['franchise_id'][1]}")
        tiempo = st.radio('Selecciona el tiempo a visualiazar', ['Diario', 'Semanal', 'Mensual'], horizontal=True)

        facturacion = utils.obtener_data(file_path='./queries/administracion/reporte_facturacion.sql',
                            columns=['tiempo', 'total_usd'],
                            franchise_id=st.session_state['franchise_id'][0],
                            tiempo=time_translate[tiempo][0])
        st.write("### Facturacion {t}: {val: .2f}$".format(t = time_translate[tiempo][1],val = facturacion.loc[0, ['total_usd']].values[0]))
        st.bar_chart(facturacion, x='tiempo', y ='total_usd')

        col1, col2 = st.columns(2)

        with col1 : # Medios de pago segun moneda
            st.write("## 💴 Medios de pago segun moneda")
            moneda = st.radio('Por favor selecciona la moneda', ['USD', 'VES'], horizontal=True)
            metodo_pago = utils.obtener_data(file_path= "./queries/administracion/metodos_de_pago.sql",
                                    columns=['payment_method', 'proporcion'],
                                    franchise_id =st.session_state['franchise_id'][0],
                                    moneda=moneda)
            fig = px.pie(metodo_pago, names = 'payment_method', values = 'proporcion', hover_data=['payment_method'])
            st.write(fig)
            pass
        with col2 : # Transacciones hechas en USD vs VES en el ultimo mes
            st.write("## 💴 Transacciones hechas en USD vs VES")
            currency_code = utils.obtener_data(file_path= "./queries/administracion/distrib_monedas.sql",
                                    columns=['currency_code', 'proporcion'],
                                    franchise_id =st.session_state['franchise_id'][0])
            fig = px.pie(currency_code, names = 'currency_code', values = 'proporcion', hover_data=['currency_code'])
            st.write(fig)
            pass

        st.write("## A continuacion podras ver el dinero facturado en una fecha especifica")
        d = st.date_input(
        "Coloca la fecha del reporte",
        datetime.date.today())
        #hello
        reporte_facturas = utils.obtener_data(file_path='./queries/administracion/facturacion_por_dia.sql',
                                            columns=['fecha_facturado', 'factura', 'monto', 'monto_usd', 'divisa', 'suma_monto'],
                                            franchise_id = st.session_state['franchise_id'][0],
                                            dia=f"{d}")
        reporte_facturas.to_excel("facturacion.xlsx", sheet_name="REPORTE")

        with open("facturacion.xlsx", "rb") as f:
            st.download_button(label="Descarga tu reporte", 
                                data=f,
                                file_name=f"facturacion_{d}.xlsx", 
                                mime = 'text/csv')


    else:
        st.write("## Por favor entra a \'actualizar data\' para seleccionar la sucursal")