
import streamlit as st
import sys
import pandas as pd
import plotly.graph_objects as go
sys.path.append('../utils')
from utils import utils
st.write("# 💲Comercial")

sucursal = st.sidebar.selectbox("Selecciona tu sucursal", utils.lista_sucursales)
st.session_state['franchise_id'] = (utils.franchise_map[sucursal], sucursal)


st.write(f" ## Ventas de {st.session_state['franchise_id'][1]}")
tiempo = st.radio('Selecciona el tiempo a visualiazar', ['Diario', 'Semanal', 'Mensual'], horizontal=True)

ventas = utils.obtener_data(file_path='./queries/comercial/ventas.sql',
                    columns=['fecha_venta', 'ventas'],
                    franchise_id=  st.session_state['franchise_id'][0],
                    tiempo = utils.time_translate[tiempo][0])

st.write("### Ventas {t}: {val: .2f}".format(t = utils.time_translate[tiempo][1],val = ventas.loc[0, ['ventas']].values[0]))

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
                        tiempo = utils.time_translate[tiempo][0])

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