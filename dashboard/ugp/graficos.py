"""Gráficos de plotly con una paleta única. Colores de estado solo para semáforos (con texto)."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.graph_objects as go

AZUL, NARANJA, AQUA, GRIS = "#2a78d6", "#eb6834", "#1baf7a", "#8a8a85"
TINTA, TINTA2 = "#1f1f1e", "#52514e"
SEM = {"Verde": "#1f8a3b", "Amarillo": "#c98500", "Rojo": "#c9302c", "Gris": "#8a8a85"}
SEC_AZUL = [[0, "#eaf2fc"], [0.5, "#7fb0ea"], [1, "#0f3f7d"]]
GEO = Path(__file__).resolve().parents[1] / "data" / "geo" / "departamentos_sv.geojson"


def _base(fig, alto=380, titulo=None):
    fig.update_layout(height=alto, title=dict(text=titulo, x=0, font=dict(size=16, color=TINTA)) if titulo else None,
                      margin=dict(l=10, r=10, t=50 if titulo else 20, b=10), paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Arial", size=14, color=TINTA2),
                      legend=dict(orientation="h", y=-0.18, x=0))
    fig.update_xaxes(showgrid=False, linecolor="#bfbfbf")
    fig.update_yaxes(gridcolor="#e6e6e3", zeroline=False)
    return fig


def avance_componentes(comp: pd.DataFrame):
    """Barras agrupadas: planificado vs físico vs financiero por componente (% del presupuesto POA)."""
    fig = go.Figure()
    for col, nom, color in (("pct_plan", "Planificado a la fecha", GRIS), ("pct_fis", "Avance físico (EV)", AZUL),
                            ("pct_fin", "Avance financiero (AC)", NARANJA)):
        fig.add_bar(x=comp["Comp."], y=comp[col], name=nom, marker_color=color, text=[f"{v:.0%}" for v in comp[col]],
                    textposition="outside", hovertemplate="%{x}: %{y:.1%}<extra>" + nom + "</extra>")
    fig.update_layout(barmode="group", bargap=0.35, bargroupgap=0.12)
    fig.update_yaxes(tickformat=".0%", range=[0, 1.15])
    return _base(fig, 380, "Avance por componente (% del presupuesto del POA del año 1)")


def plan_vs_real(plan: pd.DataFrame):
    """Línea acumulada proyectado vs real; el real solo hasta el último trimestre con dato."""
    p = plan.copy()
    p["real_ac"] = p["Real acumulado"].where(p["Real acumulado"].notna() & (p["Real USD"] > 0))
    fig = go.Figure()
    fig.add_scatter(x=p["Trimestre"], y=p["Proyectado acumulado"], name="Proyectado", mode="lines+markers",
                    line=dict(color=GRIS, width=2, dash="dot"), marker=dict(size=8))
    fig.add_scatter(x=p["Trimestre"], y=p["real_ac"], name="Real", mode="lines+markers",
                    line=dict(color=AZUL, width=2), marker=dict(size=9), connectgaps=False)
    fig.update_yaxes(tickformat=",.0f", title="USD acumulados")
    return _base(fig, 360, "Gasto acumulado: proyectado vs. real (primeros 8 trimestres)")


def mapa_calor_riesgos(riesgos: pd.DataFrame):
    z = np.zeros((5, 5), dtype=int)
    txt = [[[] for _ in range(5)] for _ in range(5)]
    for _, r in riesgos.iterrows():
        i, j = int(r["Impacto (1-5)"]) - 1, int(r["Prob. (1-5)"]) - 1
        z[i, j] += 1
        txt[i][j].append(r["ID"])
    score = np.array([[(i + 1) * (j + 1) for j in range(5)] for i in range(5)])
    fig = go.Figure(go.Heatmap(z=score, x=[1, 2, 3, 4, 5], y=[1, 2, 3, 4, 5], showscale=False, xgap=3, ygap=3,
                               colorscale=[[0, "#dcefe0"], [0.3, "#fbe8b3"], [0.55, "#f6c9a8"], [1, "#eea7a3"]],
                               hovertemplate="Prob. %{x} × Imp. %{y}<extra></extra>"))
    for i in range(5):
        for j in range(5):
            if txt[i][j]:
                fig.add_annotation(x=j + 1, y=i + 1, text="<br>".join(txt[i][j]), showarrow=False,
                                   font=dict(size=12, color=TINTA))
    fig.update_xaxes(title="Probabilidad", dtick=1, showgrid=False)
    fig.update_yaxes(title="Impacto", dtick=1, showgrid=False)
    return _base(fig, 420, "Mapa de calor de riesgos (identificadores por celda)")


def indice_focalizacion(f: pd.DataFrame):
    g = f.sort_values("indice")
    cmap = {"Alta": AZUL, "Media": "#7fb0ea", "Baja": "#c9dcf3"}
    fig = go.Figure(go.Bar(y=g["Departamento"], x=g["indice"], orientation="h",
                           marker_color=[cmap[p] for p in g["prioridad"]], text=[f"{v:.2f}" for v in g["indice"]],
                           textposition="outside", customdata=g["prioridad"],
                           hovertemplate="%{y}: índice %{x:.2f} (prioridad %{customdata})<extra></extra>"))
    fig.update_xaxes(range=[0, 1])
    return _base(fig, 470, "Índice de focalización por departamento")


def semaforo_poa(poa: pd.DataFrame):
    c = poa["sem"].value_counts().reindex(["Verde", "Amarillo", "Rojo", "Gris"]).fillna(0).astype(int)
    fig = go.Figure(go.Bar(x=c.index, y=c.values, marker_color=[SEM[k] for k in c.index], text=c.values, textposition="outside"))
    fig.update_yaxes(title="Actividades")
    return _base(fig, 300, "Actividades del POA por semáforo (SPI)")


def _anillos(geom):
    """Lista de anillos exteriores (lon, lat) de un Polygon o MultiPolygon."""
    polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
    return [p[0] for p in polys]


def mapa_choropleth(f: pd.DataFrame, variable="indice", titulo=None):
    """Mapa coroplético dibujado con polígonos (scatter con relleno): no depende de mapas base
    descargados de internet, así que funciona sin conexión."""
    from plotly.colors import sample_colorscale
    geo = json.loads(GEO.read_text(encoding="utf-8"))
    etiquetas = {"indice": "Índice de focalización", "cobertura": "Cobertura de la meta del año 1",
                 "inversion": "Inversión ejecutada (USD)", "brecha": "Brecha de cobertura"}
    datos = f.set_index("ISO 3166-2")
    z = datos[variable]
    lo, hi = float(z.min()), float(z.max())
    rango = (hi - lo) or 1.0
    fig = go.Figure()
    for ft in geo["features"]:
        iso = ft["properties"]["iso"]
        if iso not in datos.index:
            continue
        r = datos.loc[iso]
        color = sample_colorscale(SEC_AZUL, [(float(r[variable]) - lo) / rango])[0]
        txt = (f"<b>{r['Departamento']}</b><br>Índice: {r['indice']:.2f} ({r['prioridad']})<br>"
               f"Cobertura meta año 1: {r['cobertura']:.0%}<br>Beneficiarios: {r['Alcanzado acumulado']:,.0f}<br>"
               f"Inversión: US$ {r['inversion']:,.0f}")
        for anillo in _anillos(ft["geometry"]):
            xs, ys = zip(*anillo)
            fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", fill="toself", fillcolor=color, hoveron="fills",
                                     line=dict(color="#ffffff", width=1.2), text=txt, hoverinfo="text", showlegend=False))
        cx = sum(p[0] for p in _anillos(ft["geometry"])[0]) / len(_anillos(ft["geometry"])[0])
        cy = sum(p[1] for p in _anillos(ft["geometry"])[0]) / len(_anillos(ft["geometry"])[0])
        oscuro = (float(r[variable]) - lo) / rango > 0.55
        fig.add_annotation(x=cx, y=cy, text=iso.replace("SV-", ""), showarrow=False,
                           font=dict(size=11, color="#ffffff" if oscuro else TINTA))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode="markers", showlegend=False, hoverinfo="skip",
                             marker=dict(colorscale=SEC_AZUL, cmin=lo, cmax=hi, showscale=True, size=0.1,
                                         colorbar=dict(title=etiquetas.get(variable, variable), len=0.7, thickness=14))))
    fig.update_xaxes(visible=False, constrain="domain")
    fig.update_yaxes(visible=False, scaleanchor="x", scaleratio=1.03)
    fig.update_layout(height=520, margin=dict(l=0, r=0, t=40, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      title=dict(text=titulo or etiquetas.get(variable), x=0, font=dict(size=16)), font=dict(family="Arial", size=14))
    return fig
