import streamlit as st
import pandas as pd
from data_processing import cargar_datos_s3 as cargar_datos, limpiar_identificadores, limpiar_porcentajes, limpiar_valores
from filters import aplicar_filtros

def calcular_variacion(actual, anterior):
    try:
        actual = float(actual)
        anterior = float(anterior)
        if anterior == 0:
            return "N/A"
        variacion = ((actual - anterior) / anterior) * 100
        return f"{variacion:.0f}%"
    except (ValueError, TypeError):
        return "N/A"

def listado_formularios(filtros):
    st.title("Listado de Formularios")
    
    fecha_actual = filtros.get("fecha_inicio_manual")
    fecha_anterior = (pd.to_datetime(fecha_actual) - pd.DateOffset(months=1)).strftime('%Y-%m-%d')
    
    df_forms = cargar_datos("detailsforms.csv", date=fecha_actual)
    
    # Limpiar identificadores y porcentajes
    df_forms = limpiar_identificadores(df_forms)
    df_forms = limpiar_porcentajes(df_forms, ["max_score_activity", "score", "ponderation"])
    df_forms = limpiar_valores(df_forms, ["dasa", "promo", "sos", "visibilidad", "competencia", "ejecucion", "calidad", "concurso", "promo_c", "secundarias"])
    
    # Cruzar datos con el DataFrame de check-ins para obtener filtros adicionales
    df_checkins = cargar_datos("detailscheckins.csv", date=fecha_actual)
    df_checkins = limpiar_identificadores(df_checkins)
    
    df_forms = df_forms.merge(df_checkins, left_on="id_checkin", right_on="checkin_id", how="left", suffixes=("", "_checkin"))
    df_forms = aplicar_filtros(df_forms, filtros)
    
    # Filtrar los formularios que no tienen name_activity
    df_forms = df_forms[df_forms['name_activity'].notna()]
    
    # Calcular datos del periodo actual
    total_formularios = df_forms.shape[0]
    total_usuarios = df_forms["email_user"].nunique() if "email_user" in df_forms.columns else 0
    
    df_forms_anterior = cargar_datos("detailsforms.csv", date=fecha_anterior)
    df_forms_anterior = limpiar_identificadores(df_forms_anterior)
    df_forms_anterior = limpiar_porcentajes(df_forms_anterior, ["max_score_activity", "score", "ponderation"])
    df_forms_anterior = limpiar_valores(df_forms_anterior, ["dasa", "promo", "sos", "visibilidad", "competencia", "ejecucion", "calidad", "concurso", "promo_c", "secundarias"])
    df_forms_anterior = df_forms_anterior.merge(df_checkins, left_on="id_checkin", right_on="checkin_id", how="left", suffixes=("", "_checkin"))
    df_forms_anterior = aplicar_filtros(df_forms_anterior, filtros)
    
    # Calcular datos del periodo anterior
    total_formularios_anterior = df_forms_anterior.shape[0]
    total_usuarios_anterior = df_forms_anterior["email_user"].nunique() if "email_user" in df_forms_anterior.columns else 0
    
    # Calcular variaciones
    variacion_formularios = calcular_variacion(total_formularios, total_formularios_anterior)
    variacion_usuarios = calcular_variacion(total_usuarios, total_usuarios_anterior)
    
    # Mostrar solo las columnas específicas
    columnas_a_mostrar = ["date_init", "date_finish", "time_activity", "email_user", "id_checkin", "name_pos", "pos_code", "name_activity", "max_score_activity", "score", "ponderation"]
    columnas_a_mostrar = [col for col in columnas_a_mostrar if col in df_forms.columns]
    
    # Crear widgets superiores para cada name_activity en una grilla de 4 columnas por fila
    actividades_prioritarias = ["$DASA", "SOS", "Visibilidad", "Promo"]
    actividades = df_forms["name_activity"].unique()
    
    # Crear lista de actividades en orden de prioridad
    actividades_en_orden = [act for act in actividades_prioritarias if act in actividades] + [act for act in actividades if act not in actividades_prioritarias]
    
    # Mostrar las actividades en la grilla de 4 columnas
    cols = st.columns(4)
    for i, actividad in enumerate(actividades_en_orden):
        actividad_df = df_forms[df_forms["name_activity"] == actividad]
        conteo = actividad_df.shape[0]
        conteo_anterior = df_forms_anterior[df_forms_anterior["name_activity"] == actividad].shape[0]
        variacion_conteo = calcular_variacion(conteo, conteo_anterior)
        
        if actividad in actividades_prioritarias:
            promedio_ponderation = actividad_df["ponderation"].mean() if "ponderation" in actividad_df.columns else 0
            promedio_ponderation_text = f"{promedio_ponderation:.0f}%" if promedio_ponderation else "N/A"
            promedio_ponderation_anterior = df_forms_anterior[df_forms_anterior["ponderation"] == actividad]["ponderation"].mean() if "ponderation" in df_forms_anterior.columns else 0
            variacion_ponderation = calcular_variacion(promedio_ponderation, promedio_ponderation_anterior)
            
            if promedio_ponderation < 60:
                delta_color = "inverse"
                icono = "⚠️"
            elif promedio_ponderation < 80:
                delta_color = "normal"
                icono = "⚠️"
            else:
                delta_color = "normal"
                icono = ""
                
            cols[i % 4].metric(f"{actividad} - Conteo", conteo, variacion_conteo)
            cols[i % 4].metric(f"{actividad} - Promedio Ponderation", f"{promedio_ponderation_text} {icono}", variacion_ponderation, delta_color=delta_color, help="Promedio de Ponderación")
        else:
            cols[i % 4].metric(f"{actividad} - Conteo", conteo, variacion_conteo)
            
        if (i + 1) % 4 == 0:
            cols = st.columns(4)
    
    col1, col2 = st.columns(2)
    col1.metric("Total Formularios", total_formularios, variacion_formularios)
    col2.metric("Total Usuarios", total_usuarios, variacion_usuarios)
    
    st.dataframe(df_forms[columnas_a_mostrar])