"""Construye el libro integrado: herramientas_seguimiento/UGP_Sistema_Integrado_de_Control.xlsx

Uso:  python scripts/construir_excel.py [ruta_salida.xlsx]
Los datos son sintéticos y reproducibles (semilla fija en datos_demo.py).
"""
import sys
from pathlib import Path
from openpyxl import Workbook
import hojas_base as hb
import hojas_p1 as p1
import hojas_fiduciario as fd
import hojas_cumplimiento as cu
import hojas_equipo as eq
import hojas_final as fi
import datos_calculados as dc

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "herramientas_seguimiento" / "UGP_Sistema_Integrado_de_Control.xlsx"

ORDEN = [
    ("LEEME", "Base", "Gris"), ("Tablero", "Base", "Gris"), ("Parametros", "Base", "Gris"), ("Controles", "Base", "Gris"),
    ("P1_Resultados", "1 Planificación y control", "1F3864"), ("P1_POA", "1 Planificación y control", "1F3864"),
    ("P1_Avance_FF", "1 Planificación y control", "1F3864"), ("P1_Riesgos", "1 Planificación y control", "1F3864"),
    ("P2_Focalizacion", "1 Planificación y control", "1F3864"),
    ("F1_Presupuesto_PEP", "2 Gestión fiduciaria", "548235"), ("F2_Ejecucion", "2 Gestión fiduciaria", "548235"),
    ("F3_Desembolsos", "2 Gestión fiduciaria", "548235"), ("F3_Plan_Financiero", "2 Gestión fiduciaria", "548235"),
    ("F4_Plan_Adquisiciones", "2 Gestión fiduciaria", "548235"), ("F5_Contratos", "2 Gestión fiduciaria", "548235"),
    ("F6_Auditoria", "2 Gestión fiduciaria", "548235"),
    ("N1_Cumplimiento", "3 Cumplimiento normativo", "C55A11"),
    ("A1_Equipo", "4 Articulación y reporte", "7030A0"), ("A1_RACI", "4 Articulación y reporte", "7030A0"),
    ("A2_Misiones_BID", "4 Articulación y reporte", "7030A0"), ("A3_No_Objeciones", "4 Articulación y reporte", "7030A0"),
    ("A4_Interesados", "4 Articulación y reporte", "7030A0"), ("A5_Calendario_Informes", "4 Articulación y reporte", "7030A0"),
    ("A6_Informe_Mensual", "4 Articulación y reporte", "7030A0"), ("Listas", "Base", "Gris"),
]
DESC = {
    "LEEME": ("Instrucciones, código de colores y ciclo mensual", "Coordinador General", "Cuando cambie el sistema"),
    "Tablero": ("Semáforos ejecutivos, mapa de calor de riesgos y gráficos", "Esp. Planificación", "Mensual"),
    "Parametros": ("Datos del TDR, fecha de corte, umbrales y pesos", "Coordinador General", "Mensual (fecha de corte)"),
    "Controles": ("16 pruebas automáticas de consistencia entre hojas", "Esp. Planificación", "Mensual, antes del informe"),
    "P1_Resultados": ("Matriz de resultados: metas anuales, esperado al corte, cumplimiento y semáforo", "Esp. Planificación", "Mensual / anual"),
    "P1_POA": ("POA e hitos con valor ganado (EV, PV, AC, SPI, CPI) por actividad", "Esp. Planificación", "Mensual"),
    "P1_Avance_FF": ("Avance físico y financiero consolidado por componente", "Esp. Planificación", "Mensual"),
    "P1_Riesgos": ("Registro de riesgos, puntaje P×I, respuesta y riesgo residual", "Esp. Planificación", "Mensual"),
    "P2_Focalizacion": ("Metas, cobertura, índice de focalización e inversión por departamento", "Esp. Social", "Mensual"),
    "F1_Presupuesto_PEP": ("Presupuesto por componente y fuente, PEP a 5 años y ejecución", "Esp. Financiero", "Trimestral"),
    "F2_Ejecucion": ("Libro de gastos: fuente única de la ejecución", "Esp. Financiero", "Continua"),
    "F3_Desembolsos": ("Solicitudes de desembolso y control del anticipo (umbral de justificación)", "Esp. Financiero", "Quincenal / mensual"),
    "F3_Plan_Financiero": ("Gasto proyectado vs. real por trimestre", "Esp. Financiero", "Trimestral"),
    "F4_Plan_Adquisiciones": ("Plan de adquisiciones, métodos, estados, desvíos y alertas", "Esp. Adquisiciones", "Semanal"),
    "F5_Contratos": ("Contratos, pagos, saldos y vigencias", "Esp. Adquisiciones", "Mensual"),
    "F6_Auditoria": ("Plan de auditoría y seguimiento de recomendaciones", "Esp. Financiero", "Mensual"),
    "N1_Cumplimiento": ("Matriz de cumplimiento contractual, del MOP y de políticas BID, con alertas", "Coordinador General", "Mensual"),
    "A1_Equipo": ("Plazas de la UGP, estado de contratación y funciones", "Coordinador General", "Cuando cambie"),
    "A1_RACI": ("Matriz de responsabilidades de los 14 procesos de la UGP", "Coordinador General", "Cuando cambie"),
    "A2_Misiones_BID": ("Misiones del BID y matriz de compromisos con atraso", "Esp. Planificación", "Por misión / mensual"),
    "A3_No_Objeciones": ("Registro de No Objeciones y días de trámite", "Esp. Adquisiciones", "Continua"),
    "A4_Interesados": ("Interesados, poder/interés y estrategia de comunicación", "Esp. Social", "Trimestral"),
    "A5_Calendario_Informes": ("Productos P1-P12 de la consultoría: fechas límite y pago habilitado", "Coordinador General", "Mensual"),
    "A6_Informe_Mensual": ("Borrador automático del informe mensual (contenido mínimo del TDR)", "Esp. Planificación", "Mensual"),
    "Listas": ("Listas desplegables", "Esp. Planificación", "Cuando cambie"),
}


def construir(salida=SALIDA):
    wb = Workbook()
    wb.remove(wb.active)
    hb.hoja_listas(wb)
    hb.hoja_parametros(wb)
    n_gastos = fd.hoja_ejecucion(wb)
    fd.hoja_presupuesto(wb)
    fd.hoja_desembolsos(wb, dc.libro_gastos())
    fd.hoja_plan_financiero(wb)
    fd.hoja_adquisiciones(wb)
    fd.hoja_contratos(wb)
    fd.hoja_auditorias(wb)
    p1.hoja_poa(wb)
    p1.hoja_avance(wb)
    p1.hoja_riesgos(wb)
    p1.hoja_focalizacion(wb)
    fi.hoja_resultados(wb)
    cu.hoja_cumplimiento(wb)
    cu.hoja_misiones(wb)
    cu.hoja_no_objeciones(wb)
    cu.hoja_calendario(wb)
    eq.hoja_equipo(wb)
    eq.hoja_interesados(wb)
    eq.hoja_informe(wb)
    fi.hoja_controles(wb)
    fi.hoja_tablero(wb)
    idx = [(n, p, *DESC[n]) for n, p, _ in ORDEN if n != "LEEME"]
    fi.hoja_leeme(wb, idx)
    wb._sheets = [wb[n] for n, _, _ in ORDEN]
    for n, _, color in ORDEN:
        ws = wb[n]
        ws.sheet_properties.tabColor = "808080" if color == "Gris" else color
        ws.page_setup.orientation = "landscape"
        ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
        ws.sheet_properties.pageSetUpPr.fitToPage = True
    wb.active = 1
    wb.calculation.fullCalcOnLoad = True
    wb.properties.title = "UGP — Sistema integrado de control (DEMO con datos simulados)"
    wb.properties.creator = "Jessica Liset Martínez de Águila"
    salida = Path(salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    wb.save(salida)
    print("OK", salida, "| hojas:", len(wb.sheetnames), "| gastos:", n_gastos)
    return salida


if __name__ == "__main__":
    construir(sys.argv[1] if len(sys.argv) > 1 else SALIDA)
