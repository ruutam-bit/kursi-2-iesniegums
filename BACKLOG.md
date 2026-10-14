# Backlogs: «Iesniegumi» (1,5 h ar Claude Code)

Prioritātes: **MUST** — jāpabeidz; **SHOULD** — ja laiks; **COULD** — bonusa.
Laiki ir orientējoši (ar Claude kā pāri). Katrai vienībai spēkā `README.md` Definition of Done.

Pieejamības kritēriji norādīti ar WCAG 2.2 numuriem (EN 301 549 9. nodaļa).
MI kritēriji — ar MI akta pantiem.

---

## 0. Iesildīšanās (10 min)

| ID | Vienība | Gatavs, kad |
|----|---------|-------------|
| S0.1 | Atvērt Codespace, startēt `python app.py`, atvērt sākumlapu | Lapa redzama pārlūkā |
| S0.2 | Claude: «Izlasi CLAUDE.md, BACKLOG.md, schema.sql. Papildini shēmu, ja vajag, un ieraksti 10 testa iesniegumus 5 tēmās» | `data.db` ar testa datiem |
| S0.3 | Palaist `python tests/a11y_check.py` uz sākumlapu | Tests strādā (lai arī lapu maz) |

## 1. MUST (≈ 50 min)

### US-1 · Iesnieguma iesniegšana (10 min)
Kā **iedzīvotājs** vēlos iesniegt iesniegumu, lai pašvaldība to reģistrē.
- Lauki: vārds, e-pasts, tēma (saraksts no DB), adrese/vieta, apraksts, piekrišana datu apstrādei
- Servera puses validācija; pēc kļūdas forma saglabā ievadīto
- **Pieejamība:** katram laukam `<label>` (1.3.1, 3.3.2); kļūdas nosauktas tekstā, saistītas ar lauku caur `aria-describedby`, kļūdu kopsavilkums lapas sākumā ar fokusu uz to (3.3.1, 3.3.3); obligātie lauki apzīmēti ne tikai ar krāsu (1.4.1); nekādu laika limitu (2.2.1)

### US-2 · Apstiprinājums (5 min)
Kā **iedzīvotājs** vēlos redzēt iesnieguma numuru un kas notiks tālāk.
- Pēc POST → redirect → apstiprinājuma lapa (nav dubultas iesniegšanas ar F5)
- **Pieejamība:** lapas `<title>` saka «Iesniegums reģistrēts» (2.4.2); numurs tekstā, ne attēlā (1.1.1)

### US-3 · Iesniegumu saraksts (10 min)
Kā **darbinieks** vēlos redzēt visus iesniegumus un filtrēt pēc statusa un tēmas.
- Tabula: numurs, datums, tēma, iesniedzējs, statuss; filtri (GET forma); meklēšana pēc teksta
- **Pieejamība:** `<table>` ar `<caption>` un `<th scope>` (1.3.1); statuss ar tekstu, ne tikai krāsainu punktu (1.4.1); filtru forma ar `<fieldset><legend>`; saišu teksts saprotams ārpus konteksta — «Iesniegums 2026-014», ne «Skatīt» (2.4.4)

### US-4 · Iesnieguma detaļas un apstrāde (15 min)
Kā **darbinieks** vēlos mainīt statusu, pievienot komentāru un sagatavot atbildi.
- Statusi: Jauns → Apstrādē → Atbildēts / Noraidīts; katra maiņa pierakstās `notikumi`
- Atbildes teksta lauks; vēsture hronoloģiski
- **Pieejamība:** virsrakstu hierarhija h1 → h2 (1.3.1, 2.4.6); pēc statusa maiņas paziņojums `role="status"` (4.1.3); pogas ar skaidru tekstu (4.1.2); fokuss pēc darbības nepazūd zem fiksētas galvenes (2.4.11)

### US-5 · Pārskats vadītājam (10 min)
Kā **vadītājs** vēlos redzēt iesniegumu skaitu pa statusiem un tēmām un vidējo apstrādes laiku.
- Divas tabulas + vienkārša joslu diagramma (CSS vai inline SVG)
- **Pieejamība:** diagrammai teksta alternatīva — tā pati informācija tabulā (1.1.1); joslu krāsu kontrasts ≥ 3:1 pret fonu (1.4.11); diagramma nav vienīgais informācijas avots

### US-6 · Piekļūstamības paziņojums (skelets, 5 min)
Kā **iestāde** esmu spiesta publicēt piekļūstamības paziņojumu.
- Lapa `/pieklustamiba` no `docs/PIEEJAMIBAS-PRASIBAS.md` veidnes; saite kājenē katrā lapā (3.2.3)
- Saturu aizpilda pēc testēšanas (skat. 3. sadaļu)

## 2. SHOULD (≈ 20 min)

### US-7 · MI ieteikums darbiniekam (10 min)
Kā **darbinieks** vēlos, lai sistēma iesaka tēmu un sagatavo atbildes projektu.
- `ai.py`: funkcija `ieteikums(apraksts) -> {tema, atbildes_projekts}`. Noklusēti — atslēgvārdu bāzes imitācija (bez tīkla). Ja ir `ANTHROPIC_API_KEY`, var izmantot Claude API — bet funkcijas līgums paliek tas pats
- Detaļu lapā: bloks «MI ieteikums», poga «Izmantot projektu» — teksts nonāk atbildes laukā, kur darbinieks to rediģē un apstiprina. **Nekad nenosūta automātiski**
- **MI akts:** skaidrs marķējums «Ģenerēts ar MI, pārbaudiet pirms lietošanas» (50. p. gars; cilvēka uzraudzība); žurnālā (`notikumi`) ieraksts, ka ieteikums izmantots
- **Pieejamība:** bloks ir `<section aria-labelledby>`; ielāde bez «mirgojoša» indikatora (2.3.1)

### US-8 · Mans iesniegums (5 min)
Kā **iedzīvotājs** vēlos pārbaudīt statusu pēc numura.
- Forma ar vienu lauku; rezultāts: statuss, pēdējais notikums, atbilde, ja ir
- **Pieejamība:** nav CAPTCHA/puzles (3.3.8); kļūda «numurs nav atrasts» tekstā (3.3.1)

### US-9 · Pieejamības tests zaļš (5 min)
- `python tests/a11y_check.py` pārbauda visas lapas (iesk. formu ar kļūdām) — 0 critical/serious
- Atradumi, ko nevar novērst, dokumentēti paziņojumā

## 3. COULD (ja paliek laiks)

| ID | Vienība | Piezīmes |
|----|---------|----------|
| US-10 | Čata palīgs iedzīvotājam («Kā iesniegt? Kādi dokumenti?») | MI akts 50. p. 1. d.: lietotājs jāinformē, ka sarunājas ar MI. Pieejamība: čata žurnāls `aria-live="polite"`, tastatūra |
| US-11 | E-pasta paziņojums par statusa maiņu (imitācija — raksta failā) | Teksts vienkāršā valodā |
| US-12 | CSV eksports vadītājam | Saite ar aprakstu «Lejupielādēt CSV (12 KB)» |
| US-13 | Augsta kontrasta / tumšais režīms | Jāsaglabā kontrasts abos; nav atkarīgs no krāsas |
| US-14 | Reflow pārbaude 320 px un 200 % mērogā | 1.4.4, 1.4.10 — nekas nepazūd, nav horizontālās ritjoslas |

## 4. Tikai dizainam, NEIMPLEMENTĒT (2.4 uzdevums)

### US-15 · «Prioritātes vērtējums» sociālās palīdzības iesniegumiem
Vadītājs lūdz: «Lai MI sarindo sociālās palīdzības iesniegumus pēc tā, kam palīdzība vajadzīga
visvairāk, un atzīmē tos, kas, visticamāk, neatbilst kritērijiem.»

**Uzdevums:** aizpildiet `docs/MI-RISKA-KLASIFIKACIJA.md` veidni šim komponentam **pirms** jebkādas
izstrādes. Secinājums par riska klasi, pienākumiem un termiņu — prezentācijā grupai.

---

## 5. Pēc 1,5 h: pieejamības testēšana (2.3) un MI riska klasifikācija (2.4)

| Solis | Laiks | Rezultāts |
|-------|-------|-----------|
| Automātiskais tests uz visām lapām (`tests/a11y_check.py`) | 10 min | `a11y-report.md` |
| Manuālais tests: tastatūra, 200 % mērogs, ekrānlasītājs vienam ceļam (iesniegt iesniegumu) | 20 min | Protokols `docs/PIEEJAMIBAS-PRASIBAS.md` 4. sadaļā |
| Top-3 problēmu labošana ar Claude | 15 min | Commits |
| Piekļūstamības paziņojuma aizpildīšana ar reāliem atradumiem | 10 min | Lapa `/pieklustamiba` |
| MI riska klasifikācija: US-7, US-10, US-15 | 25 min | Aizpildītas veidnes |
| Grupu prezentācija: 1 ekrāns, 1 atradums, 1 MI klasifikācijas lēmums | 3 min / grupa | — |
