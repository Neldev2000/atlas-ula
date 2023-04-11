import pandas as pd
import psycopg2 as pg
import os
import subprocess
import streamlit as st
import plotly.express as px

#######################################################
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



st.write("# 👷‍♂️ Operaciones")

sucursal = st.sidebar.selectbox("Selecciona tu sucursal", lista_sucursales)
st.session_state['franchise_id'] = (franchise_map[sucursal], sucursal)

pendientes_data = obtener_data(file_path='./queries/operaciones/pendientes.sql',
                    columns=['pendientes'],
                    franchise_id = st.session_state['franchise_id'][0])
pendientes_zona_data = obtener_data(file_path='./queries/operaciones/pendientes_por_zona.sql',
                    columns=['sectores', 'pendientes'],
                    franchise_id = st.session_state['franchise_id'][0])

st.write(f" ## Instalaciones de {st.session_state['franchise_id'][1]}")
tiempo = st.radio('Selecciona el tiempo a visualiazar', ['Diario', 'Semanal', 'Mensual'], horizontal=True)

instalaciones = obtener_data(file_path='./queries/operaciones/instalaciones.sql', 
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

reporte_puertos = obtener_data(file_path='./queries/operaciones/reporte_puertos.sql',
                                columns=['clientes_que_pagan', 'promocion', 'exonerados', 'cortados_nuevos', 'cortados_viejos', 'pendientes' ],
                                franchise_id = st.session_state['franchise_id'][0])
st.write(f"## Reporte de Puertos")
st.write(reporte_puertos)

st.write("## Buscador de etiquetas")

num_etiqueta = st.text_input(
        "Coloca tu etiqueta",
        placeholder="Hola",
    )

etiquetas = obtener_data(file_path='./queries/operaciones/buscador_etiquetas.sql',
                        columns=['nombre', 'telefono_fijo', 'telefono_celular', 'direccion'],
                        etiqueta= num_etiqueta)
st.write(etiquetas)

st.write("## Buscador de seriales")

cod_serial = st.text_input(
        "Coloca tu serial",
        placeholder="Busca",
    )

serial = obtener_data(file_path='./queries/operaciones/buscador_serial.sql',
                        columns=['nombre', 'telefono_fijo', 'telefono_celular', 'direccion'],
                        serial=cod_serial)
st.write(serial)

st.write("## Buscador de MAC")

cod_mac = st.text_input(
        "Coloca tu MAC",
        placeholder="Busca",
    )

mac = obtener_data(file_path='./queries/operaciones/buscador_mac.sql',
                        columns=['nombre', 'telefono_fijo', 'telefono_celular', 'direccion'],
                        MAC=cod_mac)
st.write(mac)