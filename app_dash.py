import dash
from dash import dcc, html, Input, Output, State, dash_table
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

# Inicializar la app
app = dash.Dash(
    __name__,
    title="Philip Morris - Análisis de Operadores",
    update_title="Cargando...",
    suppress_callback_exceptions=True
)

# Cargar datos
df = pd.read_csv('data_weekly_processed.csv')
df['Fecha_Inicio'] = pd.to_datetime(df['Fecha_Inicio'])
df['Fecha_Fin'] = pd.to_datetime(df['Fecha_Fin'])

# Información de indicadores
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

# Configuración de colores
COLORS = {
    'background': '#f8f9fa',
    'sidebar': '#2c3e50',
    'card': '#ffffff',
    'text': '#2c3e50',
    'border': '#dee2e6',
    'primary': '#3498db',
    'success': '#2ecc71',
    'danger': '#e74c3c',
    'warning': '#f39c12'
}

# ==================== LAYOUT ====================
app.layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.H1("🏭 Philip Morris - Análisis de Performance de Operadores",
                   style={
                       'color': 'white',
                       'margin': '0',
                       'padding': '20px',
                       'fontSize': '28px',
                       'fontWeight': 'bold'
                   })
        ], style={
            'backgroundColor': COLORS['sidebar'],
            'textAlign': 'center'
        })
    ]),
    
    # Main Container
    html.Div([
        # Sidebar
        html.Div([
            html.H3("🎯 Filtros", style={'color': 'white', 'textAlign': 'center', 'marginBottom': '20px'}),
            
            # Coordinador
            html.Label("👤 Seleccionar Coordinador (LC)", style={'color': 'white', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='coordinador-dropdown',
                options=[{'label': 'Todos', 'value': 'Todos'}] + 
                        [{'label': c, 'value': c} for c in sorted(df['Coordinador'].unique())],
                value='Todos',
                style={'marginBottom': '20px'}
            ),
            
            # Operadores
            html.Label("👥 Seleccionar Operadores", style={'color': 'white', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='operadores-dropdown',
                multi=True,
                style={'marginBottom': '20px'}
            ),
            
            # Máquinas
            html.Label("🏭 Seleccionar Máquinas", style={'color': 'white', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='maquinas-dropdown',
                options=[{'label': m, 'value': m} for m in sorted(df['Maquina'].unique())],
                value=sorted(df['Maquina'].unique())[:2],
                multi=True,
                style={'marginBottom': '20px'}
            ),
            
            # Indicador
            html.Label("📊 Seleccionar Indicador", style={'color': 'white', 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='indicador-dropdown',
                options=[{'label': INDICATOR_INFO[k]['name'], 'value': k} 
                        for k in INDICATOR_INFO.keys()],
                value='MTBF',
                style={'marginBottom': '20px'}
            ),
            
            # Descripción del indicador
            html.Div(id='indicador-description', 
                    style={
                        'backgroundColor': 'rgba(255,255,255,0.1)',
                        'padding': '10px',
                        'borderRadius': '5px',
                        'color': 'white',
                        'fontSize': '12px',
                        'marginBottom': '20px'
                    }),
            
            # Rango de Weeks
            html.Label("📅 Rango de Weeks", style={'color': 'white', 'fontWeight': 'bold'}),
            dcc.RangeSlider(
                id='week-range-slider',
                min=int(df['Week'].min()),
                max=int(df['Week'].max()),
                value=[int(df['Week'].min()), int(df['Week'].max())],
                marks={i: str(i) for i in range(int(df['Week'].min()), int(df['Week'].max())+1, 5)},
                tooltip={"placement": "bottom", "always_visible": True},
                allowCross=False
            ),
            
            html.Hr(style={'borderColor': 'rgba(255,255,255,0.3)', 'marginTop': '30px', 'marginBottom': '20px'}),
            
            # Resumen de filtros
            html.H4("📋 Resumen", style={'color': 'white', 'textAlign': 'center'}),
            html.Div(id='filter-summary', style={'color': 'white', 'fontSize': '13px'})
            
        ], style={
            'width': '20%',
            'height': 'calc(100vh - 80px)',
            'position': 'fixed',
            'left': '0',
            'top': '80px',
            'backgroundColor': COLORS['sidebar'],
            'padding': '20px',
            'overflowY': 'auto',
            'boxShadow': '2px 0 5px rgba(0,0,0,0.1)'
        }),
        
        # Main Content
        html.Div([
            # Métricas principales
            html.Div(id='main-metrics', style={'marginBottom': '30px'}),
            
            # Gráfica principal
            html.Div([
                html.H3("📈 Evolución Temporal", 
                       style={'color': COLORS['text'], 'marginBottom': '20px'}),
                dcc.Graph(id='main-chart', style={'height': '500px'})
            ], style={
                'backgroundColor': COLORS['card'],
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'marginBottom': '30px'
            }),
            
            # Tabla comparativa
            html.Div([
                html.H3("📋 Tabla Comparativa de Performance", 
                       style={'color': COLORS['text'], 'marginBottom': '20px'}),
                html.Div(id='comparison-table')
            ], style={
                'backgroundColor': COLORS['card'],
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'marginBottom': '30px'
            }),
            
            # Resumen por coordinador
            html.Div([
                html.H3("🎯 Resumen por Coordinador (LC)", 
                       style={'color': COLORS['text'], 'marginBottom': '20px'}),
                html.Div([
                    html.Div([
                        dcc.Graph(id='coordinador-chart')
                    ], style={'width': '65%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                    
                    html.Div([
                        html.H4("📊 Estadísticas", style={'color': COLORS['text']}),
                        html.Div(id='coordinador-stats')
                    ], style={
                        'width': '33%',
                        'display': 'inline-block',
                        'verticalAlign': 'top',
                        'paddingLeft': '20px'
                    })
                ])
            ], style={
                'backgroundColor': COLORS['card'],
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'marginBottom': '30px'
            }),
            
            # Botones de descarga
            html.Div([
                html.H3("💾 Exportar Datos", 
                       style={'color': COLORS['text'], 'marginBottom': '20px'}),
                html.Div([
                    html.Button("📥 Descargar Datos Filtrados (CSV)", 
                               id='btn-download-filtered',
                               style={
                                   'backgroundColor': COLORS['primary'],
                                   'color': 'white',
                                   'border': 'none',
                                   'padding': '10px 20px',
                                   'borderRadius': '5px',
                                   'cursor': 'pointer',
                                   'marginRight': '10px',
                                   'fontSize': '14px'
                               }),
                    dcc.Download(id="download-filtered-data"),
                    
                    html.Button("📥 Descargar Tabla Resumen (CSV)", 
                               id='btn-download-summary',
                               style={
                                   'backgroundColor': COLORS['success'],
                                   'color': 'white',
                                   'border': 'none',
                                   'padding': '10px 20px',
                                   'borderRadius': '5px',
                                   'cursor': 'pointer',
                                   'fontSize': '14px'
                               }),
                    dcc.Download(id="download-summary-data")
                ])
            ], style={
                'backgroundColor': COLORS['card'],
                'padding': '20px',
                'borderRadius': '10px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'marginBottom': '30px'
            }),
            
            # Footer
            html.Div([
                html.H4("📌 Notas", style={'color': COLORS['text'], 'marginBottom': '10px'}),
                html.Ul([
                    html.Li("Promedio Semanal: Calculado promediando todos los turnos (S1, S2, S3) de cada semana"),
                    html.Li("Week 2: Inicia el 6 de enero de 2025"),
                    html.Li("Datos: Del 13 de enero al 19 de octubre de 2025 (Week 3 a Week 42)")
                ], style={'color': COLORS['text'], 'fontSize': '13px'})
            ], style={
                'backgroundColor': '#e3f2fd',
                'padding': '15px',
                'borderRadius': '10px',
                'marginBottom': '20px'
            })
            
        ], style={
            'marginLeft': '22%',
            'padding': '30px',
            'backgroundColor': COLORS['background'],
            'minHeight': '100vh'
        })
    ])
])

# ==================== CALLBACKS ====================

# Callback 1: Actualizar operadores según coordinador
@app.callback(
    Output('operadores-dropdown', 'options'),
    Output('operadores-dropdown', 'value'),
    Input('coordinador-dropdown', 'value')
)
def update_operadores(coordinador):
    if coordinador == 'Todos':
        operadores = sorted(df['Operador'].unique())
    else:
        operadores = sorted(df[df['Coordinador'] == coordinador]['Operador'].unique())
    
    options = [{'label': op, 'value': op} for op in operadores]
    default_value = operadores[:2] if len(operadores) >= 2 else operadores
    
    return options, default_value

# Callback 2: Actualizar descripción del indicador
@app.callback(
    Output('indicador-description', 'children'),
    Input('indicador-dropdown', 'value')
)
def update_indicator_description(indicador):
    return INDICATOR_INFO[indicador]['description']

# Callback 3: Actualizar resumen de filtros
@app.callback(
    Output('filter-summary', 'children'),
    Input('coordinador-dropdown', 'value'),
    Input('operadores-dropdown', 'value'),
    Input('maquinas-dropdown', 'value'),
    Input('indicador-dropdown', 'value')
)
def update_filter_summary(coordinador, operadores, maquinas, indicador):
    return html.Div([
        html.P(f"Coordinador: {coordinador}", style={'marginBottom': '5px'}),
        html.P(f"Operadores: {len(operadores) if operadores else 0}", style={'marginBottom': '5px'}),
        html.P(f"Máquinas: {len(maquinas) if maquinas else 0}", style={'marginBottom': '5px'}),
        html.P(f"Indicador: {INDICATOR_INFO[indicador]['name']}", style={'marginBottom': '5px'})
    ])

# Callback 4: Actualizar todos los componentes principales
@app.callback(
    Output('main-metrics', 'children'),
    Output('main-chart', 'figure'),
    Output('comparison-table', 'children'),
    Output('coordinador-chart', 'figure'),
    Output('coordinador-stats', 'children'),
    Input('operadores-dropdown', 'value'),
    Input('maquinas-dropdown', 'value'),
    Input('indicador-dropdown', 'value'),
    Input('week-range-slider', 'value')
)
def update_main_content(operadores, maquinas, indicador, week_range):
    # Validaciones
    if not operadores or not maquinas:
        empty_fig = go.Figure()
        empty_fig.add_annotation(
            text="Por favor selecciona al menos un operador y una máquina",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        return html.Div(), empty_fig, html.Div(), empty_fig, html.Div()
    
    # Filtrar datos
    df_filtered = df[
        (df['Operador'].isin(operadores)) &
        (df['Maquina'].isin(maquinas)) &
        (df['Indicador'] == indicador) &
        (df['Week'] >= week_range[0]) &
        (df['Week'] <= week_range[1])
    ].copy()
    
    if len(df_filtered) == 0:
        empty_fig = go.Figure()
        empty_fig.add_annotation(
            text="No hay datos disponibles con los filtros seleccionados",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        return html.Div(), empty_fig, html.Div(), empty_fig, html.Div()
    
    # 1. MÉTRICAS PRINCIPALES
    total_registros = len(df_filtered)
    weeks_analizadas = df_filtered['Week'].nunique()
    promedio_general = df_filtered['Valor_Promedio'].mean()
    mejor_performance = (df_filtered['Valor_Promedio'].min() 
                        if INDICATOR_INFO[indicador]['better'] == 'lower' 
                        else df_filtered['Valor_Promedio'].max())
    
    metrics = html.Div([
        # Métrica 1
        html.Div([
            html.Div("📊", style={'fontSize': '30px', 'marginBottom': '5px'}),
            html.Div("Registros Totales", style={'fontSize': '12px', 'color': '#7f8c8d'}),
            html.Div(f"{total_registros:,}", style={'fontSize': '24px', 'fontWeight': 'bold', 'color': COLORS['text']})
        ], style={
            'width': '23%',
            'display': 'inline-block',
            'backgroundColor': COLORS['card'],
            'padding': '20px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'marginRight': '2%'
        }),
        
        # Métrica 2
        html.Div([
            html.Div("📅", style={'fontSize': '30px', 'marginBottom': '5px'}),
            html.Div("Weeks Analizadas", style={'fontSize': '12px', 'color': '#7f8c8d'}),
            html.Div(f"{weeks_analizadas}", style={'fontSize': '24px', 'fontWeight': 'bold', 'color': COLORS['text']})
        ], style={
            'width': '23%',
            'display': 'inline-block',
            'backgroundColor': COLORS['card'],
            'padding': '20px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'marginRight': '2%'
        }),
        
        # Métrica 3
        html.Div([
            html.Div("📈", style={'fontSize': '30px', 'marginBottom': '5px'}),
            html.Div("Promedio General", style={'fontSize': '12px', 'color': '#7f8c8d'}),
            html.Div(f"{promedio_general:.2f}", style={'fontSize': '24px', 'fontWeight': 'bold', 'color': COLORS['text']})
        ], style={
            'width': '23%',
            'display': 'inline-block',
            'backgroundColor': COLORS['card'],
            'padding': '20px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
            'marginRight': '2%'
        }),
        
        # Métrica 4
        html.Div([
            html.Div("🏆", style={'fontSize': '30px', 'marginBottom': '5px'}),
            html.Div("Mejor Performance", style={'fontSize': '12px', 'color': '#7f8c8d'}),
            html.Div(f"{mejor_performance:.2f}", style={'fontSize': '24px', 'fontWeight': 'bold', 'color': COLORS['success']})
        ], style={
            'width': '23%',
            'display': 'inline-block',
            'backgroundColor': COLORS['card'],
            'padding': '20px',
            'borderRadius': '10px',
            'textAlign': 'center',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
        })
    ])
    
    # 2. GRÁFICA PRINCIPAL
    fig = go.Figure()
    
    colors_plotly = px.colors.qualitative.Set3
    color_map = {op: colors_plotly[i % len(colors_plotly)] for i, op in enumerate(operadores)}
    
    for operador in operadores:
        for maquina in maquinas:
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
                        f'{indicador}: ' + '%{y:.2f}<br>' +
                        '<extra></extra>'
                ))
    
    # Línea de promedio
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
        yaxis_title=f"{INDICATOR_INFO[indicador]['name']}",
        hovermode='x unified',
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        ),
        template='plotly_white'
    )
    
    # 3. TABLA COMPARATIVA
    stats_table = df_filtered.groupby(['Coordinador', 'Operador', 'Maquina']).agg({
        'Valor_Promedio': ['mean', 'min', 'max', 'std', 'count']
    }).round(2)
    
    stats_table.columns = ['Promedio', 'Mínimo', 'Máximo', 'Desv. Est.', 'Weeks']
    stats_table = stats_table.reset_index()
    
    # Ordenar
    if INDICATOR_INFO[indicador]['better'] == 'lower':
        stats_table = stats_table.sort_values('Promedio', ascending=True)
    else:
        stats_table = stats_table.sort_values('Promedio', ascending=False)
    
    stats_table.insert(0, 'Ranking', range(1, len(stats_table) + 1))
    
    table_component = dash_table.DataTable(
        data=stats_table.to_dict('records'),
        columns=[{'name': col, 'id': col} for col in stats_table.columns],
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
            'fontSize': '13px'
        },
        style_header={
            'backgroundColor': COLORS['primary'],
            'color': 'white',
            'fontWeight': 'bold',
            'textAlign': 'center'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 0},
                'backgroundColor': '#d4edda',
                'fontWeight': 'bold'
            }
        ],
        page_size=15
    )
    
    # 4. GRÁFICA DE COORDINADORES
    coord_stats = df_filtered.groupby('Coordinador')['Valor_Promedio'].agg(['mean', 'std']).reset_index()
    coord_stats.columns = ['Coordinador', 'Promedio', 'Desv_Est']
    
    fig_coord = go.Figure()
    
    fig_coord.add_trace(go.Bar(
        x=coord_stats['Coordinador'],
        y=coord_stats['Promedio'],
        error_y=dict(type='data', array=coord_stats['Desv_Est']),
        marker_color=[COLORS['primary'], COLORS['danger'], COLORS['success']],
        text=coord_stats['Promedio'].round(2),
        textposition='outside'
    ))
    
    fig_coord.update_layout(
        title=f"Comparación de Coordinadores - {INDICATOR_INFO[indicador]['name']}",
        xaxis_title="Coordinador",
        yaxis_title="Promedio",
        showlegend=False,
        template='plotly_white'
    )
    
    # 5. ESTADÍSTICAS DE COORDINADORES
    coordinadores_en_datos = df_filtered['Coordinador'].unique()
    coord_stats_div = []
    
    for coord in coordinadores_en_datos:
        df_coord = df_filtered[df_filtered['Coordinador'] == coord]
        promedio = df_coord['Valor_Promedio'].mean()
        operadores_count = df_coord['Operador'].nunique()
        
        coord_stats_div.append(
            html.Div([
                html.H5(coord, style={'color': COLORS['text'], 'marginBottom': '10px'}),
                html.P(f"Promedio: {promedio:.2f}", style={'margin': '5px 0'}),
                html.P(f"Operadores: {operadores_count}", style={'margin': '5px 0'}),
                html.P(f"Registros: {len(df_coord)}", style={'margin': '5px 0'}),
                html.Hr(style={'borderColor': COLORS['border'], 'margin': '15px 0'})
            ])
        )
    
    return metrics, fig, table_component, fig_coord, html.Div(coord_stats_div)

# Callback 5: Descargar datos filtrados
@app.callback(
    Output("download-filtered-data", "data"),
    Input("btn-download-filtered", "n_clicks"),
    State('operadores-dropdown', 'value'),
    State('maquinas-dropdown', 'value'),
    State('indicador-dropdown', 'value'),
    State('week-range-slider', 'value'),
    prevent_initial_call=True
)
def download_filtered(n_clicks, operadores, maquinas, indicador, week_range):
    if not operadores or not maquinas:
        return None
    
    df_filtered = df[
        (df['Operador'].isin(operadores)) &
        (df['Maquina'].isin(maquinas)) &
        (df['Indicador'] == indicador) &
        (df['Week'] >= week_range[0]) &
        (df['Week'] <= week_range[1])
    ]
    
    return dcc.send_data_frame(
        df_filtered.to_csv,
        f"performance_{indicador}_{datetime.now().strftime('%Y%m%d')}.csv",
        index=False
    )

# Callback 6: Descargar tabla resumen
@app.callback(
    Output("download-summary-data", "data"),
    Input("btn-download-summary", "n_clicks"),
    State('operadores-dropdown', 'value'),
    State('maquinas-dropdown', 'value'),
    State('indicador-dropdown', 'value'),
    State('week-range-slider', 'value'),
    prevent_initial_call=True
)
def download_summary(n_clicks, operadores, maquinas, indicador, week_range):
    if not operadores or not maquinas:
        return None
    
    df_filtered = df[
        (df['Operador'].isin(operadores)) &
        (df['Maquina'].isin(maquinas)) &
        (df['Indicador'] == indicador) &
        (df['Week'] >= week_range[0]) &
        (df['Week'] <= week_range[1])
    ]
    
    stats_table = df_filtered.groupby(['Coordinador', 'Operador', 'Maquina']).agg({
        'Valor_Promedio': ['mean', 'min', 'max', 'std', 'count']
    }).round(2)
    
    stats_table.columns = ['Promedio', 'Mínimo', 'Máximo', 'Desv. Est.', 'Weeks']
    stats_table = stats_table.reset_index()
    
    if INDICATOR_INFO[indicador]['better'] == 'lower':
        stats_table = stats_table.sort_values('Promedio', ascending=True)
    else:
        stats_table = stats_table.sort_values('Promedio', ascending=False)
    
    stats_table.insert(0, 'Ranking', range(1, len(stats_table) + 1))
    
    return dcc.send_data_frame(
        stats_table.to_csv,
        f"resumen_{indicador}_{datetime.now().strftime('%Y%m%d')}.csv",
        index=False
    )

# ==================== RUN APP ====================
if __name__ == '__main__':
    app.run(debug=True, port=8050)
    