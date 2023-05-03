import pandas as pd
import json
import psycopg2 as pg
import os
import subprocess
import streamlit as st
from pprint import pprint
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

name, auth_status, main_username = authenticator.login("Login", "main")

role = utils.get_roles(users, main_username)
role_list = ['full']
if not (role in role_list):
    st.error('You don\'t have access to this module')

if auth_status == False:
    st.error("/username/password incorrect")
if auth_status == None:
    st.warning("Please enter your username and password")
if auth_status and (role in role_list):
    authenticator.logout("Logout", "sidebar")

    st.write("# Bienvenido al sistema de usuarios")

    st.write("# Lista de usuarios en el sistema")
    df = pd.DataFrame.from_dict(users)
    st.write(df)
    usernames = df['key']
    st.write("# Agrega un usuario")
    
    username = st.text_input("Indica tu nombre de usuario", placeholder="Username")
    name = st.text_input("Indica tu nombre completo", placeholder="Name")
    password = st.text_input("Indica tu contraseña", placeholder="Password")
    password = stauth.Hasher(password).generate()
    role = st.radio("Indica tu rol", ['full', 'operaciones', 'ventas', 'administracion'])
    if st.button('Agregar usuario'):
        db.insert_user(username, name, password[0], role)
    
    st.write("# Elimina o actualiza un usuario")
    st.write("### Si vas a eliminar, solo selecciona el usuario")
    user = st.radio("Selecciona tu usuario", usernames)
    
    
    name = st.text_input("Indica tu nuevo nombre completo", placeholder="Name")
    password = st.text_input("Indica tu nueva contraseña", placeholder="Password")
    password = stauth.Hasher(password).generate()
    role = st.radio("Indica tu nuevo rol", ['full', 'operaciones', 'ventas', 'administracion'], horizontal=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Eliminar usuario') and user != main_username:
            db.delete_user(user)
    
    with col2:
        if st.button('Actualizar datos') and user != main_username:
            db.update_user(user, {'name' : name, 'password': password[0], 'role' : role})
    