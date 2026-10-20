# 04 · Supuestos, limitaciones y datos simulados

Leer antes de usar o compartir este repositorio.

## 1. Qué es y qué no es

- **Es** una demostración metodológica: cómo se controlaría, con herramientas simples y auditables, un Programa BID de US$104 millones desde una UGP.
- **No es** información oficial del BID, de la Dirección de Integración ni del Gobierno de El Salvador.
- **No acredita** experiencia previa en proyectos financiados por el BID. El TDR exige, como **factor habilitante**, experiencia en al menos un programa con financiamiento externo, que se demuestra con documentos (cartas, constancias, contratos). Este repositorio muestra método y criterio; no reemplaza esa evidencia.

## 2. Qué proviene del TDR (hechos citados)

| Dato | Valor |
|---|---|
| Operaciones | ES-L1175 y ES-J0003; CCLIP ES-O0023 |
| Contrato de Préstamo / Convenio | 6153/OC-ES (US$100.000.000) / 6154/GR-ES (US$4.000.000) |
| Resolución | DE-43/26, 24 de junio de 2026 |
| Organismo Ejecutor / unidad | Dirección de Integración / Gerencia de Cooperación Institucional |
| Duración del Programa | 5 años |
| Consultoría | 12 meses, US$4.200 mensuales (total US$50.400) |
| Productos | P1 a P12; informe mensual en tres días hábiles |
| Criterios 3CV | Los de la sección XV del TDR |

## 3. Qué es simulado o supuesto

| Elemento | Naturaleza |
|---|---|
| Componentes C1–C5, su nombre y su monto | **Ilustrativos.** El TDR no los enumera. |
| POA (24 actividades), Plan de Adquisiciones (20 procesos), contratos, libro de gastos, desembolsos | **Sintéticos**, generados con semilla fija (2027) en `scripts/datos_demo.py` |
| Fecha de inicio (1/1/2027) y fecha de corte (30/6/2027) | **Supuestos** |
| Metas e indicadores, beneficiarios por departamento, vulnerabilidad | **Sintéticos** |
| Umbrales: 80% de justificación de anticipos, 15 días de No Objeción, 120 días para EEFF auditados, semáforos | **Supuestos** a validar contra el Contrato y el MOP |
| Obligaciones de la matriz N1 | **Ilustrativas**; en un Programa real se construyen desde el Contrato, el MOP y los planes aprobados |
| Misiones, compromisos, interesados, riesgos | **Ilustrativos** |
| Nombres de personas y firmas | **No se usan** (solo roles) |

Todas las hojas del Excel llevan el aviso «DATOS SIMULADOS» en la fila 2; el dashboard lo muestra en la parte superior.

## 4. Limitaciones técnicas

1. El libro es una herramienta de control gerencial. **No sustituye** la contabilidad oficial ni los sistemas del BID.
2. El Excel usa fórmulas compatibles con Excel 2016+ y LibreOffice; no usa funciones dinámicas (XLOOKUP, FILTER) para evitar incompatibilidades.
3. La protección es por convención (colores y validaciones), no por control de acceso.
4. El valor ganado se calcula por actividad con avance lineal en el tiempo (`% planificado` proporcional a los días). Para hitos no lineales conviene un perfil de avance propio.
5. El índice de focalización es transparente pero simplificado; los pesos (50/20/30) son supuestos.
6. El mapa usa límites departamentales de Natural Earth (dominio público), simplificados para visualización.
7. El dashboard lee valores calculados guardados en el libro; si el archivo se generó sin abrirse en Excel/LibreOffice, no tendrá valores en caché.

## 5. Datos personales y confidencialidad

- El repositorio **no contiene datos personales** de beneficiarios ni de funcionarios.
- Para un Programa real, la analítica territorial debe hacerse con **agregados** (por departamento o municipio), con reglas de supresión de celdas pequeñas y bajo las políticas de protección de datos aplicables.
- El TDR incluye cláusulas de confidencialidad y propiedad intelectual: los documentos y datos producidos para un contrato son del contratante. No publicar información de un Programa real sin autorización escrita.

## 6. Cómo se verifica

| Verificación | Dónde |
|---|---|
| 16 pruebas de integridad en el Excel | Hoja `Controles` |
| Cálculo independiente en pandas vs. Excel | `dashboard/tests/test_consistencia.py` (`python -m pytest -q`) |
| Cero errores de fórmula tras recalcular con LibreOffice | Proceso de construcción (`scripts/`) |

## 7. Uso responsable en una postulación

- Presentar el repositorio como **portafolio de método** («sé cómo se estructura y se controla un Programa BID»), no como experiencia ejecutada.
- No describir los datos simulados como resultados reales.
- Acompañar el enlace con la evidencia documental real de experiencia en proyectos con fondos externos o públicos (constancias, contratos, cartas).
- Si se menciona el enlace en el currículo, usar una frase como: *«Repositorio de demostración con datos simulados: sistema de control para un Programa BID de US$104 M»*.
