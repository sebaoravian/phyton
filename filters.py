import pandas as pd

def obtener_fechas_rango(rango):
    """ Devuelve las fechas de inicio y fin para un rango de fechas dado. """
    hoy = pd.Timestamp.today()
    
    if rango == "Mes en curso":
        inicio = hoy.replace(day=1)
        fin = hoy
    elif rango == "Mes anterior":
        inicio = (hoy.replace(day=1) - pd.DateOffset(months=1)).replace(day=1)
        fin = hoy.replace(day=1) - pd.DateOffset(days=1)
    elif rango == "Últimos 30 días":
        inicio = hoy - pd.DateOffset(days=30)
        fin = hoy
    elif rango == "Últimos 60 días":
        inicio = hoy - pd.DateOffset(days=60)
        fin = hoy
    elif rango == "Últimos 90 días":
        inicio = hoy - pd.DateOffset(days=90)
        fin = hoy
    elif rango == "Últimos 7 días":
        inicio = hoy - pd.DateOffset(days=7)
        fin = hoy
    elif rango == "Semana anterior":
        inicio = hoy - pd.DateOffset(days=hoy.weekday() + 7)
        fin = hoy - pd.DateOffset(days=hoy.weekday() + 1)
    elif rango == "Personalizado":
        inicio = hoy
        fin = hoy
    else:
        inicio = hoy
        fin = hoy
    
    return inicio.strftime('%Y-%m-%d'), fin.strftime('%Y-%m-%d')

def aplicar_filtros(df, filtros):
    """ Aplica los filtros al DataFrame. """
    if filtros["user_email"]:
        df = df[df["user_email"].str.contains(filtros["user_email"], case=False, na=False)]
    if filtros["pos_code"]:
        df = df[df["pos_code"].str.contains(filtros["pos_code"], case=False, na=False)]
    if filtros["user_area_name"]:
        df = df[df["user_area_name"].isin(filtros["user_area_name"])]
    if filtros["user_role_name"]:
        df = df[df["user_role_name"].isin(filtros["user_role_name"])]
    if filtros["user_region_name"]:
        df = df[df["user_region_name"].isin(filtros["user_region_name"])]
    if filtros["user_department_name"]:
        df = df[df["user_department_name"].isin(filtros["user_department_name"])]
    if filtros["pos_area_name"]:
        df = df[df["pos_area_name"].isin(filtros["pos_area_name"])]
    if filtros["pos_format_name"]:
        df = df[df["pos_format_name"].isin(filtros["pos_format_name"])]
    if filtros["pos_cluster_name"]:
        df = df[df["pos_cluster_name"].isin(filtros["pos_cluster_name"])]
    if filtros["pos_retailer_name"]:
        df = df[df["pos_retailer_name"].isin(filtros["pos_retailer_name"])]
    if filtros["pos_region_name"]:
        df = df[df["pos_region_name"].isin(filtros["pos_region_name"])]
    if filtros["pos_flag_name"]:
        df = df[df["pos_flag_name"].isin(filtros["pos_flag_name"])]
    if filtros["objective"]:
        df = df[df["objective"] == 1]
    if "fecha_inicio_manual" in filtros and "fecha_fin_manual" in filtros:
        df["date_init"] = pd.to_datetime(df["date_init"], errors='coerce')
        filtros["fecha_inicio_manual"] = pd.to_datetime(filtros["fecha_inicio_manual"])
        filtros["fecha_fin_manual"] = pd.to_datetime(filtros["fecha_fin_manual"])
        df = df[(df["date_init"] >= filtros["fecha_inicio_manual"]) & (df["date_init"] <= filtros["fecha_fin_manual"])]
    
    return df