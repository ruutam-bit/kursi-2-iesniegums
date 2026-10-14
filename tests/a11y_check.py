"""Automātiskais pieejamības tests: axe-core (WCAG 2.2 A/AA) uz katru lietotnes lapu.

Lietošana (lietotnei jābūt startētai: python app.py):
    python tests/a11y_check.py                      # apstaigā saites no sākumlapas (līdz 30 lapām)
    python tests/a11y_check.py /iesniegt /saraksts  # tikai norādītie ceļi
    BASE_URL=http://localhost:5000 python tests/a11y_check.py

Rezultāts: izdruka terminālī + a11y-report.md. Izejas kods 1, ja ir critical/serious atradumi.
Atceries: automātiskie rīki atrod tikai daļu problēmu — tastatūra, ekrānlasītājs un mērogs jāpārbauda ar rokām.
"""
import os
import sys
from urllib.parse import urljoin, urlparse

from playwright.sync_api import sync_playwright
from axe_playwright_python.sync_playwright import Axe

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000").rstrip("/")
MAX_PAGES = 30
AXE_OPTIONS = {"runOnly": {"type": "tag", "values": ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"]}}
IMPACT_ORDER = {"critical": 0, "serious": 1, "moderate": 2, "minor": 3}


def discover(page, start):
    """Apstaigā iekšējās saites (GET) no sākumlapas."""
    seen, queue = [], [start]
    while queue and len(seen) < MAX_PAGES:
        url = queue.pop(0)
        if url in seen:
            continue
        page.goto(url, wait_until="domcontentloaded")
        seen.append(url)
        for href in page.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href'))"):
            if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue
            full = urljoin(url, href).split("#")[0]
            if urlparse(full).netloc == urlparse(BASE_URL).netloc and full not in seen and full not in queue:
                queue.append(full)
    return seen


def main(paths):
    axe = Axe()
    total = {"critical": 0, "serious": 0, "moderate": 0, "minor": 0}
    lines = ["# Pieejamības tests (axe-core, WCAG 2.2 AA)", "", f"Bāzes URL: {BASE_URL}", ""]

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        urls = [BASE_URL + ("" if x.startswith("/") else "/") + x for x in paths] if paths else discover(page, BASE_URL + "/")

        for url in urls:
            page.goto(url, wait_until="networkidle")
            result = axe.run(page, options=AXE_OPTIONS)
            violations = sorted(result.response["violations"], key=lambda v: IMPACT_ORDER.get(v["impact"], 9))
            title = page.title()
            print(f"\n== {url}  «{title}»  — {len(violations)} pārkāpumu veidi")
            lines.append(f"## {url} — «{title}»")
            if not violations:
                print("   OK")
                lines.append("OK — pārkāpumi nav atrasti.\n")
                continue
            for v in violations:
                total[v["impact"]] = total.get(v["impact"], 0) + 1
                n = len(v["nodes"])
                print(f"  [{v['impact'].upper():8}] {v['id']}: {v['help']}  ({n} elem.)  {v['helpUrl']}")
                lines.append(f"- **{v['impact']}** `{v['id']}` — {v['help']} ({n} elementi). [Skaidrojums]({v['helpUrl']})")
                for node in v["nodes"][:3]:
                    sel = ", ".join(node["target"]) if isinstance(node["target"], list) else str(node["target"])
                    print(f"             → {sel}")
                    lines.append(f"  - `{sel}`")
            lines.append("")
        browser.close()

    summary = f"Kopā: critical {total['critical']}, serious {total['serious']}, moderate {total['moderate']}, minor {total['minor']}"
    print("\n" + summary)
    lines += ["---", summary, "", "Manuālās pārbaudes (tastatūra, 200 % mērogs, ekrānlasītājs) skat. docs/PIEEJAMIBAS-PRASIBAS.md 4. sadaļā."]
    with open("a11y-report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Atskaite: a11y-report.md")
    return 1 if (total["critical"] or total["serious"]) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
