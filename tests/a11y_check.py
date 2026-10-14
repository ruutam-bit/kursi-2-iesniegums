"""Automātiskais pieejamības tests: axe-core (WCAG 2.2 A/AA) uz katru lietotnes lapu.

Lietošana (lietotnei jābūt startētai: python app.py):
    python tests/a11y_check.py                      # apstaigā saites no sākumlapas (bez lomas un katrai lomai)
                                                    # + scenāriji pēc POST (forma ar kļūdām)
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


def izveleties_lomu(page, loma):
    """Izvēlas lomu sākumlapā (lomu glabā sesijā; tā pati pārlūka sesija paliek nākamajām lapām)."""
    page.goto(BASE_URL + "/", wait_until="domcontentloaded")
    page.check(f"#loma-{loma}")
    page.click("button[type=submit]")
    page.wait_for_load_state("networkidle")


def tuksa_forma(page):
    """Iesniedz tukšu iesnieguma formu → lapa ar kļūdām (3.3.1). Pārbauda arī fokusu uz kopsavilkumu."""
    page.goto(BASE_URL + "/iesniegt", wait_until="domcontentloaded")
    page.click("form[action$='/iesniegt'] button[type=submit]")
    page.wait_for_load_state("networkidle")
    ok = page.evaluate("document.activeElement && document.activeElement.classList.contains('kludu-kopsavilkums')")
    return None if ok else "Pēc kļūdas fokuss NAV uz kļūdu kopsavilkuma (3.3.1)"


def apstiprinajums(page):
    """Apstiprinājuma lapa (pēc POST → redirect; testa datos esošs numurs, lai neveidotu jaunus ierakstus)."""
    page.goto(BASE_URL + "/apstiprinajums/2026-0001", wait_until="networkidle")


def lapa_nav_atrasta(page):
    page.goto(BASE_URL + "/apstiprinajums/nav-tada", wait_until="networkidle")


# Stāvokļi, ko nevar sasniegt ar GET saitēm: (nosaukums, funkcija). Funkcija atgriež papildu kļūdu vai None.
SCENARIJI = [
    ("Iesnieguma forma ar kļūdām (tukša forma)", tuksa_forma),
    ("Apstiprinājums /apstiprinajums/2026-0001", apstiprinajums),
    ("Lapa nav atrasta (404)", lapa_nav_atrasta),
]
LOMAS = ["iedzivotajs", "darbinieks", "vaditajs"]


def main(paths):
    axe = Axe()
    total = {"critical": 0, "serious": 0, "moderate": 0, "minor": 0}
    lines = ["# Pieejamības tests (axe-core, WCAG 2.2 AA)", "", f"Bāzes URL: {BASE_URL}", ""]
    papildu_kludas = []

    def parbaudit(page, nosaukums):
        result = axe.run(page, options=AXE_OPTIONS)
        violations = sorted(result.response["violations"], key=lambda v: IMPACT_ORDER.get(v["impact"], 9))
        title = page.title()
        print(f"\n== {nosaukums}  «{title}»  — {len(violations)} pārkāpumu veidi")
        lines.append(f"## {nosaukums} — «{title}»")
        if not violations:
            print("   OK")
            lines.append("OK — pārkāpumi nav atrasti.\n")
            return
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

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        if paths:
            for url in [BASE_URL + ("" if x.startswith("/") else "/") + x for x in paths]:
                page.goto(url, wait_until="networkidle")
                parbaudit(page, url)
        else:
            # 1) Bez lomas, 2) katrai lomai (izvēlnē redzamas citas saites)
            parbauditie = set()
            for loma in [None] + LOMAS:
                if loma:
                    izveleties_lomu(page, loma)
                for url in discover(page, BASE_URL + "/"):
                    if url in parbauditie:
                        continue
                    parbauditie.add(url)
                    page.goto(url, wait_until="networkidle")
                    parbaudit(page, url + (f" [loma: {loma}]" if loma else ""))
            # 3) Stāvokļi pēc POST (formas ar kļūdām u. c.)
            for nosaukums, scenarijs in SCENARIJI:
                kluda = scenarijs(page)
                parbaudit(page, nosaukums)
                if kluda:
                    print(f"  [SERIOUS ] {kluda}")
                    lines.append(f"- **serious** {kluda}\n")
                    papildu_kludas.append(kluda)
                    total["serious"] += 1
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
