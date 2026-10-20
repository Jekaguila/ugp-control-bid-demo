"""Pilares 3 y 4 (parte 1): N1_Cumplimiento, A2_Misiones_BID, A3_No_Objeciones, A5_Calendario_Informes."""
from datetime import date
from xl_base import *
from hojas_base import REF
from datos_demo import *  # noqa: F401,F403

TIPOS_NO = '"Plan de Adquisiciones,TdR / pliegos,Evaluación y adjudicación,Contrato o enmienda,MOP,Reasignación presupuestaria,Otros"'


def hoja_cumplimiento(wb):
    ws = wb.create_sheet("N1_Cumplimiento")
    titulo(ws, "N1 · Matriz de cumplimiento normativo y contractual",
           "Obligaciones TÍPICAS de una operación BID. La columna «Cláusula» queda por completar al contrastar con el Contrato de Préstamo "
           "6153/OC-ES, el Convenio 6154/GR-ES y el MOP, que no se tuvieron a la vista.")
    cols = [dict(h="ID", w=7), dict(h="Instrumento", w=30), dict(h="Obligación", w=54, wrap=True),
            dict(h="Cláusula / sección", w=18, wrap=True), dict(h="Frecuencia", w=12), dict(h="Fecha límite", w=12, fmt=FECHA),
            dict(h="Estado", w=12), dict(h="Responsable", w=24), dict(h="Evidencia (expediente)", w=22),
            dict(h="Días al vencimiento", w=10, fmt="0", tipo="calc"), dict(h="Alerta", w=16, tipo="calc"),
            dict(h="Exigible a la fecha", w=9, fmt="0", tipo="calc")]
    I = LISTAS_INSTR = ["Contrato de Préstamo 6153/OC-ES", "Convenio GR 6154/GR-ES", "MOP", "Políticas BID", "Normativa nacional", "TDR / UGP"]
    F = "Fecha_Corte"
    fil = [
        (I[0], "Condiciones previas al primer desembolso cumplidas y certificadas", "Única", date(2027, 2, 5), "Cumplida", R_CG, "EV-01"),
        (I[2], "Manual Operativo del Programa (MOP) aprobado y vigente", "Única", date(2027, 1, 31), "Cumplida", R_CG, "EV-02"),
        (I[0], "Cuenta bancaria específica para los recursos del Programa", "Única", date(2027, 2, 5), "Cumplida", R_FIN, "EV-03"),
        (I[2], "Plan de Ejecución Plurianual (PEP) y POA del año aprobados", "Anual", date(2027, 1, 31), "Cumplida", R_PLAN, "EV-04"),
        (I[3], "Plan de Adquisiciones inicial registrado con No Objeción", "Única", date(2027, 1, 31), "Cumplida", R_ADQ, "EV-05"),
        (I[3], "Plan de Adquisiciones actualizado", "Trimestral", date(2027, 7, 15), "En proceso", R_ADQ, "EV-06"),
        (I[0], "Informe de progreso semestral al BID", "Semestral", date(2027, 7, 31), "En proceso", R_PLAN, "EV-07"),
        (I[0], "Estados financieros auditados del ejercicio 2027", "Anual", "=F6_Auditoria!F5", "Pendiente", R_FIN, "EV-08"),
        (I[0], "Justificación de anticipos hasta el umbral para solicitar uno nuevo", "Continua", date(2027, 7, 15), "En proceso", R_FIN, "EV-09"),
        (I[3], "Revisión ex post de adquisiciones (expedientes completos)", "Anual", date(2027, 12, 15), "Pendiente", R_ADQ, "EV-10"),
        (I[3], "Informe ambiental y social semestral", "Semestral", date(2027, 7, 31), "En proceso", R_SOC, "EV-11"),
        (I[3], "Mecanismo de quejas y reclamos operativo", "Única", date(2027, 3, 31), "Cumplida", R_SOC, "EV-12"),
        (I[5], "Protocolo de protección de datos de las personas beneficiarias", "Única", date(2027, 3, 31), "Cumplida", R_SOC, "EV-13"),
        (I[2], "Línea base de indicadores de resultados", "Única", date(2027, 6, 15), "En proceso", R_PLAN, "EV-14"),
        (I[5], "Informe mensual de gestión (P2-P11)", "Mensual", "=WORKDAY(EOMONTH(Fecha_Corte,0),Plazo_Informe)", "En proceso", R_CG, "EV-15"),
        (I[3], "Certificación de elegibilidad e integridad GN-2350-15 de consultores contratados", "Continua", date(2027, 6, 30), "Cumplida", R_ADQ, "EV-16"),
        (I[5], "Declaración de conflicto de interés y código de conducta del equipo", "Anual", date(2027, 12, 15), "Pendiente", R_CG, "EV-17"),
        (I[2], "No Objeción previa a cambios del MOP y reasignaciones entre categorías", "Por evento", None, "Pendiente", R_CG, "EV-18"),
        (I[0], "Evaluación de medio término", "Única", date(2029, 12, 31), "Pendiente", R_PLAN, "EV-19"),
    ]
    filas = []
    for i, (ins, ob, fr, fl, es, rs, ev) in enumerate(fil):
        n = FIRST + i
        filas.append([f"N-{i + 1:02d}", ins, ob, "Por verificar", fr, fl, es, rs, ev,
                      f'=IF(OR(G{n}="Cumplida",F{n}=""),"",F{n}-{F})',
                      f'=IF(G{n}="Cumplida","Cumplida",IF(F{n}="","Por evento",IF(F{n}<{F},"Vencida",IF(F{n}-{F}<=Dias_Alerta,"Próxima a vencer","En plazo"))))',
                      f'=IF(AND(F{n}<>"",F{n}<={F}),1,0)'])
    tabla(ws, cols, filas, altura=40)
    lista(ws, f"B{FIRST}:B200", "=" + REF["Instrumento"])
    lista(ws, f"G{FIRST}:G200", "=" + REF["Estado_cumpl"])
    lista(ws, f"H{FIRST}:H200", "=" + REF["Responsable"])
    semaforo(ws, f"K{FIRST}:K200", "Cumplida", "Próxima a vencer", "Vencida")
    # resumen a la derecha
    ws.column_dimensions["M"].width = 3
    ws.column_dimensions["N"].width = 46
    ws.column_dimensions["O"].width = 12
    G, FL, K = f"$G${FIRST}:$G$200", f"$F${FIRST}:$F$200", f"$K${FIRST}:$K$200"
    res = [("Obligaciones registradas", f'=COUNTIF($A${FIRST}:$A$200,"N-*")', "0"),
           ("Exigibles a la fecha de corte", f'=COUNTIFS({FL},"<="&Fecha_Corte)', "0"),
           ("Cumplidas (de las exigibles)", f'=COUNTIFS({G},"Cumplida",{FL},"<="&Fecha_Corte)', "0"),
           ("Vencidas", f'=COUNTIF({K},"Vencida")', "0"),
           ("Próximas a vencer", f'=COUNTIF({K},"Próxima a vencer")', "0"),
           ("% cumplimiento de exigibles", "=IF(O6=0,0,O7/O6)", PCT)]
    for j, h in ((14, "Resumen de cumplimiento"), (15, "Valor")):
        c = ws.cell(HDR, j, h)
        c.font, c.fill, c.border = f(True, "FFFFFF"), C_ENCAB, BORDE
    for i, (lab, fm, nf) in enumerate(res):
        r = FIRST + i
        ws.cell(r, 14, lab).font = f()
        v = ws.cell(r, 15, fm)
        v.font, v.fill, v.number_format = f(True), C_CALC, nf
        ws.cell(r, 14).border = v.border = BORDE
    return len(filas)


def hoja_misiones(wb):
    ws = wb.create_sheet("A2_Misiones_BID")
    titulo(ws, "A2 · Misiones del BID y matriz de compromisos (aide-mémoire)",
           "Tabla 1 (fila 4): misiones. Tabla 2 (fila 13): compromisos asumidos. La UGP responde como punto focal ante el BID.")
    c1 = [dict(h="ID", w=8), dict(h="Tipo de misión", w=22), dict(h="Inicio", w=11, fmt=FECHA), dict(h="Fin", w=11, fmt=FECHA),
          dict(h="Participantes (roles)", w=34, wrap=True), dict(h="Temas", w=46, wrap=True),
          dict(h="N.º compromisos", w=11, fmt="0", tipo="calc"), dict(h="Cumplidos", w=10, fmt="0", tipo="calc"),
          dict(h="% cumplimiento", w=11, fmt=PCT, tipo="calc")]
    M = [("M-01", "Misión de arranque", date(2027, 2, 15), date(2027, 2, 17), "Equipo de proyecto, especialistas fiduciarios y sectoriales (BID)", "Arranque, MOP, plan de adquisiciones, cuenta del Programa"),
         ("M-02", "Misión de seguimiento", date(2027, 5, 17), date(2027, 5, 21), "Equipo de proyecto y especialistas fiduciarios (BID)", "Avance del POA, adquisiciones, anticipos y riesgos")]
    f1 = [list(m) + [f'=COUNTIFS($B$14:$B$100,A{FIRST + i})', f'=COUNTIFS($B$14:$B$100,A{FIRST + i},$G$14:$G$100,"Cumplido")',
                     f'=IF(G{FIRST + i}=0,"",H{FIRST + i}/G{FIRST + i})'] for i, m in enumerate(M)]
    tabla(ws, c1, f1, filtro=False)
    ws.cell(12, 1, "Compromisos de misión").font = f(True, AZUL, 12)
    c2 = [dict(h="ID", w=8), dict(h="Misión", w=22), dict(h="Compromiso", w=46, wrap=True), dict(h="Responsable", w=34),
          dict(h="Fecha límite", w=11, fmt=FECHA), dict(h="Fecha de cumplimiento", w=13, fmt=FECHA), dict(h="Estado", w=12),
          dict(h="Días de atraso", w=11, fmt="0", tipo="calc"), dict(h="Cumplido en plazo", w=11, tipo="calc")]
    C = [("M-01", "Presentar el Plan de Adquisiciones a 18 meses para No Objeción", R_ADQ, date(2027, 2, 28), date(2027, 2, 19), "Cumplido"),
         ("M-01", "Entregar la matriz de resultados con línea base provisional", R_PLAN, date(2027, 3, 31), date(2027, 3, 30), "Cumplido"),
         ("M-01", "Abrir la cuenta bancaria exclusiva del Programa", R_FIN, date(2027, 2, 5), date(2027, 2, 4), "Cumplido"),
         ("M-01", "Aprobar el manual de procedimientos fiduciarios internos", R_FIN, date(2027, 4, 15), date(2027, 4, 22), "Cumplido"),
         ("M-01", "Presentar el marco de gestión ambiental y social", R_SOC, date(2027, 4, 30), date(2027, 4, 28), "Cumplido"),
         ("M-02", "Subsanar observaciones al expediente de adquisición PA-02", R_ADQ, date(2027, 6, 15), date(2027, 6, 12), "Cumplido"),
         ("M-02", "Actualizar PEP y POA con la reprogramación del sistema de información", R_PLAN, date(2027, 6, 30), None, "En proceso"),
         ("M-02", "Justificar el umbral de anticipos antes de un nuevo pedido", R_FIN, date(2027, 7, 15), None, "En proceso"),
         ("M-02", "Informar plan de mitigación del retraso en C4-03 y C4-04", R_CG, date(2027, 6, 20), None, "Pendiente"),
         ("M-02", "Enviar el informe de línea base de indicadores", R_PLAN, date(2027, 6, 15), None, "En proceso")]
    f2 = []
    for i, (m, c, r, fl, fc, es) in enumerate(C):
        n = 14 + i
        f2.append([f"CM-{i + 1:02d}", m, c, r, fl, fc, es,
                   f'=IF(G{n}="Cumplido",MAX(0,F{n}-E{n}),MAX(0,Fecha_Corte-E{n}))',
                   f'=IF(G{n}="Cumplido",IF(F{n}<=E{n},"Sí","No"),"")'])
    tabla(ws, c2, f2, hdr=13, filtro=False)
    ws.freeze_panes = "A5"
    lista(ws, "G14:G100", "=" + REF["Estado_compromiso"])
    lista(ws, "D14:D100", "=" + REF["Responsable"])
    for col, w in (("A", 8), ("B", 22), ("C", 46), ("D", 34), ("E", 13), ("F", 46), ("G", 12), ("H", 11), ("I", 11)):
        ws.column_dimensions[col].width = w
    return len(f1), len(f2)


def hoja_no_objeciones(wb):
    ws = wb.create_sheet("A3_No_Objeciones")
    titulo(ws, "A3 · Registro de No Objeciones y solicitudes al BID",
           "La UGP es el canal ordinario con el BID. El plazo de referencia (Parametros: Plazo_NO) es interno, no un plazo del BID.")
    cols = [dict(h="ID", w=8), dict(h="Asunto", w=52, wrap=True), dict(h="Tipo", w=24), dict(h="Fecha de solicitud", w=12, fmt=FECHA),
            dict(h="Fecha de respuesta", w=12, fmt=FECHA), dict(h="Estado", w=16), dict(h="Responsable", w=24),
            dict(h="Días de trámite", w=10, fmt="0", tipo="calc"), dict(h="Plazo de referencia", w=26, tipo="calc"),
            dict(h="Observaciones", w=38, wrap=True)]
    D = date
    NO = [("Plan de Adquisiciones inicial", "Plan de Adquisiciones", D(2027, 1, 20), D(2027, 1, 27), "Otorgada", R_ADQ, ""),
          ("TdR y selección de especialistas de la UGP (3CV)", "TdR / pliegos", D(2026, 12, 2), D(2026, 12, 9), "Otorgada", R_ADQ, ""),
          ("Pliego SBCC: consultoría del modelo de captación (PA-01)", "TdR / pliegos", D(2027, 1, 28), D(2027, 2, 1), "Otorgada", R_ADQ, ""),
          ("Evaluación y adjudicación CT-01", "Evaluación y adjudicación", D(2027, 3, 1), D(2027, 3, 8), "Otorgada", R_ADQ, ""),
          ("Pliego LPN: plataforma de registro (PA-02)", "TdR / pliegos", D(2027, 2, 12), D(2027, 2, 19), "Otorgada", R_ADQ, ""),
          ("Evaluación y adjudicación CT-02", "Evaluación y adjudicación", D(2027, 4, 12), D(2027, 4, 25), "Otorgada", R_ADQ, ""),
          ("Modificación del MOP: anexo de criterios de elegibilidad", "MOP", D(2027, 3, 15), D(2027, 4, 12), "Con observaciones", R_CG, "El BID pidió precisar criterios de personas con discapacidad; respuesta en preparación"),
          ("Pliego LPI: sistema de información de trayectorias (PA-10)", "TdR / pliegos", D(2027, 3, 1), D(2027, 3, 5), "Otorgada", R_ADQ, ""),
          ("Evaluación y adjudicación CT-09", "Evaluación y adjudicación", D(2027, 5, 10), D(2027, 5, 26), "Otorgada", R_ADQ, ""),
          ("Pliego LPI: equipamiento tecnológico (PA-11)", "TdR / pliegos", D(2027, 5, 12), D(2027, 5, 28), "Otorgada", R_ADQ, ""),
          ("Pliego LPN: equipamiento de accesibilidad (PA-06)", "TdR / pliegos", D(2027, 5, 25), D(2027, 5, 31), "Otorgada", R_ADQ, ""),
          ("TdR y SBCC: capacitación a instituciones (PA-12)", "TdR / pliegos", D(2027, 6, 10), None, "Pendiente", R_ADQ, "Esperando respuesta"),
          ("Reasignación entre categorías de inversión (ajuste del POA)", "Reasignación presupuestaria", D(2027, 6, 22), None, "Pendiente", R_FIN, "")]
    filas = []
    for i, (a, t, fs, fr, es, rs, ob) in enumerate(NO):
        n = FIRST + i
        filas.append([f"NO-{i + 1:02d}", a, t, fs, fr, es, rs, f'=IF(E{n}<>"",E{n}-D{n},Fecha_Corte-D{n})',
                      f'=IF(F{n}="Pendiente",IF(H{n}>Plazo_NO,"Pendiente fuera de referencia","Pendiente dentro de referencia"),'
                      f'IF(H{n}>Plazo_NO,"Respondida fuera de referencia","Respondida en referencia"))', ob])
    tabla(ws, cols, filas, altura=40)
    lista(ws, f"C{FIRST}:C200", TIPOS_NO)
    lista(ws, f"F{FIRST}:F200", "=" + REF["Estado_NO"])
    lista(ws, f"G{FIRST}:G200", "=" + REF["Responsable"])
    semaforo(ws, f"I{FIRST}:I200", "Respondida en referencia", "Pendiente dentro de referencia", "Pendiente fuera de referencia")
    semaforo(ws, f"I{FIRST}:I200", None, "Respondida fuera de referencia", None)
    return len(filas)


def hoja_calendario(wb):
    ws = wb.create_sheet("A5_Calendario_Informes")
    titulo(ws, "A5 · Calendario de productos de la consultoría (P1-P12) y habilitación de pagos",
           "TDR §VII y §XIII: informes mensuales a 3 días hábiles del cierre; el pago de US$4,200 se libera con la aprobación formal del informe.")
    cols = [dict(h="Código", w=8, tipo="lbl"), dict(h="Producto", w=44, tipo="lbl"), dict(h="Periodicidad", w=44, tipo="lbl", wrap=True),
            dict(h="Fecha límite", w=13, fmt=FECHA, tipo="calc"), dict(h="Fecha de entrega", w=13, fmt=FECHA),
            dict(h="Estado de entrega", w=22, tipo="calc"), dict(h="Conformidad", w=17), dict(h="Honorario USD", w=13, fmt=USD, tipo="calc"),
            dict(h="Pago habilitado", w=11, tipo="calc"), dict(h="Desvío (días)", w=10, fmt="0", tipo="calc")]
    ent = {1: date(2027, 1, 29), 2: date(2027, 3, 3), 3: date(2027, 4, 6), 4: date(2027, 5, 5), 5: date(2027, 6, 2)}
    filas = []
    for k in range(1, 13):
        n = FIRST + k - 1
        if k == 1:
            prod, per, lim = "Plan de trabajo inicial e informe mensual de gestión", "Al final del primer mes de la contratación", "=EOMONTH(Inicio_Consultoria,0)"
        elif k <= 11:
            prod, per = "Informe mensual de gestión", "Mensual / tres días hábiles posteriores al cierre del mes a reportar"
            lim = f"=WORKDAY(EOMONTH(Inicio_Consultoria,{k - 1}),Plazo_Informe)"
        else:
            prod, per, lim = "Informe anual", "Diez días previos al cierre del año", "=DATE(YEAR(Inicio_Consultoria),12,31)-10"
        filas.append([f"P{k}", prod, per, lim, ent.get(k), f'=IF(E{n}<>"",IF(E{n}<=D{n},"Entregado a tiempo","Entregado con retraso"),IF(D{n}<Fecha_Corte,"Vencido","Programado"))',
                      "Conforme" if k in ent else "Pendiente", "=Pago_Mensual", f'=IF(G{n}="Conforme","Sí","No")',
                      f'=IF(E{n}<>"",E{n}-D{n},"")'])
    tabla(ws, cols, filas, filtro=False)
    lista(ws, f"G{FIRST}:G{FIRST + 11}", "=" + REF["Conformidad"])
    semaforo(ws, f"F{FIRST}:F{FIRST + 11}", "Entregado a tiempo", "Entregado con retraso", "Vencido")
    nota(ws, FIRST + 13, "Los feriados no se descuentan en WORKDAY; si el MOP o el contrato los excluyen, agregue la lista de feriados como tercer argumento.")
    return 12
