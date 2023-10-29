import altair as alt
import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st

con = duckdb.connect(database='matriculaciones.duckdb', read_only=True)

df_tot = con.sql("""
        SELECT A.AÑO AS Año,
            CAST(COUNT(*) AS DECIMAL) AS 'Número de vehículos'
        FROM matriculaciones AS A
        GROUP BY 1
    """).df()

# Modificar la consulta SQL para que los valores de 'Media de años' sean números
df_matr = con.sql("""
        SELECT A.AÑO AS Año,
            A.MES AS Mes,
            CAST(COUNT(*) AS DECIMAL) AS 'Número de vehículos'
        FROM matriculaciones AS A
        GROUP BY 1, 2
        UNION ALL
        SELECT -1 AS AÑO, -- Valor negativo para representar 'Media de años'
            B.MES,
            AVG(B.N) AS 'Número de vehículos'
        FROM(
            SELECT AÑO,
                MES,
                COUNT(*) AS N
            FROM matriculaciones
            WHERE AÑO < YEAR(current_date)
            GROUP BY 1, 2
        ) B
        GROUP BY 2
    """).df()

# Ordenar el DataFrame por el mes y por el valor de 'Media de años'
df_matr = df_matr.sort_values(['Mes', 'Año'])

# Reemplazar el valor -1 en la columna 'Año' por 'Media de años'
df_matr['Año'] = df_matr['Año'].replace(-1, 'Media de años')

@st.cache_data
def run_data():
    st.image('logo.png')
    st.markdown(
    '<h1 style="font-size: 32px; line-height: 1;">Sernauto - Matriculaciones de vehículos nuevos <span style="font-size: 18px;">(Turismos y Todoterrenos)</span></h1>',
    unsafe_allow_html=True
)
    
    fig1 = px.line(df_matr, x="Mes", y="Número de vehículos", color="Año"
            , markers=True, template="seaborn", line_shape="spline"
            , title="Matriculaciones por Mes y Año")
    fig1.update_xaxes(dtick=1)
    fig1.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f")
    fig1.update_traces(line=dict(dash='dot'), selector=dict(name='Media de años'))
    st.plotly_chart(fig1, use_container_width=True)

    c1_left, c1_right = st.columns(2)
    with c1_left:
        fig2 = px.bar(df_tot, x="Año", y="Número de vehículos", template="seaborn"
            , title="Matriculaciones por Año")
        fig2.update_xaxes(dtick=1)
        fig2.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f")
        st.plotly_chart(fig2, use_container_width=True)

    with c1_right:
          
        # Gráfico 3: Matriculaciones por Mes y Año (Desglosado por Mes)
      fig3 = px.histogram(df_matr, x="Año", y="Número de vehículos", color="Mes",
                         template="plotly_dark", title="Matriculaciones por Mes y Año")

      # Configurar el ancho de las barras en el eje x
      fig3.update_xaxes(dtick=1, title_text='Año', showgrid=True, categoryorder='total ascending', categoryarray=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])

      fig3.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f", title_text='Número de vehículos', showgrid=True)
      fig3.update_layout(showlegend=True, legend_title="Mes")
      st.plotly_chart(fig3, use_container_width=True)

        
    c2_left, c2_right = st.columns(2)
    with c2_left:
        df_fig4 = con.sql("""
            SELECT CASE WHEN PROPULSION = 'Diesel' THEN PROPULSION
                WHEN PROPULSION = 'Gasolina' THEN PROPULSION
                WHEN PROPULSION = 'Eléctrico' THEN PROPULSION
                ELSE 'Otros' END AS Combustible
                , COUNT(*) AS 'Número de vehículos'
            FROM matriculaciones
            GROUP BY 1
        """).df()    
        fig4 = px.pie(df_fig4, values="Número de vehículos", names="Combustible"
            , template="seaborn", title="Matriculaciones por combustible")
        st.plotly_chart(fig4, use_container_width=True)

    with c2_right:
        df_fig5 = con.sql("""
        SELECT CATEGORIA_VEHICULO_ELECTRICO AS Tipo
            , COUNT(*) AS 'Número de vehículos'
        FROM matriculaciones
        WHERE CATEGORIA_VEHICULO_ELECTRICO IS NOT NULL
        GROUP BY 1
        """).df()
        fig5 = px.pie(df_fig5, values="Número de vehículos", names="Tipo"
            , template="seaborn", title="Matriculaciones de Eléctricos")
        st.plotly_chart(fig5, use_container_width=True)

    c3_left, c3_center, c3_right = st.columns(3)
    with c3_left:
        df_fig6 = con.sql("""
            SELECT CASE WHEN KW_ITV < 60 THEN '01. <60'
                WHEN KW_ITV < 70  THEN '02. 70'
                WHEN KW_ITV < 80  THEN '03. 80'
                WHEN KW_ITV < 90  THEN '04. 90'
                WHEN KW_ITV < 100 THEN '05. 100'
                WHEN KW_ITV < 110 THEN '06. 110'
                WHEN KW_ITV < 120 THEN '07. 120'
                ELSE '08. >120' END AS Potencia
                , COUNT(*) AS 'Número de vehículos'
            FROM matriculaciones
            GROUP BY 1
            ORDER BY 1
        """).df()        
        fig6 = px.bar(df_fig6, x="Potencia", y="Número de vehículos", template="seaborn"
            , title="Matriculaciones por Potencia")
        fig6.update_xaxes(dtick=1)
        fig6.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f")
        st.plotly_chart(fig6, use_container_width=True)
    
    with c3_center:
        df_fig7 = con.sql("""
            SELECT CASE WHEN CILINDRADA_ITV < 800 THEN '01. <800'
                WHEN CILINDRADA_ITV < 900  THEN '02. 900'
                WHEN CILINDRADA_ITV < 1000 THEN '03. 1000'
                WHEN CILINDRADA_ITV < 1100 THEN '04. 1100'
                WHEN CILINDRADA_ITV < 1200 THEN '05. 1200'
                WHEN CILINDRADA_ITV < 1300 THEN '06. 1300'
                WHEN CILINDRADA_ITV < 1400 THEN '07. 1400'
                WHEN CILINDRADA_ITV < 1500 THEN '08. 1500'
                WHEN CILINDRADA_ITV < 1600 THEN '09. 1600'
                WHEN CILINDRADA_ITV < 1700 THEN '10. 1700'
                WHEN CILINDRADA_ITV < 1800 THEN '11. 1800'
                WHEN CILINDRADA_ITV < 1900 THEN '12. 1900'
                WHEN CILINDRADA_ITV < 2000 THEN '13. 2000'
                ELSE '14. >2000' END AS Cilindrada
                , COUNT(*) AS 'Número de vehículos'
            FROM matriculaciones
            GROUP BY 1
            ORDER BY 1
        """).df()        
        fig7 = px.bar(df_fig7, x="Cilindrada", y="Número de vehículos", template="seaborn"
            , title="Matriculaciones por Cilindrada")
        fig7.update_xaxes(dtick=1)
        fig7.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f")
        st.plotly_chart(fig7, use_container_width=True)
 
    with c3_right:
            df_fig8 = con.sql("""
                SELECT IFNULL(CARROCERIA, 'No informado') AS Vehículo 
                , COUNT(*) AS 'Número de vehículos'
                FROM matriculaciones
                GROUP BY 1
                ORDER BY 2 DESC
            """).df()
            fig8 = px.bar(df_fig8, x="Vehículo", y="Número de vehículos", template="seaborn"
                , title="Matriculaciones por tipo de vehículo")
            fig8.update_xaxes(dtick=1)
            fig8.update_yaxes(nticks=20, rangemode="tozero", tickformat=",.0f")
            st.plotly_chart(fig8, use_container_width=True)