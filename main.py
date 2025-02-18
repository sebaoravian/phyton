import streamlit as st
from filters import obtener_fechas_rango
from dashboard import dashboard
from forms import listado_formularios
from data_processing import cargar_datos_s3 as cargar_datos  # Actualizar la importación

def main():
    st.set_page_config(layout="wide")
    
    if "filtros" not in st.session_state:
        fecha_inicio, fecha_fin = obtener_fechas_rango("Mes en curso")
        st.session_state.filtros = {
            "user_email": "",
            "pos_code": "",
            "user_area_name": [],
            "user_role_name": [],
            "user_region_name": [],
            "user_department_name": [],
            "pos_area_name": [],
            "pos_format_name": [],
            "pos_cluster_name": [],
            "pos_retailer_name": [],
            "pos_region_name": [],
            "pos_flag_name": [],
            "objective": False,
            "fecha_inicio_manual": fecha_inicio,
            "fecha_fin_manual": fecha_fin
        }
    
    filtros = st.session_state.filtros
    
    with st.sidebar:
        st.header("Filtros")
        
        if st.button("Limpiar Filtros"):
            fecha_inicio, fecha_fin = obtener_fechas_rango("Mes en curso")
            st.session_state.filtros = {
                "user_email": "",
                "pos_code": "",
                "user_area_name": [],
                "user_role_name": [],
                "user_region_name": [],
                "user_department_name": [],
                "pos_area_name": [],
                "pos_format_name": [],
                "pos_cluster_name": [],
                "pos_retailer_name": [],
                "pos_region_name": [],
                "pos_flag_name": [],
                "objective": False,
                "fecha_inicio_manual": fecha_inicio,
                "fecha_fin_manual": fecha_fin
            }
            st.rerun()
        
        rango_fechas = st.selectbox("Seleccionar Rango de Fechas", ["Mes en curso", "Mes anterior", "Últimos 30 días", "Últimos 60 días", "Últimos 90 días", "Últimos 7 días", "Semana anterior", "Últimos 14 días", "Últimos 365 días"])
        fecha_inicio, fecha_fin = obtener_fechas_rango(rango_fechas)
        
        filtros["fecha_inicio_manual"] = st.date_input("Fecha de Inicio", fecha_inicio)
        filtros["fecha_fin_manual"] = st.date_input("Fecha de Fin", fecha_fin)
        
        filtros["objective"] = st.checkbox("Mostrar solo usuarios que cumplen el objetivo", False)
        
        filtros["user_email"] = st.text_input("Buscar por Email de Usuario", "")
        filtros["pos_code"] = st.text_input("Buscar por Código de Posición", "")
        
        df_checkins = cargar_datos("detailscheckins.csv")
        user_area_name_options = df_checkins["user_area_name"].dropna().unique()
        user_role_name_options = df_checkins["user_role_name"].dropna().unique()
        user_region_name_options = df_checkins["user_region_name"].dropna().unique()
        user_department_name_options = df_checkins["user_department_name"].dropna().unique()
        pos_area_name_options = df_checkins["pos_area_name"].dropna().unique()
        pos_format_name_options = df_checkins["pos_format_name"].dropna().unique()
        pos_cluster_name_options = df_checkins["pos_cluster_name"].dropna().unique()
        pos_retailer_name_options = df_checkins["pos_retailer_name"].dropna().unique()
        pos_region_name_options = df_checkins["pos_region_name"].dropna().unique()
        pos_flag_name_options = df_checkins["pos_flag_name"].dropna().unique()
        
        filtros["user_area_name"] = st.multiselect("Seleccionar Áreas de Usuario", user_area_name_options)
        filtros["user_role_name"] = st.multiselect("Seleccionar Roles de Usuario", user_role_name_options)
        filtros["user_region_name"] = st.multiselect("Seleccionar Regiones de Usuario", user_region_name_options)
        filtros["user_department_name"] = st.multiselect("Seleccionar Departamentos de Usuario", user_department_name_options)
        
        filtros["pos_area_name"] = st.multiselect("Seleccionar Áreas de Posición", pos_area_name_options)
        filtros["pos_format_name"] = st.multiselect("Seleccionar Formatos de Posición", pos_format_name_options)
        filtros["pos_cluster_name"] = st.multiselect("Seleccionar Clusters de Posición", pos_cluster_name_options)
        filtros["pos_retailer_name"] = st.multiselect("Seleccionar Retailers de Posición", pos_retailer_name_options)
        filtros["pos_region_name"] = st.multiselect("Seleccionar Regiones de Posición", pos_region_name_options)
        filtros["pos_flag_name"] = st.multiselect("Seleccionar Flags de Posición", pos_flag_name_options)
    
    tabs = st.tabs(["Dashboard de Check-ins", "Listado de Formularios"])
    
    with tabs[0]:
        dashboard(filtros)
    
    with tabs[1]:
        listado_formularios(filtros)

if __name__ == "__main__":
    main()