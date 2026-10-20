"""Tablero nacional de la UGP (DEMOSTRACIÓN con datos simulados).

Ejecutar:  streamlit run app.py
Lee el libro de Excel (hojas de entrada) y recalcula los indicadores con pandas.
"""
from __future__ import annotations
import io
import streamlit as st
import pandas as pd
from ugp.cargar_datos import cargar, RUTA_POR_DEFECTO
from ugp import indicadores as ind, graficos as g

st.set_page_config(page_title="UGP · Tablero de control (demo)", page_icon="📊", layout="wide")
st.markdown("""<style>
html, body, [class*="css"] { font-size: 18px; }
div[data-testid="stMetricValue"] { font-size: 2rem; }
h1 { font-size: 2.1rem !important; }
.aviso { background:#fff2cc; border-left:6px solid #c98500; padding:.6rem 1rem; border-radius:4px; color:#3b2e00; }
.pill { display:inline-block; padding:.1rem .7rem; border-radius:999px; font-weight:700; color:#fff; font-size:.9rem; }
</style>""", unsafe_allow_html=True)

SEM_TXT = {"Verde": "● En meta", "Amarillo": "▲ Atención", "Rojo": "■ Crítico", "Gris": "○ Sin dato"}


def pill(estado: str) -> str:
    return f'<span class="pill" style="background:{g.SEM[estado]}">{SEM_TXT[estado]}</span>'


@st.cache_data(show_spinner=False)
def _cargar(ruta_o_bytes):
    return cargar(io.BytesIO(ruta_o_bytes) if isinstance(ruta_o_bytes, bytes) else ruta_o_bytes)


with st.sidebar:
    st.header("Fuente de datos")
    subido = st.file_uploader("Libro de Excel (opcional)", type=["xlsx"],
                              help="Si no se sube, se usa el libro del repositorio.")
    st.caption("El libro debe haberse abierto y guardado en Excel/LibreOffice al menos una vez (valores calculados).")
    st.markdown("---")
    st.caption("Los datos son **simulados**. No representan cifras reales del BID ni de la Dirección de Integración.")

try:
    d = _cargar(subido.getvalue() if subido else str(RUTA_POR_DEFECTO))
except Exception as e:  # noqa: BLE001
    st.error(f"No se pudo leer el libro: {e}")
    st.stop()

p = d["param"]
poa = ind.poa_evm(d)
comp = ind.por_componente(d, poa)
k = ind.kpis(d)
foc = ind.focalizacion(d)
sem_spi = ind.semaforo_ratio(k["SPI"], p["EVM_Verde"], p["EVM_Amarillo"])
sem_cpi = ind.semaforo_ratio(k["CPI"], p["EVM_Verde"], p["EVM_Amarillo"])
sem_just = "Verde" if k["pct_justificado"] >= p["Pct_Justif_Min"] else ("Amarillo" if k["pct_justificado"] >= p["Pct_Justif_Min"] - 0.1 else "Rojo")

st.title("Unidad Gestora del Programa — Tablero de control")
st.caption(f"Programa de Integración Académica y Comunitaria para Jóvenes · Préstamo 6153/OC-ES + Donación 6154/GR-ES · "
           f"Corte simulado: **{p['Fecha_Corte']:%d/%m/%Y}**")
st.markdown('<div class="aviso"><b>DEMOSTRACIÓN METODOLÓGICA.</b> Todos los datos son sintéticos (semilla fija). '
            'Este tablero ilustra cómo se controlaría un Programa BID; no es información oficial.</div>', unsafe_allow_html=True)

tabs = st.tabs(["Resumen", "1 · Planificación y control", "2 · Gestión fiduciaria", "3 · Cumplimiento", "4 · Articular y reportar", "Mapa de focalización"])

# ------------------------------------------------------------------ Resumen
with tabs[0]:
    c = st.columns(4)
    c[0].metric("Presupuesto del Programa", f"US$ {k['total_programa']/1e6:,.0f} M")
    c[1].metric("Ejecutado acumulado", f"US$ {k['ejecutado']/1e6:,.2f} M", f"{k['pct_ejecutado']:.1%} del total", delta_color="off")
    c[2].metric("Desembolsado por el BID", f"US$ {k['total_desembolsado']/1e6:,.2f} M")
    c[3].metric("Beneficiarios alcanzados", f"{k['beneficiarios']:,}", f"meta año 1: {k['meta_anio1']:,}", delta_color="off")
    filas = [("Avance físico (EV) vs. planificado", f"{k['avance_fisico']:.1%}", f"{k['avance_planificado']:.1%}", ind.semaforo_ratio(k['avance_fisico']/k['avance_planificado'], p['Umbral_Verde'], p['Umbral_Amarillo'])),
             ("SPI — cronograma", f"{k['SPI']:.2f}", "≥ " + f"{p['EVM_Verde']:.2f}", sem_spi),
             ("CPI — costo", f"{k['CPI']:.2f}", "≥ " + f"{p['EVM_Verde']:.2f}", sem_cpi),
             ("Anticipos justificados", f"{k['pct_justificado']:.1%}", f"≥ {p['Pct_Justif_Min']:.0%}", sem_just),
             ("Riesgos altos abiertos", str(k["riesgos_altos"]), "0", "Rojo" if k["riesgos_altos"] else "Verde"),
             ("Procesos de adquisición atrasados", str(k["alertas_pa"]), "0", "Amarillo" if k["alertas_pa"] else "Verde"),
             ("Obligaciones normativas vencidas", str(k["obligaciones_vencidas"]), "0", "Amarillo" if k["obligaciones_vencidas"] else "Verde"),
             ("Cumplimiento de obligaciones exigibles", f"{k['pct_cumplimiento']:.1%}", "100%", "Verde" if k["pct_cumplimiento"] >= 1 else "Amarillo")]
    tabla = "".join(f"<tr><td>{a}</td><td style='text-align:right'><b>{b}</b></td><td style='text-align:right'>{r}</td><td>{pill(s)}</td></tr>" for a, b, r, s in filas)
    st.markdown("#### Indicadores clave")
    st.markdown(f"<table style='width:100%'><tr><th align=left>Indicador</th><th align=right>Valor</th><th align=right>Referencia</th><th align=left>Estado</th></tr>{tabla}</table>", unsafe_allow_html=True)
    a, b = st.columns(2)
    a.plotly_chart(g.avance_componentes(comp), width="stretch")
    b.plotly_chart(g.plan_vs_real(d["plan_fin"]), width="stretch")

# --------------------------------------------------------- 1 Planificación
with tabs[1]:
    st.subheader("Avance físico y financiero, indicadores y riesgos")
    a, b = st.columns([3, 2])
    a.plotly_chart(g.avance_componentes(comp), width="stretch", key="av2")
    b.plotly_chart(g.semaforo_poa(poa), width="stretch")
    filtro = st.multiselect("Filtrar actividades por componente", sorted(poa["Comp."].unique()), default=sorted(poa["Comp."].unique()))
    v = poa[poa["Comp."].isin(filtro)][["ID", "Comp.", "Actividad", "Responsable", "Presupuesto POA USD", "% avance físico", "pct_plan", "AC", "SPI", "CPI", "sem"]]
    v.columns = ["ID", "Comp.", "Actividad", "Responsable", "Presupuesto", "% físico", "% planificado", "Ejecutado", "SPI", "CPI", "Semáforo"]
    st.dataframe(v.style.format({"Presupuesto": "{:,.0f}", "Ejecutado": "{:,.0f}", "% físico": "{:.0%}", "% planificado": "{:.0%}", "SPI": "{:.2f}", "CPI": "{:.2f}"})
                 .map(lambda x: f"background-color:{ {'Verde':'#c6efce','Amarillo':'#ffeb9c','Rojo':'#ffc7ce'}.get(x,'') }", subset=["Semáforo"]),
                 width="stretch", hide_index=True)
    st.subheader("Matriz de resultados")
    r = d["resultados"][["ID", "Indicador", "Unidad", "Comp.", "Meta final", "Valor actual", "Esperado al corte", "Cumplimiento", "Semáforo"]].copy()
    for c_ in ("Valor actual", "Esperado al corte", "Meta final", "Cumplimiento"):
        r[c_] = r[c_].map(lambda x: x if isinstance(x, str) else ("" if pd.isna(x) else f"{x:,.2f}".rstrip("0").rstrip(".")))
    st.dataframe(r, width="stretch", hide_index=True)
    a, b = st.columns([2, 3])
    a.plotly_chart(g.mapa_calor_riesgos(d["riesgos"]), width="stretch")
    ri = d["riesgos"].sort_values("Puntaje", ascending=False)[["ID", "Categoría", "Riesgo", "Puntaje", "Nivel", "Respuesta", "Responsable", "Estado"]]
    b.dataframe(ri, width="stretch", hide_index=True, height=420)

# ------------------------------------------------------------ 2 Fiduciario
with tabs[2]:
    st.subheader("Presupuesto, desembolsos, adquisiciones y auditoría")
    c = st.columns(4)
    c[0].metric("Anticipos desembolsados", f"US$ {k['anticipos']:,.0f}")
    c[1].metric("Justificado ante el BID", f"US$ {k['justificado']:,.0f}")
    c[2].metric("% justificado", f"{k['pct_justificado']:.1%}", f"umbral {p['Pct_Justif_Min']:.0%}", delta_color="off")
    c[3].metric("Saldo por justificar", f"US$ {k['saldo_por_justificar']:,.0f}")
    if k["pct_justificado"] < p["Pct_Justif_Min"]:
        faltan = p["Pct_Justif_Min"] * k["anticipos"] - k["justificado"]
        st.warning(f"No solicitar un nuevo anticipo: faltan US$ {faltan:,.0f} por justificar para llegar al {p['Pct_Justif_Min']:.0%}.")
    else:
        st.success("Se puede solicitar un nuevo anticipo.")
    pr = d["presupuesto"][["Comp.", "Componente", "Total asignado", "PEP Año 1", "Ejecutado acumulado", "% ejecución s/ PEP año vigente", "Saldo por ejecutar"]]
    st.dataframe(pr.style.format({"Total asignado": "{:,.0f}", "PEP Año 1": "{:,.0f}", "Ejecutado acumulado": "{:,.0f}", "Saldo por ejecutar": "{:,.0f}", "% ejecución s/ PEP año vigente": "{:.0%}"}),
                 width="stretch", hide_index=True)
    a, b = st.columns(2)
    a.plotly_chart(g.plan_vs_real(d["plan_fin"]), width="stretch", key="pf2")
    pa = d["pa"]["Alerta"].value_counts().rename_axis("Estado").reset_index(name="Procesos")
    b.markdown("**Plan de Adquisiciones — estado de alertas**")
    b.dataframe(pa, width="stretch", hide_index=True)
    st.markdown("**Contratos (pagado vs. saldo)**")
    ct = d["contratos"][["ID contrato", "Comp.", "Proveedor / consultor", "Monto contrato", "Pagado (USD)", "Saldo (USD)", "% pagado", "Vigencia"]]
    st.dataframe(ct.style.format({"Monto contrato": "{:,.0f}", "Pagado (USD)": "{:,.0f}", "Saldo (USD)": "{:,.0f}", "% pagado": "{:.0%}"}), width="stretch", hide_index=True)
    st.markdown("**Auditorías y recomendaciones**")
    st.dataframe(d["auditorias"].iloc[:, :9], width="stretch", hide_index=True)

# ------------------------------------------------------------ 3 Cumplimiento
with tabs[3]:
    st.subheader("Matriz de cumplimiento (contrato, MOP y políticas del BID)")
    cum = d["cumplimiento"]
    c = st.columns(4)
    c[0].metric("Obligaciones registradas", len(cum))
    c[1].metric("Exigibles a la fecha", int((cum["Exigible a la fecha"] == 1).sum()))
    c[2].metric("Vencidas", k["obligaciones_vencidas"])
    c[3].metric("% cumplimiento", f"{k['pct_cumplimiento']:.0%}")
    est = st.multiselect("Filtrar por alerta", sorted(cum["Alerta"].astype(str).unique()), default=sorted(cum["Alerta"].astype(str).unique()))
    st.dataframe(cum[cum["Alerta"].astype(str).isin(est)].drop(columns=["Exigible a la fecha"]), width="stretch", hide_index=True)
    st.caption("Las obligaciones y plazos son ilustrativos; deben construirse desde el Contrato, el MOP y los planes aprobados.")

# ----------------------------------------------------------- 4 Articulación
with tabs[4]:
    st.subheader("Misiones, compromisos, No Objeciones e informes")
    a, b = st.columns(2)
    a.markdown("**Misiones del BID**")
    a.dataframe(d["misiones"].drop(columns=["Participantes (roles)"], errors="ignore"), width="stretch", hide_index=True)
    no = d["no_objeciones"]
    b.markdown("**No Objeciones**")
    b.dataframe(no[["ID", "Asunto", "Estado", "Días de trámite", "Plazo de referencia"]], width="stretch", hide_index=True)
    st.markdown("**Matriz de compromisos con el BID**")
    st.dataframe(d["compromisos"], width="stretch", hide_index=True)
    st.markdown("**Calendario de informes (P1–P12)**")
    st.dataframe(d["informes"], width="stretch", hide_index=True)

# ------------------------------------------------------------------- Mapa
with tabs[5]:
    st.subheader("Focalización territorial")
    var = st.radio("Variable del mapa", ["indice", "cobertura", "inversion", "brecha"], horizontal=True,
                   format_func=lambda x: {"indice": "Índice de focalización", "cobertura": "Cobertura meta año 1", "inversion": "Inversión ejecutada", "brecha": "Brecha de cobertura"}[x])
    a, b = st.columns([3, 2])
    a.plotly_chart(g.mapa_choropleth(foc, var), width="stretch")
    b.plotly_chart(g.indice_focalizacion(foc), width="stretch")
    t = foc[["Departamento", "Meta año 1", "Alcanzado acumulado", "cobertura", "indice", "prioridad", "inversion"]].sort_values("indice", ascending=False)
    t.columns = ["Departamento", "Meta año 1", "Alcanzado", "Cobertura", "Índice", "Prioridad", "Inversión (USD)"]
    st.dataframe(t.style.format({"Meta año 1": "{:,.0f}", "Alcanzado": "{:,.0f}", "Cobertura": "{:.0%}", "Índice": "{:.2f}", "Inversión (USD)": "{:,.0f}"}), width="stretch", hide_index=True)
    st.caption("Índice = 50% vulnerabilidad + 20% población objetivo + 30% brecha de cobertura (pesos en la hoja Parametros).")
