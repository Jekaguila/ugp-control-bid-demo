"""Recalcula en pandas los indicadores del Tablero a partir de las columnas de ENTRADA del Excel.

Se replica la lógica del libro (valor ganado, justificación de anticipos, índice de focalización)
de forma independiente; `tests/test_consistencia.py` compara ambos cálculos.
"""
from __future__ import annotations
import datetime as dt
import numpy as np
import pandas as pd


def _fecha(s):
    return pd.to_datetime(s).dt.date


def semaforo_ratio(x, verde, amarillo):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "Gris"
    return "Verde" if x >= verde else ("Amarillo" if x >= amarillo else "Rojo")


def poa_evm(d) -> pd.DataFrame:
    p, corte = d["param"], d["param"]["Fecha_Corte"]
    poa = d["poa"].copy()
    ini, fin = _fecha(poa["Inicio"]), _fecha(poa["Fin"])
    dur = np.array([(f - i).days for i, f in zip(ini, fin)], dtype=float)
    trans = np.array([(corte - i).days for i in ini], dtype=float)
    plan = np.where(trans <= 0, 0.0, np.where(corte >= np.array(fin), 1.0, trans / np.where(dur == 0, 1, dur)))
    ac = d["gastos"].groupby("Actividad POA")["Monto USD"].sum()
    poa["pct_plan"] = plan
    poa["AC"] = poa["ID"].map(ac).fillna(0.0)
    poa["EV"] = poa["Presupuesto POA USD"] * poa["% avance físico"]
    poa["PV"] = poa["Presupuesto POA USD"] * poa["pct_plan"]
    poa["SPI"] = np.where(poa["PV"] > 0, poa["EV"] / poa["PV"].replace(0, np.nan), np.nan)
    poa["CPI"] = np.where(poa["AC"] > 0, poa["EV"] / poa["AC"].replace(0, np.nan), np.nan)
    poa["sem"] = [
        "Verde" if a >= 1 else ("Gris" if np.isnan(s) else semaforo_ratio(s, p["EVM_Verde"], p["EVM_Amarillo"]))
        for a, s in zip(poa["% avance físico"], poa["SPI"])]
    return poa


def por_componente(d, poa=None) -> pd.DataFrame:
    poa = poa_evm(d) if poa is None else poa
    g = poa.groupby("Comp.").agg(presupuesto=("Presupuesto POA USD", "sum"), AC=("AC", "sum"),
                                  EV=("EV", "sum"), PV=("PV", "sum"), actividades=("ID", "count")).reset_index()
    g["pct_fin"] = g["AC"] / g["presupuesto"]
    g["pct_fis"] = g["EV"] / g["presupuesto"]
    g["pct_plan"] = g["PV"] / g["presupuesto"]
    g["SPI"] = g["EV"] / g["PV"].replace(0, np.nan)
    g["CPI"] = g["EV"] / g["AC"].replace(0, np.nan)
    nombres = d["presupuesto"].set_index("Comp.")["Componente"]
    g["Componente"] = g["Comp."].map(nombres)
    return g


def anticipos(d) -> dict:
    ds, gt = d["desembolsos"], d["gastos"]
    ok = ds["Estado"] == "Desembolsado"
    ant = ds.loc[ok & (ds["Mecanismo"] == "Anticipo de fondos"), "Monto desembolsado"].sum()
    dir_ = ds.loc[ok & (ds["Mecanismo"] == "Pago directo"), "Monto desembolsado"].sum()
    just = gt.loc[gt["Justificado al BID"] == "Sí", "Monto USD"].sum()
    con_ant = gt.loc[(gt["Mecanismo"] == "Anticipo de fondos") & (gt["Estado de pago"] == "Pagado"), "Monto USD"].sum()
    return dict(anticipos=ant, pagos_directos=dir_, justificado=just, pagado_con_anticipo=con_ant,
                pct_justificado=(just / ant) if ant else np.nan, saldo_por_justificar=ant - just,
                total_desembolsado=ant + dir_)


def focalizacion(d) -> pd.DataFrame:
    p = d["param"]
    f = d["focal"].copy()
    f = f[f["ISO 3166-2"].astype(str).str.startswith("SV-")].copy()
    f["cobertura"] = f["Alcanzado acumulado"] / f["Meta año 1"]
    f["pob_rel"] = f["Peso población objetivo"] / f["Peso población objetivo"].max()
    f["brecha"] = 1 - f["cobertura"].clip(upper=1)
    f["indice"] = p["W_Vuln"] * f["Vulnerabilidad (0-1)"] + p["W_Pob"] * f["pob_rel"] + p["W_Brecha"] * f["brecha"]
    f["prioridad"] = np.where(f["indice"] >= p["Prior_Alta"], "Alta", np.where(f["indice"] >= p["Prior_Media"], "Media", "Baja"))
    inv = d["gastos"].groupby("Departamento")["Monto USD"].sum()
    f["inversion"] = f["Departamento"].map(inv).fillna(0.0)
    return f


def kpis(d) -> dict:
    p, poa = d["param"], poa_evm(d)
    comp = por_componente(d, poa)
    a = anticipos(d)
    ejecutado = float(d["gastos"]["Monto USD"].sum())
    ev, pv, ac, pres = poa["EV"].sum(), poa["PV"].sum(), poa["AC"].sum(), poa["Presupuesto POA USD"].sum()
    f = focalizacion(d)
    cum = d["cumplimiento"]
    exig = cum[cum["Exigible a la fecha"] == 1]
    return dict(
        total_programa=p["Total_Programa"], ejecutado=ejecutado, pct_ejecutado=ejecutado / p["Total_Programa"],
        presupuesto_poa=pres, EV=ev, PV=pv, AC=ac, SPI=ev / pv, CPI=ev / ac,
        avance_fisico=ev / pres, avance_planificado=pv / pres, avance_financiero=ac / pres,
        **a,
        riesgos_altos=int(((d["riesgos"]["Nivel"] == "Alto") & (d["riesgos"]["Estado"] != "Cerrado")).sum()),
        alertas_pa=int((d["pa"]["Alerta"] == "Atrasado").sum()),
        obligaciones_vencidas=int((cum["Alerta"] == "Vencida").sum()),
        pct_cumplimiento=float((exig["Estado"] == "Cumplida").sum() / len(exig)) if len(exig) else np.nan,
        beneficiarios=int(f["Alcanzado acumulado"].sum()), meta_anio1=int(f["Meta año 1"].sum()),
        deptos_prioridad_alta=int((f["prioridad"] == "Alta").sum()),
    )
