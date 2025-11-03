import streamlit as st
import pandas as pd
import plotly.express as px
import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams
from collections import Counter
import re

# Descargar recursos de NLTK (solo la primera vez)
nltk.download('stopwords', quiet=True)
stop_words = set(stopwords.words('spanish'))

# ===========================
# FUNCIONES DE PROCESAMIENTO
# ===========================

def limpiar_texto(texto):
    """Limpieza básica de texto."""
    if pd.isna(texto):
        return ""
    texto = texto.lower()
    texto = re.sub(r'[^a-záéíóúñü\s]', '', texto)
    tokens = [t for t in texto.split() if t not in stop_words and len(t) > 2]
    return " ".join(tokens)

def obtener_ngrams(textos, n=2, top=15):
    """Devuelve los n-gramas más frecuentes."""
    all_tokens = []
    for texto in textos:
        tokens = texto.split()
        all_tokens.extend(list(ngrams(tokens, n)))
    counter = Counter(all_tokens)
    return counter.most_common(top)

# ===========================
# INTERFAZ STREAMLIT
# ===========================

st.set_page_config(page_title="Análisis de Preguntas Abiertas", layout="wide")
st.title("📊 Análisis Automático de Preguntas Abiertas")

st.markdown("""
Sube tu archivo Excel o CSV con las columnas:
**'ASIGNATURA', 'PREGUNTA', 'RESPUESTA'**  
Ahora puedes:
- Analizar varias **hojas de Excel**.  
- Seleccionar **más de una asignatura**.  
- Ver respuestas completas de **varios n-gramas**.
""")

archivo = st.file_uploader("📂 Sube tu archivo", type=["xlsx", "csv"])

if archivo:
    # ===========================
    # CARGA DE DATOS
    # ===========================
    if archivo.name.endswith(".csv"):
        df = pd.read_csv(archivo)
        hojas = ["Única hoja (CSV)"]
    else:
        xls = pd.ExcelFile(archivo)
        hojas = xls.sheet_names
        hoja_sel = st.selectbox("Selecciona la hoja del Excel a analizar:", hojas)
        df = pd.read_excel(xls, sheet_name=hoja_sel)

    columnas_requeridas = {"ASIGNATURA", "PREGUNTA", "RESPUESTA"}
    if not columnas_requeridas.issubset(set(df.columns)):
        st.error("❌ El archivo no contiene las columnas requeridas: 'ASIGNATURA', 'PREGUNTA', 'RESPUESTA'")
    else:
        st.success(f"✅ Archivo cargado correctamente ({len(df)} registros).")

        asignaturas = sorted(df['ASIGNATURA'].dropna().unique())
        asignaturas_sel = st.multiselect(
            "Selecciona una o varias asignaturas para analizar:",
            asignaturas,
            default=[asignaturas[0]] if asignaturas else None
        )

        df_asig = df[df['ASIGNATURA'].isin(asignaturas_sel)].copy()

        preguntas_unicas = df_asig['PREGUNTA'].dropna().unique()
        st.write(f"📘 **Preguntas encontradas:** {len(preguntas_unicas)}")
        for p in preguntas_unicas:
            st.write(f"🟢 {p}")

        st.write(f"💬 **Total de respuestas:** {len(df_asig)}")

        # ===========================
        # LIMPIEZA DE TEXTO
        # ===========================
        st.subheader("🔧 Limpieza de texto")
        df_asig["texto_limpio"] = df_asig["RESPUESTA"].apply(limpiar_texto)

        # ===========================
        # BIGRAMAS Y TRIGRAMAS
        # ===========================
        st.subheader("📈 Frecuencia de Bigramas y Trigramas")
        col1, col2 = st.columns(2)

        with col1:
            bigramas = obtener_ngrams(df_asig["texto_limpio"], n=2, top=15)
            if bigramas:
                df_bi = pd.DataFrame(bigramas, columns=["Bigrama", "Frecuencia"])
                df_bi["Bigrama"] = df_bi["Bigrama"].apply(lambda x: " ".join(x))
                fig_bi = px.bar(df_bi, x="Frecuencia", y="Bigrama", orientation="h", title="Top 15 Bigramas")
                st.plotly_chart(fig_bi, use_container_width=True)
            else:
                st.info("No se encontraron bigramas significativos.")

        with col2:
            trigramas = obtener_ngrams(df_asig["texto_limpio"], n=3, top=15)
            if trigramas:
                df_tri = pd.DataFrame(trigramas, columns=["Trigrama", "Frecuencia"])
                df_tri["Trigrama"] = df_tri["Trigrama"].apply(lambda x: " ".join(x))
                fig_tri = px.bar(df_tri, x="Frecuencia", y="Trigrama", orientation="h", title="Top 15 Trigramas")
                st.plotly_chart(fig_tri, use_container_width=True)
            else:
                st.info("No se encontraron trigramas significativos.")

        # ===========================
        # FILTRO POR N-GRAMAS
        # ===========================
        st.subheader("🔍 Filtrar respuestas por Bigramas/Trigramas")
        todas_opciones = []
        if bigramas:
            todas_opciones += [b[0] for b in bigramas]
        if trigramas:
            todas_opciones += [t[0] for t in trigramas]

        todas_opciones_texto = [" ".join(t) for t in todas_opciones]
        ngramas_sel = st.multiselect(
            "Selecciona uno o más n-gramas para ver las respuestas completas:",
            todas_opciones_texto
        )

        if ngramas_sel:
            st.markdown("### 🗒️ Respuestas que contienen los n-gramas seleccionados")
            for ngrama_sel in ngramas_sel:
                st.markdown(f"#### 🔹 {ngrama_sel}")
                respuestas_filtradas = df_asig[df_asig["texto_limpio"].str.contains(ngrama_sel)]
                for i, r in enumerate(respuestas_filtradas["RESPUESTA"], start=1):
                    st.write(f"**{i}.** {r}")

else:
    st.info("📥 Esperando que subas un archivo para comenzar el análisis...")
