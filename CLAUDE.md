# CLAUDE.md — noteikumi šim projektam

> Ja šī mape ir daļa no lielāka repozitorija (piem., `praktiskie-darbi/m2-iesniegumi/`), šeit rakstītie
> noteikumi ir prioritāri pār saknes CLAUDE.md visam, kas notiek šajā mapē.

Projekts: pašvaldības iesniegumu sistēma «Iesniegumi». Mācību uzdevums (1,5 h), publiskā
sektora tīmekļvietne. Lietotāja saskarne — **latviešu valodā**.

## Tehnoloģijas (nemainīt)
- Python 3.12, Flask, Jinja2 šabloni, SQLite (`sqlite3` no standarta bibliotēkas), `data.db`
- Servera pusē renderēts HTML. Bez JS ietvariem, bez build soļa. JavaScript tikai tad, ja bez tā nevar, un tad progresīvi (lapa strādā arī bez JS)
- Viens `app.py` (var sadalīt `db.py`, `ai.py`), `templates/`, `static/style.css`, `schema.sql`
- Startēšana: `python app.py` (host 0.0.0.0, ports 5000). Pieteikšanās nav: lomu glabā sesijā

## Kā strādāt
- Pirms koda: pasaki 2–3 teikumos, ko darīsi. Pēc koda: kā pārbaudīt pārlūkā
- Mazi soļi: viena backloga vienība vienā reizē. Nepievieno funkcijas, kas nav prasītas
- Pēc katras vienības: `python tests/a11y_check.py` un izlabo critical/serious atradumus
- Ja prasība ir neskaidra — pajautā, neizdomā

## Pieejamība (obligāti katrā lapā; EN 301 549 / WCAG 2.2 AA)
- `<html lang="lv">`, unikāls `<title>` formā «Lapa – Iesniegumi», tieši viens `<h1>`
- Orientieri: `<header>`, `<nav aria-label="Galvenā izvēlne">`, `<main id="saturs">`, `<footer>`; skip-link «Pāriet uz saturu» pirmais lapā
- Virsraksti hierarhijā (h1 → h2 → h3), bez izlaistiem līmeņiem
- Formas: katram laukam `<label for>`; obligātie lauki ar tekstu «(obligāts)», ne tikai `*` vai krāsu; kļūdas: kopsavilkums `<div role="alert">` lapas sākumā ar saitēm uz laukiem + ziņa pie lauka caur `aria-describedby` + `aria-invalid="true"`; ievadītais saglabājas
- Tabulas: `<caption>`, `<th scope="col|row">`; nekad tabulas izkārtojumam
- Statuss vienmēr tekstā (piem., «Apstrādē»), krāsa tikai papildus
- Saites teksts saprotams ārpus konteksta; pogas — `<button>`, saites — `<a href>`; nav `div onclick`
- Fokuss redzams (`:focus-visible` ar ≥ 3:1 kontrastu, 2 px kontūra); loģiska tab secība; nav `tabindex > 0`
- Kontrasts: teksts ≥ 4,5:1, lieli virsraksti un UI elementi ≥ 3:1. Paletes: teksts `#1a1a1a`, fons `#ffffff`, akcents `#0b5394`, kļūda `#a4262c`, veiksme `#1e6b3a`
- Mērķu izmērs ≥ 24×24 CSS px; atstarpes starp klikšķināmiem elementiem
- Paziņojumi pēc darbībām: `<p role="status">` (ne `alert`, ja nav kļūda)
- Attēliem `alt`; dekoratīviem `alt=""`; diagrammām tā pati informācija tabulā
- Nav satura, kas mirgo; nav laika limitu; nav CAPTCHA
- Reflow: 320 px platumā bez horizontālās ritjoslas; 200 % mērogā nekas nepārklājas
- Katrā lapā kājenē saite «Piekļūstamības paziņojums» (`/pieklustamiba`)

## MI komponenti (MI akts)
- `ai.py` ar funkciju `ieteikums(apraksts: str) -> dict(tema=str, atbildes_projekts=str, avots=str)`
- Noklusēti — atslēgvārdu imitācija bez tīkla. Ja vides mainīgais `ANTHROPIC_API_KEY` ir, drīkst izmantot `anthropic` SDK ar modeli no `AI_MODEL` mainīgā; atbildes līgums nemainās; kļūdas gadījumā — atgriežas uz imitāciju
- MI ģenerēts saturs UI vienmēr marķēts: «Ģenerēts ar MI – pārbaudiet pirms lietošanas» (tekstā, ne tikai ikonā)
- Cilvēks apstiprina: MI teksts nonāk rediģējamā laukā; nekad netiek nosūtīts vai saglabāts kā atbilde automātiski
- Žurnāls: `notikumi` ierakstā `veids='mi_ieteikums'` ar laiku un lietotāja lomu
- Nebūvēt neko, kas vērtē, sarindo vai atlasa personas pēc atbilstības pabalstam vai pakalpojumam (augsta riska joma — MI akta III pielikuma 5. punkts) — tas ir tikai klasifikācijas uzdevums `docs/MI-RISKA-KLASIFIKACIJA.md`

## Datu aizsardzība (minimums)
- Glabā tikai vajadzīgos laukus; e-pastu rāda tikai darbiniekam
- Testa dati — izdomāti; nekādu reālu personu datu
