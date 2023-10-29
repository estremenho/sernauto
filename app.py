import streamlit as st
from src.page_1 import run_data
from src.page_2 import run_tend
from src.page_3 import run_model
from src.page_4 import run_bastidor
from src.page_5 import run_marcas

  
st.set_page_config(page_title="SERNAUTO | Asociación Española de Proveedores de Automoción",
    page_icon="Empty", layout="wide")  

def main():
    page_names = ['Página Inicial', 'Matriculaciones','Tendencias', 'Predicción de venta', 'Consulta Bastidor', "Marcas"]
    page_selection = st.sidebar.selectbox('Selecciona una página:',page_names)
    
    pages_main = {
        "Página Inicial": run_intro,
        "Matriculaciones": run_page_1,
        "Tendencias": run_page_2,
        "Predicción de ventas": run_page_3,
        "Consulta Bastidor": run_page_4,
        "Marcas": run_page_5
    }

    pages_main[page_selection]()
    
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def run_intro():
    st.image('logo.png')
    st.header('Sernauto - Matriculaciones en España 2015-2023')
    st.text("Herramienta para el análisis de las matriculaciones de Turismos y Todoterrenos nuevos")
    st.text("Contenido:")
    st.code("""
        - Matriculaciones: datos generales de matriculaciones.
        - Tendencias: sección que analiza las principales tendencias
        - Predicción de ventas: sección que permite obtener predicciones sobre las nuevas matriculaciones de coches.
        - Consulta Bastidor: sección que permite obtener los datos de un vehículo a partir de su nº de bastidor.
        - Marcas: consulta la evolución de las matriculaciones por marca y modelo.
    """)

def run_page_1():
    run_data()
    
def run_page_2():
    run_tend()
        
def run_page_3():
    run_model()

def run_page_4():
    run_bastidor()
    
def run_page_5():
    run_marcas()

if __name__ == '__main__':
	main()