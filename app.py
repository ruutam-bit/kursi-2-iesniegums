"""Iesniegumi — minimāls skelets. Visu pārējo būvē komanda kopā ar Claude (skat. BACKLOG.md)."""
import os
import re
import sqlite3
from datetime import datetime
from flask import Flask, g, render_template, session, redirect, url_for, request, flash, abort

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "macibu-uzdevums-nav-drosa-atslega")

LOMAS = {"iedzivotajs": "Iedzīvotājs", "darbinieks": "Darbinieks", "vaditajs": "Vadītājs"}

# Galvenā izvēlne: vienmēr šajā secībā (WCAG 3.2.3); rāda tikai lomai atbilstošās saites.
# None lomu sarakstā = arī tad, ja loma vēl nav izvēlēta.
IZVELNE = [
    ("index", "Sākums", None),
    ("iesniegt", "Iesniegt iesniegumu", {"iedzivotajs", None}),
]

EPASTS_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Izveido tabulas un sākumdatus, ja datubāzes vēl nav."""
    if os.path.exists(DB_PATH):
        return
    with sqlite3.connect(DB_PATH) as db, open(SCHEMA_PATH, encoding="utf-8") as f:
        db.executescript(f.read())


@app.context_processor
def inject_globals():
    loma = session.get("loma")
    izvelne = [(ep, teksts) for ep, teksts, lomas in IZVELNE if lomas is None or loma in lomas]
    return {"loma": loma, "lomas_nosaukums": LOMAS.get(loma), "LOMAS": LOMAS, "izvelne": izvelne}


@app.route("/")
def index():
    temas = get_db().execute("SELECT id, nosaukums FROM temas ORDER BY nosaukums").fetchall()
    return render_template("index.html", temas=temas)


@app.post("/loma")
def izveleties_lomu():
    loma = request.form.get("loma")
    if loma in LOMAS:
        session["loma"] = loma
    return redirect(url_for("index"))


def nakamais_numurs(db):
    """Iesnieguma numurs formā GGGG-NNNN (piem., 2026-0011)."""
    gads = datetime.now().year
    pedejais = db.execute(
        "SELECT numurs FROM iesniegumi WHERE numurs LIKE ? ORDER BY numurs DESC LIMIT 1", (f"{gads}-%",)
    ).fetchone()
    nr = int(pedejais["numurs"].split("-")[1]) + 1 if pedejais else 1
    return f"{gads}-{nr:04d}"


def parbaudit_iesniegumu(dati, temas_ids):
    """Servera puses validācija. Atgriež {lauks: ziņa}; ziņa saka, KĀ labot (WCAG 3.3.3)."""
    kludas = {}
    if not dati["vards"]:
        kludas["vards"] = "Ievadiet savu vārdu un uzvārdu."
    if not dati["epasts"]:
        kludas["epasts"] = "Ievadiet e-pasta adresi, piemēram, vards@piemers.lv."
    elif not EPASTS_RE.match(dati["epasts"]):
        kludas["epasts"] = "E-pasta adresei jābūt formā vards@piemers.lv."
    if dati["temas_id"] not in temas_ids:
        kludas["temas_id"] = "Izvēlieties tēmu no saraksta."
    if len(dati["apraksts"]) < 10:
        kludas["apraksts"] = "Aprakstiet problēmu vismaz 10 rakstzīmēs: kas noticis un kur."
    elif len(dati["apraksts"]) > 2000:
        kludas["apraksts"] = "Saīsiniet aprakstu līdz 2000 rakstzīmēm."
    if not dati["piekrisana"]:
        kludas["piekrisana"] = "Atzīmējiet, ka piekrītat datu apstrādei — bez tā iesniegumu nevar reģistrēt."
    return kludas


@app.route("/iesniegt", methods=["GET", "POST"])
def iesniegt():
    """US-1: iesnieguma forma ar servera puses validāciju."""
    db = get_db()
    temas = db.execute("SELECT id, nosaukums, apraksts FROM temas ORDER BY id").fetchall()
    dati = {"vards": "", "epasts": "", "temas_id": "", "adrese": "", "apraksts": "", "piekrisana": False}
    kludas = {}

    if request.method == "POST":
        f = request.form
        dati = {
            "vards": f.get("vards", "").strip(),
            "epasts": f.get("epasts", "").strip(),
            "temas_id": f.get("temas_id", ""),
            "adrese": f.get("adrese", "").strip(),
            "apraksts": f.get("apraksts", "").strip(),
            "piekrisana": f.get("piekrisana") == "jā",
        }
        kludas = parbaudit_iesniegumu(dati, {str(t["id"]) for t in temas})
        if not kludas:
            numurs = nakamais_numurs(db)
            cur = db.execute(
                "INSERT INTO iesniegumi (numurs, temas_id, vards, epasts, adrese, apraksts) VALUES (?, ?, ?, ?, ?, ?)",
                (numurs, int(dati["temas_id"]), dati["vards"], dati["epasts"], dati["adrese"] or None, dati["apraksts"]),
            )
            db.execute(
                "INSERT INTO notikumi (iesnieguma_id, veids, loma, teksts) VALUES (?, 'statuss', ?, ?)",
                (cur.lastrowid, session.get("loma") or "iedzivotajs", "Iesniegums reģistrēts ar statusu «Jauns»."),
            )
            db.commit()
            # POST → redirect → GET: F5 apstiprinājuma lapā neiesniedz atkārtoti (US-2)
            return redirect(url_for("apstiprinajums", numurs=numurs))

    return render_template("iesniegt.html", temas=temas, dati=dati, kludas=kludas)


@app.route("/apstiprinajums/<numurs>")
def apstiprinajums(numurs):
    """US-2: iesnieguma numurs un kas notiks tālāk. Personas datus nerāda (numuri ir secīgi)."""
    iesniegums = get_db().execute(
        "SELECT i.numurs, i.izveidots, t.nosaukums AS tema FROM iesniegumi i JOIN temas t ON t.id = i.temas_id "
        "WHERE i.numurs = ?", (numurs,)
    ).fetchone()
    if iesniegums is None:
        abort(404)
    return render_template("apstiprinajums.html", i=iesniegums)


@app.errorhandler(404)
def nav_atrasts(_e):
    return render_template("404.html"), 404


@app.route("/pieklustamiba")
def pieklustamiba():
    # US-6: aizpildiet pēc testēšanas (veidne docs/PIEEJAMIBAS-PRASIBAS.md, 5. sadaļa)
    return render_template("pieklustamiba.html")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
