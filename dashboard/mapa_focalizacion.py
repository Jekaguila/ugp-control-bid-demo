"""Mapa de focalización por departamento (datos SIMULADOS).

Uso:
    python mapa_focalizacion.py                       # escribe mapa_focalizacion.html
    python mapa_focalizacion.py --variable cobertura  # indice | cobertura | inversion | brecha
    python mapa_focalizacion.py --excel ruta.xlsx --salida mapa.html
"""
import argparse
from pathlib import Path
from ugp.cargar_datos import cargar, RUTA_POR_DEFECTO
from ugp.indicadores import focalizacion
from ugp.graficos import mapa_choropleth


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--excel", default=str(RUTA_POR_DEFECTO))
    ap.add_argument("--variable", default="indice", choices=["indice", "cobertura", "inversion", "brecha"])
    ap.add_argument("--salida", default="mapa_focalizacion.html")
    a = ap.parse_args()
    f = focalizacion(cargar(a.excel))
    fig = mapa_choropleth(f, a.variable, "Focalización por departamento — DATOS SIMULADOS")
    fig.write_html(a.salida, include_plotlyjs=True)
    print("Mapa escrito en", Path(a.salida).resolve())
    print(f[["Departamento", "indice", "prioridad"]].sort_values("indice", ascending=False).head(5).to_string(index=False))


if __name__ == "__main__":
    main()
