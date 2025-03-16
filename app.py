import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import math

# Configuración de la página
st.set_page_config(
    page_title="Seguimiento de Pagos MBA BCG",
    page_icon="🎓",
    layout="wide",
)

# Título y descripción
st.title("🎓 ¿Cuánto has pagado de tu deuda MBA?")

# Fechas clave
fecha_inicio = datetime(2024, 8, 1)
duracion_meses = 24
fecha_fin = datetime(2026, 7, 31)  # Fecha fija en lugar de cálculo con timedelta

# Cálculo del progreso
fecha_actual = datetime.now()
if fecha_actual < fecha_inicio:
    dias_transcurridos = 0
    porcentaje_completado = 0
elif fecha_actual > fecha_fin:
    dias_transcurridos = duracion_meses * 30
    porcentaje_completado = 100
else:
    dias_transcurridos = (fecha_actual - fecha_inicio).days
    porcentaje_completado = min(100, (dias_transcurridos / (duracion_meses * 30)) * 100)

dias_restantes = max(0, (fecha_fin - fecha_actual).days)
meses_restantes = math.ceil(dias_restantes / 30)

# Crear columnas para el diseño
col1, col2 = st.columns([2, 1])

with col1:
    # Mostrar el porcentaje de progreso de manera simple
    st.markdown(f"### Progreso: {porcentaje_completado:.1f}%")
    
    # Agregar pie chart para el progreso
    fig_pie = go.Figure(data=[go.Pie(
        values=[porcentaje_completado, 100-porcentaje_completado],
        labels=['Completado', 'Pendiente'],
        hole=.3,
        marker_colors=['royalblue', 'lightgray']
    )])
    
    fig_pie.update_layout(
        height=300,
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    # Tarjeta informativa
    st.markdown(f"""
    #### Detalles importantes:
    - **Día que volviste:** {fecha_inicio.strftime('%d/%m/%Y')}
    - **Día que terminas:** {fecha_fin.strftime('%d/%m/%Y')}
    - **Duración total:** {duracion_meses} meses
    - **Tiempo transcurrido:** {dias_transcurridos} días
    - **Tiempo restante:** {dias_restantes} días 
    """)

# Crear un gráfico de timeline
st.markdown("### Línea de tiempo del MBA")

# Crear datos para la línea de tiempo
meses = pd.date_range(start=fecha_inicio, end=fecha_fin, freq='MS')
meses_df = pd.DataFrame({
    'Mes': [d.strftime('%b %Y') for d in meses],
    'Valor': [100/duracion_meses] * len(meses),
    'Estado': ['Completado' if d <= fecha_actual else 'Pendiente' for d in meses]
})

fig_timeline = go.Figure()

# Añadir barras completadas
fig_timeline.add_trace(go.Bar(
    x=meses_df[meses_df['Estado'] == 'Completado']['Mes'],
    y=meses_df[meses_df['Estado'] == 'Completado']['Valor'],
    name='Completado',
    marker_color='royalblue'
))

# Añadir barras pendientes
fig_timeline.add_trace(go.Bar(
    x=meses_df[meses_df['Estado'] == 'Pendiente']['Mes'],
    y=meses_df[meses_df['Estado'] == 'Pendiente']['Valor'],
    name='Pendiente',
    marker_color='lightgray'
))

# Actualizar diseño
fig_timeline.update_layout(
    title='Progreso mensual',
    xaxis_title='Mes',
    yaxis_title='Porcentaje',
    barmode='stack',
    height=300,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)

st.plotly_chart(fig_timeline, use_container_width=True)

# Añadir un footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Vamos que se puede</p>", 
    unsafe_allow_html=True
)