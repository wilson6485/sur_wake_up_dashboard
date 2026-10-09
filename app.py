import streamlit as st
import pandas as pd
import joblib


# --------------------------------------------------
# CONFIGURACIÓN DEL DASHBOARD
# --------------------------------------------------

st.set_page_config(
    page_title="Sur Wake Up",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# ENCABEZADO
# --------------------------------------------------

st.image(
    "logo_sur_wake_up.png",
    width=200
)

st.title("Marketing Intelligence Dashboard")

st.write(
    "Sistema de Análisis de Marketing, "
    "Business Intelligence e Inteligencia Artificial."
)

st.info(
    "Versión de portafolio desarrollada con datos sintéticos."
)

# --------------------------------------------------
# CARGA DE DATOS
# --------------------------------------------------

@st.cache_data
def cargar_datos():
    return pd.read_csv(
        "sur_wake_up_data_kpi.csv",
        parse_dates=["fecha"]
    )

df = cargar_datos()


st.success(
   
    f"Dataset cargado correctamente: "
    f"{len(df):,} registros."
)

st.success(
    "Modelos predictivos A, B y C  "
    "cargados correctamente."
)



# --------------------------------------------------
# CARGA DE MODELOS PREDICTIVOS
# --------------------------------------------------

@st.cache_resource
def cargar_modelos():

    modelo_a = joblib.load(
        "modelos/modelo_a.joblib"
    )

    modelo_b = joblib.load(
        "modelos/modelo_b.joblib"
    )

    modelo_c = joblib.load(
        "modelos/modelo_c.joblib"
    )

    return {
        "A": modelo_a,
        "B": modelo_b,
        "C": modelo_c
    }

modelos_predictivos = cargar_modelos()


# --------------------------------------------------
# FILTROS INTERACTIVOS
# --------------------------------------------------

st.sidebar.header("Filtros")

meses = sorted(
    df["fecha"].dt.to_period("M").astype(str).unique()
)

mes_seleccionado = st.sidebar.multiselect(
    "Mes",
    meses
)

canal_seleccionado = st.sidebar.multiselect(
    "Canal",
    sorted(df["canal"].unique())
)

campaña_seleccionada = st.sidebar.multiselect(
    "Campaña",
    sorted(df["campaña"].unique())
)

contenido_seleccionado = st.sidebar.multiselect(
    "Contenido",
    sorted(df["contenido"].unique())
)

# --------------------------------------------------
# CONTEXTO DE LOS FILTROS SELECCIONADOS
# --------------------------------------------------

contexto_mes = (
    ", ".join(mes_seleccionado)
    if mes_seleccionado
    else "Todos"
)

contexto_canal = (
    ", ".join(canal_seleccionado)
    if canal_seleccionado
    else "Todos"
)

contexto_campaña = (
    ", ".join(campaña_seleccionada)
    if campaña_seleccionada
    else "Todas"
)

contexto_contenido = (
    ", ".join(contenido_seleccionado)
    if contenido_seleccionado
    else "Todos"
)

# Copia del dataset para aplicar los filtros
df_filtrado = df.copy()

if mes_seleccionado:
    df_filtrado = df_filtrado[
        df_filtrado["fecha"]
        .dt.to_period("M")
        .astype(str)
        .isin(mes_seleccionado)
    ]

if canal_seleccionado:
    df_filtrado = df_filtrado[
        df_filtrado["canal"].isin(canal_seleccionado)
    ]

if campaña_seleccionada:
    df_filtrado = df_filtrado[
        df_filtrado["campaña"].isin(campaña_seleccionada)
    ]

if contenido_seleccionado:
    df_filtrado = df_filtrado[
        df_filtrado["contenido"].isin(contenido_seleccionado)
    ]
# --------------------------------------------------
# VALIDACIÓN DE FILTROS SIN RESULTADOS
# --------------------------------------------------

if df_filtrado.empty:
    st.warning(
        "La combinación de filtros seleccionada "
        "no contiene registros."
    )

    st.info(
        "Modifica uno o más filtros para continuar "
        "con el análisis."
    )

    st.stop()


# --------------------------------------------------
# KPIs EJECUTIVOS
# --------------------------------------------------

st.divider()

st.header("📊 Resumen ejecutivo")

st.caption(
    "Principales indicadores de rendimiento según "
    "los filtros seleccionados."
)

inversion_total = df_filtrado["inversion"].sum()
ingresos_total = df_filtrado["ingresos"].sum()
conversiones_total = df_filtrado["conversiones"].sum()

ctr_mediana = df_filtrado["CTR"].median()
roas_mediana = df_filtrado["ROAS"].median()
roi_mediana = df_filtrado["ROI"].median()

# --------------------------------------------------
# VALORES GENERALES DE REFERENCIA
# --------------------------------------------------

ctr_general = df["CTR"].median()
roas_general = df["ROAS"].median()
roi_general = df["ROI"].median()

# --------------------------------------------------
# DIFERENCIAS FRENTE A LA REFERENCIA GENERAL
# --------------------------------------------------

dif_ctr = ctr_mediana - ctr_general
dif_roas = roas_mediana - roas_general
dif_roi = roi_mediana - roi_general


# --------------------------------------------------
# CLASIFICACIÓN CONTEXTUAL
# --------------------------------------------------

def clasificar_resultado(valor_actual, valor_general):
    tolerancia = abs(valor_general) * 0.05

    if valor_actual > valor_general + tolerancia:
        return "por encima de"

    elif valor_actual < valor_general - tolerancia:
        return "por debajo de"

    else:
        return "similar a"


nivel_ctr = clasificar_resultado(
    ctr_mediana,
    ctr_general
)

nivel_roas = clasificar_resultado(
    roas_mediana,
    roas_general
)

nivel_roi = clasificar_resultado(
    roi_mediana,
    roi_general
)

# --------------------------------------------------
# SÍNTESIS EJECUTIVA DEL RESULTADO
# --------------------------------------------------

niveles = [nivel_ctr, nivel_roas, nivel_roi]

cantidad_superior = niveles.count("por encima de")
cantidad_inferior = niveles.count("por debajo de")

if cantidad_superior >= 2:
    sintesis_ejecutiva = (
        "La selección actual presenta un desempeño general "
        "superior a la referencia del conjunto analizado."
    )

elif cantidad_inferior >= 2:
    sintesis_ejecutiva = (
        "La selección actual presenta un desempeño general "
        "inferior a la referencia del conjunto analizado."
    )

else:
    sintesis_ejecutiva = (
        "La selección actual presenta un comportamiento general "
        "similar o mixto frente a la referencia del conjunto analizado."
    )


# --------------------------------------------------
# RESULTADOS DEL NEGOCIO
# --------------------------------------------------

st.markdown("#### Resultados del negocio")

col1, col2, col3 = st.columns(3)

col1.metric(
    "💰 Inversión",
    f"RD$ {inversion_total:,.0f}"
)

col2.metric(
    "💵 Ingresos",
    f"RD$ {ingresos_total:,.0f}"
)

col3.metric(
    "🎯 Conversiones",
    f"{conversiones_total:,.0f}"
)


# --------------------------------------------------
# EFICIENCIA DE MARKETING
# --------------------------------------------------

st.markdown("#### Eficiencia de marketing")

col4, col5, col6 = st.columns(3)

col4.metric(
    "CTR mediano",
    f"{ctr_mediana:.2f}%"
)

col5.metric(
    "ROAS mediano",
    f"{roas_mediana:.2f}"
)

col6.metric(
    "ROI mediano",
    f"{roi_mediana:.2f}%"
)

# --------------------------------------------------
# INTERPRETACIÓN DE RESULTADOS
# --------------------------------------------------

# --------------------------------------------------
# INTERPRETACIÓN DINÁMICA DE RESULTADOS
# --------------------------------------------------

st.header("📌 Interpretación de resultados")

st.caption(
    "Lectura educativa de los principales indicadores "
    "según los filtros seleccionados."
)

st.markdown("#### Contexto analizado")

st.write(
    f"**Mes:** {contexto_mes}  |  "
    f"**Canal:** {contexto_canal}  |  "
    f"**Campaña:** {contexto_campaña}  |  "
    f"**Contenido:** {contexto_contenido}"
)

st.markdown(
    f"""
**CTR mediano — {ctr_mediana:.2f}%**

Este indicador muestra qué proporción de las impresiones generó clics.
Permite comprender la capacidad del contenido para atraer la atención
del público hacia una acción.

**ROAS mediano — {roas_mediana:.2f}**

Por cada **RD\\$1.00 invertido**, los datos de la selección actual muestran
aproximadamente **RD\\${roas_mediana:.2f} en ingresos**.

**ROI mediano — {roi_mediana:.2f}%**

Este indicador refleja la rentabilidad obtenida en relación con la
inversión dentro de los datos analizados.
"""
)

st.markdown("#### Comparación con el conjunto general")

st.write(
    f"• **CTR:** la selección actual presenta un resultado **{nivel_ctr}** "
    f"la referencia general "
    f"({dif_ctr:+.2f} puntos porcentuales)."
)

st.write(
    f"• **ROAS:** la selección actual presenta un resultado **{nivel_roas}** "
    f"la referencia general "
    f"({dif_roas:+.2f})."
)

st.write(
    f"• **ROI:** la selección actual presenta un resultado **{nivel_roi}** "
    f"la referencia general "
    f"({dif_roi:+.2f} puntos porcentuales)."
)

st.markdown("#### Síntesis ejecutiva")

st.info(sintesis_ejecutiva)

st.caption(
    "La comparación utiliza como referencia los valores medianos "
    "del conjunto general de datos demostrativos. La clasificación "
    "es descriptiva y utiliza una tolerancia del 5 % para identificar "
    "resultados similares, superiores o inferiores a la referencia."
)

# --------------------------------------------------
# PRESENTACIÓN DE SERVICIOS PROFESIONALES
# --------------------------------------------------

st.caption(
    "Los valores cambian automáticamente según los filtros seleccionados. "
    "Esta interpretación tiene fines educativos y demostrativos y no "
    "constituye una recomendación específica de inversión."
)


st.divider()

st.header("🚀 Servicios profesionales de Sur Wake Up")

st.markdown(
    """
**Sur Wake Up — Analítica e Inteligencia de Datos**

Transformamos datos en conocimiento para comprender resultados,
identificar tendencias y apoyar decisiones.

### Nuestras especialidades

**1. Inteligencia Empresarial y Marketing**

Análisis de negocios, publicidad digital, indicadores de
rendimiento, modelos predictivos y asesoría para nuevos
emprendedores, Micros, Pequeñas y Medianas Empresas.

**2. Inteligencia y Análisis Político — Área en desarrollo**

Análisis de opinión pública, tendencias, conversación digital
e indicadores políticos mediante metodologías basadas en datos.

**3. Inteligencia y Analítica Deportiva — Béisbol — Área en desarrollo**

Análisis estadístico de jugadores y equipos, comparaciones
de rendimiento, tendencias deportivas y modelos predictivos.

---

Nuestro dashboard empresarial actual demuestra capacidades
analíticas. Los diagnósticos, estrategias y recomendaciones
específicas se desarrollan mediante servicios profesionales
personalizados.
"""
)




# --------------------------------------------------
# VISUALIZACIONES DINÁMICAS
# --------------------------------------------------

st.divider()


# --------------------------------------------------
# ANÁLISIS VISUAL
# --------------------------------------------------

st.header("📈 Análisis visual")

st.caption(
    "Comparación del rendimiento por canal, campaña y contenido, "
    "junto con la evolución mensual de los ingresos."
)

# --------------------------------------------------
# GRÁFICOS 1 Y 2
# --------------------------------------------------

col_grafico1, col_grafico2 = st.columns(2)

# ROI POR CANAL

roi_canal = (
    df_filtrado
    .groupby("canal")["ROI"]
    .median()
    .sort_values(ascending=False)
)

with col_grafico1:
    st.markdown("#### ROI mediano por canal")
    st.bar_chart(roi_canal)

# INGRESOS POR MES

ingresos_mes = (
    df_filtrado
    .assign(
        mes=df_filtrado["fecha"]
        .dt.to_period("M")
        .astype(str)
    )
    .groupby("mes")["ingresos"]
    .sum()
)

with col_grafico2:
    st.markdown("#### Evolución mensual de ingresos")
    st.line_chart(ingresos_mes)


# --------------------------------------------------
# GRÁFICOS 3 Y 4
# --------------------------------------------------

col_grafico3, col_grafico4 = st.columns(2)

# ROI POR CAMPAÑA

roi_campaña = (
    df_filtrado
    .groupby("campaña")["ROI"]
    .median()
    .sort_values(ascending=False)
)

with col_grafico3:
    st.markdown("#### ROI mediano por campaña")
    st.bar_chart(roi_campaña)

# ROI POR CONTENIDO

roi_contenido = (
    df_filtrado
    .groupby("contenido")["ROI"]
    .median()
    .sort_values(ascending=False)
)

with col_grafico4:
    st.markdown("#### ROI mediano por contenido")
    st.bar_chart(roi_contenido)


# --------------------------------------------------
# SEPARACIÓN
# --------------------------------------------------

st.divider()


# --------------------------------------------------
# COMBINACIONES ESTRATÉGICAS
# --------------------------------------------------

st.header("🎯 Combinaciones estratégicas")

st.caption(
    "Identifica las combinaciones de canal, campaña y contenido "
    "con mejor rendimiento según los filtros seleccionados."
)

combinaciones = (
    df_filtrado
    .groupby(
        ["canal", "campaña", "contenido"]
    )
    .agg(
        registros=("ROI", "count"),
        inversion_total=("inversion", "sum"),
        ingresos_total=("ingresos", "sum"),
        conversiones_total=("conversiones", "sum"),
        roas_mediana=("ROAS", "median"),
        roi_mediana=("ROI", "median")
    )
    .round(2)
    .reset_index()
)

top_combinaciones = (
    combinaciones
    .sort_values(
        "roi_mediana",
        ascending=False
    )
    .head(10)
)

top_combinaciones["combinacion"] = (
    top_combinaciones["canal"]
    + " | "
    + top_combinaciones["campaña"]
    + " | "
    + top_combinaciones["contenido"]
)

st.markdown("#### Top 10 por ROI mediano")

st.dataframe(
    top_combinaciones[
        [
            "combinacion",
            "registros",
            "inversion_total",
            "ingresos_total",
            "conversiones_total",
            "roas_mediana",
            "roi_mediana"
        ]
    ],
    width="stretch",
    hide_index=True,
    column_config={
        "combinacion": st.column_config.TextColumn(
            "Combinación"
        ),
        "registros": st.column_config.NumberColumn(
            "Registros",
            format="%d"
        ),
        "inversion_total": st.column_config.NumberColumn(
            "Inversión total",
            format="RD$ %.2f"
        ),
        "ingresos_total": st.column_config.NumberColumn(
            "Ingresos totales",
            format="RD$ %.2f"
        ),
        "conversiones_total": st.column_config.NumberColumn(
            "Conversiones",
            format="%d"
        ),
        "roas_mediana": st.column_config.NumberColumn(
            "ROAS mediano",
            format="%.2f"
        ),
        "roi_mediana": st.column_config.NumberColumn(
            "ROI mediano",
            format="%.2f%%"
        )
    }
)


# --------------------------------------------------
# INTELIGENCIA PREDICTIVA
# --------------------------------------------------

st.divider()

st.header("🤖 Inteligencia Predictiva")

st.caption(
    "Sistema de apoyo a decisiones basado en modelos "
    "predictivos para diferentes momentos de la campaña."
)

st.write(
    "Introduce los datos disponibles de una campaña. "
    "El sistema seleccionará automáticamente el modelo "
    "compatible con el momento de la campaña."
)

with st.form("formulario_predictivo"):

    col_p1, col_p2, col_p3 = st.columns(3)

    with col_p1:
        canal_input = st.selectbox(
            "Canal",
            sorted(df["canal"].unique())
        )

        campaña_input = st.selectbox(
            "Campaña",
            sorted(df["campaña"].unique())
        )

        contenido_input = st.selectbox(
            "Contenido",
            sorted(df["contenido"].unique())
        )

    with col_p2:
        inversion_input = st.number_input(
            "Inversión (RD$)",
            min_value=0.0,
            value=15000.0
        )

        impresiones_input = st.number_input(
            "Impresiones",
            min_value=0,
            value=30000
        )

        alcance_input = st.number_input(
            "Alcance",
            min_value=0,
            value=24000
        )

        interacciones_input = st.number_input(
            "Interacciones",
            min_value=0,
            value=2500
        )

    with col_p3:
        clics_input = st.number_input(
            "Clics",
            min_value=0,
            value=1200
        )

        leads_disponibles = st.checkbox(
            "Leads disponibles",
            value=True
        )

        if leads_disponibles:
            leads_input = st.number_input(
                "Leads",
                min_value=0,
                value=180
            )
        else:
            leads_input = None

        conversiones_disponibles = st.checkbox(
            "Conversiones disponibles",
            value = True,
            disabled = not leads_disponibles
        )

        if conversiones_disponibles:
             conversiones_input = st.number_input(
                 "Conversiones",
                  min_value = 0,
                  value = 35
             )
        else:
             conversiones_input = None



    ejecutar_prediccion = st.form_submit_button(
        "Analizar campaña"
    )

    # --------------------------------------------------
    # EJECUTAR PREDICCIÓN
    # --------------------------------------------------

    if ejecutar_prediccion:

        # --------------------------------------------------
        # VALIDACIÓN DE ENTRADAS
        # --------------------------------------------------

        errores = []

        if alcance_input > impresiones_input:
            errores.append(
                "El alcance no puede ser mayor que las impresiones."
            )

        if interacciones_input > alcance_input:
            errores.append(
                "Las interacciones no pueden ser mayores que el alcance."
            )

        if clics_input > impresiones_input:
            errores.append(
                "Los clics no pueden ser mayores que las impresiones."
            )

        if leads_input is not None and leads_input > clics_input:
            errores.append(
                "Los leads no pueden ser mayores que los clics."
            )

        if (
                conversiones_input is not None
                and leads_input is not None
                and conversiones_input > leads_input
        ):
            errores.append(
                "Las conversiones no pueden ser mayores que los leads."
            )

        if errores:
            st.error("Se encontraron datos inconsistentes:")

            for error in errores:
                st.write(f"• {error}")

            st.stop()



    # --------------------------------------------------
    # CONTROL DE VALORES FUERA DEL RANGO HISTÓRICO
    # --------------------------------------------------

    variables_control = {
        "Impresiones": ("impresiones", impresiones_input),
        "Alcance": ("alcance", alcance_input),
        "Interacciones": ("interacciones", interacciones_input),
        "Clics": ("clics", clics_input),
        "Inversión": ("inversion", inversion_input)
    }

    if leads_input is not None:
        variables_control["Leads"] = ("leads", leads_input)

    if conversiones_input is not None:
        variables_control["Conversiones"] = (
            "conversiones",
            conversiones_input
        )

    fuera_de_rango = []

    for nombre, (columna, valor) in variables_control.items():

        minimo = df[columna].min()
        maximo = df[columna].max()

        margen = (maximo - minimo) * 0.05

        limite_inferior = minimo - margen
        limite_superior = maximo + margen

    if valor < limite_inferior or valor > limite_superior:

        fuera_de_rango.append(
              f"{nombre}: {valor:,.2f} "
              f"(rango histórico: {minimo:,.2f} - {maximo:,.2f})"
        )

    if fuera_de_rango:
        st.warning(
            "Algunos valores están fuera del rango observado "
            "en los datos utilizados para desarrollar el modelo:"
        )

        for advertencia in fuera_de_rango:
            st.write(f"• {advertencia}")

        st.caption(
            "La predicción puede continuar, pero debe interpretarse "
            "con mayor cautela porque el modelo está recibiendo valores "
            "fuera de su experiencia histórica."
        )

    if conversiones_input is not None:
        escenario = "A"

    elif leads_input is not None:
        escenario = "B"

    else:
        escenario = "C"

    modelo = modelos_predictivos[escenario]

    if escenario == "A":

        datos_modelo = pd.DataFrame([{
            "conversiones": conversiones_input
        }])

    elif escenario == "B":

        datos_modelo = pd.DataFrame([{
            "impresiones": impresiones_input,
            "alcance": alcance_input,
            "interacciones": interacciones_input,
            "clics": clics_input,
            "leads": leads_input,
            "inversion": inversion_input,
            "canal": canal_input,
            "campaña": campaña_input,
            "contenido": contenido_input
        }])

    else:

        datos_modelo = pd.DataFrame([{
            "impresiones": impresiones_input,
            "alcance": alcance_input,
            "interacciones": interacciones_input,
            "clics": clics_input,
            "inversion": inversion_input,
            "canal": canal_input,
            "campaña": campaña_input,
            "contenido": contenido_input
        }])

    ingresos_estimados = float(
        modelo.predict(datos_modelo)[0]
    )

    if inversion_input > 0:
        roas_estimado = ingresos_estimados / inversion_input
    else:
        roas_estimado = None

    # --------------------------------------------------
    # CONTEXTO DEL ESCENARIO
    # --------------------------------------------------

    contexto_escenarios = {
        "A": {
            "momento": "Tardío",
            "variable_clave": "Conversiones",
            "r2": 71.22,
            "precision": "Mayor",
            "anticipacion": "Baja"
        },
        "B": {
            "momento": "Intermedio",
            "variable_clave": "Leads",
            "r2": 47.32,
            "precision": "Moderada",
            "anticipacion": "Media"
        },
        "C": {
            "momento": "Temprano",
            "variable_clave": "Clics",
            "r2": 30.72,
            "precision": "Menor",
            "anticipacion": "Alta"
        }
    }

    contexto = contexto_escenarios[escenario]

    st.divider()

    st.markdown("### Resultado predictivo")

    col_r1, col_r2, col_r3 = st.columns(3)

    col_r1.metric(
        "Escenario seleccionado",
        escenario
    )

    col_r2.metric(
        "Ingresos estimados",
        f"RD$ {ingresos_estimados:,.2f}"
    )

    if roas_estimado is not None:
        col_r3.metric(
            "ROAS estimado",
            f"{roas_estimado:.2f}"
        )
    else:
        col_r3.metric(
            "ROAS estimado",
            "No disponible"
        )

    # --------------------------------------------------
    # INTERPRETACIÓN EMPRESARIAL
    # --------------------------------------------------

    st.markdown("### Interpretación empresarial")

    if roas_estimado is None:

        lectura_roas = (
            "No puede calcularse el ROAS estimado "
            "porque no existe una inversión válida."
        )

    elif roas_estimado >= 5:

        lectura_roas = (
            "La estimación presenta una relación alta "
            "entre ingresos e inversión."
        )

    elif roas_estimado >= 2:

        lectura_roas = (
            "La estimación presenta una relación moderada "
            "entre ingresos e inversión."
        )

    elif roas_estimado >= 1:

        lectura_roas = (
            "Los ingresos estimados superan la inversión, "
            "aunque el margen debe analizarse con cautela."
        )

    else:

        lectura_roas = (
            "Los ingresos estimados son inferiores "
            "a la inversión considerada."
        )

    st.info(
        f"{lectura_roas} "
        f"La predicción corresponde a un momento "
        f"{contexto['momento'].lower()} de la campaña "
        f"y utiliza {contexto['variable_clave'].lower()} "
        f"como variable de referencia principal. "
        f"Su precisión relativa es "
        f"{contexto['precision'].lower()} y su capacidad "
        f"de anticipación es "
        f"{contexto['anticipacion'].lower()}. "
        f"El R² de referencia del escenario es "
        f"{contexto['r2']:.2f}%. "
        f"El resultado debe utilizarse como apoyo "
        f"a la decisión y no como garantía de ingresos."
    )