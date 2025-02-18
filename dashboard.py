import streamlit as st
import pandas as pd
from data_processing import cargar_datos_rango_fechas, limpiar_identificadores, limpiar_valores
from filters import aplicar_filtros
from visualizations import grafico_formularios_por_dia, mapa_checkins

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

def dashboard(filtros):
    st.title("📊 Dashboard de Check-ins y Cumplimiento")
    
    fecha_actual = filtros.get("fecha_inicio_manual")
    fecha_anterior = (pd.to_datetime(fecha_actual) - pd.DateOffset(months=1)).strftime('%Y-%m-%d')
    
    print(f"Cargando datos para el rango: {filtros['fecha_inicio_manual']} - {filtros['fecha_fin_manual']}")
    df_checkins = cargar_datos_rango_fechas(filtros["fecha_inicio_manual"], filtros["fecha_fin_manual"], "detailscheckins.csv")
    
    if df_checkins.empty:
        st.warning("No se encontraron datos para la fecha actual.")
        return
    
    # Limpiar valores de los conteos de formularios y los identificadores
    columnas_a_limpiar = ["dasa", "promo", "sos", "visibilidad", "competencia", "ejecucion", "calidad", "concurso", "promo_c", "secundarias", "form_count"]
    df_checkins = limpiar_valores(df_checkins, columnas_a_limpiar)
    
    df_checkins = limpiar_identificadores(df_checkins)
    df_checkins = aplicar_filtros(df_checkins, filtros)
    
    # Calcular datos del periodo actual
    total_checkins = df_checkins["checkin_id"].nunique() if "checkin_id" in df_checkins.columns else 0
    objetivos_cumplidos = df_checkins[df_checkins["objective"] == 1].shape[0] if "objective" in df_checkins.columns else 0
    porcentaje_objetivos = int((objetivos_cumplidos / total_checkins) * 100) if total_checkins > 0 else 0
    total_usuarios = df_checkins["user_email"].nunique() if "user_email" in df_checkins.columns else 0
    total_formularios = df_checkins[[col for col in df_checkins.columns if col.lower() in {"dasa", "promo", "sos", "visibilidad", "competencia", "ejecucion", "calidad", "concurso", "promo_c", "secundarias"}]].sum().sum()
    
    print(f"Cargando datos para la fecha anterior: {fecha_anterior}")
    df_checkins_anterior = cargar_datos_rango_fechas(fecha_anterior, fecha_anterior, "detailscheckins.csv")
    
    if df_checkins_anterior.empty:
        st.warning("No se encontraron datos para la fecha anterior.")
        return
    
    df_checkins_anterior = limpiar_identificadores(df_checkins_anterior)
    df_checkins_anterior = aplicar_filtros(df_checkins_anterior, filtros)
    
    # Calcular datos del periodo anterior
    total_checkins_anterior = df_checkins_anterior["checkin_id"].nunique() if "checkin_id" in df_checkins_anterior.columns else 0
    objetivos_cumplidos_anterior = df_checkins_anterior[df_checkins_anterior["objective"] == 1].shape[0] if "objective" in df_checkins_anterior.columns else 0
    porcentaje_objetivos_anterior = int((objetivos_cumplidos_anterior / total_checkins_anterior) * 100) if total_checkins_anterior > 0 else 0
    total_usuarios_anterior = df_checkins_anterior["user_email"].nunique() if "user_email" in df_checkins_anterior.columns else 0
    total_formularios_anterior = df_checkins_anterior[[col for col in df_checkins_anterior.columns if col.lower() in {"dasa", "promo", "sos", "visibilidad", "competencia", "ejecucion", "calidad", "concurso", "promo_c", "secundarias"}]].sum().sum()
    
    # Calcular variaciones
    variacion_checkins = calcular_variacion(total_checkins, total_checkins_anterior)
    variacion_objetivos_cumplidos = calcular_variacion(objetivos_cumplidos, objetivos_cumplidos_anterior)
    variacion_porcentaje_objetivos = calcular_variacion(porcentaje_objetivos, porcentaje_objetivos_anterior)
    variacion_usuarios = calcular_variacion(total_usuarios, total_usuarios_anterior)
    variacion_formularios = calcular_variacion(total_formularios, total_formularios_anterior)
    
    # Widgets de información
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Usuarios", total_usuarios, variacion_usuarios)
    col2.metric("Checkins", total_checkins, variacion_checkins)
    col3.metric("Objetivos cumplidos", objetivos_cumplidos, variacion_objetivos_cumplidos)
    col4.metric("Porcentaje de Objetivos", f"{porcentaje_objetivos}%", variacion_porcentaje_objetivos)
    col5.metric("Formularios", total_formularios, variacion_formularios)
    
    grafico_formularios_por_dia(df_checkins)
    mapa_checkins(df_checkins)
    
    # Tabla interactiva
    st.subheader("Detalle de Check-ins")
    columnas_a_mostrar = ["date_init", "date_finish", "checkin_duration", "checkin_id", "user_email", "user_area_name", "user_role_name", "user_region_name", "user_department_name", "pos_name", "dasa", "promo", "sos", "visibilidad", "competencia", "ejecucion", "calidad", "concurso", "promo_c", "secundarias", "form_count"]
    columnas_a_mostrar = [col for col in columnas_a_mostrar if col in df_checkins.columns]
    st.dataframe(df_checkins[columnas_a_mostrar])
    
    # Alertas dinámicas
    st.subheader("🚨 Alertas")
    usuarios_incumplidos = df_checkins[df_checkins['objective'] == 0] if "objective" in df_checkins.columns else pd.DataFrame()
    if not usuarios_incumplidos.empty:
        st.warning(f"Usuarios que no cumplen el objetivo: {len(usuarios_incumplidos)}")
    
    st.success("Análisis completado. Ajusta los filtros para ver más detalles.")