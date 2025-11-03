# 🏭 Philip Morris - Operator Performance Analytics Dashboard

<div align="center">

![Philip Morris](https://img.shields.io/badge/Philip%20Morris-Manufacturing%20Excellence-red?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Dash](https://img.shields.io/badge/Dash-2.14.2-00D4FF?style=for-the-badge&logo=plotly&logoColor=white)
![License](https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge)

**Un sistema avanzado de análisis de performance para operadores de líneas de producción KDF**

[Características](#-características-principales) •
[Demo](#-demo) •
[Instalación](#-instalación-rápida) •
[Uso](#-uso) •
[Arquitectura](#-arquitectura-del-sistema) •
[Contribución](#-contribución)

</div>

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Características Principales](#-características-principales)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación Rápida](#-instalación-rápida)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Uso](#-uso)
- [Indicadores de Performance](#-indicadores-de-performance)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Roadmap](#-roadmap)
- [Contribución](#-contribución)
- [Licencia](#-licencia)
- [Contacto](#-contacto)

---

## 🎯 Descripción General

Este proyecto es un **dashboard interactivo de análisis de performance** desarrollado para Philip Morris International, diseñado específicamente para monitorear y evaluar el desempeño de operadores en las líneas de producción KDF (KDF-7, KDF-8, KDF-9, KDF-10, KDF-11, KDF-17).

### 🎪 El Problema que Resuelve

En entornos de manufactura de alta precisión, es crítico:
- ✅ Identificar operadores de alto rendimiento
- ✅ Detectar áreas de mejora operacional
- ✅ Optimizar la rotación de turnos
- ✅ Reducir tiempos de inactividad no planificados
- ✅ Minimizar tasas de rechazo de productos

### 💡 La Solución

Un sistema de visualización de datos en tiempo real que:
- 📊 Consolida métricas de **6 máquinas** y **4 indicadores clave**
- 👥 Rastrea el desempeño de **15 operadores** bajo **3 coordinadores**
- 📅 Analiza datos semanales con granularidad diaria
- 🔍 Permite comparaciones multi-dimensionales
- 📈 Genera insights accionables para la toma de decisiones

---

## ✨ Características Principales

### 🎛️ Filtros Dinámicos e Interactivos

| Filtro | Descripción |
|--------|-------------|
| **👤 Coordinador (LC)** | Selección de Line Coordinator para filtrar su equipo |
| **👥 Operadores** | Multi-selección para comparativas entre múltiples operadores |
| **🏭 Máquinas** | Análisis de 1 o más líneas KDF simultáneamente |
| **📊 Indicadores** | MTBF, Reject Rate, Strategic PR, UPDT |
| **📅 Rango Temporal** | Slider de weeks (Week 2 - Week 43, 2025) |

### 📈 Visualizaciones Avanzadas
```
┌─────────────────────────────────────────────────────────┐
│  📊 Métricas KPI en Tiempo Real                         │
│  • Registros Totales  • Weeks Analizadas               │
│  • Promedio General   • Mejor Performance              │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  📈 Gráfica de Evolución Temporal                       │
│  • Líneas comparativas multi-operador/máquina          │
│  • Línea de tendencia general                          │
│  • Hover tooltips con detalles                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  📋 Tabla de Rankings                                   │
│  • Ordenamiento automático por performance             │
│  • Estadísticas descriptivas (mean, std, min, max)    │
│  • Resaltado del top performer                         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  🎯 Comparativa de Coordinadores                        │
│  • Gráfica de barras con error bars                    │
│  • Estadísticas por Line Coordinator                   │
└─────────────────────────────────────────────────────────┘
```

### 💾 Exportación de Datos

- **CSV de datos filtrados**: Exporta el dataset completo según filtros aplicados
- **CSV de tabla resumen**: Rankings y estadísticas descriptivas
- **Timestamps automáticos**: Cada archivo incluye fecha de generación

---

## 🛠️ Tecnologías Utilizadas

### Core Technologies

<div align="center">

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| ![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white) | 3.11+ | Lenguaje principal |
| ![Pandas](https://img.shields.io/badge/Pandas-2.1.0-150458?style=flat-square&logo=pandas&logoColor=white) | 2.1.0 | Procesamiento de datos |
| ![Plotly](https://img.shields.io/badge/Plotly-5.17.0-3F4F75?style=flat-square&logo=plotly&logoColor=white) | 5.17.0 | Visualizaciones interactivas |
| ![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-FF4B4B?style=flat-square&logo=streamlit&logoColor=white) | 1.29.0 | Framework UI principal |
| ![Dash](https://img.shields.io/badge/Dash-2.14.2-00D4FF?style=flat-square&logo=plotly&logoColor=white) | 2.14.2 | Framework UI alternativo |

</div>

### Additional Libraries
```python
numpy==1.25.0          # Computación numérica
openpyxl==3.1.2        # Lectura de archivos Excel
matplotlib==3.8.0      # Visualizaciones estáticas (análisis exploratorio)
seaborn==0.12.2        # Visualizaciones estadísticas avanzadas
```

---

## 📋 Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **Python 3.11 o superior** ([Descargar](https://www.python.org/downloads/))
- **pip** (gestor de paquetes de Python)
- **Git** (opcional, para clonar el repositorio)

### Verificación de Instalación
```bash
python --version  # Debe mostrar Python 3.11.x o superior
pip --version     # Debe mostrar pip 23.x o superior
```

---

## 🚀 Instalación Rápida

### Opción 1: Clonar el Repositorio
```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/philip-morris-operator-dashboard.git
cd philip-morris-operator-dashboard

# 2. Crear entorno virtual (recomendado)
python -m venv venv

# 3. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar dashboard Streamlit
streamlit run app.py

# O ejecutar dashboard Dash
python app_dash.py
```

### Opción 2: Instalación Manual
```bash
# Instalar paquetes individuales
pip install streamlit pandas plotly numpy openpyxl matplotlib seaborn dash
```

---

## 📁 Estructura del Proyecto
```
philip-morris-operator-dashboard/
│
├── 📄 README.md                          # Este archivo
├── 📄 requirements.txt                   # Dependencias del proyecto
├── 📄 .gitignore                         # Archivos ignorados por Git
│
├── 📂 data/                              # Datos de entrada (XLSX)
│   ├── 📂 KDF-7/
│   │   ├── MTBF - Shift 3.xlsx
│   │   ├── Reject Rate - Shift 3.xlsx
│   │   ├── Stratergic PR - Shift 3.xlsx
│   │   └── UPDT Categories - Shift 3.xlsx
│   ├── 📂 KDF-8/
│   ├── 📂 KDF-9/
│   ├── 📂 KDF-10/
│   ├── 📂 KDF-11/
│   └── 📂 KDF-17/
│
├── 📂 notebooks/                         # Jupyter notebooks (análisis exploratorio)
│   └── 📓 data_exploration.ipynb
│
├── 📂 processed_data/                    # Datos procesados (CSV)
│   ├── data_weekly_processed.csv         # Dataset principal agregado por semana
│   ├── data_daily_processed.csv          # Dataset diario completo (backup)
│   └── operators_assignments.csv         # Asignaciones de operadores
│
├── 📂 assets/                            # Recursos estáticos (solo Dash)
│   └── styles.css                        # Estilos personalizados
│
├── 🐍 app.py                             # Dashboard Streamlit (principal)
├── 🐍 app_dash.py                        # Dashboard Dash (alternativo)
│
└── 📂 src/                               # Código fuente modular (futuro)
    ├── data_processing.py
    ├── visualizations.py
    └── utils.py
```

---

## 💻 Uso

### Iniciar el Dashboard

#### Streamlit (Recomendado para uso interno)
```bash
streamlit run app.py
```

**Acceso:** http://localhost:8501

#### Dash (Recomendado para producción)
```bash
python app_dash.py
```

**Acceso:** http://localhost:8050

---

### Flujo de Trabajo Típico

1. **Seleccionar Coordinador** - Filtrar por Line Coordinator (MAYRA, PEDRO, ANDRES)
2. **Filtrar Operadores** - Elegir uno o varios operadores del equipo
3. **Elegir Máquinas** - Seleccionar las líneas KDF a analizar
4. **Seleccionar Indicador** - MTBF, Reject Rate, Strategic PR o UPDT
5. **Ajustar Rango de Weeks** - Definir período temporal de análisis
6. **Analizar Visualizaciones** - Interpretar gráficas y tablas
7. **Exportar Resultados** - Descargar datos en CSV

### Casos de Uso Comunes

#### 1️⃣ Comparar Desempeño de Operadores de un Coordinador
```
1. Seleccionar Coordinador: MAYRA
2. Operadores: [Todos los de MAYRA]
3. Máquinas: KDF-7, KDF-9
4. Indicador: MTBF
5. Análisis: ¿Quién tiene mejor tiempo entre fallas?
```

#### 2️⃣ Evaluar Impacto de Rotación de Turnos
```
1. Seleccionar Operador: Ramirez Alvarado Fernando
2. Máquina: KDF-7
3. Indicador: Reject Rate
4. Ver evolución week-by-week durante cambios de turno
```

#### 3️⃣ Identificar Mejores Prácticas por Máquina
```
1. Coordinador: Todos
2. Máquina: KDF-10 (solo una)
3. Indicador: Strategic PR
4. Ranking: Ver top 3 operadores
```

---

## 📊 Indicadores de Performance

### 1. MTBF (Mean Time Between Failures)

**Descripción:** Tiempo promedio entre fallas de la máquina  
**Unidad:** Minutos  
**Interpretación:** ⬆️ **Mayor es mejor**  
**Rango típico:** 50 - 500 minutos  
```
MTBF = Tiempo Total de Operación / Número de Fallas
```

**Ejemplo:**
- Operador A: MTBF = 450 min → 1 falla cada 7.5 horas ✅
- Operador B: MTBF = 120 min → 1 falla cada 2 horas ⚠️

---

### 2. Reject Rate (Tasa de Rechazo)

**Descripción:** Porcentaje de productos que no pasan control de calidad  
**Unidad:** % (porcentaje)  
**Interpretación:** ⬇️ **Menor es mejor**  
**Rango típico:** 0.5% - 5%  
```
Reject Rate = (Productos Rechazados / Total Producido) × 100
```

**Ejemplo:**
- Operador A: 1.2% → Excelente calidad ✅
- Operador B: 4.8% → Requiere capacitación ⚠️

---

### 3. Strategic PR (Production Rate)

**Descripción:** Tasa de producción estratégica vs objetivo  
**Unidad:** % (porcentaje del objetivo)  
**Interpretación:** ⬆️ **Mayor es mejor**  
**Rango típico:** 85% - 105%  
```
Strategic PR = (Producción Real / Producción Objetivo) × 100
```

**Ejemplo:**
- Operador A: 102% → Supera expectativas ✅
- Operador B: 88% → Por debajo del objetivo ⚠️

---

### 4. UPDT (Unplanned Downtime)

**Descripción:** Tiempo de inactividad no planificado  
**Unidad:** % (porcentaje del tiempo total)  
**Interpretación:** ⬇️ **Menor es mejor**  
**Rango típico:** 2% - 15%  
```
UPDT = (Tiempo de Inactividad No Planificado / Tiempo Total) × 100
```

**Ejemplo:**
- Operador A: 3.5% → Gestión eficiente ✅
- Operador B: 12.8% → Muchas paradas imprevistas ⚠️

---

## 🏗️ Arquitectura del Sistema

### Pipeline de Datos
```
┌─────────────────┐
│  Excel Files    │  ← Datos crudos por máquina/indicador
│  (.xlsx)        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Data Loading    │  ← Lectura con pandas (skiprows=2)
│ & Parsing       │  ← Parseo de columna 'Shift'
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Week Calculation│  ← Asignación de week numbers
│ & Date Mapping  │  ← Week 2 = 06/Ene/2025
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Operator        │  ← Merge con asignaciones
│ Assignment      │  ← fecha + turno + máquina → operador
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Weekly          │  ← Agregación semanal
│ Aggregation     │  ← Promedio S1+S2+S3 por week
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Processed CSV   │  ← data_weekly_processed.csv
│ (Ready for UI)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Dashboard UI    │  ← Streamlit / Dash
│ (Interactive)   │  ← Filtros + Visualizaciones
└─────────────────┘
```

### Modelo de Datos
```sql
-- Tabla Principal: data_weekly_processed
Week (int)                    -- Número de semana (2-43)
Mes (string)                  -- Nombre del mes
Mes_Num (int)                 -- Número del mes (1-12)
Coordinador (string)          -- LC: MAYRA, PEDRO, ANDRES
Operador (string)             -- Nombre completo del operador
Maquina (string)              -- KDF-7, KDF-8, ..., KDF-17
Indicador (string)            -- MTBF, Reject_Rate, Strategic_PR, UPDT
Valor_Promedio (float)        -- Promedio semanal del indicador
Fecha_Inicio (date)           -- Primera fecha de la week
Fecha_Fin (date)              -- Última fecha de la week
Dias_Trabajados (int)         -- Días con datos en esa week
```

---

## 📸 Capturas de Pantalla

### Dashboard Principal (Streamlit)

> *Próximamente: Agregar screenshots del dashboard en acción*

### Filtros Interactivos

> *Próximamente: Capturas de los filtros dinámicos*

### Análisis Comparativo

> *Próximamente: Ejemplos de gráficas comparativas*

---

## 🗺️ Roadmap

### ✅ Fase 1: MVP (Completado)
- [x] Procesamiento de datos Excel
- [x] Cálculo de weeks
- [x] Asignación de operadores
- [x] Dashboard Streamlit funcional
- [x] Dashboard Dash alternativo
- [x] Exportación de datos

### 🚧 Fase 2: Mejoras (En Progreso)
- [ ] Autenticación de usuarios (dash-auth)
- [ ] Carga automática de datos desde servidor
- [ ] Notificaciones de anomalías
- [ ] Reportes PDF automatizados

### 🔮 Fase 3: Avanzado (Planeado)
- [ ] Machine Learning para predicción de performance
- [ ] Alertas en tiempo real (Slack/Email)
- [ ] Integración con ERP de Philip Morris
- [ ] Mobile-responsive design
- [ ] API REST para consumo externo

---

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Por favor sigue estos pasos:

### Proceso de Contribución

1. **Fork** el repositorio
2. **Crea** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abre** un Pull Request

### Coding Standards

- **PEP 8** para estilo de código Python
- **Type hints** para funciones críticas
- **Docstrings** para todas las funciones públicas
- **Tests unitarios** para nuevas funcionalidades

### Reportar Bugs

Usa el [Issue Tracker](https://github.com/tu-usuario/philip-morris-operator-dashboard/issues) e incluye:
- Descripción clara del problema
- Pasos para reproducirlo
- Comportamiento esperado vs actual
- Screenshots (si aplica)
- Versión de Python y dependencias

---

## 📄 Licencia

Este proyecto es **propiedad de Philip Morris International** y está bajo licencia propietaria.

**Todos los derechos reservados © 2025 Philip Morris International**

El uso, reproducción o distribución de este software sin autorización expresa está **estrictamente prohibido**.

---

### Soporte Técnico

Para soporte interno de Philip Morris:
- **Helpdesk:** +1 (XXX) XXX-XXXX
- **Email:** it-support@philipmorris.com
- **Portal Interno:** [PM Internal Portal](https://internal.philipmorris.com)

---

## 🙏 Agradecimientos

Este proyecto fue posible gracias a:

- **Streamlit & Plotly Teams** - Por sus excelentes frameworks
- **Python Community** - Por las increíbles librerías open-source

---

## 📚 Recursos Adicionales

### Documentación Oficial

- [Streamlit Docs](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Dash User Guide](https://dash.plotly.com/)

### Tutoriales Relacionados

- [Data Visualization Best Practices](https://www.storytellingwithdata.com/)
- [Manufacturing KPIs Guide](https://www.industryweek.com/technology-and-iiot/article/21134424/10-manufacturing-kpis-you-should-be-tracking)
- [Python for Data Analysis](https://wesmckinney.com/book/)

---

<div align="center">

**Hecho con ❤️ para Philip Morris International**

⭐ Si este proyecto te resultó útil, considera darle una estrella

[![Star on GitHub](https://img.shields.io/github/stars/tu-usuario/philip-morris-operator-dashboard.svg?style=social)](https://github.com/tu-usuario/philip-morris-operator-dashboard)

</div>

---

<div align="center">
  <sub>Built with Python 🐍 | Powered by Streamlit ⚡ | Visualized with Plotly 📊</sub>
</div>
