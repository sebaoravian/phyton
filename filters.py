import pandas as pd
import datetime

def obtener_fechas_rango(opcion):
    hoy = datetime.date.today()
    if opcion == "Mes en curso":
        inicio = hoy.replace(day=1)
        fin = hoy
    elif opcion == "Mes anterior":
        primer_dia_mes_actual = hoy.replace(day=1)
        ultimo_dia_mes_anterior = primer_dia_mes_actual - datetime.timedelta(days=1)
        inicio = ultimo_dia_mes_anterior.replace(day=1)
        fin = ultimo_dia_mes_anterior
    elif opcion == "Últimos 30 días":
        inicio = hoy - datetime.timedelta(days=30)
        fin = hoy
    elif opcion == "Últimos 60 días":
        inicio = hoy - datetime.timedelta(days=60)
        fin = hoy
    elif opcion == "Últimos 90 días":
        inicio = hoy - datetime.timedelta(days=90)
        fin = hoy
    elif opcion == "Últimos 7 días":
        inicio = hoy - datetime.timedelta(days=7)
        fin = hoy
    elif opcion == "Semana anterior":
        fin = hoy - datetime.timedelta(days=hoy.weekday() + 1)
        inicio = fin - datetime.timedelta(days=6)
    else:
        inicio = hoy.replace(day=1)
        fin = hoy
    return inicio, fin

def aplicar_filtros(df, filtros):
    if filtros["user_email"] and "user_email" in df.columns:
        df = df[df["user_email"].str.contains(filtros["user_email"], case=False, na=False)]
        
    if filtros["pos_code"] and "pos_code" in df.columns:
        df = df[df["pos_code"].str.contains(filtros["pos_code"], case=False, na=False)]
    
    if filtros["user_area_name"] and "user_area_name" in df.columns:
        df = df[df["user_area_name"].isin(filtros["user_area_name"])]
    if filtros["user_role_name"] and "user_role_name" in df.columns:
        df = df[df["user_role_name"].isin(filtros["user_role_name"])]
    if filtros["user_region_name"] and "user_region_name" in df.columns:
        df = df[df["user_region_name"].isin(filtros["user_region_name"])]
    if filtros["user_department_name"] and "user_department_name" in df.columns:
        df = df[df["user_department_name"].isin(filtros["user_department_name"])]
    
    if filtros["pos_area_name"] and "pos_area_name" in df.columns:
        df = df[df["pos_area_name"].isin(filtros["pos_area_name"])]
    if filtros["pos_format_name"] and "pos_format_name" in df.columns:
        df = df[df["pos_format_name"].isin(filtros["pos_format_name"])]
    if filtros["pos_cluster_name"] and "pos_cluster_name" in df.columns:
        df = df[df["pos_cluster_name"].isin(filtros["pos_cluster_name"])]
    if filtros["pos_retailer_name"] and "pos_retailer_name" in df.columns:
        df = df[df["pos_retailer_name"].isin(filtros["pos_retailer_name"])]
    if filtros["pos_region_name"] and "pos_region_name" in df.columns:
        df = df[df["pos_region_name"].isin(filtros["pos_region_name"])]
    if filtros["pos_flag_name"] and "pos_flag_name" in df.columns:
        df = df[df["pos_flag_name"].isin(filtros["pos_flag_name"])]
    
    if filtros["objective"] and "objective" in df.columns:
        df = df[df["objective"] == 1]
    
    if "date_init" in df.columns and "date_finish" in df.columns:
        df["date_init"] = pd.to_datetime(df["date_init"], format='mixed', errors='coerce')
        df["date_finish"] = pd.to_datetime(df["date_finish"], format='mixed', errors='coerce')
        df = df[(df["date_init"] >= pd.to_datetime(filtros["fecha_inicio_manual"])) & (df["date_finish"] <= pd.to_datetime(filtros["fecha_fin_manual"]))]
    
    return df