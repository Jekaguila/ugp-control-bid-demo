# 03 · Protocolo de control, ciclo mensual y escalamiento

Cómo se **usa** el sistema: quién hace qué, cuándo, con qué umbrales y a quién se escala. Los umbrales son supuestos parametrizados en la hoja `Parametros`.

## 1. Ciclo mensual (compatible con el informe en tres días hábiles)

| Momento | Actividad | Responsable | Herramienta |
|---|---|---|---|
| Durante el mes | Registrar cada gasto en las 48 h siguientes al pago | Esp. Financiero | `F2_Ejecucion` |
| Durante el mes | Actualizar estados de procesos y contratos | Esp. Adquisiciones | `F4`, `F5`, `A3` |
| Semana 4 | Actualizar % de avance físico de actividades, indicadores y riesgos | Esp. Planificación M&S | `P1_POA`, `P1_Resultados`, `P1_Riesgos` |
| Semana 4 | Actualizar avance territorial y cobertura | Esp. Social | `P2_Focalizacion` |
| Último día hábil | Fijar la **fecha de corte** | Coordinador General | `Parametros` |
| Día hábil 1 | Revisar la hoja `Controles`; corregir hasta que todo esté en OK | Esp. Planificación M&S | `Controles` |
| Día hábil 1 | Revisar alertas de cumplimiento y vencimientos | Coordinador General | `N1_Cumplimiento` |
| Día hábil 2 | Revisar el borrador automático del informe y completar los textos | Coordinador General | `A6_Informe_Mensual` |
| Día hábil 3 | Entregar el informe a la Gerencia de Cooperación Institucional | Coordinador General | `A5_Calendario_Informes` |
| Mensual | Reunión de seguimiento con minuta y compromisos | Coordinador General | `Minuta_Seguimiento` |

## 2. Semáforos y umbrales

| Indicador | Verde | Amarillo | Rojo | Parámetro |
|---|---|---|---|---|
| Cumplimiento de indicadores vs. esperado a la fecha | ≥ 90% | 70–89% | < 70% | `Umbral_Verde`, `Umbral_Amarillo` |
| SPI y CPI | ≥ 0,95 | 0,85–0,94 | < 0,85 | `EVM_Verde`, `EVM_Amarillo` |
| Riesgo (P×I, escala 1–25) | < 8 (bajo) | 8–14 (medio) | ≥ 15 (alto) | `Riesgo_Medio`, `Riesgo_Alto` |
| Anticipos justificados | ≥ 80% | — | < 80% (no pedir otro anticipo) | `Pct_Justif_Min` |
| Obligaciones normativas | Cumplida / en plazo | Próxima a vencer (≤ 30 días) | Vencida | `Dias_Alerta` |
| Plan de Adquisiciones | En plazo / a tiempo | Próximo a vencer | Atrasado | `Dias_Alerta` |
| No Objeción | Dentro del plazo de referencia (15 días) | — | Fuera del plazo | `Plazo_NO` |

## 3. Reglas de decisión y escalamiento

| Situación | Acción inmediata | Escala a | Plazo |
|---|---|---|---|
| Algún control en `Controles` ≠ OK | No emitir informe; corregir causa | Coordinador General | Mismo día |
| SPI o CPI en rojo en un componente | Plan correctivo con responsable y fecha | Gerencia de Cooperación Institucional | Informe del mes |
| Riesgo alto abierto | Responsable y respuesta definidos; revisar semanalmente | Dirección General | Informe del mes |
| Anticipos < umbral de justificación | Congelar nuevas solicitudes; priorizar justificación | Dirección General y equipo del BID | Antes de la siguiente solicitud |
| Proceso de adquisición atrasado | Solicitud de cambio al CCB; ajustar el PA | Coordinador General | Quincena |
| No Objeción fuera de plazo | Seguimiento formal al BID; evaluar efecto en cronograma | Coordinador General | Semana siguiente |
| Obligación vencida | Plan de regularización y comunicación al BID si aplica | Dirección General | Informe del mes |
| Hallazgo de auditoría sin plan | Plan de acción con fecha | Gerencia de Cooperación Institucional | 15 días |
| Incidente de alta prioridad | Registro, responsable y reporte en el informe | Gerencia de Cooperación Institucional | 48 h |

## 4. Control de cambios

1. Todo cambio de alcance, cronograma, presupuesto o PA se registra en `Solicitud_Cambios` / `Registro_Cambios`.
2. El CCB (Coordinador, Esp. Financiero, Esp. Adquisiciones, Esp. Planificación M&S, Esp. Social) decide.
3. Si el cambio modifica el PA, el POA/PEP o las categorías de inversión, se identifica la necesidad de **No Objeción** y se registra en `A3_No_Objeciones`.
4. Los cambios aprobados actualizan, en este orden: `Parametros` (si aplica) → POA/PEP → PA → informe.

## 5. Trazabilidad TDR → herramienta

| Función del TDR | Qué demuestra | Hojas |
|---|---|---|
| F1 · Gerenciar y liderar la UGP | Estructura, roles y responsabilidades | `A1_Equipo`, `A1_RACI`, `Acta_Constitucion` |
| F2 · Punto focal con el BID | Misiones, compromisos y trámites | `A2_Misiones_BID`, `A3_No_Objeciones`, `Solicitud_No_Objecion`, `Minuta_Seguimiento` |
| F3 · Articulación institucional | Interesados y comunicación | `A4_Interesados` |
| F4 · Planificación y control integral | Avance, indicadores, hitos, riesgos | `P1_POA`, `P1_Avance_FF`, `P1_Resultados`, `P1_Riesgos`, `P2_Focalizacion`, `Tablero` |
| F5 · Supervisión fiduciaria | Presupuesto, desembolsos, adquisiciones, contratos, auditoría | `F1`–`F6` |
| F6 · Cumplimiento contractual y normativo; informes | Obligaciones y reportes | `N1_Cumplimiento`, `A5_Calendario_Informes`, `A6_Informe_Mensual` |
| F7 · Decisiones, riesgos y cierre | Control de cambios, incidentes, lecciones, cierre | `Registro_Cambios`, `Registro_Incidentes`, `Lecciones_Aprendidas`, `Reporte_Cierre` |
| F8 · Apoyo a la DI | Fuera del sistema de control | — |

| Producto del TDR | Hoja |
|---|---|
| P1 Plan de trabajo e informe | `A5_Calendario_Informes`, `Acta_Constitucion` |
| P2–P11 Informe mensual | `A6_Informe_Mensual` + `Tablero` |
| P12 Informe anual | `A5_Calendario_Informes` (plazo), `P1_Resultados` (cierre del año) |

## 6. Pruebas de integridad (hoja `Controles`)

| N.º | Control |
|---|---|
| 1–3 | Los componentes suman US$104 M; préstamo US$100 M; donación US$4 M |
| 4 | El PEP a 5 años de cada componente coincide con su asignación |
| 5 | El plan financiero del año 1 coincide con el presupuesto del POA |
| 6 | La ejecución acumulada no supera el presupuesto |
| 7 | Ninguna actividad ejecuta más de su presupuesto |
| 8 | Ningún contrato recibe pagos mayores a su monto |
| 9 | El componente del gasto coincide con el de su actividad |
| 10 | Todos los gastos están dentro del período [inicio, corte] |
| 11–12 | Todo gasto referencia un contrato y una actividad existentes |
| 13 | Los pagos directos del libro igualan las solicitudes de desembolso por pago directo |
| 14 | La meta nacional de beneficiarios es la suma de los departamentos |
| 15 | La inversión territorializada no supera la ejecución total |
| 16 | Cada proceso del RACI tiene exactamente una «A» |

La misma lógica se verifica de forma independiente en Python (`dashboard/tests/test_consistencia.py`).
