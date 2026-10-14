# Pieejamība (piekļūstamība) praksē: prasības → izstrāde → testēšana → paziņojums

Attiecas uz uzdevumu «Iesniegumi». Mērķis: pēc 1,5 h izstrādes **pierādīt** atbilstību, ne tikai apgalvot.

## 1. Kas mums ir saistošs

| Līmenis | Akts | Kam | Ko prasa | Kas uzrauga |
|---------|------|-----|----------|-------------|
| ES | Direktīva (ES) 2016/2102 — publiskā sektora tīmekļvietnes un mobilās lietotnes | Iestādēm | Atbilstība EN 301 549; piekļūstamības paziņojums; atgriezeniskās saites mehānisms | Dalībvalstu uzraudzība |
| LV | MK noteikumi Nr. 445 (14.07.2020) «Kārtība, kādā iestādes ievieto informāciju internetā» | Iestāžu tīmekļvietnēm un lietotnēm | EN 301 549 (WCAG 2.1 AA), piekļūstamības paziņojums, izvērtējums pēc VARAM vadlīnijām | VARAM |
| ES | Direktīva (ES) 2019/882 — Eiropas Piekļūstamības akts (EAA), piemēro no 28.06.2025 | Uzņēmumiem: e-komercija, bankas un finanšu pakalpojumi, e-grāmatas, elektroniskie sakari, pasažieru transporta tīmekļvietnes/lietotnes/biļetes, pašapkalpošanās termināļi, datori, viedtālruņi, e-lasītāji | Produkti un pakalpojumi piekļūstami; informācija par piekļūstamību; dokumentācija | Dalībvalstu tirgus uzraudzība |
| LV | Preču un pakalpojumu piekļūstamības likums + MK noteikumi Nr. 128 (27.02.2024), spēkā no 28.06.2025 | Tas pats | Tas pats; izņēmumi: mikrouzņēmumi (pakalpojumiem), nesamērīgs slogs, būtiskas izmaiņas | PTAC |
| Standarts | **EN 301 549** V3.2.1 (2021) → WCAG 2.1 AA; **V4.1.1 (publicēts 02.09.2026)** → WCAG 2.2 AA; V4 citēšana ES Oficiālajā Vēstnesī vēl gaidāma | Tehniskā prasību bāze visiem augstāk minētajiem | 9. nod. tīmeklis, 10. dokumenti, 11. programmatūra, 12. dokumentācija un atbalsts | — |

**Mūsu uzdevumā:** «Iesniegumi» ir iestādes tīmekļvietne → MK 445 + EN 301 549. Mērķējam uz **WCAG 2.2 AA**
(ietver visu 2.1 AA; sešas jaunas AA prasības — zemāk), lai esam gatavi V4.1.1.

Ja tā pati sistēma būtu, piemēram, pašvaldības e-pakalpojums ar maksājumu — papildus EAA / Preču un
pakalpojumu piekļūstamības likums.

## 2. Četri WCAG principi (POUR) — kā tie izskatās mūsu ekrānos

| Princips | Nozīmē | Piemērs uzdevumā |
|----------|--------|------------------|
| **Uztverams** (Perceivable) | Informācija sasniedz lietotāju vismaz vienā maņā | Diagramma pārskatā + tā pati tabula; statuss tekstā, ne tikai krāsa; kontrasts ≥ 4,5:1 |
| **Darbināms** (Operable) | Visu var izdarīt ar tastatūru, bez laika spiediena, bez «lamatām» | Forma aizpildāma ar Tab/Enter; redzams fokuss; skip-link; pogas ≥ 24 px |
| **Saprotams** (Understandable) | Valoda, kļūdas un navigācija ir prognozējamas | `lang="lv"`; kļūda «Ievadiet e-pastu formā vards@domens.lv», ne «Nederīgs»; izvēlne vienāda visās lapās |
| **Robusts** (Robust) | Darbojas ar palīgtehnoloģijām | Semantisks HTML (`<button>`, `<label>`, `<th scope>`); `role="status"` paziņojumiem |

## 3. Kontrolsaraksts «Iesniegumi» (prasība → kritērijs → kā pārbauda → kur)

| # | Prasība | WCAG | Kā pārbauda | Ekrāns |
|---|---------|------|-------------|--------|
| 1 | Attēliem un diagrammām ir teksta alternatīva | 1.1.1 | axe `image-alt`; vai tabula dublē diagrammu | 6 |
| 2 | Virsrakstu hierarhija, tabulu galvenes, formu lauku saistība | 1.3.1 | axe `heading-order`, `th-has-data-cells`, `label`; ekrānlasītājs: H / T taustiņi | visi |
| 3 | Krāsa nav vienīgais informācijas nesējs | 1.4.1 | Pelēktoņu filtrs (DevTools › Rendering › Emulate vision deficiencies) | 4, 5 |
| 4 | Teksta kontrasts ≥ 4,5:1, UI elementu un fokusa ≥ 3:1 | 1.4.3, 1.4.11 | axe `color-contrast`; DevTools krāsu pipete | visi |
| 5 | 200 % mērogs un 320 px platums bez zuduma un horizontālās ritjoslas | 1.4.4, 1.4.10 | Ctrl + «+» līdz 200 %; DevTools ierīču režīms 320 px | visi |
| 6 | Viss darbināms ar tastatūru; nav fokusa lamatu | 2.1.1, 2.1.2 | Tab cauri visam ceļam «iesniegt iesniegumu» | 2, 5 |
| 7 | Skip-link uz saturu; lapas nosaukums; fokusa secība; saišu teksts | 2.4.1, 2.4.2, 2.4.3, 2.4.4 | Pirmais Tab = «Pāriet uz saturu»; `<title>` unikāls; saite «Iesniegums 2026-0001», ne «Skatīt» | visi |
| 8 | Fokuss redzams un nav aizsegts | 2.4.7, **2.4.11** (jauns 2.2) | Tab: kontūra redzama; fiksēta galvene neaizsedz fokusēto elementu | visi |
| 9 | Mērķa izmērs ≥ 24×24 px | **2.5.8** (jauns 2.2) | DevTools: pogu/saišu izmērs; atstarpes rindās | 4 |
| 10 | Lapas valoda | 3.1.1 | `<html lang="lv">`; axe `html-has-lang` | visi |
| 11 | Navigācija un elementi konsekventi; palīdzība vienā vietā | 3.2.3, 3.2.4, **3.2.6** (jauns 2.2) | Izvēlne un kājene vienādas; kontakti vienā vietā | visi |
| 12 | Kļūdas identificētas, lauki marķēti, ieteikts labojums | 3.3.1, 3.3.2, 3.3.3 | Iesniedz tukšu formu: kopsavilkums + ziņa pie lauka + fokuss uz kopsavilkumu | 2, 8 |
| 13 | Nav atkārtotas ievades; nav kognitīvu testu autentifikācijai | **3.3.7**, **3.3.8** (jauni 2.2) | Numurs no apstiprinājuma nav jāpārraksta no galvas; nav CAPTCHA | 3, 8 |
| 14 | Statusa ziņas nolasa ekrānlasītājs bez fokusa maiņas | 4.1.3 | `role="status"` pēc statusa maiņas; NVDA nolasa | 5 |
| 15 | Vilkšanai ir alternatīva (ja ir) | **2.5.7** (jauns 2.2) | Nav drag-and-drop bez pogas alternatīvas | — |

## 4. Testēšanas protokols (aizpilda komanda)

**A. Automātiski** — `python tests/a11y_check.py` (axe-core, visas lapas). Pārbaudiet arī formu ar kļūdām:
iesniedziet tukšu formu un palaidiet testu uz to pašu URL ar rezultātu.
Papildus: Chrome DevTools › Lighthouse › Accessibility; WAVE paplašinājums.
Automātiskie rīki atrod tikai **daļu** problēmu (tipiski 30–50 %). Pārējais — ar rokām.

**B. Tastatūra** (10 min, ceļš: sākums → loma → iesniegt → apstiprinājums → mans iesniegums)

| Pārbaude | Rezultāts | Piezīme |
|----------|-----------|---------|
| Pirmais Tab atver «Pāriet uz saturu» | ☐ OK ☐ Nē | |
| Fokuss redzams uz katra elementa | ☐ OK ☐ Nē | |
| Secība loģiska (pa lapu no augšas uz leju) | ☐ OK ☐ Nē | |
| Formu var iesniegt ar Enter; radio ar bultiņām | ☐ OK ☐ Nē | |
| Pēc kļūdas fokuss nonāk uz kļūdu kopsavilkumu | ☐ OK ☐ Nē | |
| Nav vietas, kur fokuss «iestrēgst» | ☐ OK ☐ Nē | |

**C. Mērogs un reflow** — 200 % (Ctrl +) un 320 px (DevTools): teksts nepārklājas, nav horizontālās ritjoslas, tabulas lasāmas.

**D. Ekrānlasītājs** (10 min; NVDA + Firefox/Chrome uz Windows, VoiceOver uz Mac, Narrator kā rezerve)

| Pārbaude | Rezultāts |
|----------|-----------|
| Lapas nosaukums tiek nolasīts, atverot lapu | ☐ |
| H taustiņš staigā pa virsrakstiem loģiskā secībā | ☐ |
| D taustiņš — orientieri: banner, navigation, main, contentinfo | ☐ |
| Formas laukiem nolasa nosaukumu, obligātumu, kļūdu | ☐ |
| Tabulā nolasa kolonnu galvenes, pārvietojoties pa šūnām | ☐ |
| Pēc statusa maiņas paziņojums nolasīts | ☐ |
| MI bloks tiek nosaukts kā «Ģenerēts ar MI …» | ☐ |

**E. Saturs** — vienkārša valoda, saišu teksts, kļūdu ziņojumi saka, *kā* labot.

**Atradumu reģistrs**

| # | Lapa | Problēma | WCAG | Smagums | Labots (commit) / Paliek paziņojumā |
|---|------|----------|------|---------|------------------------------------|
| 1 | | | | | |

## 5. Piekļūstamības paziņojuma veidne (MK 445; ES paraugs — Īstenošanas lēmums (ES) 2018/1523)

```
PIEKĻŪSTAMĪBAS PAZIŅOJUMS
[Iestāde] apņemas nodrošināt tīmekļvietnes [nosaukums, URL] piekļūstamību saskaņā ar
MK 14.07.2020. noteikumiem Nr. 445 «Kārtība, kādā iestādes ievieto informāciju internetā».

Cik piekļūstama ir šī tīmekļvietne?
[Pilnībā atbilst / Daļēji atbilst / Neatbilst] EN 301 549 (WCAG 2.1 AA) prasībām.

Nepiekļūstamais saturs
- [Problēma] — [lapa] — [WCAG kritērijs] — [iemesls: neatbilstība / nesamērīgs slogs / nav prasību tvērumā] — [termiņš].

Piekļūstamības alternatīvas
[Tālrunis, e-pasts, klātiene; kā saņemt to pašu pakalpojumu]

Atsauksmēm un saziņai
[E-pasts, tālrunis; atbildes termiņš]

Sūdzību iesniegšana
Ja atbilde nav saņemta vai neapmierina — [pārraugošā iestāde]; tālāk — Tiesībsargs.

Ziņas par paziņojuma sagatavošanu
Sagatavots [datums]. Metode: [pašnovērtējums pēc VARAM vadlīnijām / automātiskais tests (axe) /
manuālā pārbaude ar tastatūru un ekrānlasītāju]. Apstiprināja: [vārds, amats]. Pārskatīts: [datums].
```

## 6. Prompti Claude Code pieejamībai (kopējiet un pielāgojiet)

- «Pārskati `templates/iesniegt.html` pret WCAG 2.2 AA: label, kļūdu ziņojumi ar aria-describedby, kļūdu kopsavilkums ar role="alert" un fokusu, obligātie lauki tekstā. Saraksti, ko maini un kāpēc, pēc tam labo.»
- «Palaid `python tests/a11y_check.py`, izlasi a11y-report.md un izlabo visus critical un serious atradumus. Pēc labošanas palaid vēlreiz.»
- «Pārbaudi, vai saraksta tabulai ir caption un th scope, un vai statuss ir nodots tekstā, ne tikai ar krāsu.»
- «Pārskata diagrammai pievieno teksta alternatīvu: tā pati informācija tabulā un aria-hidden diagrammai, ja tā ir dekoratīva.»
- «Izveido lapu /pieklustamiba pēc docs/PIEEJAMIBAS-PRASIBAS.md 5. sadaļas veidnes un ieliec tajā šos atradumus: …»

**Ko Claude NEVAR izdarīt jūsu vietā:** pārbaudīt ar tastatūru un ekrānlasītāju, novērtēt, vai kļūdu ziņa ir saprotama cilvēkam, un uzņemties atbildību paziņojumā.
