import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def grafico_formularios_por_dia(df_checkins):
    if "date_init" in df_checkins.columns:
        df_checkins["date"] = pd.to_datetime(df_checkins["date_init"]).dt.date
        daily_forms = df_checkins.groupby("date").size().reset_index(name="total_forms")
        
        daily_form_details = df_checkins.groupby("date").agg({
            "dasa": "sum",
            "promo": "sum",
            "sos": "sum",
            "visibilidad": "sum",
            "competencia": "sum",
            "ejecucion": "sum",
            "calidad": "sum",
            "concurso": "sum",
            "promo_c": "sum",
            "secundarias": "sum",
            "checkin_id": "count"
        }).reset_index()

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=daily_forms["date"], 
            y=daily_forms["total_forms"],
            fill='tozeroy',
            mode='none',
            name='Total Formularios',
            fillcolor='rgba(0,100,80,0.2)'
        ))

        for column in ["dasa", "promo", "sos", "visibilidad", "competencia", "ejecucion", "calidad", "concurso", "promo_c", "secundarias"]:
            if column in daily_form_details.columns:
                fig.add_trace(go.Scatter(
                    x=daily_form_details["date"], 
                    y=daily_form_details[column], 
                    mode='lines',
                    name=column
                ))

        fig.add_trace(go.Scatter(
            x=daily_form_details["date"], 
            y=daily_form_details["checkin_id"], 
            mode='lines',
            name='Total Checkins',
            line=dict(color='firebrick', width=4, dash='dash')
        ))

        fig.update_layout(title="Detalle de Formularios y Checkins por Día",
                          xaxis_title="Fecha",
                          yaxis_title="Cantidad",
                          showlegend=True)

        st.plotly_chart(fig)
    else:
        st.warning("La columna 'date_init' no existe en los datos de check-ins.")

def mapa_checkins(df_checkins):
    if "checkin_location" in df_checkins.columns:
        df_checkins[['latitude', 'longitude']] = df_checkins['checkin_location'].str.split(',', expand=True)
        df_checkins['latitude'] = pd.to_numeric(df_checkins['latitude'], errors='coerce')
        df_checkins['longitude'] = pd.to_numeric(df_checkins['longitude'], errors='coerce')
        if "objective" in df_checkins.columns and "form_count" in df_checkins.columns:
            df_checkins['color'] = df_checkins.apply(lambda row: 'Complete' if row['objective'] == 1 else ('Incomplete' if row['form_count'] > 0 else 'Empty'), axis=1)
        
            fig = px.scatter_mapbox(df_checkins.dropna(subset=['latitude', 'longitude']), 
                                  lat='latitude', lon='longitude', 
                                  color='color', 
                                  color_discrete_map={'Complete':'#0000FF', 'Incomplete':'#FFEA00', 'Empty':'#FF0000'},
                                  title='Mapa de Check-ins',
                                  height=700)

            fig.update_layout(mapbox=dict(
                style="open-street-map",  # Usa OpenStreetMap
                zoom=4,
                center={"lat": -34.6037, "lon": -58.3816}
            ))

            fig.update_traces(marker=dict(size=10),
                               selector=dict(mode='markers'))
            fig.update_layout(coloraxis_colorbar=dict(
                title="Status",
                tickvals=['#0000FF', '#FFEA00', '#FF0000'],
                ticktext=['complete', 'incomplete', 'empty']
            ))
            st.plotly_chart(fig)
        else:
            st.warning("Las columnas 'objective' o 'form_count' no existen en los datos de check-ins.")
    else:
        st.warning("La columna 'checkin_location' no existe en los datos de check-ins.")