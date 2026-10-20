"""Lectura del libro integrado de Excel (hojas por encabezado, no por posición de celda).

El libro debe haberse calculado al menos una vez (Excel o LibreOffice) para que existan valores
en caché de las fórmulas; el dashboard usa de las hojas solo las columnas de **entrada** y
recalcula los indicadores en `indicadores.py`.
"""
from __future__ import annotations
from pathlib import Path
import datetime as dt
import pandas as pd
import openpyxl

RAIZ = Path(__file__).resolve().parents[2]
RUTA_POR_DEFECTO = RAIZ / "herramientas_seguimiento" / "UGP_Sistema_Integrado_de_Control.xlsx"
HDR = 3          # fila 4 de Excel (índice 0-based para pandas)


def _tabla(ruta, hoja, header=HDR, clave=None, hasta_vacio=True, usecols=None) -> pd.DataFrame:
    df = pd.read_excel(ruta, sheet_name=hoja, header=header, engine="openpyxl", usecols=usecols)
    df.columns = [str(c).strip() for c in df.columns]
    col0 = df.columns[0] if clave is None else clave
    if hasta_vacio:                      # corta en la primera fila vacía (hojas con dos tablas)
        vacio = df[col0].isna()
        if vacio.any():
            df = df.loc[: vacio.idxmax() - 1]
    return df.dropna(subset=[col0]).reset_index(drop=True)


def parametros(ruta) -> dict:
    """Valores de los nombres definidos (Fecha_Corte, Umbral_Verde, ...), leídos de su celda."""
    wb = openpyxl.load_workbook(ruta, data_only=True)
    out = {}
    for nom, dn in wb.defined_names.items():
        try:
            hoja, celda = dn.attr_text.split("!")
            v = wb[hoja.strip("'")][celda.replace("$", "")].value
        except Exception:
            continue
        out[nom] = v.date() if isinstance(v, dt.datetime) else v
    return out


def cargar(ruta=RUTA_POR_DEFECTO) -> dict:
    ruta = Path(ruta)
    d = {"param": parametros(ruta)}
    d["gastos"] = _tabla(ruta, "F2_Ejecucion")
    d["poa"] = _tabla(ruta, "P1_POA")
    d["avance"] = _tabla(ruta, "P1_Avance_FF")
    d["riesgos"] = _tabla(ruta, "P1_Riesgos")
    d["focal"] = _tabla(ruta, "P2_Focalizacion")
    d["resultados"] = _tabla(ruta, "P1_Resultados")
    d["presupuesto"] = _tabla(ruta, "F1_Presupuesto_PEP")
    d["desembolsos"] = _tabla(ruta, "F3_Desembolsos", usecols="A:I")
    d["plan_fin"] = _tabla(ruta, "F3_Plan_Financiero")
    d["pa"] = _tabla(ruta, "F4_Plan_Adquisiciones")
    d["contratos"] = _tabla(ruta, "F5_Contratos")
    d["auditorias"] = _tabla(ruta, "F6_Auditoria")
    d["recomendaciones"] = _tabla(ruta, "F6_Auditoria", header=12)
    d["cumplimiento"] = _tabla(ruta, "N1_Cumplimiento", usecols="A:L")
    d["misiones"] = _tabla(ruta, "A2_Misiones_BID")
    d["compromisos"] = _tabla(ruta, "A2_Misiones_BID", header=12)
    d["no_objeciones"] = _tabla(ruta, "A3_No_Objeciones")
    d["informes"] = _tabla(ruta, "A5_Calendario_Informes")
    for k in ("gastos", "poa", "pa", "contratos", "desembolsos", "no_objeciones", "informes", "compromisos"):
        for c in d[k].columns:
            if pd.api.types.is_datetime64_any_dtype(d[k][c]):
                d[k][c] = d[k][c].dt.date
    return d
