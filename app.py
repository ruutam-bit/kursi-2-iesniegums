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
    ("saraksts", "Iesniegumu saraksts", {"darbinieks"}),
    ("parskats", "Pārskats", {"vaditajs"}),
]

STATUSI = ["Jauns", "Apstrādē", "Atbildēts", "Noraidīts"]
# CSS klase statusa nozīmītei; statuss vienmēr arī tekstā (1.4.1)
STATUSA_KLASE = {"Jauns": "statuss-jauns", "Apstrādē": "statuss-apstrade",
                 "Atbildēts": "statuss-atbildets", "Noraidīts": "statuss-noraidits"}

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
    return {"loma": loma, "lomas_nosaukums": LOMAS.get(loma), "LOMAS": LOMAS, "izvelne": izvelne,
            "STATUSA_KLASE": STATUSA_KLASE}


def nav_pieejams(lapa, *lomas):
    """Ja lietotāja loma nav starp atļautajām — lapa ar paskaidrojumu (403), citādi None."""
    if session.get("loma") in lomas:
        return None
    vajadzigas = " vai ".join(LOMAS[l].lower() for l in lomas)
    return render_template("nav_pieejams.html", lapa=lapa, vajadzigas=vajadzigas), 403


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


@app.route("/saraksts")
def saraksts():
    """US-3: iesniegumu saraksts darbiniekam ar filtriem (GET) un meklēšanu."""
    if (atbilde := nav_pieejams("Iesniegumu saraksts", "darbinieks")):
        return atbilde
    db = get_db()
    temas = db.execute("SELECT id, nosaukums FROM temas ORDER BY id").fetchall()
    filtrs = {
        "statuss": request.args.get("statuss", ""),
        "tema": request.args.get("tema", ""),
        "q": request.args.get("q", "").strip(),
    }
    sql = ("SELECT i.numurs, i.izveidots, i.vards, i.statuss, t.nosaukums AS tema "
           "FROM iesniegumi i JOIN temas t ON t.id = i.temas_id WHERE 1=1")
    params = []
    if filtrs["statuss"] in STATUSI:
        sql += " AND i.statuss = ?"
        params.append(filtrs["statuss"])
    if filtrs["tema"].isdigit():
        sql += " AND i.temas_id = ?"
        params.append(int(filtrs["tema"]))
    if filtrs["q"]:
        sql += " AND (i.numurs LIKE ? OR i.vards LIKE ? OR i.adrese LIKE ? OR i.apraksts LIKE ?)"
        params += [f"%{filtrs['q']}%"] * 4
    sql += " ORDER BY i.izveidots DESC"
    iesniegumi = db.execute(sql, params).fetchall()
    ir_filtrs = any(filtrs.values())
    return render_template("saraksts.html", iesniegumi=iesniegumi, temas=temas, statusi=STATUSI,
                           filtrs=filtrs, ir_filtrs=ir_filtrs)


def pierakstit(db, iesnieguma_id, veids, teksts):
    """Notikums vēsturē (statusa maiņa, komentārs, atbilde) ar lietotāja lomu."""
    db.execute("INSERT INTO notikumi (iesnieguma_id, veids, loma, teksts) VALUES (?, ?, ?, ?)",
               (iesnieguma_id, veids, session.get("loma"), teksts))
    db.execute("UPDATE iesniegumi SET atjaunots = datetime('now', 'localtime') WHERE id = ?", (iesnieguma_id,))


@app.route("/iesniegums/<numurs>", methods=["GET", "POST"])
def iesniegums(numurs):
    """US-4: detaļas, statusa maiņa, komentārs, atbilde un vēsture (darbiniekam)."""
    if (atbilde := nav_pieejams("Iesnieguma detaļas", "darbinieks")):
        return atbilde
    db = get_db()
    i = db.execute(
        "SELECT i.*, t.nosaukums AS tema FROM iesniegumi i JOIN temas t ON t.id = i.temas_id WHERE i.numurs = ?",
        (numurs,),
    ).fetchone()
    if i is None:
        abort(404)

    kludas, ievade = {}, {"komentars": "", "atbilde": i["atbilde"] or ""}
    if request.method == "POST":
        darbiba = request.form.get("darbiba")
        if darbiba == "statuss":
            jauns = request.form.get("statuss", "")
            if jauns not in STATUSI or jauns == i["statuss"]:
                kludas["statuss"] = f"Izvēlieties statusu, kas atšķiras no pašreizējā «{i['statuss']}»."
            elif jauns == "Atbildēts" and not i["atbilde"]:
                kludas["statuss"] = "Lai mainītu statusu uz «Atbildēts», vispirms saglabājiet atbildi iedzīvotājam."
            else:
                db.execute("UPDATE iesniegumi SET statuss = ? WHERE id = ?", (jauns, i["id"]))
                pierakstit(db, i["id"], "statuss", f"Statuss mainīts no «{i['statuss']}» uz «{jauns}».")
                db.commit()
                flash(f"Statuss mainīts uz «{jauns}».")
                return redirect(url_for("iesniegums", numurs=numurs))
        elif darbiba == "komentars":
            ievade["komentars"] = request.form.get("komentars", "").strip()
            if not ievade["komentars"]:
                kludas["komentars"] = "Ierakstiet komentāra tekstu."
            else:
                pierakstit(db, i["id"], "komentars", ievade["komentars"])
                db.commit()
                flash("Komentārs pievienots vēsturei.")
                return redirect(url_for("iesniegums", numurs=numurs))
        elif darbiba == "atbilde":
            ievade["atbilde"] = request.form.get("atbilde", "").strip()
            if len(ievade["atbilde"]) < 10:
                kludas["atbilde"] = "Uzrakstiet atbildi iedzīvotājam — vismaz 10 rakstzīmes."
            else:
                db.execute("UPDATE iesniegumi SET atbilde = ? WHERE id = ?", (ievade["atbilde"], i["id"]))
                pierakstit(db, i["id"], "atbilde", ievade["atbilde"])
                db.commit()
                flash("Atbilde saglabāta. Lai to nosūtītu iedzīvotājam, mainiet statusu uz «Atbildēts».")
                return redirect(url_for("iesniegums", numurs=numurs))
        else:
            abort(400)

    vesture = db.execute(
        "SELECT laiks, veids, loma, teksts FROM notikumi WHERE iesnieguma_id = ? ORDER BY laiks, id", (i["id"],)
    ).fetchall()
    return render_template("iesniegums.html", i=i, vesture=vesture, statusi=STATUSI, kludas=kludas,
                           ievade=ievade), (400 if kludas else 200)


def dienas(vertiba):
    """Dienu skaits latviskā formā: 2,6 dienas / 1 diena / — ."""
    if vertiba is None:
        return "—"
    teksts = f"{vertiba:.1f}".replace(".", ",")
    return f"{teksts} diena" if teksts == "1,0" else f"{teksts} dienas"


@app.route("/parskats")
def parskats():
    """US-5: skaits pa statusiem un tēmām, vidējais apstrādes laiks (vadītājam)."""
    if (atbilde := nav_pieejams("Pārskats", "vaditajs")):
        return atbilde
    db = get_db()
    pa_statusiem = dict(db.execute("SELECT statuss, COUNT(*) FROM iesniegumi GROUP BY statuss").fetchall())
    statusi = [(s, pa_statusiem.get(s, 0)) for s in STATUSI]

    # Apstrādes laiks: no iesniegšanas līdz pēdējai statusa maiņai pabeigtam iesniegumam (Atbildēts / Noraidīts)
    pa_temam = db.execute("""
        SELECT t.nosaukums AS tema,
               COUNT(i.id) AS skaits,
               SUM(i.statuss IN ('Atbildēts', 'Noraidīts')) AS pabeigti,
               AVG(CASE WHEN i.statuss IN ('Atbildēts', 'Noraidīts')
                        THEN julianday((SELECT MAX(n.laiks) FROM notikumi n
                                        WHERE n.iesnieguma_id = i.id AND n.veids = 'statuss'))
                             - julianday(i.izveidots) END) AS vid_dienas
        FROM temas t LEFT JOIN iesniegumi i ON i.temas_id = t.id
        GROUP BY t.id ORDER BY t.id
    """).fetchall()
    kopa = sum(sk for _, sk in statusi)
    pabeigti = sum(r["pabeigti"] or 0 for r in pa_temam)
    vid = db.execute("""
        SELECT AVG(julianday((SELECT MAX(n.laiks) FROM notikumi n WHERE n.iesnieguma_id = i.id AND n.veids = 'statuss'))
                   - julianday(i.izveidots))
        FROM iesniegumi i WHERE i.statuss IN ('Atbildēts', 'Noraidīts')
    """).fetchone()[0]
    maks = max((r["skaits"] for r in pa_temam), default=0) or 1
    return render_template("parskats.html", statusi=statusi, pa_temam=pa_temam, kopa=kopa,
                           pabeigti=pabeigti, vid=dienas(vid), dienas=dienas, maks=maks)


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
