# Uzdevums: pašvaldības iesniegumu sistēma «Iesniegumi»

**Kurss:** Digitālo risinājumu izstrāde · M2 Sistēmanalīze un lietotājcentrēta pieeja
**Nodarbība:** 2.3. Pieejamība praksē (EAA, EN 301 549 / WCAG) · 2.4. MI komponentu riska klasifikācija (MI akts)
**Vide:** GitHub Codespace + Claude Code
**Laiks:** 1,5 h izstrāde + pieejamības testēšana + MI riska klasifikācija

---

## 1. Scenārijs

Novada pašvaldība vēlas aizstāt e-pasta kasti ar vienkāršu tīmekļa sistēmu, kurā
iedzīvotāji iesniedz iesniegumus (bedres uz ielas, apgaismojums, atkritumi, bērnudārza
rinda, sociālā palīdzība), darbinieki tos apstrādā, bet vadītājs redz pārskatu.

Sistēma ir **publiskās pārvaldes tīmekļvietne**, tāpēc tai no pirmās dienas jāatbilst
piekļūstamības prasībām (MK noteikumi Nr. 445, EN 301 549 / WCAG AA) un tai jābūt
piekļūstamības paziņojumam. Sistēmā ir arī **MI komponenti**, kuru riska klase jānosaka
pirms izstrādes (MI akts).

> Vārdu lietojums: tiesību aktos latviski lieto terminu **piekļūstamība** (accessibility).
> Kursā un sarunvalodā bieži saka «pieejamība» — domāts viens un tas pats.

## 2. Ko būvējam

Strādājoša tīmekļa lietotne ar datubāzi un vismaz **6 ekrāniem**.

| # | Ekrāns | Loma | Īsumā |
|---|--------|------|-------|
| 1 | Sākumlapa | visi | Lomas izvēle (iedzīvotājs / darbinieks / vadītājs), īss apraksts |
| 2 | Iesnieguma iesniegšana | iedzīvotājs | Forma ar validāciju un kļūdu ziņojumiem |
| 3 | Apstiprinājums | iedzīvotājs | Iesnieguma numurs, kas notiks tālāk |
| 4 | Iesniegumu saraksts | darbinieks | Tabula, filtri pēc statusa un tēmas, meklēšana |
| 5 | Iesnieguma detaļas | darbinieks | Statusa maiņa, komentāri, vēsture, **MI ieteikums** (tēma + atbildes projekts) |
| 6 | Pārskats | vadītājs | Skaits pa statusiem un tēmām, vidējais apstrādes laiks |
| 7 | Piekļūstamības paziņojums | visi | Obligāta lapa publiskā sektora vietnei |
| 8 | Mans iesniegums | iedzīvotājs | Statusa pārbaude pēc numura |

**Tehnoloģijas (fiksētas, lai neko nezaudētu uz vides iestatīšanu):**
Python 3.12 · Flask · Jinja2 (servera pusē renderēts HTML) · SQLite · bez JS ietvariem.
Repozitorijā jau ir minimāls skelets (`app.py`, `schema.sql`, `templates/base.html`), kas
startē un rāda sākumlapu. Viss pārējais — jums kopā ar Claude.

**Datu modelis (minimums):** `temas`, `iesniegumi`, `notikumi` (statusa vēsture un
komentāri). Skatiet `schema.sql`.

**Pieteikšanās nav jābūvē.** Lomu izvēlas sākumlapā (saite vai poga), lomu glabā sesijā.

## 3. Kā strādāt

1. Atveriet Codespace. Terminālī: `claude` (Claude Code). Pirmais prompts:
   `Izlasi CLAUDE.md un BACKLOG.md. Apkopo, ko būvēsim, un piedāvā secību.`
2. Startējiet lietotni: `python app.py` → Codespace piedāvās atvērt portu 5000.
3. Strādājiet pa backloga vienībām (`BACKLOG.md`): viena vienība → viens prompts → pārbaude pārlūkā → nākamā.
4. Pirms atzīmējat vienību kā gatavu, izpildiet **Definition of Done** (zemāk).
5. Pēc 1,5 h: pieejamības testēšana (`docs/PIEEJAMIBAS-PRASIBAS.md`) un MI riska
   klasifikācija (`docs/MI-RISKA-KLASIFIKACIJA.md`).

**Claude ir pāris programmētājs, ne autors.** Jūs lemjat, ko būvēt un vai rezultāts ir
pieņemams. Lasiet, ko Claude ģenerē, un prasiet paskaidrot, ja nesaprotat.

## 4. Definition of Done (katrai backloga vienībai)

- [ ] Funkcija strādā pārlūkā ar reāliem datiem no SQLite
- [ ] Lapai ir unikāls `<title>`, viens `<h1>`, `lang="lv"`, orientieri (`header`, `nav`, `main`, `footer`)
- [ ] Visu var izdarīt tikai ar tastatūru; fokuss ir redzams
- [ ] Katram formas laukam ir `<label>`; kļūdas nosauktas tekstā un piesaistītas laukam
- [ ] Teksta kontrasts ≥ 4,5:1; informācija nav nodota tikai ar krāsu
- [ ] `python tests/a11y_check.py` — 0 kritisku vai nopietnu (critical/serious) axe atradumu
- [ ] MI ģenerēts saturs vienmēr marķēts un cilvēks to apstiprina pirms lietošanas

## 5. Vērtēšana (M2 pārbaudījums)

Prototips + EAA/WCAG un MI akta atbilstības pārbaude:

| Kritērijs | Ko rāda |
|-----------|---------|
| Strādājoša lietotne | ≥ 6 ekrāni, dati saglabājas DB, galvenais lietotāja ceļš (iesniegt → apstrādāt → atbildēt) izpildāms |
| Pieejamība | axe bez critical/serious; tastatūras tests izturēts; piekļūstamības paziņojums aizpildīts ar reāliem atradumiem |
| MI riska klasifikācija | Aizpildīta veidne katram MI komponentam ar pamatojumu un termiņiem |
| Darbs ar MI rīku | Prompti ir konkrēti, rezultāts pārbaudīts, kļūdas atrastas un labotas |

## 6. Faili

```
README.md                      šis fails
BACKLOG.md                     backlogs 1,5 h (MUST / SHOULD / COULD) + pieejamības un MI prasības
CLAUDE.md                      noteikumi Claude Code (tehnoloģijas, pieejamība, MI komponenti)
app.py, schema.sql             minimāls skelets
templates/base.html            piekļūstams lapas karkass (skip-link, orientieri, fokuss)
static/style.css               pamata stils ar pietiekamu kontrastu un redzamu fokusu
tests/a11y_check.py            automātiskais pieejamības tests (axe-core + Playwright)
docs/PIEEJAMIBAS-PRASIBAS.md   prasības, kontrolsaraksts, testēšanas protokols, paziņojuma veidne
docs/MI-RISKA-KLASIFIKACIJA.md lēmumu koks, veidne, aizpildīts piemērs
.devcontainer/devcontainer.json Codespace konfigurācija
```
