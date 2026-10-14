#!/usr/bin/env bash
# Vienreizēja M2 uzdevuma sagatavošana ESOŠĀ Codespace (bez konteinera pārbūves).
# Palaist no repo saknes:  bash praktiskie-darbi/m2-iesniegumi/setup-m2.sh
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
echo "== 1/3 Python pakotnes"
pip install -q -r "$DIR/requirements.txt"
echo "== 2/3 Chromium pieejamības testam (axe + Playwright)"
python -m playwright install --with-deps chromium
echo "== 3/3 Pārbaude"
cd "$DIR" && python - <<'PY'
import flask, playwright, axe_playwright_python
print("OK: flask, playwright, axe-playwright-python")
PY
echo
echo "Gatavs. Tālāk:"
echo "  cd praktiskie-darbi/m2-iesniegumi"
echo "  python app.py            # ports 5000, Codespace piedāvās atvērt"
echo "  claude                   # otrā terminālī; pirmais prompts: 'Izlasi CLAUDE.md un BACKLOG.md'"
echo "  python tests/a11y_check.py"
