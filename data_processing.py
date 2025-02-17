import pandas as pd

def cargar_datos(nombre_archivo):
    return pd.read_csv(nombre_archivo, low_memory=False)

def limpiar_valores(valor):
    if isinstance(valor, str):
        valor = valor.replace('*', '').replace('Alert!', '').strip().replace('"', '')
    return pd.to_numeric(valor, errors='coerce')

def limpiar_identificadores(df):
    for col in df.columns:
        if 'id_' in col or '_id' in col:
            df[col] = df[col].apply(lambda x: x.replace('"', '') if isinstance(x, str) else x)
    return df

def limpiar_porcentajes(df, columnas):
    for columna in columnas:
        if columna in df.columns:
            df[columna] = df[columna].astype(str).str.replace('%', '').apply(pd.to_numeric, errors='coerce')
    return df