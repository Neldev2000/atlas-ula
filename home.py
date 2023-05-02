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

    st.write(""" # BIENVENIDOS """)

    sucursal = st.sidebar.selectbox("Selecciona tu sucursal", utils.lista_sucursales)
    st.session_state['franchise_id'] = (utils.franchise_map[sucursal], sucursal)

    st.write("## Esta es la pagina oficial para ver las estadisticas de tu sucursal")