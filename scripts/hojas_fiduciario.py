"""Pilar 2 — Gestión fiduciaria: F1..F6."""
from datetime import date, timedelta
from xl_base import *
from hojas_base import REF
from datos_demo import *  # noqa: F401,F403
import datos_calculados as dc

LAST = 500
FUNC_POA = lambda col: rng("P1_POA", col, 200)   # noqa: E731


def hoja_ejecucion(wb):
    ws = wb.create_sheet("F2_Ejecucion")
    titulo(ws, "F2 · Libro de ejecución de gastos (devengado)",
           "Fuente única de la ejecución: alimenta presupuesto, POA, contratos, anticipos, focalización y tablero. "
           "Para agregar un gasto copie la última fila (incluida la columna de chequeo).")
    cols = [dict(h="ID gasto", w=10), dict(h="Fecha", w=12, fmt=FECHA), dict(h="Comp.", w=8),
            dict(h="Actividad POA", w=12), dict(h="Contrato", w=10), dict(h="Departamento", w=16),
            dict(h="Concepto", w=46), dict(h="Categoría", w=26), dict(h="Fuente", w=11),
            dict(h="Monto USD", w=14, fmt=USD), dict(h="Estado de pago", w=12),
            dict(h="Mecanismo", w=19), dict(h="Justificado al BID", w=12),
            dict(h="Chequeo comp.", w=11, tipo="calc", fmt="0")]
    filas = []
    for i, r in enumerate(dc.libro_gastos()):
        n = FIRST + i
        chq = f'=IF(D{n}="","",IF(INDEX({FUNC_POA("B")},MATCH(D{n},{FUNC_POA("A")},0))=C{n},0,1))'
        filas.append([r["id"], r["fecha"], r["comp"], r["act"], r["contrato"] or None, r["depto"],
                      r["concepto"], r["categoria"], r["fuente"], r["monto"], r["estado"],
                      r["mecanismo"], r["justificado"], chq])
    tabla(ws, cols, filas)
    for col, lst in (("C", "Componente"), ("F", "Departamento"), ("H", "Categoria_gasto"), ("I", "Fuente"),
                     ("K", "Estado_pago"), ("L", "Mecanismo"), ("M", "Justificado")):
        lista(ws, f"{col}{FIRST}:{col}{LAST}", "=" + REF[lst])
    return len(filas)


def hoja_presupuesto(wb):
    ws = wb.create_sheet("F1_Presupuesto_PEP")
    titulo(ws, "F1 · Presupuesto y Plan de Ejecución Plurianual (PEP) por componente",
           "Estructura de componentes ILUSTRATIVA. Año 1 = suma del POA (fórmula); años 2-5 son el plan plurianual (editable).")
    cols = [dict(h="Comp.", w=8, tipo="lbl"), dict(h="Componente", w=36, tipo="lbl"),
            dict(h="Préstamo 6153/OC-ES", w=16, fmt=USD), dict(h="Donación 6154/GR-ES", w=16, fmt=USD),
            dict(h="Total asignado", w=16, fmt=USD, tipo="calc"), dict(h="% del total", w=9, fmt=PCT, tipo="calc")]
    cols += [dict(h=f"PEP Año {k}", w=14, fmt=USD, tipo="calc" if k == 1 else "in") for k in range(1, 6)]
    cols += [dict(h="Total PEP", w=16, fmt=USD, tipo="calc"), dict(h="PEP = Asignado", w=10, tipo="calc"),
             dict(h="Ejecutado acumulado", w=16, fmt=USD, tipo="calc"), dict(h="% ejecución s/ total", w=11, fmt=PCT, tipo="calc"),
             dict(h="% ejecución s/ PEP año vigente", w=13, fmt=PCT, tipo="calc"),
             dict(h="Saldo por ejecutar", w=16, fmt=USD, tipo="calc")]
    pep = dc.pep()
    filas = []
    for i, (cod, nom, pre, don) in enumerate(COMPONENTES):
        n = FIRST + i
        y = pep[cod]
        filas.append([cod, nom, pre, don, f"=C{n}+D{n}", f"=E{n}/$E${FIRST + 5}",
                      f'=SUMIFS({FUNC_POA("G")},{FUNC_POA("B")},A{n})', y[1], y[2], y[3], y[4],
                      f"=SUM(G{n}:K{n})", f'=IF(ROUND(L{n}-E{n},0)=0,"OK","REVISAR")',
                      f'=SUMIFS({rng("F2_Ejecucion", "J", LAST)},{rng("F2_Ejecucion", "C", LAST)},A{n})',
                      f"=N{n}/E{n}", f"=N{n}/INDEX(G{n}:K{n},Anio_Programa)", f"=E{n}-N{n}"])
    tabla(ws, cols, filas, filtro=False, altura=44)
    t = FIRST + 5
    ws.cell(t, 1, "TOTAL")
    ws.cell(t, 2, "Programa")
    for j in (3, 4, 5, 7, 8, 9, 10, 11, 12, 14, 17):
        ws.cell(t, j, f"=SUM({L(j)}{FIRST}:{L(j)}{t - 1})")
    ws.cell(t, 6, f"=E{t}/E{t}")
    ws.cell(t, 13, f'=IF(AND(ROUND(E{t}-Total_Programa,0)=0,ROUND(C{t}-Total_Prestamo,0)=0,ROUND(D{t}-Total_Donacion,0)=0),"OK","REVISAR")')
    ws.cell(t, 15, f"=N{t}/E{t}")
    ws.cell(t, 16, f"=N{t}/INDEX(G{t}:K{t},Anio_Programa)")
    for j in range(1, len(cols) + 1):
        c = ws.cell(t, j)
        c.font, c.fill, c.border = f(True), C_SUB, BORDE
        c.number_format = cols[j - 1].get("fmt", "General")
    semaforo(ws, f"M{FIRST}:M{t}", "OK", None, "REVISAR")
    # ejecución por fuente
    r0 = t + 3
    ws.cell(r0 - 1, 1, "Ejecución por fuente de financiamiento").font = f(True, AZUL, 12)
    for j, h in enumerate(["Fuente", "", "Asignado", "Ejecutado", "% ejecución", "Saldo"], 1):
        c = ws.cell(r0, j, h)
        c.font, c.fill, c.border = f(True, "FFFFFF"), C_ENCAB, BORDE
    for k, (fte, asig) in enumerate((("Préstamo", "Total_Prestamo"), ("Donación", "Total_Donacion"))):
        r = r0 + 1 + k
        ws.cell(r, 1, fte)
        ws.cell(r, 3, f"={asig}").number_format = USD
        ws.cell(r, 4, f'=SUMIFS({rng("F2_Ejecucion", "J", LAST)},{rng("F2_Ejecucion", "I", LAST)},A{r})').number_format = USD
        ws.cell(r, 5, f"=IF(C{r}=0,0,D{r}/C{r})").number_format = PCT
        ws.cell(r, 6, f"=C{r}-D{r}").number_format = USD
        for j in range(1, 7):
            ws.cell(r, j).font, ws.cell(r, j).border = f(), BORDE
    nota(ws, r0 + 4, "Año vigente del programa y fecha de corte: ver hoja Parametros. Los años 2-5 se actualizan en cada revisión del PEP (con No Objeción del BID si hay reasignaciones).")
    return t


def hoja_desembolsos(wb, ledger_rows):
    ws = wb.create_sheet("F3_Desembolsos")
    titulo(ws, "F3 · Solicitudes de desembolso y control de anticipos",
           "Mecanismos: anticipo de fondos, reembolso de gastos y pago directo a proveedores. Bloque derecho = control del anticipo.")
    cols = [dict(h="ID solicitud", w=11), dict(h="Fecha solicitud", w=13, fmt=FECHA), dict(h="Mecanismo", w=19),
            dict(h="Fuente", w=11), dict(h="Monto solicitado", w=15, fmt=USD), dict(h="Estado", w=16),
            dict(h="Fecha desembolso", w=13, fmt=FECHA), dict(h="Monto desembolsado", w=15, fmt=USD),
            dict(h="Días de trámite", w=10, tipo="calc", fmt="0")]
    filas = [["DS-01", date(2027, 1, 28), "Anticipo de fondos", "Préstamo", 2_400_000, "Desembolsado", date(2027, 2, 10), 2_400_000]]
    directos = {}
    for r in ledger_rows:
        if r["mecanismo"] == "Pago directo" and r["estado"] == "Pagado":
            d = directos.setdefault(r["contrato"], [r["fecha"], 0])
            d[1] += r["monto"]
    for k, (ct, (f0, m)) in enumerate(sorted(directos.items()), 2):
        filas.append([f"DS-{k:02d}", f0 - timedelta(days=9), "Pago directo", "Préstamo", m, "Desembolsado", f0, m])
    filas.append([f"DS-{len(filas) + 1:02d}", None, "Anticipo de fondos", "Préstamo", 1_800_000, "En preparación", None, None])
    for i, fila in enumerate(filas):
        n = FIRST + i
        fila.append(f'=IF(G{n}<>"",G{n}-B{n},IF(AND(B{n}<>"",F{n}="Solicitado"),Fecha_Corte-B{n},""))')
    tabla(ws, cols, filas)
    for col, lst in (("C", "Mecanismo"), ("D", "Fuente")):
        lista(ws, f"{col}{FIRST}:{col}{LAST}", "=" + REF[lst])
    lista(ws, f"F{FIRST}:F{LAST}", '"En preparación,Solicitado,Desembolsado"')
    E = lambda c: rng("F2_Ejecucion", c, LAST)   # noqa: E731
    ws.column_dimensions["J"].width = 3
    ws.column_dimensions["K"].width = 52
    ws.column_dimensions["L"].width = 46
    kp = [
        ("Anticipos desembolsados (USD)", f'=SUMIFS($H${FIRST}:$H${LAST},$C${FIRST}:$C${LAST},"Anticipo de fondos",$F${FIRST}:$F${LAST},"Desembolsado")', USD),
        ("Gasto pagado con anticipo (USD)", f'=SUMIFS({E("J")},{E("L")},"Anticipo de fondos",{E("K")},"Pagado")', USD),
        ("Gasto justificado ante el BID (USD)", f'=SUMIFS({E("J")},{E("M")},"Sí")', USD),
        ("% justificado sobre anticipos", '=IF(L5=0,"n/a",L7/L5)', PCT),
        ("Saldo de anticipo por justificar (USD)", "=L5-L7", USD),
        ("Fondos disponibles de anticipo (USD)", "=L5-L6", USD),
        ("Pagos directos desembolsados (USD)", f'=SUMIFS($H${FIRST}:$H${LAST},$C${FIRST}:$C${LAST},"Pago directo",$F${FIRST}:$F${LAST},"Desembolsado")', USD),
        ("Pagos directos registrados en el libro (USD)", f'=SUMIFS({E("J")},{E("L")},"Pago directo",{E("K")},"Pagado")', USD),
        ("Total desembolsado por el BID (USD)", "=L5+L11", USD),
        ("Desembolsado / total del Programa", "=L13/Total_Programa", PCT),
        ("Alerta para solicitar nuevo anticipo", '=IF(L8="n/a","",IF(L8>=Pct_Justif_Min,"Puede solicitar nuevo anticipo","NO solicitar: justificar al "&ROUND(Pct_Justif_Min*100,0)&"% (faltan US$ "&ROUND(Pct_Justif_Min*L5-L7,0)&")"))', "General"),
    ]
    c = ws.cell(HDR, 11, "Control de anticipos")
    c.font, c.fill, c.border = f(True, "FFFFFF"), C_ENCAB, BORDE
    c2 = ws.cell(HDR, 12, "Valor")
    c2.font, c2.fill, c2.border = f(True, "FFFFFF"), C_ENCAB, BORDE
    for i, (lab, fm, nf) in enumerate(kp):
        r = FIRST + i
        ws.cell(r, 11, lab).font = f()
        v = ws.cell(r, 12, fm)
        v.font, v.fill, v.number_format = f(True), C_CALC, nf
        v.alignment = Alignment(wrap_text=True, horizontal="right")
        ws.cell(r, 11).border = v.border = BORDE
    ws.row_dimensions[FIRST + 10].height = 48
    nota(ws, FIRST + len(kp) + 1, "El umbral de justificación (Pct_Justif_Min) es un parámetro a validar con el Contrato de Préstamo.", 11)
    return len(filas)


def hoja_plan_financiero(wb):
    ws = wb.create_sheet("F3_Plan_Financiero")
    titulo(ws, "F3 · Plan financiero trimestral (proyectado vs. real)",
           "Proyección de gasto por trimestre (base para calcular anticipos). Real = suma del libro de gastos en el trimestre.")
    cols = [dict(h="Trimestre", w=12, tipo="lbl"), dict(h="Inicio", w=12, fmt=FECHA, tipo="lbl"), dict(h="Fin", w=12, fmt=FECHA, tipo="lbl"),
            dict(h="Proyectado USD", w=16, fmt=USD), dict(h="Real USD", w=16, fmt=USD, tipo="calc"),
            dict(h="Proyectado acumulado", w=18, fmt=USD, tipo="calc"), dict(h="Real acumulado", w=16, fmt=USD, tipo="calc"),
            dict(h="Variación acumulada", w=16, fmt=USD, tipo="calc"), dict(h="Cumplimiento acumulado", w=14, fmt=PCT, tipo="calc")]
    pep = dc.pep()
    y1 = sum(v[0] for v in pep.values())
    y2 = sum(v[1] for v in pep.values())
    w1, w2 = [0.12, 0.30, 0.28, 0.30], [0.22, 0.25, 0.26, 0.27]
    proy = [round(y1 * w, -4) for w in w1] + [round(y2 * w, -4) for w in w2]
    ini = [date(2027, 1, 1), date(2027, 4, 1), date(2027, 7, 1), date(2027, 10, 1),
           date(2028, 1, 1), date(2028, 4, 1), date(2028, 7, 1), date(2028, 10, 1)]
    fin = [date(2027, 3, 31), date(2027, 6, 30), date(2027, 9, 30), date(2027, 12, 31),
           date(2028, 3, 31), date(2028, 6, 30), date(2028, 9, 30), date(2028, 12, 31)]
    E = lambda c: rng("F2_Ejecucion", c, LAST)   # noqa: E731
    filas = []
    for i in range(8):
        n = FIRST + i
        filas.append([f"{ini[i].year}-T{(ini[i].month - 1) // 3 + 1}", ini[i], fin[i], proy[i],
                      f'=SUMIFS({E("J")},{E("B")},">="&B{n},{E("B")},"<="&C{n})',
                      f"=SUM($D${FIRST}:D{n})", f'=IF(B{n}>Fecha_Corte,"",SUM($E${FIRST}:E{n}))',
                      f'=IF(G{n}="","",G{n}-F{n})', f'=IF(G{n}="","",G{n}/F{n})'])
    tabla(ws, cols, filas, filtro=False)
    nota(ws, FIRST + 9, "La proyección del año 1 suma el POA vigente; la del año 2 suma el PEP. Se revisa cada trimestre y sustenta la solicitud de anticipos.")
    return 8


def hoja_adquisiciones(wb):
    ws = wb.create_sheet("F4_Plan_Adquisiciones")
    titulo(ws, "F4 · Plan de Adquisiciones (PA) y seguimiento de procesos",
           "Métodos según políticas GN-2349-15 (bienes, obras y servicios de no consultoría) y GN-2350-15 (consultorías). "
           "Los montos umbral de cada método están en el PA aprobado por el BID (no se reproducen aquí).")
    cols = [dict(h="ID PA", w=8), dict(h="Comp.", w=7), dict(h="Actividad POA", w=11), dict(h="Descripción", w=44, wrap=True),
            dict(h="Categoría", w=24), dict(h="Método", w=18), dict(h="Revisión", w=10), dict(h="Monto estimado", w=14, fmt=USD),
            dict(h="Estado del proceso", w=14), dict(h="Publicación prevista", w=13, fmt=FECHA), dict(h="Publicación real", w=13, fmt=FECHA),
            dict(h="Adjudicación prevista", w=13, fmt=FECHA), dict(h="Adjudicación real", w=13, fmt=FECHA),
            dict(h="Desvío adjudicación (días)", w=12, tipo="calc", fmt="0"), dict(h="Monto contratado", w=14, tipo="calc", fmt=USD),
            dict(h="Alerta", w=24, tipo="calc")]
    filas = []
    for i, p in enumerate(PA):
        n = FIRST + i
        filas.append(list(p[:8]) + [p[8], p[9], p[10], p[11], p[12]] + [
            f'=IF(M{n}<>"",M{n}-L{n},IF(L{n}<>"",MAX(0,Fecha_Corte-L{n}),""))',
            f'=SUMIFS({rng("F5_Contratos", "G", 200)},{rng("F5_Contratos", "B", 200)},A{n})',
            f'=IF(OR(I{n}="Contratado",I{n}="Cerrado"),IF(N{n}>0,"Contratado con atraso","Contratado a tiempo"),'
            f'IF(AND(K{n}="",J{n}<>"",Fecha_Corte>J{n}),"Atrasado",IF(L{n}="","Sin fecha prevista",IF(Fecha_Corte>L{n},"Atrasado",IF(L{n}-Fecha_Corte<=Dias_Alerta,"Próximo a vencer","En plazo")))))'])
    tabla(ws, cols, filas, altura=44)
    for col, lst in (("B", "Componente"), ("E", "Categoria_adq"), ("F", "Metodo_adq"), ("G", "Revision"), ("I", "Estado_adq")):
        lista(ws, f"{col}{FIRST}:{col}{LAST}", "=" + REF[lst])
    semaforo(ws, f"P{FIRST}:P{LAST}", "Contratado a tiempo", "Próximo a vencer", "Atrasado")
    semaforo(ws, f"P{FIRST}:P{LAST}", None, "Contratado con atraso", None)
    return len(filas)


def hoja_contratos(wb):
    ws = wb.create_sheet("F5_Contratos")
    titulo(ws, "F5 · Registro y seguimiento de contratos",
           "Pagado = suma del libro de gastos por contrato. El saldo y el chequeo detectan pagos que excedan el monto contratado.")
    cols = [dict(h="ID contrato", w=10), dict(h="ID PA", w=8), dict(h="Actividad POA", w=11),
            dict(h="Comp.", w=7, tipo="calc"), dict(h="Proveedor / consultor", w=32), dict(h="Objeto", w=38, wrap=True),
            dict(h="Monto contrato", w=14, fmt=USD), dict(h="Fecha firma", w=12, fmt=FECHA), dict(h="Fin de vigencia", w=12, fmt=FECHA),
            dict(h="Mecanismo de pago", w=19), dict(h="Pagado (USD)", w=14, tipo="calc", fmt=USD),
            dict(h="Saldo (USD)", w=14, tipo="calc", fmt=USD), dict(h="% pagado", w=9, tipo="calc", fmt=PCT),
            dict(h="Vigencia", w=12, tipo="calc"), dict(h="Responsable de supervisión", w=24, tipo="calc"),
            dict(h="Chequeo pago ≤ contrato", w=11, tipo="calc", fmt="0")]
    filas = []
    for i, c in enumerate(CONTRATOS):
        n = FIRST + i
        filas.append([c[0], c[1], c[2], f'=INDEX({FUNC_POA("B")},MATCH(C{n},{FUNC_POA("A")},0))', c[3], c[4], c[5], c[6], c[7], c[9],
                      f'=SUMIFS({rng("F2_Ejecucion", "J", LAST)},{rng("F2_Ejecucion", "E", LAST)},A{n})',
                      f"=G{n}-K{n}", f"=K{n}/G{n}",
                      f'=IF(I{n}<Fecha_Corte,"Vencido",IF(I{n}-Fecha_Corte<=Dias_Alerta,"Por vencer","Vigente"))',
                      f'=INDEX({FUNC_POA("D")},MATCH(C{n},{FUNC_POA("A")},0))', f"=IF(K{n}>G{n},1,0)"])
    tabla(ws, cols, filas, altura=44)
    lista(ws, f"J{FIRST}:J{LAST}", "=" + REF["Mecanismo"])
    semaforo(ws, f"N{FIRST}:N{LAST}", "Vigente", "Por vencer", "Vencido")
    return len(filas)


def hoja_auditorias(wb):
    ws = wb.create_sheet("F6_Auditoria")
    titulo(ws, "F6 · Plan de auditorías y seguimiento de recomendaciones",
           "Tabla 1 (fila 4): plan de auditoría y revisiones. Tabla 2 (fila 12): recomendaciones y hallazgos.")
    c1 = [dict(h="ID", w=9), dict(h="Tipo de auditoría / revisión", w=44, wrap=True), dict(h="Período", w=18),
          dict(h="Responsable externo/interno", w=40, wrap=True), dict(h="Cierre del período", w=13, fmt=FECHA),
          dict(h="Fecha límite de entrega", w=13, fmt=FECHA), dict(h="Estado", w=15),
          dict(h="Días al vencimiento", w=11, tipo="calc", fmt="0"), dict(h="Alerta", w=18, tipo="calc"),
          dict(h="Recomendaciones", w=12, tipo="calc", fmt="0"), dict(h="Cerradas", w=9, tipo="calc", fmt="0"),
          dict(h="% cierre", w=9, tipo="calc", fmt=PCT)]
    A = [("AU-01", "Estados financieros auditados del Programa", "Ejercicio 2027", "Firma auditora externa (por contratar, PA-18)", date(2027, 12, 31), None, "Planificada"),
         ("AU-02", "Revisión ex post de adquisiciones (expedientes)", "Ejercicio 2027", "Revisión BID con expedientes preparados por la UGP", date(2027, 11, 30), date(2027, 12, 15), "Planificada"),
         ("AU-03", "Auditoría interna: transferencias a beneficiarios (muestra)", "Semestre 1-2027", "Unidad de Auditoría Interna de la DI (supuesto)", date(2027, 6, 30), date(2027, 7, 31), "En ejecución"),
         ("AU-04", "Evaluación inicial de control interno de la UGP", "Arranque 2027", "Unidad de Auditoría Interna de la DI (supuesto)", date(2027, 3, 31), date(2027, 4, 30), "Informe emitido")]
    f1 = []
    for i, a in enumerate(A):
        n = FIRST + i
        lim = "=E5+Plazo_EEFF" if a[5] is None else a[5]
        f1.append([a[0], a[1], a[2], a[3], a[4], lim, a[6],
                   f'=IF(G{n}="Cerrada","",F{n}-Fecha_Corte)',
                   f'=IF(G{n}="Cerrada","Cerrada",IF(F{n}<Fecha_Corte,"Vencida",IF(F{n}-Fecha_Corte<=Dias_dummy,"Próxima","En plazo")))'.replace("Dias_dummy", "Dias_Alerta"),
                   f'=COUNTIFS($B$14:$B$100,A{n})', f'=COUNTIFS($B$14:$B$100,A{n},$H$14:$H$100,"Cerrada")',
                   f'=IF(J{n}=0,"",K{n}/J{n})'])
    tabla(ws, c1, f1, filtro=False)
    lista(ws, f"G{FIRST}:G{FIRST + 20}", "=" + REF["Estado_audit"])
    semaforo(ws, f"I{FIRST}:I{FIRST + 20}", "En plazo", "Próxima", "Vencida")
    # tabla 2
    h2 = 13
    ws.cell(h2 - 1, 1, "Recomendaciones y hallazgos").font = f(True, AZUL, 12)
    c2 = [dict(h="ID rec.", w=9), dict(h="ID auditoría", w=11), dict(h="Recomendación / hallazgo", w=50, wrap=True),
          dict(h="Riesgo", w=9), dict(h="Responsable", w=22), dict(h="Fecha compromiso", w=13, fmt=FECHA),
          dict(h="Fecha de cierre", w=13, fmt=FECHA), dict(h="Estado", w=12), dict(h="Días vencida", w=10, tipo="calc", fmt="0")]
    R = [("RA-01", "AU-04", "Formalizar el manual de funciones de los especialistas de la UGP", "Medio", R_CG, date(2027, 5, 15), date(2027, 5, 10), "Cerrada"),
         ("RA-02", "AU-04", "Implementar lista de verificación de expediente por contrato", "Medio", R_ADQ, date(2027, 5, 31), date(2027, 5, 28), "Cerrada"),
         ("RA-03", "AU-04", "Segregar el registro y la aprobación de pagos", "Alto", R_FIN, date(2027, 5, 15), date(2027, 5, 14), "Cerrada"),
         ("RA-04", "AU-04", "Documentar la conciliación bancaria mensual de la cuenta del Programa", "Medio", R_FIN, date(2027, 6, 15), None, "En proceso"),
         ("RA-05", "AU-03", "Completar expedientes de beneficiarios con la documentación de elegibilidad (preliminar)", "Alto", R_SOC, date(2027, 7, 15), None, "Abierta")]
    f2 = []
    for i, r in enumerate(R):
        n = h2 + 1 + i
        f2.append(list(r) + [f'=IF(H{n}="Cerrada",0,MAX(0,Fecha_Corte-F{n}))'])
    # la tabla 2 comienza en la fila 14; cabecera en 13 (el filtro/freeze ya lo fijó la tabla 1)
    ws.freeze_panes = "A5"
    tabla(ws, c2, f2, hdr=h2, filtro=False)
    ws.freeze_panes = "A5"
    lista(ws, "H14:H100", "=" + REF["Estado_hallazgo"])
    lista(ws, "D14:D100", '"Alto,Medio,Bajo"')
    # ancho de columnas compartido entre las dos tablas
    for col, w in (("A", 9), ("B", 44), ("C", 50), ("D", 40), ("E", 22), ("F", 15), ("G", 15), ("H", 13), ("I", 18)):
        ws.column_dimensions[col].width = w
    return len(f1), len(f2)
