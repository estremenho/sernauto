import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st

con = duckdb.connect(database='matriculaciones.duckdb', read_only=True)

# Consulta para obtener los datos de matriculaciones por marca
consulta = """
    SELECT FECHA AS Fecha,
        MARCA AS Marca,
        COUNT(*) AS 'Número de Coches'
    FROM matriculaciones
    GROUP BY 1, 2
    ORDER BY 2, 1
"""

df = con.sql(consulta).df()

def run_marcas():
    # Agregar un selector para elegir las marcas
    selected_marcas = st.multiselect('Selecciona las marcas:', df['Marca'].unique())

    if not selected_marcas:
        st.warning('Por favor, selecciona al menos una marca.')
    else:
        # Filtrar el DataFrame según las marcas seleccionadas
        df_filtered = df[df['Marca'].isin(selected_marcas)]

        # Crear un gráfico de líneas para mostrar la suma de matriculaciones por marca
        fig_marcas = px.line(df_filtered, x='Fecha', y='Número de Coches', color='Marca',
                             title='Matriculaciones por Marca', template='seaborn')

        # Personalizar el gráfico, si es necesario
        fig_marcas.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f")

        # Mostrar el gráfico
        st.plotly_chart(fig_marcas, use_container_width=True)

        # Consulta para obtener los modelos de la marca seleccionada
        consulta_modelo = f"""
            SELECT MARCA as Marca, MODELO AS Modelo,
                COUNT(*) AS 'Número de Coches'
            FROM matriculaciones
            WHERE MARCA IN {tuple(selected_marcas)}
            GROUP BY 2, 1
            ORDER BY 3 DESC
        """
        # Ejecutar la consulta y cargar los resultados en un DataFrame
        df_modelo = con.sql(consulta_modelo).df()


        # Mostrar una tabla con los modelos de la marca seleccionada y la suma de coches por modelo
        st.subheader('Modelos de la Marca Seleccionada')
        st.dataframe(df_modelo, height=300)  # Muestra los primeros 10 registros y permite desplazarse para ver el resto


# Llama a la función si es necesario
if __name__ == "__main__":
    run_marcas()
