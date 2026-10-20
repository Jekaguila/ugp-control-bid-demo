"""Pilar 4 (parte 2): A1_Equipo_RACI, A4_Interesados, A6_Informe_Mensual."""
from xl_base import *
from hojas_base import REF
from datos_demo import *  # noqa: F401,F403

E = lambda sh, c, u=500: rng(sh, c, u)   # noqa: E731


def hoja_equipo(wb):
    ws = wb.create_sheet("A1_Equipo")
    titulo(ws, "A1 · Equipo de la UGP",
           "Plazas de la UGP según el TDR: Coordinador General, Especialistas Financiero, en Adquisiciones, en Planificación, Monitoreo y Seguimiento, Social, entre otros.")
    c1 = [dict(h="Rol", w=40), dict(h="Plazas", w=8), dict(h="Función clave en el ciclo de control", w=60, wrap=True),
          dict(h="Estado de contratación", w=18), dict(h="Contrato", w=10), dict(h="Instrumento principal que mantiene", w=36, wrap=True),
          dict(h="Reporta a", w=30, wrap=True)]
    eq = [("Coordinador General de la UGP", 1, "Conduce la UGP; punto focal con el BID; responsabilidad fiduciaria gerencial; decisiones y escalamiento", "Contratado", "CT-10", "Tablero, informe mensual (P1-P12), matriz de compromisos", "Gerencia de Cooperación Institucional"),
          ("Especialista Financiero", 1, "Presupuesto, desembolsos, justificación de anticipos, contabilidad y auditorías", "Contratado", "CT-11", "F1, F2, F3 y F6", "Coordinador General"),
          ("Especialista en Adquisiciones", 1, "Plan de Adquisiciones, procesos, contratos y No Objeciones", "Contratado", "CT-12", "F4, F5 y A3", "Coordinador General"),
          ("Especialista en Planificación, Monitoreo y Seguimiento", 1, "POA/PEP, indicadores, riesgos, informes y línea base", "Contratado", "CT-13", "P1_POA, P1_Resultados y P1_Riesgos", "Coordinador General"),
          ("Especialista Social", 1, "Focalización, inclusión, salvaguardas ambientales y sociales, quejas y protección de datos", "Contratado", "CT-14", "P2 y N1 (ambiental y social)", "Coordinador General"),
          ("Apoyo administrativo y de archivo", 1, "Archivo físico y digital del Programa, logística y trámites", "Por contratar", "", "Índice de archivo del Programa", "Coordinador General")]
    tabla(ws, c1, [list(r) for r in eq], filtro=False)
    lista(ws, "D5:D20", '"Contratado,En selección,Por contratar"')
    ws.column_dimensions["A"].width = 44
    ws2 = wb.create_sheet("A1_RACI")
    titulo(ws2, "A1 · Matriz de responsabilidades (RACI) de los procesos de la UGP",
           "R = ejecuta · A = rinde cuentas (una sola por proceso) · C = consultado · I = informado. «A/R» = rinde cuentas y ejecuta.")
    roles = ["Coord. General", "Esp. Financiero", "Esp. Adquisic.", "Esp. Planif. M&S", "Esp. Social", "Gerencia Coop. Inst.", "Dirección General", "BID"]
    c2 = [dict(h="Proceso", w=62, tipo="lbl", wrap=True)] + [dict(h=r, w=12, al="center") for r in roles] + [dict(h="Chequeo (una sola A)", w=13, tipo="calc")]
    P = [("Elaborar el PEP y el POA anual", "A C C R C C I C"), ("Actualizar el Plan de Adquisiciones", "A C R C C I I C"),
         ("Conducir procesos de adquisición y contratación", "A C R C C C I C"), ("Tramitar No Objeciones ante el BID", "A C R C C I I C"),
         ("Ejecución presupuestaria y registros contables", "A R C C I C I I"), ("Solicitudes de desembolso y justificación de anticipos", "A R C C I I I C"),
         ("Pagos a proveedores y consultores", "A R C I I I I I"), ("Seguimiento de indicadores y matriz de resultados", "A C I R C I I C"),
         ("Gestión de riesgos y plan de mitigación", "A C C R C I I I"), ("Cumplimiento ambiental y social, inclusión y protección de datos", "A I C C R I I C"),
         ("Informe mensual de gestión (P2-P11)", "A/R C C R C I I I"), ("Preparar misiones del BID y dar seguimiento a compromisos", "A C C R C I I C"),
         ("Auditorías y seguimiento de recomendaciones", "A R C C C I I I"), ("Cierre técnico, fiduciario y administrativo", "A R R R R C I C")]
    f2 = []
    for i, (pr, rc) in enumerate(P):
        n = FIRST + i
        f2.append([pr] + rc.split(" ") + [f'=IF(COUNTIF(B{n}:I{n},"A*")=1,"OK","REVISAR")'])
    tabla(ws2, c2, f2, filtro=False, altura=40)
    ws2.freeze_panes = "B5"
    semaforo(ws2, f"J{FIRST}:J40", "OK", None, "REVISAR")
    lista(ws2, f"B{FIRST}:I40", '"R,A,C,I,A/R"')
    return len(eq), len(P)


def hoja_interesados(wb):
    ws = wb.create_sheet("A4_Interesados")
    titulo(ws, "A4 · Registro y estrategia de interesados (poder / interés)",
           "Cuadrante: poder ≥ 4 e interés ≥ 4 → gestionar de cerca; poder ≥ 4 → mantener satisfecho; interés ≥ 4 → mantener informado; resto → monitorear.")
    cols = [dict(h="ID", w=7), dict(h="Interesado", w=40, wrap=True), dict(h="Rol en el Programa", w=42, wrap=True),
            dict(h="Poder (1-5)", w=8), dict(h="Interés (1-5)", w=8), dict(h="Actitud", w=11), dict(h="Cuadrante", w=20, tipo="calc"),
            dict(h="Prioridad (P×I)", w=9, fmt="0", tipo="calc"), dict(h="Estrategia de comunicación", w=46, wrap=True),
            dict(h="Frecuencia", w=14), dict(h="Responsable", w=24)]
    S = [("Banco Interamericano de Desarrollo (equipo de proyecto)", "Financiador; no objeciones, misiones y desembolsos", 5, 5, "Líder", "Informe mensual, reuniones de seguimiento y misiones", "Mensual", R_CG),
         ("Dirección General de la Dirección de Integración", "Autoridad del Organismo Ejecutor; decisiones estratégicas", 5, 5, "Líder", "Reunión de decisiones y alertas escaladas", "Mensual", R_CG),
         ("Gerencia de Cooperación Institucional", "Supervisión contractual y aprobación de productos de la UGP", 5, 5, "A favor", "Informe mensual y reunión de coordinación", "Semanal", R_CG),
         ("Ministerio de Hacienda", "Autoridad fiscal; programación y contrapartidas", 4, 3, "Neutral", "Informes de ejecución y proyecciones de desembolso", "Trimestral", R_FIN),
         ("Ministerio de Educación, Ciencia y Tecnología", "Rector del sistema educativo; articulación con educación media", 4, 5, "A favor", "Mesa técnica y convenios", "Mensual", R_SOC),
         ("Corte de Cuentas de la República", "Control externo", 4, 2, "Neutral", "Entrega de información y atención de requerimientos", "Por requerimiento", R_FIN),
         ("Instituciones de educación postsecundaria (públicas)", "Receptoras de beneficiarios; fortalecimiento institucional", 3, 5, "A favor", "Convenios, capacitación y mesas de coordinación", "Mensual", R_SOC),
         ("Instituciones de educación postsecundaria (privadas)", "Receptoras de beneficiarios", 3, 4, "Neutral", "Convocatorias y convenios", "Trimestral", R_SOC),
         ("Empleadores y gremios", "Vinculación laboral de las personas graduadas", 3, 4, "Neutral", "Alianzas y encuentros sectoriales", "Trimestral", R_SOC),
         ("Organizaciones de personas con discapacidad y de sociedad civil", "Accesibilidad, veeduría social y mecanismo de quejas", 2, 5, "A favor", "Consultas y devolución de resultados", "Trimestral", R_SOC),
         ("Jóvenes beneficiarios y sus familias", "Población objetivo", 2, 5, "A favor", "Canales de atención, mecanismo de quejas y comunicación directa", "Continua", R_SOC),
         ("Proveedores y consultores", "Ejecutores de contratos y servicios", 2, 4, "Neutral", "Reuniones de arranque y supervisión de contratos", "Según contrato", R_ADQ),
         ("Gobiernos locales", "Facilitan acceso territorial y ferias de orientación", 2, 3, "Neutral", "Coordinación territorial", "Trimestral", R_SOC)]
    filas = []
    for i, s in enumerate(S):
        n = FIRST + i
        filas.append([f"I-{i + 1:02d}", s[0], s[1], s[2], s[3], s[4],
                      f'=IF(AND(D{n}>=4,E{n}>=4),"Gestionar de cerca",IF(D{n}>=4,"Mantener satisfecho",IF(E{n}>=4,"Mantener informado","Monitorear")))',
                      f"=D{n}*E{n}", s[5], s[6], s[7]])
    tabla(ws, cols, filas, altura=36)
    for col, lst in (("D", "Escala"), ("E", "Escala"), ("F", "Actitud"), ("K", "Responsable")):
        lista(ws, f"{col}{FIRST}:{col}200", "=" + REF[lst])
    return len(filas)


def hoja_informe(wb):
    ws = wb.create_sheet("A6_Informe_Mensual")
    titulo(ws, "A6 · Informe mensual de gestión — borrador automático (contenido mínimo del TDR §VII)",
           "Cada línea se calcula desde las demás hojas. Los textos en azul (decisiones, prioridades) los redacta la UGP antes de entregar el informe.")
    cols = [dict(h="Sección del TDR", w=40, tipo="lbl", wrap=True), dict(h="Elemento", w=58, tipo="lbl", wrap=True),
            dict(h="Valor", w=44, tipo="calc", al="right", wrap=True), dict(h="Fuente", w=26, tipo="lbl")]
    S1, S2, S3, S4, S5, S6, S7, S8, S9, S10 = ("1. Resumen ejecutivo", "2. Avance de actividades y productos vs. POA", "3. Metas e indicadores",
                                              "4. Ejecución financiera y proyecciones", "5. Adquisiciones y contratos", "6. Compromisos, No Objeciones y BID",
                                              "7. Riesgos, incidentes y asuntos escalados", "8. Cumplimiento ambiental, social, inclusión y datos",
                                              "9. Gestión de la UGP", "10-12. Próximo período, matriz y anexos")
    A = "P1_Avance_FF"
    poa = lambda c: E("P1_POA", c, 200)   # noqa: E731
    rie = lambda c: E("P1_Riesgos", c, 200)   # noqa: E731
    L_ = [
        (S1, "Fecha de corte del informe", "=Fecha_Corte", "Parametros", FECHA),
        (S1, "Avance físico acumulado del POA", f"={A}!F10", "P1_Avance_FF", PCT),
        (S1, "Avance físico planificado a la fecha", f"={A}!G10", "P1_Avance_FF", PCT),
        (S1, "Ejecución financiera del POA", f"={A}!E10", "P1_Avance_FF", PCT),
        (S1, "SPI / CPI del Programa", f'=IF(ISNUMBER({A}!J10),ROUND({A}!J10,2)&" / "&ROUND({A}!K10,2),"n/a")', "P1_Avance_FF", "General"),
        (S1, "Alertas críticas (rojos: actividades, riesgos altos, obligaciones y compromisos vencidos)",
         f'=COUNTIF({poa("R")},"Rojo")+COUNTIFS({rie("H")},"Alto",{rie("M")},"<>Cerrado")+COUNTIF({E("N1_Cumplimiento", "K", 200)},"Vencida")+COUNTIFS({E("A2_Misiones_BID", "E", 100)},"<"&Fecha_Corte,{E("A2_Misiones_BID", "G", 100)},"<>Cumplido",{E("A2_Misiones_BID", "A", 100)},"CM-*")', "Varias hojas", "0"),
        (S1, "Logros y decisiones requeridas (redactar)", "Aprobar la reprogramación de C4 y priorizar las No Objeciones pendientes", "Redacción UGP", "General"),
        (S2, "Actividades del POA", f"={A}!M10", "P1_POA", "0"),
        (S2, "Completadas", f'=COUNTIF({poa("Q")},"Completada")', "P1_POA", "0"),
        (S2, "Con alerta (semáforo amarillo o rojo)", f"={A}!N10", "P1_POA", "0"),
        (S2, "Vencidas sin completar", f'=COUNTIF({poa("Q")},"Vencida sin completar")', "P1_POA", "0"),
        (S3, "Indicadores en verde", f'=COUNTIF({E("P1_Resultados", "Q", 100)},"Verde")', "P1_Resultados", "0"),
        (S3, "Indicadores en amarillo", f'=COUNTIF({E("P1_Resultados", "Q", 100)},"Amarillo")', "P1_Resultados", "0"),
        (S3, "Indicadores en rojo", f'=COUNTIF({E("P1_Resultados", "Q", 100)},"Rojo")', "P1_Resultados", "0"),
        (S3, "Indicadores sin dato en el período", f'=COUNTIF({E("P1_Resultados", "Q", 100)},"Sin dato")', "P1_Resultados", "0"),
        (S4, "Presupuesto total del Programa (USD)", "=Total_Programa", "Parametros", USD),
        (S4, "Ejecutado acumulado (USD)", "=F1_Presupuesto_PEP!N10", "F1_Presupuesto_PEP", USD),
        (S4, "% ejecutado sobre el total", "=F1_Presupuesto_PEP!O10", "F1_Presupuesto_PEP", PCT),
        (S4, "Proyectado acumulado a los trimestres cerrados (USD)", f'=SUMIFS({E("F3_Plan_Financiero", "D", 20)},{E("F3_Plan_Financiero", "C", 20)},"<="&Fecha_Corte)', "F3_Plan_Financiero", USD),
        (S4, "Real acumulado a la fecha de corte (USD)", f'=SUMIFS({E("F2_Ejecucion", "J")},{E("F2_Ejecucion", "B")},"<="&Fecha_Corte)', "F2_Ejecucion", USD),
        (S4, "Total desembolsado por el BID (USD)", "=F3_Desembolsos!L13", "F3_Desembolsos", USD),
        (S4, "% de anticipos justificado", "=F3_Desembolsos!L8", "F3_Desembolsos", PCT),
        (S4, "Alerta de anticipos", "=F3_Desembolsos!L15", "F3_Desembolsos", "General"),
        (S5, "Procesos en el Plan de Adquisiciones", f'=COUNTIF({E("F4_Plan_Adquisiciones", "A", 200)},"PA-*")', "F4_Plan_Adquisiciones", "0"),
        (S5, "Procesos contratados", f'=COUNTIF({E("F4_Plan_Adquisiciones", "I", 200)},"Contratado")', "F4_Plan_Adquisiciones", "0"),
        (S5, "Procesos atrasados", f'=COUNTIF({E("F4_Plan_Adquisiciones", "P", 200)},"Atrasado")', "F4_Plan_Adquisiciones", "0"),
        (S5, "Contratos vigentes / por vencer / vencidos",
         f'=COUNTIF({E("F5_Contratos", "N", 200)},"Vigente")&" / "&COUNTIF({E("F5_Contratos", "N", 200)},"Por vencer")&" / "&COUNTIF({E("F5_Contratos", "N", 200)},"Vencido")', "F5_Contratos", "General"),
        (S6, "No Objeciones pendientes", f'=COUNTIF({E("A3_No_Objeciones", "F", 200)},"Pendiente")', "A3_No_Objeciones", "0"),
        (S6, "No Objeciones pendientes fuera del plazo de referencia", f'=COUNTIF({E("A3_No_Objeciones", "I", 200)},"Pendiente fuera de referencia")', "A3_No_Objeciones", "0"),
        (S6, "Compromisos con el BID vencidos", f'=COUNTIFS({E("A2_Misiones_BID", "E", 100)},"<"&Fecha_Corte,{E("A2_Misiones_BID", "G", 100)},"<>Cumplido",{E("A2_Misiones_BID", "A", 100)},"CM-*")', "A2_Misiones_BID", "0"),
        (S7, "Riesgos altos abiertos", f'=COUNTIFS({rie("H")},"Alto",{rie("M")},"<>Cerrado")', "P1_Riesgos", "0"),
        (S7, "Riesgos medios abiertos", f'=COUNTIFS({rie("H")},"Medio",{rie("M")},"<>Cerrado")', "P1_Riesgos", "0"),
        (S7, "Riesgo prioritario n.º 1", f'=INDEX({rie("C")},MATCH(1,{rie("T")},0))', "P1_Riesgos", "General"),
        (S7, "Riesgo prioritario n.º 2", f'=INDEX({rie("C")},MATCH(2,{rie("T")},0))', "P1_Riesgos", "General"),
        (S7, "Riesgo prioritario n.º 3", f'=INDEX({rie("C")},MATCH(3,{rie("T")},0))', "P1_Riesgos", "General"),
        (S8, "Obligaciones normativas vencidas", f'=COUNTIF({E("N1_Cumplimiento", "K", 200)},"Vencida")', "N1_Cumplimiento", "0"),
        (S8, "% de cumplimiento de obligaciones exigibles", "=N1_Cumplimiento!O10", "N1_Cumplimiento", PCT),
        (S8, "Beneficiarios alcanzados / meta año 1", '=P2_Focalizacion!G19&" / "&P2_Focalizacion!F19', "P2_Focalizacion", "General"),
        (S8, "Madres jóvenes, personas con discapacidad y retornadas/os atendidas",
         '=P2_Focalizacion!H19&" / "&P2_Focalizacion!I19&" / "&P2_Focalizacion!J19', "P2_Focalizacion", "General"),
        (S9, "Informes entregados a tiempo", f'=COUNTIF({E("A5_Calendario_Informes", "F", 30)},"Entregado a tiempo")&" de "&COUNTIF({E("A5_Calendario_Informes", "F", 30)},"Entregado*")', "A5_Calendario_Informes", "General"),
        (S9, "Plazas de la UGP cubiertas", f'=COUNTIF({E("A1_Equipo", "D", 12)},"Contratado")&" de "&COUNTA({E("A1_Equipo", "A", 10)})', "A1_Equipo", "General"),
        (S9, "Recomendaciones de auditoría vencidas", f'=COUNTIF({rng("F6_Auditoria", "I", 100, 14)},">0")', "F6_Auditoria", "0"),
        (S10, "Prioridades del próximo período (redactar)", "Cerrar adjudicaciones PA-11 y PA-12; presentar la línea base; justificar anticipos al 80 %", "Redacción UGP", "General"),
        (S10, "Anexos y archivo", "Enlaces a evidencia documental organizada por proceso (expediente del Programa)", "Redacción UGP", "General"),
    ]
    filas = [[s, el, v, fu] for s, el, v, fu, _ in L_]
    tabla(ws, cols, filas, filtro=False, altura=26)
    for i, (*_, nf) in enumerate(L_):
        c = ws.cell(FIRST + i, 3)
        c.number_format = nf
        c.alignment = Alignment(horizontal="right", vertical="top", wrap_text=True)
        if not str(L_[i][2]).startswith("="):
            c.font, c.fill = f(False, "0000FF"), PatternFill(fill_type=None)
    ws.freeze_panes = "A5"
    return len(L_)
