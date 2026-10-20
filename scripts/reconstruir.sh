#!/usr/bin/env bash
# Reconstruye ambos libros de Excel y calcula las fórmulas con LibreOffice (valores en caché).
# Requisitos: python3 + openpyxl, LibreOffice (soffice). Uso: bash scripts/reconstruir.sh
set -euo pipefail
cd "$(dirname "$0")/.."
TMP="$(mktemp -d)"
for pair in "construir_excel.py:UGP_Sistema_Integrado_de_Control" "construir_formatos.py:UGP_Formatos_de_Gestion"; do
  script="${pair%%:*}"; nombre="${pair##*:}"
  (cd scripts && python3 "$script" "$TMP/pre/$nombre.xlsx")
  soffice --headless --calc --convert-to xlsx:"Calc MS Excel 2007 XML" --outdir "$TMP/post" "$TMP/pre/$nombre.xlsx" >/dev/null
  cp "$TMP/post/$nombre.xlsx" "herramientas_seguimiento/$nombre.xlsx"
  echo "OK  herramientas_seguimiento/$nombre.xlsx"
done
