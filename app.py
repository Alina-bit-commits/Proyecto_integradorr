import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing



st.title("Análisis de viviendas de California")

# Cargar el dataset
california = fetch_california_housing()

df_california = pd.DataFrame(
    california.data,
    columns=california.feature_names
)

df_california["MedHouseVal"] = california.target

# Mostrar los datos
st.subheader("Primeras cinco filas")
st.dataframe(df_california.head())

st.subheader("Tipos de datos")
st.write(df_california.dtypes)

st.subheader("Valores faltantes")
st.write(df_california.isna().sum())

st.sidebar.markdown("## Filtros de exploración")
st.sidebar.write("Seleccioná los filtros para analizar los datos.")

edad_minima = int(df_california["HouseAge"].min())
edad_maxima = int(df_california["HouseAge"].max())

rango_edad = st.sidebar.slider(
    "Edad mediana de las viviendas",
    min_value=edad_minima,
    max_value=edad_maxima,
    value=(edad_minima, edad_maxima),
    step=1
)

df_filtrado = df_california[
    (df_california["HouseAge"] >= rango_edad[0]) &
    (df_california["HouseAge"] <= rango_edad[1])
].copy()



activar_latitud = st.sidebar.checkbox(
    "Activar filtro por latitud"
)

latitud_minima = st.sidebar.number_input(
    "Latitud mínima",
    min_value=float(df_california["Latitude"].min()),
    max_value=float(df_california["Latitude"].max()),
    value=float(df_california["Latitude"].min()),
    step=0.1
)

if activar_latitud:
    df_filtrado = df_filtrado[
        df_filtrado["Latitude"] >= latitud_minima
    ]

st.subheader("Datos filtrados")
st.dataframe(df_filtrado.head())

st.write("Cantidad de registros:", len(df_filtrado))

st.subheader("Resumen descriptivo")

if not df_filtrado.empty:

    mediana = df_filtrado["MedHouseVal"].median()

    rango = (
        df_filtrado["MedHouseVal"].max()
        - df_filtrado["MedHouseVal"].min()
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Mediana del valor",
            f"USD {mediana * 100000:,.0f}"
        )

    with col2:
        st.metric(
            "Rango del valor",
            f"USD {rango * 100000:,.0f}"
        )

else:
    st.warning("No hay datos para los filtros seleccionados.")

st.header("Visualización de datos")

st.subheader("Distribución del valor de las viviendas")

if not df_filtrado.empty:

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(
        df_filtrado["MedHouseVal"],
        bins=30,
        color="skyblue",
        edgecolor="black"
    )

    ax.set_title("Distribución del valor mediano de las viviendas")
    ax.set_xlabel("Valor mediano (cientos de miles de USD)")
    ax.set_ylabel("Frecuencia")

    st.pyplot(fig)

else:
    st.warning("No hay datos para mostrar el histograma.")


st.subheader("Relación entre ingresos y valor de vivienda")

if not df_filtrado.empty:

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.scatter(
        df_filtrado["MedInc"],
        df_filtrado["MedHouseVal"],
        color="steelblue",
        alpha=0.4
    )

    ax.set_title("Ingresos y valor mediano de las viviendas")
    ax.set_xlabel("Ingreso mediano (decenas de miles de USD)")
    ax.set_ylabel("Valor mediano (cientos de miles de USD)")

    st.pyplot(fig)

else:
    st.warning("No hay datos para mostrar el gráfico.")

st.subheader("Ubicación geográfica de las viviendas")

if not df_filtrado.empty:

    df_mapa = df_filtrado[
        ["Latitude", "Longitude"]
    ].rename(
        columns={
            "Latitude": "latitude",
            "Longitude": "longitude"
        }
    )

    st.map(df_mapa)

else:
    st.warning("No hay datos para mostrar en el mapa.")

streamlit
pandas
scikit-learn
matplotlib
