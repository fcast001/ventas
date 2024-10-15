import pandas as pd #pip install pandas
import plotly.express as px #pip install plotly-express
import streamlit as st #pip install streamlit

#Streamlit run Ventas.py

st.set_page_config(page_title='Reporte de Ventas',  # Nombre de la página
                   page_icon=':moneybag:',  # https://www.webfx.com/tools/emoji-cheat-sheet/
                   layout="wide")

st.title(':clipboard: Reporte de Ventas')  # Título del Dash
st.subheader('Compañía TECH SAS')
st.markdown('##')  # Para separar el título de los KPIs

# Cargar el archivo de datos
archivo_excel = 'Data/Reporte de Ventas.xlsx'
hoja_excel = 'BASE DE DATOS'

df = pd.read_excel(archivo_excel,
                   sheet_name=hoja_excel,
                   usecols='A:P')  # Lee las columnas A a P

# st.dataframe(df)  # Muestra los datos para revisión

# Sidebar para los filtros
st.sidebar.header("Opciones a filtrar:")
vendedor = st.sidebar.multiselect(
    "Seleccione el Vendedor:",
    options=df['Vendedor'].unique(),
    default=df['Vendedor'].unique()
)

status_factura = st.sidebar.multiselect(
    "Factura Pagada (?):",
    options=df['Pagada'].unique(),
    default=df['Pagada'].unique()
)

ciudad = st.sidebar.multiselect(
    "Seleccione Ciudad:",
    options=df['Ciudad'].unique(),
    default=df['Ciudad'].unique()
)

industria = st.sidebar.multiselect(
    "Seleccione Industria:",
    options=df['Industria'].unique(),
    default=df['Industria'].unique()
)

cliente = st.sidebar.multiselect(
    "Seleccione Cliente:",
    options=df['Cliente'].unique(),
    default=df['Cliente'].unique()
)

plazo = st.sidebar.multiselect(
    "Seleccione plazo:",
    options=df['Términos'].unique(),
    default=df['Términos'].unique()
)

def format_number(value):
    return f"{value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Filtrar los datos según las selecciones
df_seleccion = df.query(
    "Vendedor == @vendedor & Ciudad == @ciudad & Pagada == @status_factura & Industria == @industria & Cliente == @cliente & Términos == @plazo")

# Asegurarse de que la columna 'Valor' sea numérica, ignorando cualquier columna de fecha
df_seleccion['Valor'] = pd.to_numeric(df_seleccion['Valor'], errors='coerce')  # Convierte y reemplaza no numéricos por NaN

# Llenar NaN con 0 en la columna 'Valor'
df_seleccion['Valor'].fillna(0, inplace=True)

# Calcular el total de ventas y el número de facturas
total_ventas = int(df_seleccion['Valor'].sum())
total_facturas = len(df_seleccion)  # Contar el número de facturas

# Crear columnas para mostrar KPIs
left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Ventas Totales:")
    st.subheader(f"US $ {total_ventas:,}")

with right_column:
    st.subheader('Facturas:')
    st.subheader(f" {total_facturas}")

st.markdown("---")

# Mostrar la tabla filtrada
st.dataframe(df_seleccion)

# Agrupación por cliente para las ventas
ventas_por_cliente = df_seleccion.groupby('Cliente').agg({'Valor': 'sum'})

#ventas_por_cliente = df_seleccion.groupby(by=['Cliente']).sum()[['Valor']].sort_values(by='Valor')

# Crear gráfico de barras para ventas por cliente
fig_ventas_cliente = px.bar(
    ventas_por_cliente,
    x='Valor',
    y=ventas_por_cliente.index,
    orientation="h",  # gráfico de barras horizontal
    title="<b>Ventas por Cliente</b>",
    color_discrete_sequence=["#f5b932"] * len(ventas_por_cliente),
    template='plotly_white',
    text='Valor'
)

fig_ventas_cliente.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# Agrupación por vendedor para las ventas
ventas_por_vendedor = df_seleccion.groupby('Vendedor').agg({'Valor': 'sum'})

#ventas_por_vendedor = df_seleccion.groupby(by=['Vendedor']).sum()[['Valor']].sort_values(by='Valor')

# Crear gráfico de barras para ventas por vendedor
fig_ventas_por_vendedor = px.bar(
    ventas_por_vendedor,
    x=ventas_por_vendedor.index,
    y='Valor',
    title='<b>Ventas por Vendedor</b>',
    color_discrete_sequence=["#F5B932"] * len(ventas_por_vendedor),
    template='plotly_white',
    text='Valor'
)

fig_ventas_por_vendedor.update_layout(
    xaxis=dict(tickmode='linear'),
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=(dict(showgrid=False)),
)


fig_ventas_por_vendedor.update_traces(
    texttemplate=[format_number(val) for val in ventas_por_vendedor['Valor']],
    textposition='outside'
)

fig_ventas_cliente.update_traces(
    texttemplate=[format_number(val) for val in ventas_por_cliente['Valor']],
    textposition='outside'
)



# Mostrar los gráficos en columnas
left_column, right_column = st.columns(2)

left_column.plotly_chart(fig_ventas_por_vendedor, use_container_width=True)
right_column.plotly_chart(fig_ventas_cliente, use_container_width=True)

# Ocultar el estilo de Streamlit
hide_st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
