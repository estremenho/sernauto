# source/page_4.py
import duckdb
import pandas as pd
import streamlit as st

# Conéctate a la base de datos DuckDB en modo de solo lectura
con = duckdb.connect(database='matriculaciones.duckdb', read_only=True)

# Crear una página en Streamlit
def run_bastidor():
    st.image('logo.png')
    st.title("Buscar detalles vehículo por Bastidor 🚗")
     
    # Solicitar al usuario que ingrese un número de bastidor
    st.text("Ingrese un número de bastidor:")
    bastidor = st.text_input("Por ejemplo, WV2ZZZ7HZJH039651")

    # Botón para buscar el bastidor
    if st.button(f"Buscar 🔍"):
        if bastidor:
            matching_rows = con.execute("""
                SELECT FECHA_MATRICULA,
                    MARCA,
                    MODELO,
                    COD_PROCEDENCIA_ITV,
                    BASTIDOR,
                    COD_TIPO,
                    PROPULSION,
                    CILINDRADA_ITV,
                    COD_PROVINCIA_MAT,
                    CP,
                    PERSONA_FISICA_JURIDICA,
                    SERVICIO,
                    RENTING,
                    CARROCERIA
                FROM matriculaciones 
                WHERE BASTIDOR = ?""", [bastidor]).df()
            if not matching_rows.empty:
                st.markdown(f"✅ Bastidor encontrado.", unsafe_allow_html=True)
                for column in matching_rows.columns:
                    value = matching_rows[column].values[0]
                    st.write(f"**{column}:** {value}")
            else:
                st.markdown(f"❌ Bastidor no encontrado.", unsafe_allow_html=True)

# Ejecutar la función para mostrar la página
if __name__ == "__main__":
    run_bastidor()