"""Datos SINTÉTICOS de demostración (financiero y operativo).

Nada de lo que se genera aquí son cifras reales del BID ni de la Dirección de Integración.
Las únicas cifras tomadas del TDR son: montos del préstamo (US$100 M) y de la donación
(US$4 M), números de operación y condiciones de la consultoría.
La estructura de componentes es ILUSTRATIVA: debe sustituirse por la del Contrato de
Préstamo / MOP cuando se disponga de ellos.
"""
import random
from datetime import date, timedelta

SEMILLA = 2027
INICIO = date(2027, 1, 1)          # supuesto: inicio de ejecución
CORTE = date(2027, 6, 30)          # fecha de corte simulada (mes 6)
INICIO_CONSULTORIA = date(2027, 1, 4)

# ---------------------------------------------------------------- componentes
# (cod, nombre, préstamo 6153/OC-ES, donación 6154/GR-ES)
COMPONENTES = [
    ("C1", "Acceso y orientación", 13_500_000, 500_000),
    ("C2", "Permanencia y graduación", 44_000_000, 2_000_000),
    ("C3", "Vinculación laboral y trayectorias", 20_000_000, 0),
    ("C4", "Fortalecimiento institucional", 16_000_000, 1_000_000),
    ("C5", "Administración, M&E y auditoría", 6_500_000, 500_000),
]

R_ADQ, R_PLAN, R_FIN, R_SOC = ("Esp. Adquisiciones", "Esp. Planificación, M&S",
                               "Esp. Financiero", "Esp. Social")
R_CG = "Coordinador General"

# POA año 1: (id, comp, actividad, responsable, inicio, fin, presupuesto, %avance)
POA = [
    ("C1-01", "C1", "Diseño del modelo de captación y orientación vocacional", R_SOC, date(2027, 1, 15), date(2027, 3, 31), 130_000, 100),
    ("C1-02", "C1", "Convenios con centros de educación media", R_SOC, date(2027, 2, 1), date(2027, 5, 31), 160_000, 90),
    ("C1-03", "C1", "Campaña nacional de difusión", R_PLAN, date(2027, 3, 1), date(2027, 8, 31), 310_000, 58),
    ("C1-04", "C1", "Plataforma de registro de aspirantes", R_PLAN, date(2027, 2, 15), date(2027, 7, 15), 290_000, 78),
    ("C1-05", "C1", "Ferias de orientación departamentales", R_SOC, date(2027, 6, 1), date(2027, 11, 30), 140_000, 14),
    ("C2-01", "C2", "Esquema de apoyos y criterios de elegibilidad", R_SOC, date(2027, 1, 15), date(2027, 3, 15), 70_000, 100),
    ("C2-02", "C2", "Selección de la primera cohorte", R_SOC, date(2027, 3, 1), date(2027, 6, 15), 180_000, 85),
    ("C2-03", "C2", "Apoyos económicos primera cohorte", R_FIN, date(2027, 4, 1), date(2027, 12, 15), 900_000, 40),
    ("C2-04", "C2", "Acompañamiento socioeducativo (tutorías)", R_SOC, date(2027, 4, 15), date(2027, 12, 15), 420_000, 30),
    ("C2-05", "C2", "Servicios de accesibilidad para personas con discapacidad", R_SOC, date(2027, 5, 1), date(2027, 12, 15), 150_000, 24),
    ("C2-06", "C2", "Atención a madres jóvenes y personas retornadas", R_SOC, date(2027, 5, 1), date(2027, 12, 15), 80_000, 25),
    ("C3-01", "C3", "Diagnóstico de demanda laboral", R_PLAN, date(2027, 2, 1), date(2027, 5, 31), 195_000, 100),
    ("C3-02", "C3", "Alianzas con empleadores", R_SOC, date(2027, 4, 1), date(2027, 10, 31), 95_000, 38),
    ("C3-03", "C3", "Rutas de vinculación laboral", R_SOC, date(2027, 5, 1), date(2027, 9, 30), 120_000, 35),
    ("C3-04", "C3", "Piloto de prácticas profesionales", R_SOC, date(2027, 9, 1), date(2027, 12, 15), 90_000, 0),
    ("C4-01", "C4", "Diagnóstico institucional y plan de fortalecimiento", R_PLAN, date(2027, 1, 15), date(2027, 4, 30), 350_000, 100),
    ("C4-02", "C4", "Sistema de información de trayectorias", R_PLAN, date(2027, 3, 1), date(2027, 11, 30), 1_000_000, 38),
    ("C4-03", "C4", "Capacitación a instituciones de educación postsecundaria", R_SOC, date(2027, 5, 1), date(2027, 12, 15), 300_000, 5),
    ("C4-04", "C4", "Equipamiento tecnológico", R_ADQ, date(2027, 4, 1), date(2027, 10, 31), 650_000, 5),
    ("C5-01", "C5", "Conformación y operación de la UGP", R_CG, date(2027, 1, 4), date(2027, 12, 31), 400_000, 50),
    ("C5-02", "C5", "Plan de M&E y línea base", R_PLAN, date(2027, 1, 15), date(2027, 7, 15), 190_000, 65),
    ("C5-03", "C5", "Auditoría externa de estados financieros 2027", R_FIN, date(2027, 10, 1), date(2027, 12, 31), 90_000, 0),
    ("C5-04", "C5", "Gestión ambiental y social (marco y mecanismo de quejas)", R_SOC, date(2027, 2, 1), date(2027, 12, 15), 110_000, 40),
    ("C5-05", "C5", "Comunicación y gestión del conocimiento", R_PLAN, date(2027, 3, 1), date(2027, 12, 15), 80_000, 36),
]

# Plan de adquisiciones: (id, comp, actividad, descripción, categoría, método, revisión, estimado,
#                         estado, f_publ_prev, f_publ_real, f_adj_prev, f_adj_real)
D = date
PA = [
    ("PA-01", "C1", "C1-01", "Consultoría: diseño del modelo de captación", "Consultoría (firma)", "SBCC", "Ex ante", 125_000, "Contratado", D(2027, 2, 1), D(2027, 2, 2), D(2027, 3, 10), D(2027, 3, 9)),
    ("PA-02", "C1", "C1-04", "Plataforma de registro de aspirantes", "Servicios de no consultoría", "LPN", "Ex ante", 260_000, "Contratado", D(2027, 2, 15), D(2027, 2, 20), D(2027, 4, 15), D(2027, 4, 26)),
    ("PA-03", "C1", "C1-03", "Campaña nacional de difusión", "Servicios de no consultoría", "Comparación de precios", "Ex post", 300_000, "Contratado", D(2027, 3, 1), D(2027, 3, 3), D(2027, 4, 20), D(2027, 4, 22)),
    ("PA-04", "C2", "C2-01", "Consultoría individual: esquema de apoyos", "Consultor individual", "3CV", "Ex ante", 60_000, "Contratado", D(2027, 1, 18), D(2027, 1, 18), D(2027, 2, 15), D(2027, 2, 12)),
    ("PA-05", "C2", "C2-04", "Servicios de tutorías y acompañamiento", "Consultoría (firma)", "SBCC", "Ex ante", 400_000, "Contratado", D(2027, 3, 15), D(2027, 3, 18), D(2027, 5, 10), D(2027, 5, 24)),
    ("PA-06", "C2", "C2-05", "Equipamiento de accesibilidad", "Bienes", "LPN", "Ex ante", 240_000, "Publicado", D(2027, 5, 15), D(2027, 6, 1), D(2027, 8, 15), None),
    ("PA-07", "C3", "C3-01", "Consultoría: diagnóstico de demanda laboral", "Consultoría (firma)", "SBCC", "Ex ante", 190_000, "Contratado", D(2027, 2, 1), D(2027, 2, 3), D(2027, 3, 31), D(2027, 3, 29)),
    ("PA-08", "C3", "C3-02", "Consultoría individual: alianzas con empleadores", "Consultor individual", "3CV", "Ex ante", 70_000, "Contratado", D(2027, 3, 15), D(2027, 3, 16), D(2027, 4, 30), D(2027, 5, 7)),
    ("PA-09", "C4", "C4-01", "Consultoría: diagnóstico institucional", "Consultoría (firma)", "SBCC", "Ex ante", 340_000, "Contratado", D(2027, 1, 20), D(2027, 1, 22), D(2027, 3, 15), D(2027, 3, 12)),
    ("PA-10", "C4", "C4-02", "Sistema de información de trayectorias", "Servicios de no consultoría", "LPI", "Ex ante", 900_000, "Contratado", D(2027, 3, 1), D(2027, 3, 8), D(2027, 5, 15), D(2027, 5, 27)),
    ("PA-11", "C4", "C4-04", "Equipamiento tecnológico para instituciones", "Bienes", "LPI", "Ex ante", 600_000, "Evaluación", D(2027, 4, 15), D(2027, 5, 30), D(2027, 7, 15), None),
    ("PA-12", "C4", "C4-03", "Consultoría: capacitación a instituciones", "Consultoría (firma)", "SBCC", "Ex ante", 380_000, "Preparación", D(2027, 5, 15), None, D(2027, 8, 15), None),
    ("PA-13", "C5", "C5-01", "Coordinador(a) General de la UGP", "Consultor individual", "3CV", "Ex ante", 50_400, "Contratado", D(2026, 12, 1), D(2026, 12, 1), D(2027, 1, 4), D(2027, 1, 4)),
    ("PA-14", "C5", "C5-01", "Especialista Financiero", "Consultor individual", "3CV", "Ex ante", 48_000, "Contratado", D(2026, 12, 1), D(2026, 12, 1), D(2027, 1, 4), D(2027, 1, 11)),
    ("PA-15", "C5", "C5-01", "Especialista en Adquisiciones", "Consultor individual", "3CV", "Ex ante", 48_000, "Contratado", D(2026, 12, 1), D(2026, 12, 1), D(2027, 1, 4), D(2027, 1, 11)),
    ("PA-16", "C5", "C5-01", "Esp. en Planificación, Monitoreo y Seguimiento", "Consultor individual", "3CV", "Ex ante", 48_000, "Contratado", D(2026, 12, 1), D(2026, 12, 1), D(2027, 1, 4), D(2027, 1, 18)),
    ("PA-17", "C5", "C5-01", "Especialista Social", "Consultor individual", "3CV", "Ex ante", 48_000, "Contratado", D(2026, 12, 1), D(2026, 12, 1), D(2027, 1, 4), D(2027, 1, 18)),
    ("PA-18", "C5", "C5-03", "Firma auditora de estados financieros 2027", "Consultoría (firma)", "SBCC", "Ex ante", 85_000, "Publicado", D(2027, 5, 15), D(2027, 6, 10), D(2027, 9, 15), None),
    ("PA-19", "C5", "C5-02", "Consultoría: línea base y plan de M&E", "Consultoría (firma)", "SBCC", "Ex ante", 150_000, "Contratado", D(2027, 1, 25), D(2027, 1, 27), D(2027, 3, 15), D(2027, 3, 22)),
    ("PA-20", "C5", "C5-04", "Consultoría individual: gestión ambiental y social", "Consultor individual", "3CV", "Ex ante", 36_000, "Contratado", D(2027, 1, 25), D(2027, 1, 25), D(2027, 2, 28), D(2027, 3, 1)),
]

# Contratos: (id, pa, actividad, proveedor, objeto, monto, firma, fin, %pagado, mecanismo)
CONTRATOS = [
    ("CT-01", "PA-01", "C1-01", "Consultora Alfa (ficticia)", "Diseño del modelo de captación", 118_000, D(2027, 3, 12), D(2027, 6, 30), 100, "Anticipo de fondos"),
    ("CT-02", "PA-02", "C1-04", "Tecnologías Beta (ficticia)", "Plataforma de registro", 248_500, D(2027, 5, 5), D(2027, 12, 31), 60, "Pago directo"),
    ("CT-03", "PA-03", "C1-03", "Comunicaciones Gamma (ficticia)", "Campaña nacional de difusión", 285_000, D(2027, 4, 28), D(2027, 9, 30), 50, "Pago directo"),
    ("CT-04", "PA-04", "C2-01", "Consultor individual 1 (ficticio)", "Esquema de apoyos", 58_800, D(2027, 2, 16), D(2027, 5, 31), 100, "Anticipo de fondos"),
    ("CT-05", "PA-05", "C2-04", "Fundación Delta (ficticia)", "Tutorías y acompañamiento", 395_000, D(2027, 5, 28), D(2027, 12, 15), 30, "Anticipo de fondos"),
    ("CT-06", "PA-07", "C3-01", "Estudios Épsilon (ficticia)", "Diagnóstico de demanda laboral", 185_000, D(2027, 4, 5), D(2027, 6, 15), 100, "Anticipo de fondos"),
    ("CT-07", "PA-08", "C3-02", "Consultor individual 2 (ficticio)", "Alianzas con empleadores", 68_000, D(2027, 5, 10), D(2027, 10, 31), 40, "Anticipo de fondos"),
    ("CT-08", "PA-09", "C4-01", "Consultora Zeta (ficticia)", "Diagnóstico institucional", 332_000, D(2027, 3, 16), D(2027, 5, 31), 100, "Anticipo de fondos"),
    ("CT-09", "PA-10", "C4-02", "Sistemas Eta (ficticia)", "Sistema de información de trayectorias", 871_000, D(2027, 6, 1), D(2027, 11, 30), 35, "Pago directo"),
    ("CT-10", "PA-13", "C5-01", "Coordinador(a) General UGP", "Consultoría individual (TDR: US$50,400)", 50_400, D(2027, 1, 4), D(2027, 12, 31), 50, "Anticipo de fondos"),
    ("CT-11", "PA-14", "C5-01", "Especialista Financiero", "Consultoría individual", 48_000, D(2027, 1, 11), D(2027, 12, 31), 50, "Anticipo de fondos"),
    ("CT-12", "PA-15", "C5-01", "Especialista en Adquisiciones", "Consultoría individual", 48_000, D(2027, 1, 11), D(2027, 12, 31), 50, "Anticipo de fondos"),
    ("CT-13", "PA-16", "C5-01", "Esp. Planificación, M&S", "Consultoría individual", 48_000, D(2027, 1, 18), D(2027, 12, 31), 50, "Anticipo de fondos"),
    ("CT-14", "PA-17", "C5-01", "Especialista Social", "Consultoría individual", 48_000, D(2027, 1, 18), D(2027, 12, 31), 50, "Anticipo de fondos"),
    ("CT-15", "PA-19", "C5-02", "Evaluaciones Theta (ficticia)", "Línea base y plan de M&E", 146_000, D(2027, 3, 25), D(2027, 7, 15), 70, "Anticipo de fondos"),
    ("CT-16", "PA-20", "C5-04", "Consultor individual 3 (ficticio)", "Gestión ambiental y social", 36_000, D(2027, 3, 1), D(2027, 12, 15), 50, "Anticipo de fondos"),
]

# Gastos directos (sin contrato): actividad -> [(concepto, categoría, monto, territorial?)]
DIRECTOS = {
    "C1-01": [("Talleres de validación del modelo", "Servicios de no consultoría", 6_000, False)],
    "C1-02": [("Logística de reuniones y convenios regionales", "Servicios de no consultoría", 128_000, True)],
    "C1-03": [("Producción de materiales de difusión", "Bienes", 20_000, False)],
    "C1-04": [("Licencias y alojamiento en la nube", "Bienes", 50_000, False)],
    "C1-05": [("Preparación de ferias de orientación", "Servicios de no consultoría", 14_000, True)],
    "C2-01": [("Talleres de consulta de criterios", "Servicios de no consultoría", 5_000, False)],
    "C2-02": [("Operativo de selección y verificación", "Servicios de no consultoría", 150_000, True)],
    "C2-03": [("Apoyos económicos a beneficiarios", "Transferencias a beneficiarios", 330_000, True)],
    "C2-04": [("Materiales de acompañamiento", "Bienes", 20_000, True)],
    "C2-05": [("Consultas y ajustes razonables", "Servicios de no consultoría", 34_000, True)],
    "C2-06": [("Apoyos complementarios", "Transferencias a beneficiarios", 19_000, True)],
    "C3-01": [("Levantamiento de información", "Servicios de no consultoría", 4_000, False)],
    "C3-02": [("Encuentros con empleadores", "Servicios de no consultoría", 12_000, False)],
    "C3-03": [("Talleres de diseño de rutas", "Servicios de no consultoría", 40_000, True)],
    "C4-01": [("Talleres con instituciones", "Servicios de no consultoría", 6_000, False)],
    "C4-02": [("Infraestructura y pruebas", "Bienes", 40_000, False)],
    "C4-03": [("Preparación de convocatorias", "Servicios de no consultoría", 15_000, False)],
    "C4-04": [("Especificaciones técnicas", "Servicios de no consultoría", 25_000, False)],
    "C5-01": [("Equipo de oficina y servicios", "Costos operativos", 40_000, False),
              ("Viáticos y transporte a campo", "Costos operativos", 30_000, False)],
    "C5-02": [("Trabajo de campo línea base", "Servicios de no consultoría", 15_000, False)],
    "C5-04": [("Capacitación y mecanismo de quejas", "Servicios de no consultoría", 20_000, False)],
    "C5-05": [("Productos de comunicación", "Servicios de no consultoría", 28_000, False)],
}
FUENTE_DONACION = {"C1-05", "C2-05", "C2-06", "C4-03", "C5-04"}   # resto: préstamo

DEPTOS = [  # (nombre, ISO, peso población objetivo, vulnerabilidad sintética 0-1)
    ("Ahuachapán", "SV-AH", 0.06, 0.72), ("Cabañas", "SV-CA", 0.03, 0.76),
    ("Chalatenango", "SV-CH", 0.04, 0.70), ("Cuscatlán", "SV-CU", 0.04, 0.52),
    ("La Libertad", "SV-LI", 0.12, 0.42), ("La Paz", "SV-PA", 0.05, 0.60),
    ("La Unión", "SV-UN", 0.05, 0.74), ("Morazán", "SV-MO", 0.03, 0.78),
    ("San Miguel", "SV-SM", 0.09, 0.58), ("San Salvador", "SV-SS", 0.22, 0.35),
    ("San Vicente", "SV-SV", 0.04, 0.66), ("Santa Ana", "SV-SA", 0.10, 0.55),
    ("Sonsonate", "SV-SO", 0.07, 0.62), ("Usulután", "SV-US", 0.06, 0.68),
]
META_BENEF_5A = 60_000
ALCANZADO_CORTE = 2_380
