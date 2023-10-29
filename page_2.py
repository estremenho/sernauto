import altair as alt
import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st

con = duckdb.connect(database='matriculaciones.duckdb', read_only=True)

df_fig2_1 = con.sql("""
        SELECT FECHA AS Fecha,
            MARCA AS Marca,
            COUNT(*) AS 'Número de Vehículos'
        FROM matriculaciones
        WHERE MARCA IN ('AIWAYS','BYD','DFSK','DR','LYNK&CO','MG','OTROS','POLESTAR','SWM','TESLA')
        GROUP BY 1, 2
        ORDER BY 2, 1      
        """).df()

df_fig2_2 = con.sql("""
        WITH TOP20 AS(
            SELECT MARCA
            FROM matriculaciones
            GROUP BY 1
            ORDER BY COUNT(*) DESC
            LIMIT 10
        )
        SELECT M.FECHA AS Fecha,
            M.MARCA AS Marca,
            COUNT(*) AS 'Número de Vehículos'
        FROM matriculaciones AS M
        INNER JOIN TOP20 AS T ON M.MARCA = T.MARCA
        GROUP BY 1, 2
        ORDER BY 2, 1  
        """).df()

df_fig2_3 = con.sql("""
        SELECT FECHA AS Fecha,
            PROPULSION AS Combustible,
            COUNT(*) AS 'Número de Vehículos'
        FROM matriculaciones
        GROUP BY 1, 2
        ORDER BY 2, 1  
        """).df()

df_fig2_4 = con.sql("""
        SELECT FECHA AS Fecha,
            CATEGORIA_VEHICULO_ELECTRICO AS Vehículo,
            COUNT(*) AS 'Número de Vehículos'
        FROM matriculaciones
        WHERE CATEGORIA_VEHICULO_ELECTRICO IS NOT NULL
        GROUP BY 1, 2
        ORDER BY 2, 1  
        """).df()

df_fig2_5 = con.sql("""
        SELECT FECHA AS Fecha,
            CASE WHEN KW_ITV < 60 THEN '01. <60'
                WHEN KW_ITV < 70  THEN '02. 70'
                WHEN KW_ITV < 80  THEN '03. 80'
                WHEN KW_ITV < 90  THEN '04. 90'
                WHEN KW_ITV < 100 THEN '05. 100'
                WHEN KW_ITV < 110 THEN '06. 110'
                WHEN KW_ITV < 120 THEN '07. 120'
                ELSE '08. >120' END AS Potencia,
            COUNT(*) AS 'Número de Vehículos'
        FROM matriculaciones
        GROUP BY 1, 2
        ORDER BY 2, 1  
        """).df()

df_fig2_6 = con.sql("""
        SELECT FECHA AS Fecha,
            CASE WHEN PESO_MAX < 800 THEN '01. <800'
                WHEN PESO_MAX < 900  THEN '02. 900'
                WHEN PESO_MAX < 1000 THEN '03. 1000'
                WHEN PESO_MAX < 1100 THEN '04. 1100'
                WHEN PESO_MAX < 1200 THEN '05. 1200'
                WHEN PESO_MAX < 1300 THEN '06. 1300'
                WHEN PESO_MAX < 1400 THEN '07. 1400'
                WHEN PESO_MAX < 1500 THEN '08. 1500'
                WHEN PESO_MAX < 1600 THEN '09. 1600'
                WHEN PESO_MAX < 1700 THEN '10. 1700'
                WHEN PESO_MAX < 1800 THEN '11. 1800'
                WHEN PESO_MAX < 1900 THEN '12. 1900'
                WHEN PESO_MAX < 2000 THEN '13. 2000'
                WHEN PESO_MAX < 2000 THEN '14. 2100'
                WHEN PESO_MAX < 2000 THEN '15. 2200'
                ELSE '16. >2200' END AS Peso,
            COUNT(*) AS 'Número de Vehículos'
        FROM matriculaciones
        GROUP BY 1, 2
        ORDER BY 2, 1  
        """).df()

df_fig2_7 = con.sql("""
        SELECT FECHA AS Fecha,
            IFNULL(SERVICIO, 'No informado') AS Servicio,
            COUNT(*) AS 'Número de Vehículos'
        FROM matriculaciones
        GROUP BY 1, 2
        ORDER BY 2, 1  
        """).df()

df_fig2_8 = con.sql("""
        SELECT FECHA AS Fecha,
            IFNULL(CARROCERIA, 'No informado') AS Carroceria,
            COUNT(*) AS 'Número de Vehículos'
        FROM matriculaciones
        GROUP BY 1, 2
        ORDER BY 2, 1  
        """).df()

df_fig2_9 = con.sql("""
        SELECT FECHA AS Fecha,
            IFNULL(COD_PROCEDENCIA_ITV, 'No informado') AS Procedencia,
            COUNT(*) AS 'Número de Vehículos'
        FROM matriculaciones
        GROUP BY 1, 2
        ORDER BY 2, 1  
        """).df()

df_fig2_10 = con.sql("""
        SELECT EXTRACT(DAY FROM FECHA_MATRICULA) AS Dia,
           COUNT(*) AS 'Número de Vehículos'
        FROM matriculaciones
        GROUP BY EXTRACT(DAY FROM FECHA_MATRICULA)
        ORDER BY Dia;
        """).df()

df_fig2_11 = con.sql("""
        SELECT COD_PROVINCIA_MAT AS Provincia,
            EXTRACT(YEAR FROM FECHA_MATRICULA) AS Año,
            COUNT(*) AS 'Número de Matriculaciones'
        FROM matriculaciones
        GROUP BY 1, 2
        ORDER BY 1, 2  
        """).df()

@st.cache_data
def run_tend():
    st.image('logo.png')
    st.title('Sernauto - Tendencias sobre Matriculaciones de la DGT')
    
    fig2_1 = px.line(df_fig2_1, x='Fecha', y='Número de Vehículos', color='Marca'
        , title='Tendencia ventas de Nuevas Marcas', template='seaborn')
    fig2_1.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f")
    st.plotly_chart(fig2_1, use_container_width=True)
    
    fig2_2 = px.line(df_fig2_2, x='Fecha', y='Número de Vehículos', color='Marca'
        , title='Tendencia ventas de Marcas Top Ventas', template='seaborn')
    fig2_2.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f")
    st.plotly_chart(fig2_2, use_container_width=True)
    
    c1_left, c1_right = st.columns(2)
    with c1_left:
        fig2_3 = px.line(df_fig2_3, x='Fecha', y='Número de Vehículos', color='Combustible'
            , title='Tendencia ventas por Combustible', template='seaborn')
        fig2_3.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f")
        st.plotly_chart(fig2_3, use_container_width=True)
    
    with c1_right:
        fig2_4 = px.line(df_fig2_4, x='Fecha', y='Número de Vehículos', color='Vehículo'
            , title='Tendencia ventas de Eléctricos', template='seaborn')
        fig2_4.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f")
        st.plotly_chart(fig2_4, use_container_width=True)

    c2_left, c2_right = st.columns(2)
    with c2_left:
        fig2_5 = px.line(df_fig2_5, x='Fecha', y='Número de Vehículos', color='Potencia'
            , title='Tendencia ventas por Potencia', template='seaborn')
        fig2_5.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f")
        st.plotly_chart(fig2_5, use_container_width=True)
    
    with c2_right:
        fig2_6 = px.line(df_fig2_6, x='Fecha', y='Número de Vehículos', color='Peso'
            , title='Tendencia ventas por Peso', template='seaborn')
        fig2_6.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f")
        st.plotly_chart(fig2_6, use_container_width=True)

    c3_left, c3_right = st.columns(2)
    with c3_left:
        fig2_7 = px.line(df_fig2_7, x='Fecha', y='Número de Vehículos', color='Servicio'
            , title='Tendencia ventas por Servicio', template='seaborn')
        fig2_7.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f")
        st.plotly_chart(fig2_7, use_container_width=True)
    
    with c3_right:
        fig2_8 = px.line(df_fig2_8, x='Fecha', y='Número de Vehículos', color='Carroceria'
            , title='Tendencia ventas por tipo de carroceria', template='seaborn')
        fig2_8.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f")
        st.plotly_chart(fig2_8, use_container_width=True)

        
    c4_left, c4_right = st.columns(2)
    with c4_left:
        fig2_7 = px.line(df_fig2_9, x='Fecha', y='Número de Vehículos', color='Procedencia'
            , title='Tendencia ventas por Procedencia', template='seaborn')
        fig2_7.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f")
        st.plotly_chart(fig2_7, use_container_width=True)
    
    with c4_right:
    # Crear un gráfico con Plotly Express
        fig2_10 = px.line(df_fig2_10, x='Dia', y='Número de Vehículos', markers=True, title='Matriculaciones por día del Mes')
        fig2_10.update_xaxes(dtick=1)
        fig2_10.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f")
        st.plotly_chart(fig2_10, use_container_width=True)

    
    fig2_11 = px.bar(df_fig2_11, x='Año', y='Número de Matriculaciones', color='Provincia',
                      title='Matriculaciones por Año y Provincia. Doble clic para seleccionar Provincia', template='seaborn')
    fig2_11.update_xaxes(dtick=1)
    fig2_11.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f")
    fig2_11.update_layout(legend_title='Doble clic para seleccionar Provincia')
    st.plotly_chart(fig2_11, use_container_width=True, height=1000)  # Ajusta la altura a 600 píxeles (puedes cambiar el valor según tus preferencias)

    
#    with c3_right:
#        fig2_8 = px.line(df_fig2_8, x='Fecha', y='Número de Vehículos', color='Carroceria'
#            , title='Tendencia ventas por tipo de carroceria', template='seaborn')
#        fig2_8.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f")
#       st.plotly_chart(fig2_8, use_container_width=True)
        
if __name__ == "__main__":
    run_tend()