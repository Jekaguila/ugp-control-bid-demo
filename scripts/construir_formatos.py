"""Construye herramientas_seguimiento/UGP_Formatos_de_Gestion.xlsx

Segundo libro: formatos de gestión del ciclo de vida (acta, cambios, minutas, No Objeción,
evaluación 3CV, incidentes, lecciones, cierre). Adapta y amplía el 'Formatos.xlsx' de partida
al contexto de un Programa BID. Todo el contenido es ilustrativo (datos simulados).

Uso:  python scripts/construir_formatos.py [ruta_salida.xlsx]
"""
import sys
from pathlib import Path
from datetime import date
from openpyxl import Workbook
from xl_base import *  # noqa: F401,F403

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "herramientas_seguimiento" / "UGP_Formatos_de_Gestion.xlsx"
CORTE = date(2027, 6, 30)
EST = Alignment(vertical="top", wrap_text=True)


def forma(ws, filas, ini=4, ancho_a=30, ancho_b=95):
    """Formulario etiqueta/valor. filas: [(etiqueta, valor)] ; etiqueta None -> subtítulo en blanco."""
    ws.column_dimensions["A"].width = ancho_a
    ws.column_dimensions["B"].width = ancho_b
    r = ini
    for et, val in filas:
        a, b = ws.cell(r, 1, et), ws.cell(r, 2, val)
        a.font, a.fill, a.border = f(True), C_SUB, BORDE
        b.font, b.border, b.alignment = f(False, "0000FF"), BORDE, EST
        a.alignment = EST
        if isinstance(val, str):
            n = max(1, len(val) // 95 + val.count("\n") + 1)
            ws.row_dimensions[r].height = max(20, 15.5 * n)
        if isinstance(val, date):
            b.number_format, b.alignment = FECHA, Alignment(horizontal="left", vertical="top")
        r += 1
    return r


def seccion(ws, fila, texto, ncols=2):
    c = ws.cell(fila, 1, texto)
    c.font, c.fill = f(True, "FFFFFF"), C_ENCAB
    for j in range(2, ncols + 1):
        ws.cell(fila, j).fill = C_ENCAB
    return fila + 1


def hoja_leeme(wb, indice):
    ws = wb.create_sheet("LEEME")
    titulo(ws, "UGP · Formatos de gestión del Programa", "Complementa al libro «UGP_Sistema_Integrado_de_Control.xlsx». Mismos códigos de color: azul = dato ingresado; negro/gris = fórmula.")
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 90
    r = 5
    for h, d in indice:
        a, b = ws.cell(r, 1, h), ws.cell(r, 2, d)
        a.font, b.font = f(True, AZUL), f()
        b.alignment = EST
        ws.row_dimensions[r].height = 32
        r += 1
    ws["D1"], ws["E1"] = "Fecha de corte simulada", CORTE
    ws["D1"].font, ws["E1"].font, ws["E1"].number_format = f(False, "595959", 9, True), f(False, "0000FF", 9), FECHA
    nombre(wb, "Fecha_Cierre_Demo", "LEEME", "$E$1")
    nota(ws, r + 1, "Origen: los formatos parten del archivo de ejemplo de la autora (acta, cambios, minuta, incidentes, lecciones, cierre) y se ampliaron con las exigencias de un Programa BID.")
    nota(ws, r + 2, "Los nombres, fechas y montos son ficticios. Sustituir por la información oficial al usar los formatos en un Programa real.")


def hoja_acta(wb):
    ws = wb.create_sheet("Acta_Constitucion")
    titulo(ws, "Acta de constitución de la UGP — Programa de Integración Académica y Comunitaria",
           "Formato PMBOK adaptado al ciclo BID: documenta el mandato, los objetivos, los supuestos y las restricciones antes de ejecutar.")
    forma(ws, [
        ("Programa", "Programa de Integración Académica y Comunitaria para Jóvenes en El Salvador (ES-L1175)"),
        ("Operaciones", "Préstamo 6153/OC-ES (US$100 millones) y cooperación no reembolsable 6154/GR-ES (US$4 millones) — importes del TDR; verificar contra el contrato."),
        ("Organismo Ejecutor", "Dirección de Integración — UGP bajo la Gerencia de Cooperación Institucional"),
        ("Patrocinador", "Dirección General de la Dirección de Integración (ficticio para la demostración)"),
        ("Coordinador General", "Por designar (cargo del proceso 3CV)"),
        ("Propósito del Programa", "Asegurar la trayectoria educativa de los jóvenes salvadoreños mediante la integración académica y comunitaria, evitando la deserción en la transición entre niveles."),
        ("Objetivos de la UGP", "1) Planificar y controlar el avance físico y financiero.\n2) Gestionar los aspectos fiduciarios (presupuesto, desembolsos, adquisiciones y auditorías).\n3) Asegurar el cumplimiento del contrato, del MOP y de las políticas del BID.\n4) Articular con el BID y reportar mensualmente."),
        ("Criterios de éxito", "• Ejecución anual del POA ≥ 90% y SPI/CPI ≥ 0,95.\n• Anticipos justificados ≥ 80% antes de solicitar nuevos desembolsos.\n• Cero hallazgos sin plan de acción en las auditorías.\n• Informe mensual entregado en el plazo del TDR."),
        ("Requisitos de alto nivel", "Sistema único de control (libro de gastos como fuente de la ejecución), Plan de Adquisiciones vigente, matriz de resultados con línea base y metas, registro de riesgos y matriz de cumplimiento actualizados."),
        ("Supuestos de alto nivel", "• El contrato de préstamo y el MOP están vigentes y disponibles para la UGP.\n• La Dirección de Integración provee acceso a los sistemas de información institucionales.\n• El BID mantiene el plazo de referencia para No Objeciones."),
        ("Restricciones", "Normas de adquisiciones y consultores del BID (GN-2349-15 y GN-2350-15); período de desembolsos del contrato; reglas de elegibilidad de gastos."),
        ("Riesgos iniciales", "Retraso en selección de consultores clave; baja justificación de anticipos; demora en No Objeciones; cobertura territorial desigual (ver P1_Riesgos del libro integrado)."),
        ("Hitos principales", "Instalación de la UGP y plazas clave; MOP validado; primer Plan de Adquisiciones aprobado; primer desembolso; línea base de indicadores; primera misión de administración."),
        ("Presupuesto resumido", "Ver F1_Presupuesto_PEP del libro integrado."),
        ("Autoridad del Coordinador", "Conduce a la UGP; punto focal con el BID; propone cambios al CCB; escala riesgos altos y desvíos de SPI/CPI al patrocinador."),
        ("Aprobaciones", "Patrocinador: ____________________   Fecha: ____ / ____ / ______\nCoordinador General: ____________________   Fecha: ____ / ____ / ______"),
    ])


def hoja_cambios(wb):
    ws = wb.create_sheet("Solicitud_Cambios")
    titulo(ws, "Solicitud de cambio y acta del Comité de Control de Cambios (CCB)",
           "Todo cambio al alcance, cronograma, presupuesto o Plan de Adquisiciones pasa por el CCB; los que exigen No Objeción se registran en A3 del libro integrado.")
    r = forma(ws, [
        ("N.º de solicitud", "CC-001"), ("Fecha", date(2027, 5, 12)),
        ("Asistentes", "Coordinador General · Esp. Financiero · Esp. Adquisiciones · Esp. Planificación M&S · Esp. Social"),
        ("Asunto", "Reprogramación de la contratación de la plataforma de seguimiento de trayectorias (PA-12)"),
        ("Tipo de cambio", "Acción correctiva"),
        ("Detalle", "La preparación de los documentos de contratación acumula atraso frente al Plan de Adquisiciones. Se propone mover la publicación del proceso al mes siguiente y ajustar el hito asociado del POA."),
        ("Impacto en alcance", "Ninguno."), ("Impacto en cronograma", "+30 días en el hito del componente 3; ruta crítica no afectada por holgura de 15 días."),
        ("Impacto en costo", "Sin variación del monto programado (USD)."),
        ("¿Requiere No Objeción del BID?", "Sí — modificación del Plan de Adquisiciones"),
        ("Decisión del CCB", "Aprobado"), ("Responsable de ejecutar", "Esp. Adquisiciones"), ("Fecha compromiso", date(2027, 6, 15)),
    ])
    lista(ws, "B8", '"Acción correctiva,Acción preventiva,Reparación de defecto,Cambio de alcance,Cambio presupuestario"')
    lista(ws, "B13", '"Sí — modificación del Plan de Adquisiciones,Sí — modificación del POA/PEP,Sí — reasignación de categorías,No"')
    lista(ws, "B14", '"Aprobado,Rechazado,Diferido,Aprobado con condiciones"')
    ws2 = wb.create_sheet("Registro_Cambios")
    titulo(ws2, "Registro de cambios aprobados, rechazados y diferidos", "Cada fila corresponde a una solicitud al CCB.")
    cols = [dict(h="N.º", w=9), dict(h="Fecha", w=12, fmt=FECHA), dict(h="Asunto", w=52, wrap=True), dict(h="Tipo", w=22),
            dict(h="Impacto USD", w=14, fmt=USD), dict(h="Decisión", w=18), dict(h="No Objeción", w=14), dict(h="Fecha de resolución", w=13, fmt=FECHA),
            dict(h="Días a resolver", w=11, fmt="0", tipo="calc")]
    D = [("CC-001", date(2027, 5, 12), "Reprogramación del proceso PA-12", "Acción correctiva", 0, "Aprobado", "Pendiente", date(2027, 5, 26)),
         ("CC-002", date(2027, 3, 8), "Reasignación entre categorías (C2 → C4)", "Cambio presupuestario", 120000, "Aprobado", "Concedida", date(2027, 3, 29)),
         ("CC-003", date(2027, 4, 2), "Ampliación del plazo de un contrato de consultoría", "Acción preventiva", 0, "Diferido", "N/A", date(2027, 4, 16))]
    tabla(ws2, cols, [list(d) + [f"=IF(H{FIRST + i}=\"\",\"\",H{FIRST + i}-B{FIRST + i})"] for i, d in enumerate(D)])
    lista(ws2, "D5:D60", '"Acción correctiva,Acción preventiva,Reparación de defecto,Cambio de alcance,Cambio presupuestario"')
    lista(ws2, "F5:F60", '"Aprobado,Rechazado,Diferido,Aprobado con condiciones"')
    lista(ws2, "G5:G60", '"Pendiente,Concedida,N/A,Denegada"')
    semaforo(ws2, "F5:F60", "Aprobado", "Diferido", "Rechazado")
    ws2["K4"], ws2["L4"] = "Impacto USD aprobado", '=SUMIFS(E5:E60,F5:F60,"Aprobado")'
    ws2["L4"].number_format = USD
    ws2["K4"].font = ws2["L4"].font = f(True)
    ws2.column_dimensions["K"].width = 24
    ws2.column_dimensions["L"].width = 16


def hoja_minuta(wb):
    ws = wb.create_sheet("Minuta_Seguimiento")
    titulo(ws, "Minuta de reunión de seguimiento y matriz de compromisos",
           "Se emplea en reuniones internas de la UGP y en las reuniones técnicas con el BID; los compromisos alimentan A2 del libro integrado.")
    r = forma(ws, [
        ("Reunión", "Reunión mensual de seguimiento — corte al 30/06/2027"), ("Fecha", date(2027, 7, 2)),
        ("Asistentes", "Coordinador General · Esp. Financiero · Esp. Adquisiciones · Esp. Planificación M&S · Esp. Social · Especialista sectorial del BID (ficticio)"),
        ("Asunto", "Justificación de anticipos, atrasos en adquisiciones y preparación de la misión de administración"),
        ("Temas tratados", "1) El porcentaje de anticipos justificado está por debajo del umbral de 80%; se acuerda priorizar la justificación de los apoyos del componente 2.\n2) PA-12 en atraso; se presentó solicitud de cambio CC-001.\n3) Preparación de la agenda de la misión: avance de indicadores, riesgos altos y compromisos vencidos.\n4) Se revisó el borrador del informe mensual del período."),
        ("Decisiones", "Congelar nuevas solicitudes de anticipo hasta superar el 80% de justificación. Aprobar el calendario de visitas territoriales de julio."),
        ("Próxima reunión", date(2027, 8, 4)),
    ])
    r = seccion(ws, r + 1, "Compromisos", 5)
    hdr = ["N.º", "Compromiso", "Responsable", "Fecha límite", "Estado"]
    ws.column_dimensions["C"].width = 24
    ws.column_dimensions["D"].width = 14
    ws.column_dimensions["E"].width = 14
    for j, h in enumerate(hdr):
        c = ws.cell(r, 1 + j, h)
        c.font, c.fill, c.border = f(True, "FFFFFF"), C_ENCAB, BORDE
    comp = [("M-01", "Presentar justificación de anticipos pendientes de mayo", "Esp. Financiero", date(2027, 7, 15), "En proceso"),
            ("M-02", "Publicar proceso PA-12 con No Objeción", "Esp. Adquisiciones", date(2027, 7, 20), "En proceso"),
            ("M-03", "Consolidar la matriz de indicadores con avances de junio", "Esp. Planificación M&S", date(2027, 7, 10), "Pendiente"),
            ("M-04", "Elaborar agenda y carpeta de la misión", "Coordinador General", date(2027, 7, 25), "Pendiente")]
    for i, d in enumerate(comp):
        for j, v in enumerate(d):
            c = ws.cell(r + 1 + i, 1 + j, v)
            c.font, c.border, c.alignment = f(False, "0000FF"), BORDE, EST
        ws.cell(r + 1 + i, 4).number_format = FECHA
    lista(ws, f"E{r + 1}:E{r + 20}", '"Pendiente,En proceso,Cumplido,Vencido"')
    semaforo(ws, f"E{r + 1}:E{r + 20}", "Cumplido", "En proceso", "Vencido")


def hoja_no_objecion(wb):
    ws = wb.create_sheet("Solicitud_No_Objecion")
    titulo(ws, "Solicitud de No Objeción al BID — lista de verificación previa al envío",
           "Verificar cada punto antes de enviar la solicitud; una solicitud incompleta es la causa más común de devoluciones y atrasos.")
    r = forma(ws, [
        ("N.º interno", "NO-014"), ("Fecha de envío", date(2027, 6, 18)), ("Proceso del PA", "PA-11"),
        ("Etapa a objetar", "Informe de evaluación y recomendación de adjudicación"),
        ("Descripción", "Contratación de servicios de consultoría para la evaluación de medio término del componente 4 (ficticio)."),
        ("Monto estimado (USD)", 185000), ("Método", "SBCC"), ("Revisión", "Ex ante"),
        ("Solicitado por", "Esp. Adquisiciones"), ("Aprobado internamente por", "Coordinador General"),
    ])
    ws["B9"].number_format = USD
    lista(ws, "B10", '"LPI,LPN,Comparación de precios,SBCC,3CV,Contratación directa"')
    lista(ws, "B11", '"Ex ante,Ex post"')
    r = seccion(ws, r + 1, "Lista de verificación", 3)
    ws.column_dimensions["C"].width = 16
    items = ["Proceso incluido en el Plan de Adquisiciones vigente", "Método y revisión coinciden con el PA", "Documento a objetar completo y firmado",
             "Cuadro de evaluación con puntajes y justificación", "Verificación de elegibilidad e integridad (GN-2349-15 / GN-2350-15)",
             "Disponibilidad presupuestaria confirmada (F1/F2)", "Categoría de inversión del contrato verificada", "Carta de envío firmada por la autoridad competente"]
    for i, t in enumerate(items):
        a, b = ws.cell(r + i, 1, t), ws.cell(r + i, 2, "Sí" if i < 7 else "No")
        a.font, b.font, a.border, b.border = f(), f(False, "0000FF"), BORDE, BORDE
        a.alignment = EST
        ws.row_dimensions[r + i].height = 20
    lista(ws, f"B{r}:B{r + len(items) - 1}", '"Sí,No,N/A"')
    c = ws.cell(r + len(items) + 1, 1, "Resultado")
    c.font = f(True)
    v = ws.cell(r + len(items) + 1, 2, f'=IF(COUNTIF(B{r}:B{r + len(items) - 1},"No")=0,"LISTO PARA ENVIAR","COMPLETAR ANTES DE ENVIAR")')
    v.font, v.fill = f(True), C_CALC
    semaforo(ws, f"B{r + len(items) + 1}", "LISTO PARA ENVIAR", None, "COMPLETAR ANTES DE ENVIAR")


def hoja_evaluacion(wb):
    ws = wb.create_sheet("Evaluacion_3CV")
    titulo(ws, "Evaluación técnica 3CV — calculadora de puntaje sobre 100 puntos (criterios de la sección XV del TDR)",
           "Candidaturas ficticias. La fórmula aplica los topes del TDR; el empate se resuelve por años de experiencia demostrable.")
    ws.column_dimensions["A"].width = 64
    cands = ["Candidatura A", "Candidatura B", "Candidatura C", "Candidatura D"]
    for j, n in enumerate(cands):
        ws.column_dimensions[L(2 + j)].width = 16
        c = ws.cell(4, 2 + j, n)
        c.font, c.fill, c.alignment = f(True, "FFFFFF"), C_ENCAB, Alignment(horizontal="center")
    ws.cell(4, 1, "Concepto").font = f(True, "FFFFFF")
    ws.cell(4, 1).fill = C_ENCAB
    ws.cell(4, 6, "Tope TDR").font = f(True, "FFFFFF")
    ws.cell(4, 6).fill = C_ENCAB
    ws.column_dimensions["F"].width = 10
    filas = [
        (5, "FACTORES HABILITANTES (Sí/No)", None, None),
        (6, "Título universitario de grado en área afín", ["Sí", "Sí", "Sí", "Sí"], None),
        (7, "≥ 1 programa/proyecto con fuentes externas", ["Sí", "Sí", "No", "Sí"], None),
        (8, "≥ 3 años en coordinación/gerencia de proyectos", ["Sí", "Sí", "Sí", "No"], None),
        (9, "Resultado de habilitación", "H", None),
        (10, "ENTRADAS", None, None),
        (11, "Posgrado más alto (Maestría / Especialización / Curso / Ninguno)", ["Maestría", "Maestría", "Especialización", "Maestría"], None),
        (12, "Certificación PM4R o PMP (cantidad)", [1, 0, 0, 0], None),
        (13, "Cursos/especializaciones en gestión de proyectos (cantidad)", [0, 2, 1, 4], None),
        (14, "Años de experiencia profesional en proyectos de desarrollo", [8, 7, 6, 11], None),
        (15, "Años con recursos externos (planificación, seguimiento, riesgos, informes)", [8, 5, 0, 11], None),
        (16, "Experiencias en programas financiados por el BID (cantidad)", [2, 1, 0, 2], None),
        (17, "Entrevista (0-10)", [8, 7, 6, 9], None),
        (18, "PUNTAJE", None, None),
        (19, "1.1 Posgrado", '=IF({c}11="Maestría",15,IF({c}11="Especialización",10,IF({c}11="Curso",5,0)))', 15),
        (20, "1.2 Certificaciones / formación en gestión de proyectos", '=IF({c}12>0,15,MIN(15,5*{c}13))', 15),
        (21, "2.1 Experiencia profesional (5 pts por año sobre 5)", '=MIN(35,MAX(0,{c}14-5)*5)', 35),
        (22, "2.2 Experiencia con recursos externos (≥ 5 años)", '=IF({c}15>=5,5,0)', 5),
        (23, "2.3 Experiencia en programas BID (10 pts c/u)", '=MIN(20,10*{c}16)', 20),
        (24, "3. Entrevista", '=MIN(10,MAX(0,{c}17))', 10),
        (25, "TOTAL EVALUACIÓN TÉCNICA", '=SUM({c}19:{c}24)', 100),
        (26, "Posición (solo habilitados; desempate por años de experiencia)", "R", None),
    ]
    for r, et, v, tope in filas:
        a = ws.cell(r, 1, et)
        a.border = BORDE
        if v is None:
            a.font, a.fill = f(True, AZUL), C_SUB
            for j in range(2, 7):
                ws.cell(r, j).fill = C_SUB
            continue
        a.font = f(r in (9, 25, 26))
        for j in range(4):
            col = L(2 + j)
            if v == "H":
                val = f'=IF(COUNTIF({col}6:{col}8,"No")=0,"Habilitado","No habilitado")'
            elif v == "R":
                val = (f'=IF({col}9<>"Habilitado","—",1+SUMPRODUCT(($B$9:$E$9="Habilitado")*(($B$25:$E$25>{col}25)+'
                       f'($B$25:$E$25={col}25)*($B$14:$E$14>{col}14))))')
            elif isinstance(v, list):
                val = v[j]
            else:
                val = v.format(c=col)
            c = ws.cell(r, 2 + j, val)
            es_calc = isinstance(val, str) and val.startswith("=")
            c.font = f(r in (9, 25, 26), "000000" if es_calc else "0000FF")
            c.border, c.alignment = BORDE, Alignment(horizontal="center")
            if es_calc:
                c.fill = C_CALC
        if tope:
            t = ws.cell(r, 6, tope)
            t.font, t.border, t.alignment = f(False, "595959"), BORDE, Alignment(horizontal="center")
    lista(ws, "B6:E8", '"Sí,No"')
    lista(ws, "B11:E11", '"Maestría,Especialización,Curso,Ninguno"')
    semaforo(ws, "B9:E9", "Habilitado", None, "No habilitado")
    nota(ws, 28, "Regla del TDR: el puntaje de posgrado se otorga solo por el grado más alto; los puntos de las certificaciones se topan en 15; el empate lo decide la experiencia demostrable.")
    nota(ws, 29, "Uso como autoevaluación: reemplazar una candidatura por los datos propios y comparar con la evidencia documental que se adjuntaría.")


def hoja_incidentes(wb):
    ws = wb.create_sheet("Registro_Incidentes")
    titulo(ws, "Registro de incidentes y problemas del Programa",
           "Un incidente es un hecho que ya ocurrió (a diferencia del riesgo). Los de prioridad alta se reportan al BID en el informe mensual.")
    cols = [dict(h="N.º", w=8), dict(h="Tipo", w=22), dict(h="Fecha", w=12, fmt=FECHA), dict(h="Descripción", w=54, wrap=True),
            dict(h="Prioridad", w=11), dict(h="Responsable", w=24), dict(h="Fecha límite", w=12, fmt=FECHA), dict(h="Estado", w=12),
            dict(h="Solución / acción", w=46, wrap=True), dict(h="Días abiertos", w=10, fmt="0", tipo="calc"), dict(h="Alerta", w=14, tipo="calc")]
    D = [("INC-01", "Fiduciario", date(2027, 3, 3), "Factura de proveedor sin comprobante de elegibilidad adjunto.", "Media", "Esp. Financiero", date(2027, 3, 10), "Cerrado", "Se completó el expediente y se re-archivó."),
         ("INC-02", "Adquisiciones", date(2027, 4, 19), "Oferta presentada fuera de plazo en proceso de consultoría.", "Media", "Esp. Adquisiciones", date(2027, 4, 26), "Cerrado", "Oferta rechazada y acta del hecho."),
         ("INC-03", "Datos", date(2027, 5, 21), "Planilla de beneficiarios con registros duplicados en un departamento.", "Alta", "Esp. Social", date(2027, 6, 11), "En proceso", "Depuración con el documento de identidad y validación cruzada."),
         ("INC-04", "Cronograma", date(2027, 6, 7), "Visita territorial suspendida por condiciones climáticas.", "Baja", "Esp. Planificación M&S", date(2027, 7, 15), "Abierto", "Reprogramar en julio."),
         ("INC-05", "Fiduciario", date(2027, 6, 14), "Diferencia entre el libro de gastos y el registro bancario por una transferencia devuelta.", "Alta", "Esp. Financiero", date(2027, 7, 5), "En proceso", "Conciliación y reintegro a la cuenta del Programa.")]
    rows = []
    for i, d in enumerate(D):
        n = FIRST + i
        rows.append(list(d) + [f'=IF(H{n}="Cerrado","",Fecha_Cierre_Demo-C{n})',
                               f'=IF(H{n}="Cerrado","Cerrado",IF(Fecha_Cierre_Demo>G{n},"Vencido","En plazo"))'])
    tabla(ws, cols, rows)
    lista(ws, "B5:B60", '"Fiduciario,Adquisiciones,Datos,Cronograma,Ambiental y social,Seguridad de la información,Otro"')
    lista(ws, "E5:E60", '"Alta,Media,Baja"')
    lista(ws, "H5:H60", '"Abierto,En proceso,Cerrado"')
    semaforo(ws, "K5:K60", "En plazo", None, "Vencido")
    semaforo(ws, "E5:E60", "Baja", "Media", "Alta")
    ws["M4"], ws["N4"] = "Abiertos", '=COUNTIFS(H5:H60,"<>Cerrado",A5:A60,"<>")'
    ws["M5"], ws["N5"] = "Vencidos", '=COUNTIF(K5:K60,"Vencido")'
    ws["M6"], ws["N6"] = "Alta prioridad abiertos", '=COUNTIFS(E5:E60,"Alta",H5:H60,"<>Cerrado")'
    for r in (4, 5, 6):
        ws[f"M{r}"].font, ws[f"N{r}"].font = f(True), f(True)
    ws.column_dimensions["M"].width = 24


def hoja_lecciones(wb):
    ws = wb.create_sheet("Lecciones_Aprendidas")
    titulo(ws, "Matriz de lecciones aprendidas", "Se actualiza después de cada misión, auditoría o hito. Alimenta el informe de cierre y el diseño de operaciones futuras.")
    cols = [dict(h="N.º", w=7), dict(h="Fecha", w=12, fmt=FECHA), dict(h="Proceso", w=22), dict(h="Qué se hizo bien", w=50, wrap=True),
            dict(h="Qué se pudo hacer mejor", w=50, wrap=True), dict(h="Recomendación / acción", w=50, wrap=True), dict(h="Responsable", w=22), dict(h="Aplicada", w=10)]
    D = [("L-01", date(2027, 2, 15), "Planificación", "Calendario de informes P1-P12 acordado desde la instalación.", "La matriz de indicadores se completó después de la primera misión.", "Cargar línea base y metas antes de la primera solicitud de desembolso.", "Esp. Planificación M&S", "Sí"),
         ("L-02", date(2027, 4, 5), "Fiduciario", "El libro de gastos como fuente única evitó cifras distintas entre informes.", "Algunos pagos se registraron con retraso semanal.", "Registrar en las 48 h siguientes al pago y conciliar cada quincena.", "Esp. Financiero", "Sí"),
         ("L-03", date(2027, 5, 18), "Adquisiciones", "Los términos de referencia estandarizados redujeron las consultas.", "Se subestimó el tiempo de preparación de documentos complejos.", "Añadir 15 días de holgura a procesos de más de USD 150.000.", "Esp. Adquisiciones", "No"),
         ("L-04", date(2027, 6, 20), "Territorio", "Las visitas conjuntas con el Esp. Social mejoraron la calidad de los datos.", "Hubo departamentos con baja cobertura al inicio.", "Priorizar según el índice de focalización de P2.", "Esp. Social", "No")]
    tabla(ws, cols, [list(d) for d in D])
    lista(ws, "H5:H60", '"Sí,No"')
    ws["J4"], ws["K4"] = "Lecciones aplicadas", '=COUNTIF(H5:H60,"Sí")/MAX(1,COUNTA(A5:A60))'
    ws["K4"].number_format = PCT
    ws["J4"].font = ws["K4"].font = f(True)
    ws.column_dimensions["J"].width = 22


def hoja_cierre(wb):
    ws = wb.create_sheet("Reporte_Cierre")
    titulo(ws, "Informe de cierre (formato para contrato, producto o fase)", "Plantilla con datos ilustrativos; el cierre del Programa sigue las condiciones del contrato y del MOP.")
    ws.column_dimensions["C"].width = 18
    r = forma(ws, [
        ("Objeto", "Cierre de la fase de instalación de la UGP (ficticio)"), ("Fecha", date(2027, 3, 31)),
        ("Asistentes", "Coordinador General · Especialistas de la UGP · Representante de la Dirección General"),
        ("Alcance", "Se logró instalar el equipo de la UGP, validar el MOP y aprobar el primer Plan de Adquisiciones."),
        ("Cronograma", "Cumplido con 12 días de atraso en la contratación de la plaza social."),
        ("Costo", "Ejecutado 96% del presupuesto de la fase; sin variaciones relevantes."),
        ("Calidad / aceptación", "Productos P1 y P2 aprobados por la Gerencia de Cooperación Institucional."),
        ("Conclusiones", "El sistema integrado de control quedó operando; se identificó la necesidad de reforzar la conciliación quincenal."),
        ("Pendientes", "Cargar línea base de los indicadores 3 y 4 antes de la primera misión."),
    ])
    r = seccion(ws, r + 1, "Resumen cuantitativo", 3)
    hdr = ["Concepto", "Planificado", "Real"]
    for j, h in enumerate(hdr):
        c = ws.cell(r, 1 + j, h)
        c.font, c.fill, c.border = f(True, "FFFFFF"), C_ENCAB, BORDE
    ws.cell(r, 2).alignment = ws.cell(r, 3).alignment = Alignment(horizontal="center")
    ws.column_dimensions["B"].width = 95
    q = [("Costo (USD)", 150000, 144000), ("Duración (días)", 90, 102), ("Hitos cumplidos", 8, 8)]
    for i, (a, p, rr) in enumerate(q):
        for j, v in enumerate((a, p, rr)):
            c = ws.cell(r + 1 + i, 1 + j, v)
            c.font, c.border = f(False, "0000FF" if j else "000000"), BORDE
            if j == 1 or j == 2:
                c.number_format = "#,##0"
    rv = r + 1 + len(q)
    ws.cell(rv, 1, "Variación de costo (real − plan)").font = f(True)
    ws.cell(rv, 3, f"=C{r + 1}-B{r + 1}").number_format = USD
    ws.cell(rv + 1, 1, "Variación de duración (días)").font = f(True)
    ws.cell(rv + 1, 3, f"=C{r + 2}-B{r + 2}").number_format = "0"
    ws.cell(rv, 3).fill = ws.cell(rv + 1, 3).fill = C_CALC


def construir(salida=SALIDA):
    wb = Workbook()
    wb.remove(wb.active)
    indice = [("Acta_Constitucion", "Mandato, objetivos, criterios de éxito, supuestos y restricciones de la UGP"),
              ("Solicitud_Cambios", "Solicitud de cambio y acta del Comité de Control de Cambios (CCB)"),
              ("Registro_Cambios", "Registro de cambios con decisión, No Objeción y días de resolución"),
              ("Minuta_Seguimiento", "Minuta de reunión con matriz de compromisos"),
              ("Solicitud_No_Objecion", "Lista de verificación previa al envío de una No Objeción al BID"),
              ("Evaluacion_3CV", "Calculadora del puntaje técnico sobre 100 puntos con los criterios de la sección XV del TDR"),
              ("Registro_Incidentes", "Registro de incidentes con prioridad, vencimiento y conteos"),
              ("Lecciones_Aprendidas", "Matriz de lecciones aprendidas y porcentaje aplicado"),
              ("Reporte_Cierre", "Informe de cierre con variaciones de costo y plazo")]
    hoja_leeme(wb, indice)
    hoja_acta(wb)
    hoja_cambios(wb)
    hoja_minuta(wb)
    hoja_no_objecion(wb)
    hoja_evaluacion(wb)
    hoja_incidentes(wb)
    hoja_lecciones(wb)
    hoja_cierre(wb)
    for ws in wb:
        ws.sheet_properties.tabColor = "7F7F7F" if ws.title == "LEEME" else "2E75B6"
        ws.page_setup.orientation = "landscape"
        ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.sheet_view.showGridLines = False
    wb.calculation.fullCalcOnLoad = True
    wb.properties.title = "UGP — Formatos de gestión (DEMO con datos simulados)"
    wb.properties.creator = "Jessica Liset Martínez de Águila"
    salida = Path(salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    wb.save(salida)
    print("OK", salida, "| hojas:", len(wb.sheetnames))
    return salida


if __name__ == "__main__":
    construir(sys.argv[1] if len(sys.argv) > 1 else SALIDA)
