"""Iesniegumi — minimāls skelets. Visu pārējo būvē komanda kopā ar Claude (skat. BACKLOG.md)."""
import os
import sqlite3
from flask import Flask, g, render_template, session, redirect, url_for, request

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "macibu-uzdevums-nav-drosa-atslega")

LOMAS = {"iedzivotajs": "Iedzīvotājs", "darbinieks": "Darbinieks", "vaditajs": "Vadītājs"}


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
    return {"loma": loma, "lomas_nosaukums": LOMAS.get(loma), "LOMAS": LOMAS}


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


@app.route("/pieklustamiba")
def pieklustamiba():
    # US-6: aizpildiet pēc testēšanas (veidne docs/PIEEJAMIBAS-PRASIBAS.md, 5. sadaļa)
    return render_template("pieklustamiba.html")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
