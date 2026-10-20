"""Pilar 1 — Planificación y control integral: P1_POA, P1_Avance_FF, P1_Riesgos, P1_Resultados, P2_Focalizacion."""
from xl_base import *
from hojas_base import REF
from datos_demo import *  # noqa: F401,F403
import datos_calculados as dc

POA_R = lambda c: rng("P1_POA", c, 200)           # noqa: E731
LEDG = lambda c: rng("F2_Ejecucion", c, 500)      # noqa: E731

HITOS = {
    "C1-01": "Modelo de captación aprobado", "C1-02": "Convenios firmados con centros educativos",
    "C1-03": "Campaña lanzada (fase 1)", "C1-04": "Plataforma en producción", "C1-05": "Primera feria realizada",
    "C2-01": "Esquema de apoyos aprobado (MOP)", "C2-02": "Cohorte 1 seleccionada", "C2-03": "Primer pago de apoyos",
    "C2-04": "Tutorías en marcha", "C2-05": "Servicios de accesibilidad contratados", "C2-06": "Protocolo de atención aprobado",
    "C3-01": "Informe de diagnóstico aprobado", "C3-02": "Alianzas firmadas", "C3-03": "Rutas de vinculación validadas",
    "C3-04": "Piloto iniciado", "C4-01": "Plan de fortalecimiento aprobado", "C4-02": "Módulos 1-3 del sistema en uso",
    "C4-03": "Primer ciclo de capacitaciones", "C4-04": "Equipos entregados", "C5-01": "UGP completa y operando",
    "C5-02": "Línea base entregada", "C5-03": "Firma auditora contratada", "C5-04": "Mecanismo de quejas operativo",
    "C5-05": "Plan de comunicación implementado",
}


def hoja_poa(wb):
    ws = wb.create_sheet("P1_POA")
    titulo(ws, "P1 · Plan Operativo Anual (POA) e hitos — avance físico y financiero por actividad",
           "Valor ganado: EV = presupuesto × % avance físico · PV = presupuesto × % planificado a la fecha de corte · AC = ejecutado (libro F2). "
           "SPI = EV/PV · CPI = EV/AC.")
    cols = [dict(h="ID", w=8), dict(h="Comp.", w=7), dict(h="Actividad", w=46, wrap=True), dict(h="Responsable", w=22),
            dict(h="Inicio", w=11, fmt=FECHA), dict(h="Fin", w=11, fmt=FECHA), dict(h="Presupuesto POA USD", w=14, fmt=USD),
            dict(h="% avance físico", w=10, fmt=PCT), dict(h="% planificado a corte", w=11, fmt=PCT, tipo="calc"),
            dict(h="Ejecutado USD (AC)", w=14, fmt=USD, tipo="calc"), dict(h="% ejecución financiera", w=11, fmt=PCT, tipo="calc"),
            dict(h="EV USD", w=13, fmt=USD, tipo="calc"), dict(h="PV USD", w=13, fmt=USD, tipo="calc"),
            dict(h="SPI", w=8, fmt="0.00", tipo="calc"), dict(h="CPI", w=8, fmt="0.00", tipo="calc"),
            dict(h="Días de atraso", w=9, fmt="0", tipo="calc"), dict(h="Estado", w=26, tipo="calc", wrap=True),
            dict(h="Semáforo", w=10, tipo="calc"), dict(h="Hito / entregable", w=36, wrap=True)]
    filas = []
    for i, a in enumerate(POA):
        n = FIRST + i
        filas.append([a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7] / 100,
                      f"=IF(Fecha_Corte<=E{n},0,IF(Fecha_Corte>=F{n},1,(Fecha_Corte-E{n})/(F{n}-E{n})))",
                      f'=SUMIFS({LEDG("J")},{LEDG("D")},A{n})', f"=IF(G{n}=0,0,J{n}/G{n})",
                      f"=G{n}*H{n}", f"=G{n}*I{n}", f'=IF(M{n}=0,"n/a",L{n}/M{n})', f'=IF(J{n}=0,"n/a",L{n}/J{n})',
                      f"=IF(H{n}>=1,0,MAX(0,Fecha_Corte-F{n}))",
                      f'=IF(H{n}>=1,"Completada",IF(Fecha_Corte<E{n},"No iniciada",IF(Fecha_Corte>F{n},"Vencida sin completar",'
                      f'IF(NOT(ISNUMBER(N{n})),"En curso",IF(N{n}>=EVM_Verde,"En curso a tiempo",'
                      f'IF(N{n}>=EVM_Amarillo,"En curso con retraso leve","En curso con retraso crítico"))))))',
                      f'=IF(H{n}>=1,"Verde",IF(NOT(ISNUMBER(N{n})),"Gris",IF(N{n}>=EVM_Verde,"Verde",IF(N{n}>=EVM_Amarillo,"Amarillo","Rojo"))))',
                      HITOS[a[0]]])
    tabla(ws, cols, filas, altura=48)
    lista(ws, f"B{FIRST}:B200", "=" + REF["Componente"])
    lista(ws, f"D{FIRST}:D200", "=" + REF["Responsable"])
    semaforo(ws, f"R{FIRST}:R200", "Verde", "Amarillo", "Rojo")
    semaforo_ratio(ws, f"N{FIRST}:O200", "EVM_Verde", "EVM_Amarillo")
    return len(filas)


def hoja_avance(wb):
    ws = wb.create_sheet("P1_Avance_FF")
    titulo(ws, "P1 · Avance físico y financiero consolidado por componente (POA del año vigente)",
           "Lectura: SPI < 1 = atraso físico frente a lo planificado; CPI < 1 = se gastó más de lo que el avance físico justifica.")
    cols = [dict(h="Comp.", w=8, tipo="lbl"), dict(h="Componente", w=36, tipo="lbl"),
            dict(h="Presupuesto POA", w=15, fmt=USD, tipo="calc"), dict(h="Ejecutado (AC)", w=15, fmt=USD, tipo="calc"),
            dict(h="% financiero", w=11, fmt=PCT, tipo="calc"), dict(h="% físico ponderado", w=11, fmt=PCT, tipo="calc"),
            dict(h="% planificado", w=11, fmt=PCT, tipo="calc"), dict(h="EV", w=14, fmt=USD, tipo="calc"),
            dict(h="PV", w=14, fmt=USD, tipo="calc"), dict(h="SPI", w=8, fmt="0.00", tipo="calc"),
            dict(h="CPI", w=8, fmt="0.00", tipo="calc"), dict(h="Brecha físico − financiero", w=12, fmt=PCT, tipo="calc"),
            dict(h="N.º actividades", w=10, fmt="0", tipo="calc"), dict(h="N.º con alerta", w=9, fmt="0", tipo="calc"),
            dict(h="Semáforo", w=10, tipo="calc")]
    filas = []
    for i, (cod, nom, *_r) in enumerate(COMPONENTES):
        n = FIRST + i
        s = lambda col: f"SUMIFS({POA_R(col)},{POA_R('B')},A{n})"   # noqa: E731
        filas.append([cod, nom, f"={s('G')}", f"={s('J')}", f"=IF(C{n}=0,0,D{n}/C{n})", f"=IF(C{n}=0,0,H{n}/C{n})",
                      f"=IF(C{n}=0,0,I{n}/C{n})", f"={s('L')}", f"={s('M')}", f'=IF(I{n}=0,"n/a",H{n}/I{n})',
                      f'=IF(D{n}=0,"n/a",H{n}/D{n})', f"=F{n}-E{n}", f'=COUNTIFS({POA_R("B")},A{n})',
                      f'=COUNTIFS({POA_R("B")},A{n},{POA_R("R")},"Rojo")+COUNTIFS({POA_R("B")},A{n},{POA_R("R")},"Amarillo")',
                      f'=IF(NOT(ISNUMBER(J{n})),"Gris",IF(MIN(J{n},IF(ISNUMBER(K{n}),K{n},J{n}))>=EVM_Verde,"Verde",'
                      f'IF(MIN(J{n},IF(ISNUMBER(K{n}),K{n},J{n}))>=EVM_Amarillo,"Amarillo","Rojo")))'])
    tabla(ws, cols, filas, filtro=False, altura=44)
    t = FIRST + 5
    vals = {1: "TOTAL", 2: "Programa", 3: f"=SUM(C{FIRST}:C{t - 1})", 4: f"=SUM(D{FIRST}:D{t - 1})", 5: f"=D{t}/C{t}",
            6: f"=H{t}/C{t}", 7: f"=I{t}/C{t}", 8: f"=SUM(H{FIRST}:H{t - 1})", 9: f"=SUM(I{FIRST}:I{t - 1})",
            10: f'=IF(I{t}=0,"n/a",H{t}/I{t})', 11: f'=IF(D{t}=0,"n/a",H{t}/D{t})', 12: f"=F{t}-E{t}",
            13: f"=SUM(M{FIRST}:M{t - 1})", 14: f"=SUM(N{FIRST}:N{t - 1})",
            15: f'=IF(NOT(ISNUMBER(J{t})),"Gris",IF(MIN(J{t},K{t})>=EVM_Verde,"Verde",IF(MIN(J{t},K{t})>=EVM_Amarillo,"Amarillo","Rojo")))'}
    for j, v in vals.items():
        c = ws.cell(t, j, v)
        c.font, c.fill, c.border = f(True), C_SUB, BORDE
        c.number_format = cols[j - 1].get("fmt", "General")
    semaforo(ws, f"O{FIRST}:O{t}", "Verde", "Amarillo", "Rojo")
    semaforo_ratio(ws, f"J{FIRST}:K{t}", "EVM_Verde", "EVM_Amarillo")
    nota(ws, t + 2, "Presupuesto POA = actividades del año 1 (reconciliado con el PEP en la hoja Controles). Umbrales en Parametros (EVM_Verde / EVM_Amarillo).")
    return t


RIESGOS = [  # cat, descripción, causa, P, I, respuesta, mitigación, responsable, fecha límite, estado, Pr, Ir
    ("Institucional", "Rotación o vacantes del personal clave de la UGP", "Contratos anuales y alta demanda de perfiles", 3, 4, "Mitigar", "Plan de sucesión, manual de funciones y prórrogas anticipadas", R_CG, date(2027, 9, 30), "En mitigación", 2, 3),
    ("Fiduciario", "Retrasos en adquisiciones por observaciones en las No Objeciones", "Expedientes incompletos o términos de referencia ambiguos", 4, 4, "Mitigar", "Listas de verificación previas al envío, plantillas estándar y calendario de No Objeciones", R_ADQ, date(2027, 7, 31), "En mitigación", 3, 3),
    ("Fiduciario", "Ejecución presupuestaria por debajo del PEP", "Retrasos físicos y de contratación", 4, 4, "Mitigar", "Seguimiento mensual SPI/CPI y reprogramación trimestral con alertas tempranas", R_CG, date(2027, 9, 30), "Abierto", 3, 3),
    ("Fiduciario", "Justificación tardía de anticipos retrasa nuevos desembolsos", "Rendiciones atrasadas y soporte incompleto", 3, 4, "Mitigar", "Justificación quincenal y control del umbral del 80 % de anticipos", R_FIN, date(2027, 7, 15), "En mitigación", 2, 3),
    ("Técnico", "Bajo alcance en departamentos de prioridad alta", "Barreras de acceso, difusión insuficiente en zonas rurales", 3, 4, "Mitigar", "Focalización por índice, ferias departamentales y alianzas locales", R_SOC, date(2027, 10, 31), "Abierto", 2, 3),
    ("Técnico", "Retraso en el desarrollo del sistema de información de trayectorias", "Requisitos cambiantes e integración con instituciones", 4, 3, "Mitigar", "Entregas por módulos, pruebas tempranas y gobierno de requisitos", R_PLAN, date(2027, 8, 31), "En mitigación", 3, 3),
    ("Institucional", "Débil articulación con instituciones de educación postsecundaria", "Capacidades y prioridades distintas", 3, 3, "Mitigar", "Convenios con compromisos medibles y mesa de coordinación", R_CG, date(2027, 9, 30), "Abierto", 2, 3),
    ("Ambiental y social", "Exclusión de grupos prioritarios (discapacidad, madres jóvenes, retornados)", "Barreras de accesibilidad y de información", 3, 5, "Mitigar", "Ajustes razonables, metas por grupo y monitoreo de cobertura", R_SOC, date(2027, 8, 31), "En mitigación", 2, 4),
    ("Ambiental y social", "Incidente de protección de datos personales de beneficiarios", "Manejo de información sensible en varias entidades", 2, 5, "Mitigar", "Protocolo de datos, accesos por rol y capacitación", R_SOC, date(2027, 7, 31), "En mitigación", 1, 5),
    ("Cumplimiento", "Incumplimiento de plazos de informes al BID", "Cierres contables y de indicadores desfasados", 2, 4, "Mitigar", "Calendario de reportes con alertas a 30 días", R_PLAN, date(2027, 7, 31), "En mitigación", 1, 4),
    ("Cumplimiento", "Modificar el MOP o reasignar fondos sin No Objeción previa", "Cambios operativos urgentes", 1, 4, "Evitar", "Regla: ningún cambio sin No Objeción; registro de cambios (CCB)", R_CG, date(2027, 12, 31), "Abierto", 1, 4),
    ("Externo", "Cambios de prioridades o transición institucional", "Contexto político", 2, 4, "Aceptar", "Comunicación periódica con la Dirección General y la Gerencia de Cooperación", R_CG, date(2027, 12, 31), "Abierto", 2, 4),
    ("Externo", "Emergencias climáticas que interrumpen clases y entrega de apoyos", "Temporada de lluvias", 3, 3, "Mitigar", "Plan de contingencia y flexibilidad de calendarios", R_SOC, date(2027, 10, 15), "Abierto", 3, 2),
    ("Fiduciario", "Observaciones de auditoría por soporte de transferencias a beneficiarios", "Expedientes de elegibilidad incompletos", 3, 4, "Mitigar", "Expediente digital único y revisión muestral mensual", R_FIN, date(2027, 7, 15), "En mitigación", 2, 3),
    ("Técnico", "Dificultad para medir resultados (línea base y trayectorias)", "Sistemas de información fragmentados", 3, 4, "Mitigar", "Línea base temprana y definición de fuentes de verificación", R_PLAN, date(2027, 7, 15), "En mitigación", 2, 3),
]


def hoja_riesgos(wb):
    ws = wb.create_sheet("P1_Riesgos")
    titulo(ws, "P1 · Registro y matriz de riesgos (técnicos, fiduciarios, institucionales, ambientales y sociales)",
           "Puntaje = probabilidad × impacto (escala 1-5). Las columnas S-T son auxiliares para el ranking del informe mensual.")
    cols = [dict(h="ID", w=7), dict(h="Categoría", w=18), dict(h="Riesgo", w=44, wrap=True), dict(h="Causa / disparador", w=34, wrap=True),
            dict(h="Prob. (1-5)", w=8), dict(h="Impacto (1-5)", w=8), dict(h="Puntaje", w=8, fmt="0", tipo="calc"),
            dict(h="Nivel", w=9, tipo="calc"), dict(h="Respuesta", w=11), dict(h="Acción de mitigación", w=46, wrap=True),
            dict(h="Responsable", w=22), dict(h="Fecha límite", w=11, fmt=FECHA), dict(h="Estado", w=13),
            dict(h="Prob. residual", w=8), dict(h="Impacto residual", w=8), dict(h="Puntaje residual", w=9, fmt="0", tipo="calc"),
            dict(h="Nivel residual", w=9, tipo="calc"), dict(h="Días a la fecha límite", w=10, fmt="0", tipo="calc"),
            dict(h="Aux. puntaje", w=9, fmt="0.00000", tipo="calc"), dict(h="Ranking", w=8, fmt="0", tipo="calc")]
    filas = []
    for i, r in enumerate(RIESGOS):
        n = FIRST + i
        filas.append([f"R-{i + 1:02d}", r[0], r[1], r[2], r[3], r[4], f"=E{n}*F{n}",
                      f'=IF(G{n}>=Riesgo_Alto,"Alto",IF(G{n}>=Riesgo_Medio,"Medio","Bajo"))', r[5], r[6], r[7], r[8], r[9], r[10], r[11],
                      f"=N{n}*O{n}", f'=IF(P{n}>=Riesgo_Alto,"Alto",IF(P{n}>=Riesgo_Medio,"Medio","Bajo"))',
                      f'=IF(M{n}="Cerrado","",L{n}-Fecha_Corte)', f'=IF(M{n}="Cerrado",0,G{n}+(1000-ROW())/100000)',
                      f"=RANK(S{n},$S${FIRST}:$S$200)"])
    tabla(ws, cols, filas, altura=44)
    for col, lst in (("B", "Categoria_riesgo"), ("I", "Respuesta_riesgo"), ("K", "Responsable"), ("M", "Estado_riesgo"),
                     ("E", "Escala"), ("F", "Escala"), ("N", "Escala"), ("O", "Escala")):
        lista(ws, f"{col}{FIRST}:{col}200", "=" + REF[lst])
    semaforo(ws, f"H{FIRST}:H200", "Bajo", "Medio", "Alto")
    semaforo(ws, f"Q{FIRST}:Q200", "Bajo", "Medio", "Alto")
    return len(filas)


def hoja_focalizacion(wb):
    ws = wb.create_sheet("P2_Focalizacion")
    titulo(ws, "P2 · Focalización territorial: metas, cobertura e inversión por departamento",
           "Índice de focalización = W_Vuln×vulnerabilidad + W_Pob×población relativa + W_Brecha×brecha de cobertura (pesos en Parametros). "
           "Población y vulnerabilidad son valores sintéticos.")
    cols = [dict(h="Departamento", w=16, tipo="lbl"), dict(h="ISO 3166-2", w=9, tipo="lbl"), dict(h="Peso población objetivo", w=10, fmt="0.00"),
            dict(h="Vulnerabilidad (0-1)", w=11, fmt="0.00"), dict(h="Meta 5 años (personas)", w=11, fmt="#,##0"),
            dict(h="Meta año 1", w=10, fmt="#,##0", tipo="calc"), dict(h="Alcanzado acumulado", w=11, fmt="#,##0"),
            dict(h="Madres jóvenes", w=9, fmt="#,##0"), dict(h="Personas con discapacidad", w=11, fmt="#,##0"),
            dict(h="Retornadas/os", w=10, fmt="#,##0"), dict(h="Cobertura meta año 1", w=10, fmt=PCT, tipo="calc"),
            dict(h="Población relativa", w=10, fmt="0.00", tipo="calc"), dict(h="Brecha de cobertura", w=10, fmt="0.00", tipo="calc"),
            dict(h="Índice de focalización", w=11, fmt="0.00", tipo="calc"), dict(h="Prioridad", w=10, tipo="calc"),
            dict(h="Inversión ejecutada USD (territorializada)", w=16, fmt=USD, tipo="calc"),
            dict(h="USD por beneficiario", w=11, fmt=USD, tipo="calc"), dict(h="Ranking", w=8, fmt="0", tipo="calc")]
    B = dc.beneficiarios()
    last = FIRST + len(B) - 1
    filas = []
    for i, b in enumerate(B):
        n = FIRST + i
        filas.append([b["depto"], b["iso"], b["pob_peso"], b["vuln"], b["meta5"], f"=ROUND(E{n}*Pct_Anio1_Benef,0)", b["alcanzado"],
                      b["madres"], b["discap"], b["retornados"], f'=IF(F{n}=0,0,G{n}/F{n})', f"=C{n}/MAX($C${FIRST}:$C${last})",
                      f"=1-MIN(1,K{n})", f"=W_Vuln*D{n}+W_Pob*L{n}+W_Brecha*M{n}",
                      f'=IF(N{n}>=Prior_Alta,"Alta",IF(N{n}>=Prior_Media,"Media","Baja"))',
                      f'=SUMIFS({LEDG("J")},{LEDG("F")},A{n})', f'=IF(G{n}=0,"",P{n}/G{n})', f"=RANK(N{n},$N${FIRST}:$N${last})"])
    tabla(ws, cols, filas, altura=58)
    t = last + 1
    tot = {1: "NACIONAL", 3: f"=SUM(C{FIRST}:C{last})", 5: f"=SUM(E{FIRST}:E{last})", 6: f"=SUM(F{FIRST}:F{last})",
           7: f"=SUM(G{FIRST}:G{last})", 8: f"=SUM(H{FIRST}:H{last})", 9: f"=SUM(I{FIRST}:I{last})", 10: f"=SUM(J{FIRST}:J{last})",
           11: f"=G{t}/F{t}", 16: f"=SUM(P{FIRST}:P{last})", 17: f"=P{t}/G{t}"}
    for j in range(1, len(cols) + 1):
        c = ws.cell(t, j, tot.get(j))
        c.font, c.fill, c.border = f(True), C_SUB, BORDE
        c.number_format = cols[j - 1].get("fmt", "General")
    semaforo(ws, f"O{FIRST}:O{last}", "Baja", "Media", "Alta")
    nota(ws, t + 2, "La inversión territorializada solo incluye gastos con departamento asignado; los gastos «Nacional» (UGP, sistemas, campañas) no se reparten.")
    return len(B)
