"""P1_Resultados, Controles, Tablero y LEEME."""
from openpyxl.chart import BarChart, Reference, Series
from openpyxl.chart.label import DataLabelList
from xl_base import *
from hojas_base import REF
from datos_demo import *  # noqa: F401,F403

R_ = lambda sh, c, u=500, p=FIRST: rng(sh, c, u, p)   # noqa: E731


def hoja_resultados(wb):
    ws = wb.create_sheet("P1_Resultados")
    titulo(ws, "P1 · Matriz de resultados e indicadores (marco lógico ilustrativo)",
           "Meta esperada al corte: acumulativa = interpolación lineal dentro del año · anual = meta × fracción del año · nivel = meta del año. "
           "Cumplimiento = valor actual / esperado. Los indicadores sin medición en el período quedan «Sin dato».")
    cols = [dict(h="ID", w=7), dict(h="Nivel", w=11), dict(h="Indicador", w=52, wrap=True), dict(h="Unidad", w=10), dict(h="Comp.", w=8),
            dict(h="Línea base", w=10), dict(h="Tipo de meta", w=13)] + [dict(h=f"Meta año {k}", w=10) for k in range(1, 6)] + [
        dict(h="Meta final", w=10, tipo="calc"), dict(h="Valor actual", w=11), dict(h="Esperado al corte", w=11, tipo="calc"),
        dict(h="Cumplimiento", w=11, fmt=PCT, tipo="calc"), dict(h="Semáforo", w=10, tipo="calc"),
        dict(h="Fuente de verificación", w=34, wrap=True), dict(h="Frecuencia", w=12), dict(h="Responsable", w=24)]
    PEP = "F1_Presupuesto_PEP"
    cum = lambda k: f"=SUM({PEP}!$G$10:{'GHIJK'[k - 1]}$10)/Total_Programa"   # noqa: E731
    FO = "P2_Focalizacion"
    I = [
        ("I-01", "Resultado", "Beneficiarios que continúan en educación postsecundaria al 2.º año", "%", "C2", 0.70, "Nivel", [0.70, 0.72, 0.76, 0.81, 0.85], None, "Sistema de información de trayectorias", "Anual", R_PLAN),
        ("I-02", "Resultado", "Beneficiarios que se gradúan en el tiempo previsto", "%", "C2", 0.40, "Nivel", [0.40, 0.42, 0.48, 0.54, 0.60], None, "Registros de las instituciones", "Anual", R_PLAN),
        ("I-03", "Resultado", "Personas graduadas vinculadas al empleo formal en 12 meses", "%", "C3", 0.25, "Nivel", [0.25, 0.25, 0.30, 0.38, 0.45], None, "Encuesta de seguimiento y registros de empleo", "Anual", R_PLAN),
        ("P-01", "Producto", "Estudiantes de educación media con orientación vocacional (acum.)", "personas", "C1", 0, "Acumulativa", [4000, 12000, 24000, 38000, 50000], 1650, "Registro de participantes", "Mensual", R_SOC),
        ("P-02", "Producto", "Jóvenes beneficiarios con apoyo y acompañamiento (acum.)", "personas", "C2", 0, "Acumulativa", [6000, 16000, 30000, 46000, 60000], f"={FO}!G19", "P2_Focalizacion", "Mensual", R_SOC),
        ("P-03", "Producto", "Madres jóvenes atendidas (acum.)", "personas", "C2", 0, "Acumulativa", [540, 1440, 2700, 4140, 5400], f"={FO}!H19", "P2_Focalizacion", "Mensual", R_SOC),
        ("P-04", "Producto", "Personas con discapacidad atendidas (acum.)", "personas", "C2", 0, "Acumulativa", [240, 640, 1200, 1840, 2400], f"={FO}!I19", "P2_Focalizacion", "Mensual", R_SOC),
        ("P-05", "Producto", "Personas retornadas atendidas (acum.)", "personas", "C2", 0, "Acumulativa", [180, 480, 900, 1380, 1800], f"={FO}!J19", "P2_Focalizacion", "Mensual", R_SOC),
        ("P-06", "Producto", "Convenios firmados con instituciones de educación postsecundaria (acum.)", "convenios", "C4", 0, "Acumulativa", [8, 20, 30, 36, 40], 6, "Convenios archivados", "Mensual", R_SOC),
        ("P-07", "Producto", "Empleadores aliados activos (acum.)", "empleadores", "C3", 0, "Acumulativa", [20, 60, 120, 180, 250], 7, "Alianzas firmadas", "Mensual", R_SOC),
        ("P-08", "Producto", "Instituciones con plan de fortalecimiento en implementación (acum.)", "instituciones", "C4", 0, "Acumulativa", [3, 12, 25, 35, 40], 0, "Informes de capacitación", "Trimestral", R_SOC),
        ("P-09", "Producto", "Sistema de información de trayectorias: módulos operativos", "%", "C4", 0, "Acumulativa", [0.80, 1, 1, 1, 1], 0.35, "Actas de recepción por módulo", "Mensual", R_PLAN),
        ("G-01", "Gestión", "Ejecución financiera acumulada del Programa (% del total)", "%", "Todos", 0, "Acumulativa", [cum(1), cum(2), cum(3), cum(4), cum(5)], f"={PEP}!O10", "F1_Presupuesto_PEP", "Mensual", R_FIN),
        ("G-02", "Gestión", "Avance físico ponderado del POA vigente", "%", "Todos", 0, "Anual", [1, 1, 1, 1, 1], "=P1_Avance_FF!F10", "P1_POA", "Mensual", R_PLAN),
        ("G-03", "Gestión", "Procesos del Plan de Adquisiciones con contrato firmado", "%", "Todos", 0, "Nivel", [0.90, 0.90, 0.90, 0.90, 0.90], f'=COUNTIF({R_("F4_Plan_Adquisiciones", "I", 200)},"Contratado")/COUNTIF({R_("F4_Plan_Adquisiciones", "A", 200)},"PA-*")', "F4_Plan_Adquisiciones", "Mensual", R_ADQ),
        ("G-04", "Gestión", "Informes mensuales entregados a tiempo", "%", "UGP", 1, "Nivel", [1, 1, 1, 1, 1], f'=COUNTIF({R_("A5_Calendario_Informes", "F", 30)},"Entregado a tiempo")/COUNTIF({R_("A5_Calendario_Informes", "F", 30)},"Entregado*")', "A5_Calendario_Informes", "Mensual", R_CG),
        ("G-05", "Gestión", "Compromisos con el BID cumplidos en plazo", "%", "UGP", 1, "Nivel", [1, 1, 1, 1, 1],
         f'=IFERROR(COUNTIF({rng("A2_Misiones_BID", "I", 100, 14)},"Sí")/(COUNTIF({rng("A2_Misiones_BID", "G", 100, 14)},"Cumplido")+COUNTIFS({rng("A2_Misiones_BID", "E", 100, 14)},"<"&Fecha_Corte,{rng("A2_Misiones_BID", "G", 100, 14)},"<>Cumplido",{rng("A2_Misiones_BID", "A", 100, 14)},"CM-*")),"")',
         "A2_Misiones_BID", "Por misión", R_CG),
        ("G-06", "Gestión", "Quejas atendidas dentro del plazo del mecanismo", "%", "C5", 0.90, "Nivel", [0.90, 0.90, 0.90, 0.90, 0.90], 0.88, "Registro del mecanismo de quejas", "Mensual", R_SOC),
    ]
    filas = []
    for i, (id_, niv, ind, uni, comp, base, tipo, metas, act, fuen, frec, resp) in enumerate(I):
        n = FIRST + i
        prev = f"IF(Anio_Programa=1,F{n},INDEX(H{n}:L{n},Anio_Programa-1))"
        esp = (f'=IF(G{n}="Nivel",INDEX(H{n}:L{n},Anio_Programa),IF(G{n}="Anual",INDEX(H{n}:L{n},Anio_Programa)*Frac_Anio,'
               f"{prev}+(INDEX(H{n}:L{n},Anio_Programa)-{prev})*Frac_Anio))")
        filas.append([id_, niv, ind, uni, comp, base, tipo] + metas + [
            f"=L{n}", act, esp, f'=IF(N{n}="","Sin dato",IF(O{n}=0,"n/a",N{n}/O{n}))',
            f'=IF(NOT(ISNUMBER(P{n})),"Sin dato",IF(P{n}>=Umbral_Verde,"Verde",IF(P{n}>=Umbral_Amarillo,"Amarillo","Rojo")))', fuen, frec, resp])
    tabla(ws, cols, filas, altura=44)
    for i, r in enumerate(I):
        fm = PCT if r[3] == "%" else "#,##0"
        for col in "FHIJKLMNO":
            ws[f"{col}{FIRST + i}"].number_format = fm
    lista(ws, f"G{FIRST}:G100", "=" + REF["Tipo_meta"])
    lista(ws, f"T{FIRST}:T100", "=" + REF["Responsable"])
    semaforo(ws, f"Q{FIRST}:Q100", "Verde", "Amarillo", "Rojo")
    return len(I)


CONTROLES = [
    ("Presupuesto por componentes = total del Programa (USD)", "=Total_Programa", "=F1_Presupuesto_PEP!E10"),
    ("Total préstamo asignado = monto del Contrato 6153/OC-ES", "=Total_Prestamo", "=F1_Presupuesto_PEP!C10"),
    ("Total donación asignada = monto del Convenio 6154/GR-ES", "=Total_Donacion", "=F1_Presupuesto_PEP!D10"),
    ("Componentes cuyo PEP a 5 años no coincide con lo asignado", 0, '=COUNTIF(F1_Presupuesto_PEP!M5:M9,"REVISAR")'),
    ("Plan financiero del año 1 = presupuesto POA (USD)", "=P1_Avance_FF!C10", "=SUM(F3_Plan_Financiero!D5:D8)"),
    ("Ejecución acumulada ≤ presupuesto total (USD)", "=F1_Presupuesto_PEP!E10", "=F1_Presupuesto_PEP!N10"),
    ("Actividades POA con ejecutado > presupuesto", 0, f'=SUMPRODUCT(--({R_("P1_POA", "J", 200)}>{R_("P1_POA", "G", 200)}))'),
    ("Contratos con pagos > monto contratado", 0, f'=SUM({R_("F5_Contratos", "P", 200)})'),
    ("Gastos cuyo componente no coincide con el de su actividad", 0, f'=SUM({R_("F2_Ejecucion", "N")})'),
    ("Gastos fuera del período [inicio, corte]", 0, f'=COUNTIFS({R_("F2_Ejecucion", "B")},"<"&Fecha_Inicio)+COUNTIFS({R_("F2_Ejecucion", "B")},">"&Fecha_Corte)'),
    ("Gastos con contrato inexistente en F5", 0, f'=SUMPRODUCT(({R_("F2_Ejecucion", "E")}<>"")*(COUNTIF({R_("F5_Contratos", "A", 200)},{R_("F2_Ejecucion", "E")})=0))'),
    ("Gastos con actividad inexistente en el POA", 0, f'=SUMPRODUCT(({R_("F2_Ejecucion", "D")}<>"")*(COUNTIF({R_("P1_POA", "A", 200)},{R_("F2_Ejecucion", "D")})=0))'),
    ("Pagos directos del libro = desembolsos por pago directo (USD)", "=F3_Desembolsos!L12", "=F3_Desembolsos!L11"),
    ("Meta nacional de beneficiarios = suma de departamentos", "=Meta_Benef_5A", "=P2_Focalizacion!E19"),
    ("Inversión territorializada ≤ ejecución total (USD)", "=F1_Presupuesto_PEP!N10", "=P2_Focalizacion!P19"),
    ("Procesos RACI sin una única «A»", 0, '=COUNTIF(A1_RACI!J5:J40,"REVISAR")'),
]


def hoja_controles(wb):
    ws = wb.create_sheet("Controles")
    titulo(ws, "Controles de integridad del sistema",
           "Pruebas automáticas de consistencia entre hojas. Cualquier «REVISAR» debe corregirse antes de emitir el informe mensual.")
    cols = [dict(h="N.º", w=6, tipo="lbl"), dict(h="Control", w=66, tipo="lbl", wrap=True), dict(h="Esperado", w=18, fmt="#,##0;[Red]-#,##0;0", tipo="calc"),
            dict(h="Calculado", w=18, fmt="#,##0;[Red]-#,##0;0", tipo="calc"), dict(h="Diferencia", w=14, fmt="#,##0;[Red]-#,##0;0", tipo="calc"),
            dict(h="Estado", w=12, tipo="calc")]
    filas = []
    for i, (c, esp, cal) in enumerate(CONTROLES):
        n = FIRST + i
        condic = f"D{n}<=C{n}" if "≤" in c else f"ROUND(E{n},0)=0"
        filas.append([i + 1, c, esp, cal, f"=D{n}-C{n}", f'=IF({condic},"OK","REVISAR")'])
    tabla(ws, cols, filas, filtro=False)
    last = FIRST + len(CONTROLES) - 1
    r = last + 2
    ws.cell(r, 2, "Resultado global").font = f(True)
    c = ws.cell(r, 3, f'=IF(COUNTIF(F{FIRST}:F{last},"REVISAR")=0,"TODOS LOS CONTROLES OK","REVISAR "&COUNTIF(F{FIRST}:F{last},"REVISAR")&" CONTROL(ES)")')
    c.font = f(True)
    ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=5)
    nombre(wb, "Estado_Controles", "Controles", f"$C${r}")
    semaforo(ws, f"F{FIRST}:F{last}", "OK", None, "REVISAR")
    ws.conditional_formatting.add(f"C{r}", FormulaRule(formula=[f'C{r}="TODOS LOS CONTROLES OK"'], fill=PatternFill("solid", bgColor=VERDE, fgColor=VERDE)))
    ws.conditional_formatting.add(f"C{r}", FormulaRule(formula=[f'C{r}<>"TODOS LOS CONTROLES OK"'], fill=PatternFill("solid", bgColor=ROJO, fgColor=ROJO)))
    return len(CONTROLES)


def hoja_tablero(wb):
    ws = wb.create_sheet("Tablero")
    titulo(ws, "Tablero de control de la UGP — Programa de Integración Académica y Comunitaria para Jóvenes",
           "Vista ejecutiva del cierre mensual. Todo se calcula desde las hojas de detalle; la fecha de corte se cambia en Parametros.")
    ws["A3"] = "Fecha de corte:"
    ws["A3"].font = f(True)
    ws["B3"] = "=Fecha_Corte"
    ws["B3"].number_format = FECHA
    ws["B3"].font = f(True, AZUL)
    ws["C3"] = "=Estado_Controles"
    ws["C3"].font = f(True)
    cols = [dict(h="Indicador clave", w=54, tipo="lbl"), dict(h="Valor", w=16, al="right", tipo="calc"),
            dict(h="Referencia", w=16, al="right", tipo="calc"), dict(h="Semáforo", w=12, tipo="calc")]
    ST = lambda v="Umbral_Verde", a="Umbral_Amarillo", div=False: (  # noqa: E731
        lambda r: f'=IF({"B%d/C%d" % (r, r) if div else "B%d" % r}>={v},"Verde",IF({"B%d/C%d" % (r, r) if div else "B%d" % r}>={a},"Amarillo","Rojo"))')
    CNT = lambda r: f'=IF(B{r}=0,"Verde",IF(B{r}<=2,"Amarillo","Rojo"))'  # noqa: E731
    K = [
        ("Presupuesto total del Programa (USD)", "=Total_Programa", None, None, USD),
        ("Ejecutado acumulado (USD)", "=F1_Presupuesto_PEP!N10", None, None, USD),
        ("% ejecutado sobre el total del Programa", "=F1_Presupuesto_PEP!O10", None, None, PCT),
        ("Avance físico del POA (real vs. planificado a la fecha)", "=P1_Avance_FF!F10", "=P1_Avance_FF!G10", ST(div=True), PCT),
        ("Avance financiero del POA (ejecutado / presupuesto POA)", "=P1_Avance_FF!E10", "=P1_Avance_FF!G10", None, PCT),
        ("SPI — índice de desempeño del cronograma", "=P1_Avance_FF!J10", 1, ST("EVM_Verde", "EVM_Amarillo"), "0.00"),
        ("CPI — índice de desempeño del costo", "=P1_Avance_FF!K10", 1, ST("EVM_Verde", "EVM_Amarillo"), "0.00"),
        ("Total desembolsado por el BID (USD)", "=F3_Desembolsos!L13", None, None, USD),
        ("% de anticipos justificado", "=F3_Desembolsos!L8", "=Pct_Justif_Min",
         lambda r: f'=IF(B{r}>=C{r},"Verde",IF(B{r}>=C{r}-0.1,"Amarillo","Rojo"))', PCT),
        ("Procesos de adquisición atrasados", f'=COUNTIF({R_("F4_Plan_Adquisiciones", "P", 200)},"Atrasado")', 0, CNT, "0"),
        ("No Objeciones pendientes fuera del plazo de referencia", f'=COUNTIF({R_("A3_No_Objeciones", "I", 200)},"Pendiente fuera de referencia")', 0, CNT, "0"),
        ("Compromisos con el BID vencidos", f'=COUNTIFS({rng("A2_Misiones_BID", "E", 100, 14)},"<"&Fecha_Corte,{rng("A2_Misiones_BID", "G", 100, 14)},"<>Cumplido",{rng("A2_Misiones_BID", "A", 100, 14)},"CM-*")', 0, CNT, "0"),
        ("Riesgos altos abiertos", f'=COUNTIFS({R_("P1_Riesgos", "H", 200)},"Alto",{R_("P1_Riesgos", "M", 200)},"<>Cerrado")', 0, CNT, "0"),
        ("Obligaciones normativas vencidas", "=N1_Cumplimiento!O8", 0, CNT, "0"),
        ("% de cumplimiento de obligaciones exigibles", "=N1_Cumplimiento!O10", 1, ST(), PCT),
        ("Cobertura de la meta de beneficiarios del año 1 (vs. fracción del año)", "=P2_Focalizacion!K19", "=Frac_Anio", ST(div=True), PCT),
    ]
    filas = []
    for i, (a, b, c, d, _) in enumerate(K):
        filas.append([a, b, c, d(6 + i) if callable(d) else None])
    tabla(ws, cols, filas, hdr=5, filtro=False, altura=24)
    for i, (*_, nf) in enumerate(K):
        for col in "BC":
            ws[f"{col}{6 + i}"].number_format = nf
    ws.column_dimensions["A"].width = 68
    semaforo(ws, "D6:D30", "Verde", "Amarillo", "Rojo")
    # --- mapa de calor de riesgos (probabilidad x impacto), filas 25-31
    r0 = 24
    ws.cell(r0, 1, "Mapa de calor de riesgos abiertos (n.º de riesgos por probabilidad × impacto)").font = f(True, AZUL, 12)
    ws.cell(r0 + 1, 1, "Impacto ↓  /  Probabilidad →").font = f(True)
    for p in range(1, 6):
        c = ws.cell(r0 + 1, 1 + p, p)
        c.font, c.fill, c.alignment, c.border = f(True, "FFFFFF"), C_ENCAB, Alignment(horizontal="center"), BORDE
    for k, imp in enumerate(range(5, 0, -1)):
        r = r0 + 2 + k
        c = ws.cell(r, 1, imp)
        c.font, c.fill, c.alignment, c.border = f(True, "FFFFFF"), C_ENCAB, Alignment(horizontal="right"), BORDE
        for p in range(1, 6):
            col = L(1 + p)
            cell = ws.cell(r, 1 + p, f'=COUNTIFS({R_("P1_Riesgos", "E", 200)},{col}${r0 + 1},{R_("P1_Riesgos", "F", 200)},$A{r},{R_("P1_Riesgos", "M", 200)},"<>Cerrado")')
            cell.font, cell.border, cell.alignment, cell.number_format = f(True), BORDE, Alignment(horizontal="center"), '0;-0;""'
    rng_h = f"B{r0 + 2}:F{r0 + 6}"
    for expr, color in ((f"$A{r0 + 2}*B${r0 + 1}>=Riesgo_Alto", ROJO), (f"AND($A{r0 + 2}*B${r0 + 1}>=Riesgo_Medio,$A{r0 + 2}*B${r0 + 1}<Riesgo_Alto)", AMARILLO),
                        (f"$A{r0 + 2}*B${r0 + 1}<Riesgo_Medio", VERDE)):
        ws.conditional_formatting.add(rng_h, FormulaRule(formula=[expr], fill=PatternFill("solid", bgColor=color, fgColor=color)))
    # --- gráficos nativos
    def barra(titulo_, anchor, cats, series, horizontal=False, w=17, h=8.5):
        ch = BarChart()
        ch.type, ch.title, ch.width, ch.height = ("bar" if horizontal else "col"), titulo_, w, h
        ch.y_axis.numFmt, ch.y_axis.majorGridlines = "#,##0", None
        for ref, ttl in series:
            s_ = Series(ref, title=ttl)
            ch.series.append(s_)
        ch.set_categories(cats)
        ch.legend.position = "b"
        ws.add_chart(ch, anchor)
    pf = wb["P1_Avance_FF"]
    barra("POA año 1 por componente: presupuesto, valor ganado (EV) y costo real (AC), USD", "H4", Reference(pf, min_col=1, min_row=5, max_row=9),
          [(Reference(pf, min_col=3, min_row=5, max_row=9), "Presupuesto POA"), (Reference(pf, min_col=8, min_row=5, max_row=9), "Valor ganado (EV)"),
           (Reference(pf, min_col=4, min_row=5, max_row=9), "Costo real (AC)")])
    fp = wb["F3_Plan_Financiero"]
    barra("Gasto trimestral: proyectado vs. real, USD", "H22", Reference(fp, min_col=1, min_row=5, max_row=12),
          [(Reference(fp, min_col=4, min_row=5, max_row=12), "Proyectado"), (Reference(fp, min_col=5, min_row=5, max_row=12), "Real")])
    fo = wb["P2_Focalizacion"]
    barra("Beneficiarios por departamento: meta año 1 vs. alcanzado", "H40", Reference(fo, min_col=1, min_row=5, max_row=18),
          [(Reference(fo, min_col=6, min_row=5, max_row=18), "Meta año 1"), (Reference(fo, min_col=7, min_row=5, max_row=18), "Alcanzado")],
          horizontal=True, h=11)
    return len(K)


def hoja_leeme(wb, hojas):
    ws = wb.create_sheet("LEEME")
    titulo(ws, "Sistema integrado de control de la UGP — LÉEME")
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 26
    ws.column_dimensions["C"].width = 72
    ws.column_dimensions["D"].width = 24
    ws.column_dimensions["E"].width = 22
    r = 4
    def par(txt, bold=False, color="000000", size=11):
        nonlocal r
        c = ws.cell(r, 1, txt)
        c.font = f(bold, color, size)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
        ws.row_dimensions[r].height = max(18, 16 * (len(txt) // 120 + 1))
        r += 1
    par("Qué es", True, AZUL, 13)
    par("Libro de control de ejecución para la Unidad Gestora del Programa (UGP) del Programa de Integración Académica y Comunitaria para Jóvenes en El Salvador "
        "(operaciones BID ES-L1175 / ES-J0003; Contrato de Préstamo 6153/OC-ES por US$100 M y Convenio no reembolsable 6154/GR-ES por US$4 M). "
        "Organiza el ciclo del TDR en cuatro pilares: planificación y control integral, gestión fiduciaria, cumplimiento normativo y articulación y reporte.")
    par("ADVERTENCIA: todos los datos son SIMULADOS y la estructura de componentes es ILUSTRATIVA. Se tomaron del TDR solo los montos, números de operación y condiciones de la consultoría. "
        "Antes de usarlo con datos reales hay que contrastarlo con el Contrato de Préstamo, el MOP, el PEP, el Plan de Adquisiciones y los sistemas del BID.", True, "C00000")
    r += 1
    par("Código de colores", True, AZUL, 13)
    for txt, fnt, fill in (("Texto azul = dato que se ingresa o edita", "0000FF", None), ("Texto negro sobre gris = fórmula (no editar)", "000000", C_CALC),
                           ("Semáforo verde / amarillo / rojo = según los umbrales de la hoja Parametros", "000000", None)):
        c = ws.cell(r, 1, txt)
        c.font = f(False, fnt)
        if fill:
            c.fill = fill
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
        r += 1
    r += 1
    par("Ciclo de cierre mensual (informe a más tardar 3 días hábiles tras el cierre)", True, AZUL, 13)
    for k, t in enumerate(["Registrar los gastos del mes en F2_Ejecucion y los desembolsos en F3_Desembolsos.",
                           "Actualizar % de avance físico en P1_POA, valores actuales en P1_Resultados y estados en F4/F5.",
                           "Actualizar riesgos (P1_Riesgos), cumplimiento (N1), compromisos y No Objeciones (A2, A3).",
                           "Cambiar la fecha de corte en Parametros y revisar la hoja Controles (debe decir TODOS LOS CONTROLES OK).",
                           "Leer el Tablero y A6_Informe_Mensual; redactar logros, decisiones y prioridades; emitir el informe (P2-P11).",
                           "Archivar evidencias y actualizar A5_Calendario_Informes."], 1):
        par(f"{k}. {t}")
    r += 1
    par("Índice de hojas", True, AZUL, 13)
    for j, h in enumerate(["Hoja", "Pilar", "Qué hace", "Mantiene", "Frecuencia"], 1):
        c = ws.cell(r, j, h)
        c.font, c.fill, c.border = f(True, "FFFFFF"), C_ENCAB, BORDE
    r += 1
    for nom, pil, que, quien, frec in hojas:
        c = ws.cell(r, 1, nom)
        c.hyperlink = f"#'{nom}'!A1"
        c.font = f(False, "0563C1")
        for j, v in enumerate((pil, que, quien, frec), 2):
            cc = ws.cell(r, j, v)
            cc.font = f()
            cc.alignment = Alignment(wrap_text=True, vertical="top")
        for j in range(1, 6):
            ws.cell(r, j).border = BORDE
        ws.row_dimensions[r].height = 32 if (len(que) > 72 or len(pil) > 24 or len(frec) > 22) else 20
        r += 1
    return r
