# 02 · Justificación de las herramientas de control elegidas

Este documento explica **por qué** cada herramienta existe, qué pregunta de gestión responde y qué se descartó. Parte de una idea: en un programa con financiamiento externo, un instrumento de control solo vale si (a) responde una decisión concreta, (b) tiene un responsable y una frecuencia, y (c) se reconcilia con los demás instrumentos.

## 1. Principios de diseño

| Principio | Cómo se aplicó |
|---|---|
| **Una sola fuente por dato** | La ejecución financiera vive solo en `F2_Ejecucion` (libro de gastos). El avance por actividad, por componente, por contrato, por departamento y los desembolsos por pago directo se calculan desde ese libro. |
| **Separar lo que se ingresa de lo que se calcula** | Azul = dato ingresado; negro sobre gris = fórmula. Se evita que alguien «pise» una fórmula. |
| **Parámetros visibles, no escondidos en fórmulas** | Umbrales, fecha de corte y pesos están en `Parametros` con nombres definidos (`Fecha_Corte`, `Umbral_Verde`, `Pct_Justif_Min`, …). Cambiar un umbral cambia todos los semáforos. |
| **Reconciliación automática** | `Controles` ejecuta 16 pruebas entre hojas. Si una falla, el informe mensual no debe emitirse. |
| **Alertas, no solo cifras** | Cada hoja produce un estado (semáforo o texto) que alimenta el `Tablero`. |
| **Datos reproducibles** | Los datos simulados salen de un generador con semilla fija; cualquiera puede reconstruir el libro. |

## 2. Por pilar

### Pilar 1 · Planificación y control integral

| Herramienta | Decisión que habilita | Por qué esta y no otra |
|---|---|---|
| `P1_POA` con **valor ganado** (PV, EV, AC, SPI, CPI) | ¿Qué actividades se atrasan o se encarecen y cuánto? | El porcentaje de avance solo no distingue «voy atrasado» de «gasté más». El valor ganado separa cronograma (SPI) y costo (CPI) con tres columnas simples. Se limitó a nivel de actividad del POA para mantenerlo auditable en Excel. |
| `P1_Avance_FF` | ¿Cómo va cada componente, física y financieramente? | La comparación física vs. financiera detecta gasto sin producto y producto sin gasto. |
| `P1_Resultados` | ¿Los indicadores van al ritmo de la meta anual? | Compara contra lo **esperado a la fecha de corte**, no contra la meta final, para que el semáforo no sea rojo hasta diciembre. |
| `P1_Riesgos` con matriz **probabilidad × impacto (5×5)** | ¿Qué riesgos exigen acción y escalamiento? | Escala ordinal y mapa de calor: simple de explicar al equipo y al BID. Incluye respuesta, responsable y riesgo residual. |
| `P2_Focalizacion` con índice ponderado | ¿Dónde priorizar la expansión territorial? | Índice transparente (vulnerabilidad 50%, población 20%, brecha de cobertura 30%; pesos en `Parametros`). Se prefirió un índice explicable a un modelo opaco. |

**Descartado:** diagrama de Gantt completo en Excel (se vuelve inmanejable en 24+ actividades; se recomienda MS Project, Smartsheet u otra herramienta institucional si el POA crece) y un modelo estadístico de riesgo (no hay datos históricos para calibrarlo).

### Pilar 2 · Gestión fiduciaria

| Herramienta | Decisión que habilita | Por qué esta y no otra |
|---|---|---|
| `F1_Presupuesto_PEP` | ¿El plan plurianual cubre el 100% de cada componente y fuente? | Verifica que PEP a 5 años = asignación; evita componentes sobre o sub-asignados. |
| `F2_Ejecucion` (libro de gastos) | ¿Qué se gastó, con qué fuente, contrato, actividad y mecanismo de pago? | La trazabilidad por gasto es lo que pide una auditoría; todo lo demás se deriva de aquí. |
| `F3_Desembolsos` con **control del anticipo** | ¿Puedo pedir otro anticipo o primero debo justificar? | La regla de un mínimo de justificación (80% en la demostración, a validar) es una de las más frecuentes en operaciones BID. Se ve el saldo por justificar de forma inmediata. |
| `F3_Plan_Financiero` | ¿Voy en línea con la proyección trimestral? | La proyección de desembolsos es un compromiso con el BID; esta hoja la compara con lo real. |
| `F4_Plan_Adquisiciones` | ¿Qué procesos están atrasados o próximos a vencer? | La alerta por fecha incluye el caso «sin publicar y ya pasó la fecha», que suele pasar inadvertido. |
| `F5_Contratos` | ¿Cuánto se ha pagado, cuánto falta y qué vence? | Impide pagos mayores al monto contratado (control 8). |
| `F6_Auditoria` | ¿Qué recomendaciones siguen abiertas? | Calendario de estados financieros auditados y seguimiento de plan de acción. |

**Descartado:** un sistema contable propio. Los registros contables oficiales siguen en el sistema institucional. El libro de gastos es un **registro de control gerencial**, no sustituye la contabilidad oficial.

### Pilar 3 · Cumplimiento normativo

| Herramienta | Decisión que habilita | Por qué esta y no otra |
|---|---|---|
| `N1_Cumplimiento` (19 obligaciones) | ¿Qué obligaciones contractuales, del MOP o de políticas BID vencen y quién responde? | Una matriz única con fuente, fecha, responsable, estado y alerta es más práctica que leer el contrato cada vez. Distingue «exigible a la fecha» de «por evento». |
| Porcentaje de cumplimiento de obligaciones exigibles | ¿Estamos cumpliendo lo que ya vence? | Mide solo lo exigible para no inflar ni deprimir el indicador. |

**Importante:** las obligaciones, fechas y plazos de esta matriz son **ilustrativos**. Antes de usarla en un Programa real hay que construirla desde el Contrato, el MOP y el plan de ejecución aprobado.

### Pilar 4 · Articular y reportar

| Herramienta | Decisión que habilita | Por qué esta y no otra |
|---|---|---|
| `A1_Equipo` y `A1_RACI` | ¿Quién responde por cada proceso? | El chequeo de «una sola A» por proceso evita procesos sin dueño o con dos. |
| `A2_Misiones_BID` | ¿Qué compromisos de misiones siguen pendientes? | Convierte el aide-mémoire en una matriz de compromisos con fechas. |
| `A3_No_Objeciones` | ¿Cuánto tarda cada trámite y cuáles exceden el plazo? | Mide el tiempo de respuesta y permite anticipar el efecto en el cronograma. |
| `A4_Interesados` | ¿Cómo gestiono a cada actor? | Matriz poder/interés con estrategia y frecuencia. |
| `A5_Calendario_Informes` | ¿Estoy entregando P1–P12 a tiempo? | El pago mensual depende del informe; la puntualidad se vuelve un indicador. |
| `A6_Informe_Mensual` | ¿Puedo emitir el informe en tres días hábiles? | Se arma con fórmulas desde el resto del libro, con el contenido mínimo del TDR. |

## 3. Herramientas transversales

| Herramienta | Función |
|---|---|
| `Tablero` | 16 indicadores clave con semáforo, mapa de calor de riesgos y tres gráficos. Una página para el comité. |
| `Controles` | 16 pruebas de integridad entre hojas (suma de componentes = US$104 M, PEP = asignación, pagos ≤ contrato, gasto dentro del período, etc.). |
| `Parametros` / `Listas` | Una sola fuente para umbrales y listas desplegables. |

## 4. Por qué Excel + Python y no solo uno

| Necesidad | Excel | Python (Streamlit) |
|---|---|---|
| Carga y corrección diaria por especialistas | **Sí**: lo conocen, no requiere instalación | No es el medio adecuado |
| Reglas de validación y semáforos visibles | **Sí**: fórmulas auditables | Duplicaría la lógica |
| Visualización nacional, mapa y filtros | Limitado | **Sí**: mapa de focalización interactivo |
| Prueba automatizada de consistencia | No | **Sí**: `pytest` recalcula en pandas y compara con Excel |
| Reproducibilidad y control de versiones | Parcial | **Sí**: código en Git |

El diseño es: **Excel es el sistema de registro; Python es la capa de visualización y de verificación**. El dashboard lee el libro y recomputa los indicadores por separado; una prueba falla si ambos cálculos discrepan.

## 5. Qué evolucionaría en un Programa real

1. Conectar el libro a los sistemas institucionales (extracciones del sistema contable y del Plan de Adquisiciones en línea).
2. Pasar de Excel a una base de datos cuando el volumen de registros lo exija (> 10.000 gastos).
3. Agregar control de acceso por rol (hoy, protección por convención y por colores).
4. Alinear los formatos con las plantillas oficiales del BID y el MOP vigente.
5. Evaluar herramientas institucionales para el cronograma detallado.
