import pandas as pd
import boto3
from io import StringIO
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

s3 = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
bucket_name = 'resources-one'

def cargar_datos_s3(nombre_archivo):
    """ Carga un archivo CSV desde S3 y lo convierte en un DataFrame. """
    key = 'dashboard/one_danone/' + nombre_archivo  
    csv_obj = s3.get_object(Bucket=bucket_name, Key=key)
    body = csv_obj['Body'].read().decode('utf-8')
    df = pd.read_csv(StringIO(body), low_memory=False)
    return df

def archivo_existe_s3(s3_key):
    """ Verifica si un archivo existe en S3. """
    try:
        s3.head_object(Bucket=bucket_name, Key=s3_key)
        return True
    except:
        return False

def cargar_datos_previos(s3_key):
    """ Carga datos previos desde S3 si el archivo ya existe. """
    if archivo_existe_s3(s3_key):
        csv_obj = s3.get_object(Bucket=bucket_name, Key=s3_key)
        body = csv_obj['Body'].read().decode('utf-8')
        return pd.read_csv(StringIO(body), low_memory=False)
    return pd.DataFrame()

# def split_csv_by_day_and_upload(df, folder, date_column, filename):
#     """ Divide un DataFrame en múltiples archivos CSV por día y maneja duplicados. """
#     df[date_column] = pd.to_datetime(df[date_column])
    
#     for date, group in df.groupby(df[date_column].dt.date):
#         s3_key = f'dashboard/one_danone/{folder}/{date}/{filename}'
#         df_prev = cargar_datos_previos(s3_key)
#         df_combined = pd.concat([df_prev, group]).drop_duplicates()
        
#         csv_buffer = StringIO()
#         df_combined.to_csv(csv_buffer, index=False)
#         s3.put_object(Bucket=bucket_name, Key=s3_key, Body=csv_buffer.getvalue())
#         print(f'Subido a S3: {s3_key}')

def split_csv_by_day_and_upload(df, folder, date_column, filename):
    """ Divide un DataFrame en múltiples archivos CSV por día y maneja duplicados. """
    # Convertir la columna de fechas sin especificar el formato exacto, permitiendo formatos mixtos
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce', infer_datetime_format=True)
    
    for date, group in df.groupby(df[date_column].dt.date):
        s3_key = f'dashboard/one_danone/{folder}/{date}/{filename}'
        df_prev = cargar_datos_previos(s3_key)
        df_combined = pd.concat([df_prev, group]).drop_duplicates()
        
        csv_buffer = StringIO()
        df_combined.to_csv(csv_buffer, index=False)
        s3.put_object(Bucket=bucket_name, Key=s3_key, Body=csv_buffer.getvalue())
        print(f'Subido a S3: {s3_key}')


def limpiar_identificadores(df):
    """ Elimina comillas en columnas de identificadores. """
    for col in df.columns:
        if 'id_' in col or '_id' in col:
            df[col] = df[col].apply(lambda x: x.replace('"', '') if isinstance(x, str) else x)
    return df

# Procesar los CSVs desde S3 y dividirlos por día, luego subirlos a S3
if __name__ == "__main__":
    try:
        df_checkins = cargar_datos_s3("detailscheckins.csv")
        df_forms = cargar_datos_s3("detailsforms.csv")
        
        df_checkins = limpiar_identificadores(df_checkins)
        df_forms = limpiar_identificadores(df_forms)
        
        split_csv_by_day_and_upload(df_checkins, "split_checkins", "date_init", "detailscheckins.csv")
        split_csv_by_day_and_upload(df_forms, "split_forms", "date_init", "detailsforms.csv")
        
    except Exception as e:
        print(f"Error procesando archivos: {e}")
