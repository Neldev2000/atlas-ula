import pandas as pd
import psycopg2 as pg
import os
import subprocess
import streamlit as st
lista_sucursales = ('Mérida', 'San Cristóbal', 'Valera', 'Colon', 'El Vigia', 'Coloncito', 'La Fria', 'Caja Seca', 'Puerto Ordaz', 'Maracaibo', 'San Antonio','Caracas','Machiques')

franchise_map   = {
    'Mérida' : 1,
    'San Cristóbal' : 2,
    'Valera' : 3, 
    'Colon' : 5,
    'El Vigia': 6,
    'Coloncito' : 7, 
    'La Fria' : 8, 
    'Caja Seca' : 9, 
    'Puerto Ordaz' : 10,
    'Maracaibo': 11, 
    'San Antonio' : 12,
    'Caracas' : 13,
    'Machiques' : 14
}

time_translate = {
    'Diario' : ('day', 'del ultimo dia'), 'Semanal' : ('week', 'de la ultima semana'), 'Mensual': ('month', 'del ultimo mes')
}

def get_roles(users, username):
    for user in users:
        if user['key'] == username:
            return user['role']
    return 'no hay este usuario'

def update_database(dbname):
    pwd = os.getcwd()
    print(pwd)
    pwd = pwd + f'\{dbname}'
    database = f"postgres://{st.secrets['postgres'].user}:{st.secrets['postgres'].password}@{st.secrets['postgres'].host}:{st.secrets['postgres'].port}/{st.secrets['postgres'].dbname}"
    conn = pg.connect(**st.secrets['postgres'])
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute('DROP DATABASE IF EXISTS atlas')
        print("Base de Datos eliminada")
        cur.execute('CREATE DATABASE atlas')
        print("Base de Datos creada")
        subprocess.run(['pg_restore', '-d', database, '-v', pwd])
        print('Base de datos restaurada')

def obtener_data(file_path, columns, **query_vals):
    with open(file_path) as f:
        query = f.read()
        pass
    conn = pg.connect(**st.secrets['postgres'])
    data = pd.read_sql(query.format(**query_vals), conn)
    conn.close ()
    return data.loc[:, columns]
