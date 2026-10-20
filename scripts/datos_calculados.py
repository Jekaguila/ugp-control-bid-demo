"""Derivaciones reproducibles (semilla fija) a partir de datos_demo: PEP, libro de gastos y beneficiarios."""
import random
from datetime import timedelta
from datos_demo import *  # noqa: F401,F403


def pep():
    """Plan de Ejecución Plurianual por componente y año (USD).
    El año 1 es la suma de las actividades del POA; años 2-5 reparten el remanente."""
    y1 = {c: sum(a[6] for a in POA if a[1] == c) for c, *_ in COMPONENTES}
    out = {}
    for cod, _, pre, don in COMPONENTES:
        total, rem = pre + don, pre + don - y1[cod]
        sh = [0.22, 0.30, 0.28, 0.20]
        v = [int(round(rem * s, -4)) for s in sh[:3]]
        v.append(rem - sum(v))
        out[cod] = [y1[cod]] + v
        assert sum(out[cod]) == total, cod
    return out


def _dia_habil(d):
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d


def _partir(monto, n, rng):
    if n == 1:
        return [monto]
    cortes = sorted(rng.uniform(0.2, 0.8) for _ in range(n - 1))
    pesos = [b - a for a, b in zip([0] + cortes, cortes + [1])]
    partes = [int(round(monto * p, -1)) for p in pesos[:-1]]
    partes.append(monto - sum(partes))
    return partes


def libro_gastos():
    """Libro de gastos del año 1 hasta la fecha de corte (cada fila: dict)."""
    rng = random.Random(SEMILLA)
    contratos = {c[2]: [] for c in CONTRATOS}
    for c in CONTRATOS:
        contratos[c[2]].append(c)
    filas = []
    pesos_dep = [d[2] for d in DEPTOS]
    for act in POA:
        aid, comp, nombre, _, ini, fin, _, _ = act
        ventana_ini = max(ini, INICIO) + timedelta(days=12)
        ventana_fin = CORTE - timedelta(days=2)
        items = []
        for ct in contratos.get(aid, []):
            pagado = int(round(ct[5] * ct[8] / 100, -1))
            n = 1 if pagado < 80_000 or ct[8] == 100 and pagado < 150_000 else 2
            if aid == "C5-01":
                n = 3
            for k, p in enumerate(_partir(pagado, n, rng)):
                items.append((f"Pago {ct[4]} ({k + 1}/{n})", "Consultoría" if ct[1] not in ("PA-02", "PA-03", "PA-10") else "Servicios de no consultoría",
                              p, ct[0], ct[9], False))
        for conc, cat, monto, terr in DIRECTOS.get(aid, []):
            if aid == "C2-03":      # apoyos económicos: una transferencia por departamento, proporcional a beneficiarios
                bs = beneficiarios()
                tot_b = sum(b["alcanzado"] for b in bs)
                partes = [int(round(monto * b["alcanzado"] / tot_b, -1)) for b in bs]
                partes[-1] += monto - sum(partes)
                for b, p in zip(bs, partes):
                    items.append((conc + " — " + b["depto"], cat, p, "", "Anticipo de fondos", b["depto"]))
                continue
            n = 3 if monto >= 100_000 else (2 if monto >= 20_000 else 1)
            for k, p in enumerate(_partir(monto, n, rng)):
                items.append((conc + (f" ({k + 1}/{n})" if n > 1 else ""), cat, p, "", "Anticipo de fondos", terr))
        n_items = len(items)
        span = max((ventana_fin - ventana_ini).days, 1)
        for i, (conc, cat, monto, ct, mec, terr) in enumerate(items):
            f = _dia_habil(ventana_ini + timedelta(days=int(span * (i + 1) / (n_items + 1))))
            dep = terr if isinstance(terr, str) else (rng.choices([d[0] for d in DEPTOS], weights=pesos_dep)[0] if terr else "Nacional")
            filas.append(dict(fecha=f, comp=comp, act=aid, contrato=ct, depto=dep, concepto=conc,
                              categoria=cat, fuente="Donación" if aid in FUENTE_DONACION else "Préstamo",
                              monto=monto, mecanismo=mec))
    filas.sort(key=lambda r: (r["fecha"], r["act"]))
    for n, r in enumerate(filas, 1):
        r["id"] = f"G-{n:04d}"
        r["estado"] = "Por pagar" if (CORTE - r["fecha"]).days <= 10 and r["contrato"] else "Pagado"
        r["justificado"] = "N/A" if r["mecanismo"] == "Pago directo" else ("Sí" if r["fecha"] <= date(2027, 5, 31) else "No")
    return filas


def beneficiarios():
    """Metas y avance por departamento (sintético). Devuelve lista de dicts."""
    rng = random.Random(SEMILLA + 1)
    base = [d[2] * (0.6 + 0.8 * d[3]) for d in DEPTOS]
    tot = sum(base)
    metas = [round(META_BENEF_5A * b / tot, -1) for b in base]
    metas[9] += META_BENEF_5A - sum(metas)
    alc_base = [m * rng.uniform(0.85, 1.15) * (0.7 if DEPTOS[i][3] > 0.7 else 1.0) for i, m in enumerate(metas)]
    s = sum(alc_base)
    alc = [int(round(ALCANZADO_CORTE * a / s)) for a in alc_base]
    alc[9] += ALCANZADO_CORTE - sum(alc)
    out = []
    for (nom, iso, pw, vul), m, a in zip(DEPTOS, metas, alc):
        out.append(dict(depto=nom, iso=iso, pob_peso=pw, vuln=vul, meta5=int(m), alcanzado=a,
                        madres=int(round(a * rng.uniform(0.07, 0.11))),
                        discap=int(round(a * rng.uniform(0.03, 0.05))),
                        retornados=int(round(a * rng.uniform(0.02, 0.04)))))
    return out


if __name__ == "__main__":
    p = pep()
    print("PEP año1..5 por comp:", {k: v for k, v in p.items()})
    print("Total Y1:", sum(v[0] for v in p.values()))
    g = libro_gastos()
    tot = sum(r["monto"] for r in g)
    print("Filas libro:", len(g), "| Ejecutado:", tot)
    pd_ = sum(r["monto"] for r in g if r["mecanismo"] == "Anticipo de fondos" and r["estado"] == "Pagado")
    ju = sum(r["monto"] for r in g if r["justificado"] == "Sí")
    print("Pagado con anticipo:", pd_, "| Justificado:", ju)
    for a in POA:
        ej = sum(r["monto"] for r in g if r["act"] == a[0])
        assert ej <= a[6], (a[0], ej, a[6])
    b = beneficiarios()
    print("Metas:", sum(x["meta5"] for x in b), "Alcanzado:", sum(x["alcanzado"] for x in b))
