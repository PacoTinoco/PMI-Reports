import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Configuración de página
st.set_page_config(
    page_title="Philip Morris - Análisis de Operadores",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Título principal
st.title("🏭 Philip Morris - Análisis de Performance de Operadores")
st.markdown("---")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv('data_weekly_processed.csv')
    df['Fecha_Inicio'] = pd.to_datetime(df['Fecha_Inicio'])
    df['Fecha_Fin'] = pd.to_datetime(df['Fecha_Fin'])
    return df

df = load_data()

# Información de indicadores (para colores y descripciones)
INDICATOR_INFO = {
    'MTBF': {
        'name': 'MTBF (Mean Time Between Failures)',
        'better': 'higher',
        'color': '#2ecc71',
        'description': '⬆️ Mayor es mejor - Tiempo promedio entre fallas'
    },
    'Reject_Rate': {
        'name': 'Reject Rate',
        'better': 'lower',
        'color': '#e74c3c',
        'description': '⬇️ Menor es mejor - Porcentaje de productos rechazados'
    },
    'Strategic_PR': {
        'name': 'Strategic PR (Production Rate)',
        'better': 'higher',
        'color': '#3498db',
        'description': '⬆️ Mayor es mejor - Tasa de producción estratégica'
    },
    'UPDT': {
        'name': 'UPDT (Unplanned Downtime)',
        'better': 'lower',
        'color': '#f39c12',
        'description': '⬇️ Menor es mejor - Tiempo de inactividad no planificado'
    }
}

# ==================== SIDEBAR ====================
st.sidebar.header("🎯 Filtros")

# 1. Seleccionar Coordinador
coordinadores = ['Todos'] + sorted(df['Coordinador'].unique().tolist())
coordinador_selected = st.sidebar.selectbox(
    "👤 Seleccionar Coordinador (LC)",
    coordinadores,
    index=0
)

# 2. Filtrar operadores según coordinador
if coordinador_selected == 'Todos':
    operadores_disponibles = sorted(df['Operador'].unique().tolist())
else:
    operadores_disponibles = sorted(
        df[df['Coordinador'] == coordinador_selected]['Operador'].unique().tolist()
    )

operadores_selected = st.sidebar.multiselect(
    "👥 Seleccionar Operadores (puedes elegir varios)",
    operadores_disponibles,
    default=operadores_disponibles[:2] if len(operadores_disponibles) >= 2 else operadores_disponibles
)

# 3. Seleccionar Máquinas
maquinas_disponibles = sorted(df['Maquina'].unique().tolist())
maquinas_selected = st.sidebar.multiselect(
    "🏭 Seleccionar Máquinas (puedes elegir varias)",
    maquinas_disponibles,
    default=maquinas_disponibles[:2] if len(maquinas_disponibles) >= 2 else maquinas_disponibles
)

# 4. Seleccionar Indicador
indicador_selected = st.sidebar.selectbox(
    "📊 Seleccionar Indicador",
    list(INDICATOR_INFO.keys()),
    format_func=lambda x: INDICATOR_INFO[x]['name']
)

# Mostrar descripción del indicador
st.sidebar.info(INDICATOR_INFO[indicador_selected]['description'])

# 5. Rango de Weeks (opcional)
week_min = int(df['Week'].min())
week_max = int(df['Week'].max())
week_range = st.sidebar.slider(
    "📅 Rango de Weeks",
    week_min, week_max,
    (week_min, week_max)
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Resumen de Filtros")
st.sidebar.write(f"**Coordinador:** {coordinador_selected}")
st.sidebar.write(f"**Operadores:** {len(operadores_selected)}")
st.sidebar.write(f"**Máquinas:** {len(maquinas_selected)}")
st.sidebar.write(f"**Indicador:** {INDICATOR_INFO[indicador_selected]['name']}")

# ==================== FILTRAR DATOS ====================
df_filtered = df[
    (df['Operador'].isin(operadores_selected)) &
    (df['Maquina'].isin(maquinas_selected)) &
    (df['Indicador'] == indicador_selected) &
    (df['Week'] >= week_range[0]) &
    (df['Week'] <= week_range[1])
].copy()

# ==================== VALIDACIONES ====================
if len(operadores_selected) == 0:
    st.warning("⚠️ Por favor selecciona al menos un operador")
    st.stop()

if len(maquinas_selected) == 0:
    st.warning("⚠️ Por favor selecciona al menos una máquina")
    st.stop()

if len(df_filtered) == 0:
    st.error("❌ No hay datos disponibles con los filtros seleccionados")
    st.stop()

# ==================== MÉTRICAS PRINCIPALES ====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_registros = len(df_filtered)
    st.metric("📊 Registros Totales", f"{total_registros:,}")

with col2:
    weeks_analizadas = df_filtered['Week'].nunique()
    st.metric("📅 Weeks Analizadas", weeks_analizadas)

with col3:
    promedio_general = df_filtered['Valor_Promedio'].mean()
    st.metric(f"📈 Promedio General", f"{promedio_general:.2f}")

with col4:
    mejor_performance = df_filtered['Valor_Promedio'].min() if INDICATOR_INFO[indicador_selected]['better'] == 'lower' else df_filtered['Valor_Promedio'].max()
    st.metric(f"🏆 Mejor Performance", f"{mejor_performance:.2f}")

st.markdown("---")

# ==================== GRÁFICA PRINCIPAL: EVOLUCIÓN TEMPORAL ====================
st.subheader(f"📈 Evolución Temporal - {INDICATOR_INFO[indicador_selected]['name']}")

# Crear figura con Plotly
fig = go.Figure()

# Colores para operadores
colors = px.colors.qualitative.Set3
color_map = {op: colors[i % len(colors)] for i, op in enumerate(operadores_selected)}

for operador in operadores_selected:
    for maquina in maquinas_selected:
        df_plot = df_filtered[
            (df_filtered['Operador'] == operador) &
            (df_filtered['Maquina'] == maquina)
        ].sort_values('Week')
        
        if len(df_plot) > 0:
            fig.add_trace(go.Scatter(
                x=df_plot['Week'],
                y=df_plot['Valor_Promedio'],
                mode='lines+markers',
                name=f"{operador} - {maquina}",
                line=dict(width=2, color=color_map[operador]),
                marker=dict(size=6),
                hovertemplate=
                    '<b>%{fullData.name}</b><br>' +
                    'Week: %{x}<br>' +
                    f'{indicador_selected}:' + '%{y:.2f}<br>' +
                    '<extra></extra>'
            ))

# Añadir línea de promedio general
promedio_total = df_filtered['Valor_Promedio'].mean()
fig.add_hline(
    y=promedio_total,
    line_dash="dash",
    line_color="red",
    annotation_text=f"Promedio General: {promedio_total:.2f}",
    annotation_position="top right"
)

fig.update_layout(
    xaxis_title="Week",
    yaxis_title=f"{INDICATOR_INFO[indicador_selected]['name']}",
    hovermode='x unified',
    height=500,
    showlegend=True,
    legend=dict(
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02
    )
)

st.plotly_chart(fig, use_container_width=True)

# ==================== TABLA COMPARATIVA ====================
st.markdown("---")
st.subheader("📋 Tabla Comparativa de Performance")

# Calcular estadísticas por operador y máquina
stats_table = df_filtered.groupby(['Coordinador', 'Operador', 'Maquina']).agg({
    'Valor_Promedio': ['mean', 'min', 'max', 'std', 'count']
}).round(2)

stats_table.columns = ['Promedio', 'Mínimo', 'Máximo', 'Desv. Est.', 'Weeks']
stats_table = stats_table.reset_index()

# Ordenar según el indicador (mejor performance primero)
if INDICATOR_INFO[indicador_selected]['better'] == 'lower':
    stats_table = stats_table.sort_values('Promedio', ascending=True)
else:
    stats_table = stats_table.sort_values('Promedio', ascending=False)

# Añadir ranking
stats_table.insert(0, 'Ranking', range(1, len(stats_table) + 1))

st.dataframe(stats_table, use_container_width=True, height=400)

# ==================== RESUMEN POR COORDINADOR ====================
st.markdown("---")
st.subheader("🎯 Resumen por Coordinador (LC)")

# Filtrar por todos los coordinadores disponibles en los datos filtrados
coordinadores_en_datos = df_filtered['Coordinador'].unique()

col1, col2 = st.columns([2, 1])

with col1:
    # Crear gráfica de barras comparativa
    coord_stats = df_filtered.groupby('Coordinador')['Valor_Promedio'].agg(['mean', 'std']).reset_index()
    coord_stats.columns = ['Coordinador', 'Promedio', 'Desv_Est']
    
    fig_coord = go.Figure()
    
    fig_coord.add_trace(go.Bar(
        x=coord_stats['Coordinador'],
        y=coord_stats['Promedio'],
        error_y=dict(type='data', array=coord_stats['Desv_Est']),
        marker_color=['#3498db', '#e74c3c', '#2ecc71'],
        text=coord_stats['Promedio'].round(2),
        textposition='outside'
    ))
    
    fig_coord.update_layout(
        title=f"Comparación de Coordinadores - {INDICATOR_INFO[indicador_selected]['name']}",
        xaxis_title="Coordinador",
        yaxis_title="Promedio",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig_coord, use_container_width=True)

with col2:
    st.markdown("#### 📊 Estadísticas")
    for coord in coordinadores_en_datos:
        df_coord = df_filtered[df_filtered['Coordinador'] == coord]
        promedio = df_coord['Valor_Promedio'].mean()
        operadores_count = df_coord['Operador'].nunique()
        
        st.markdown(f"""
        **{coord}**
        - Promedio: `{promedio:.2f}`
        - Operadores: `{operadores_count}`
        - Registros: `{len(df_coord)}`
        """)
        st.markdown("---")

# ==================== DESCARGA DE DATOS ====================
st.markdown("---")
st.subheader("💾 Exportar Datos")

col1, col2 = st.columns(2)

with col1:
    # Exportar datos filtrados
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Datos Filtrados (CSV)",
        data=csv,
        file_name=f"performance_{indicador_selected}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with col2:
    # Exportar tabla resumen
    csv_stats = stats_table.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Tabla Resumen (CSV)",
        data=csv_stats,
        file_name=f"resumen_{indicador_selected}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Footer
st.markdown("---")
st.markdown("### 📌 Notas")
st.info("""
- **Promedio Semanal**: Calculado promediando todos los turnos (S1, S2, S3) de cada semana
- **Week 2**: Inicia el 6 de enero de 2025
- **Datos**: Del 13 de enero al 19 de octubre de 2025 (Week 3 a Week 42)
""")