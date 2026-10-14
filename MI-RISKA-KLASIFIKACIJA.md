# MI komponentu riska klasifikācija (MI akts — Regula (ES) 2024/1689)

Attiecas uz uzdevumu «Iesniegumi». Klasificējam **katru MI komponentu atsevišķi**, pirms to būvējam.
Stāvoklis: 2026. gada oktobris, pēc «Digitālā omnibusa» grozījumiem (spēkā no 2026. g. jūlija).

## 1. Aktuālais ieviešanas grafiks

| Datums | Kas stājas spēkā | Mums |
|--------|------------------|------|
| 01.08.2024 | Regula stājas spēkā | — |
| 02.02.2025 | **Aizliegtās prakses** (5. p.) | Pārbaudām, ka nekas no tā nav mūsu sistēmā |
| 02.08.2025 | Vispārīga lietojuma MI modeļu (GPAI) pienākumi; pārvaldība, sodi | Attiecas uz modeļu nodrošinātājiem (piem., Anthropic), ne uz mums |
| 02.08.2026 | **Caurspīdīguma pienākumi (50. p.)**, lielākā daļa pārējo normu | Čata palīgs: informē, ka tas ir MI; ģenerēts saturs marķēts |
| 02.12.2026 | Jauns aizliegums (nepiekrītoša intīma satura / CSAM ģenerēšana); beidzas ūdenszīmju pārejas periods pirms 02.08.2026 tirgū laistām sistēmām | — |
| 02.08.2027 | Dalībvalstu MI «smilškastes» | Varam pieteikt eksperimentu |
| **02.12.2027** | **Augsta riska sistēmas — III pielikums** (bija 02.08.2026; pārcelts ar Omnibusu) | US-15 «Prioritātes vērtējums», ja to būvētu |
| **02.08.2028** | Augsta riska sistēmas — I pielikums (produkti ar nozaru drošības regulējumu) | Neattiecas |

Omnibuss nemaina: aizliegumus, GPAI pienākumus, sodu griestus, augsta riska prasību **saturu** (tikai termiņu).
4. pants (MI pratība): pienākums mīkstināts — Komisija un dalībvalstis «atbalsta un veicina»; iestādei darbinieku
apmācība tāpat ieteicama (un par to ir 5.2 nodarbība).

## 2. Lēmumu koks (katram komponentam)

```
0. Vai tā ir MI sistēma? (3. p. 1. pkt.: ar autonomiju, no ievades secina, kā ģenerēt izvadi — prognozes,
   saturu, ieteikumus, lēmumus). Atslēgvārdu `if/else` NAV MI sistēma; LLM, klasifikators, vērtēšanas modelis — IR.
   Nē → MI akts neattiecas (bet VDAR, pieejamība — jā).
1. Kāda ir mūsu loma? Paši izstrādājam → NODROŠINĀTĀJS (provider, 3. p. 3. pkt.) + UZTURĒTĀJS (deployer, 3. p. 4. pkt.).
   Lietojam gatavu → uzturētājs. Būtiski pārveidojam gatavu → kļūstam par nodrošinātāju (25. p.).
2. Aizliegta prakse (5. p.)? Sociālā vērtēšana, manipulācija, ievainojamību izmantošana, emociju atpazīšana
   darbā/izglītībā, biometriskā kategorizēšana pēc jutīgām pazīmēm, prognozējošā policija pēc profilēšanas, …
   Jā → NEDRĪKST. Stop.
3. Augsta riska joma? I pielikums (produkti: medicīnas ierīces, lifti, …) vai III pielikums:
   1 biometrija · 2 kritiskā infrastruktūra · 3 izglītība · 4 nodarbinātība · 5 piekļuve būtiskiem pakalpojumiem
   un pabalstiem (5.a — publiskās palīdzības pabalstu atbilstības vērtēšana, piešķiršana, samazināšana;
   5.d — neatliekamās palīdzības izsaukumu šķirošana) · 6 tiesībaizsardzība · 7 migrācija · 8 tiesvedība un demokrātija.
   Nē → 5. solis.
4. Jā, III pielikums → vai der 6. p. 3. d. izņēmums (nerada būtisku risku)?
   a) šaurs procedūras uzdevums; b) uzlabo jau pabeigtas cilvēka darbības rezultātu; c) atklāj lēmumu
   pieņemšanas modeļus/novirzes, neaizstājot cilvēka vērtējumu; d) sagatavošanās uzdevums vērtējumam.
   BET: ja veic fizisku personu PROFILĒŠANU → vienmēr augsts risks.
   Izņēmums der → dokumentējam pamatojumu, reģistrējam vienkāršotā kārtībā (49. p. 2. d.); ierobežots/minimāls risks.
   Neder → AUGSTS RISKS (8.–27. p.), piemēro no 02.12.2027.
5. Caurspīdīguma pienākumi (50. p.)? Sarunājas ar cilvēku (čats) → informē. Ģenerē tekstu/attēlu/audio → mašīnlasāms
   marķējums (nodrošinātājs). Dziļviltojums → norāda. Publicē MI ģenerētu tekstu sabiedrības informēšanai → norāda,
   ja nav cilvēka redakcionālas atbildības.
6. Pārējais → MINIMĀLS risks: brīvprātīgi rīcības kodeksi, laba prakse (cilvēka uzraudzība, žurnāls, marķējums).
```

## 3. Veidne (viens komponents = viena tabula)

| Lauks | Atbilde |
|-------|---------|
| Komponenta nosaukums | |
| Mērķis (ko dara, kam) | |
| Ievade → izvade | |
| Vai MI sistēma (3. p. 1. pkt.)? Kāpēc? | |
| Mūsu loma (nodrošinātājs / uzturētājs) | |
| Kas pieņem gala lēmumu — cilvēks vai sistēma? Vai cilvēks var lēmumu neņemt vērā? | |
| Ietekme uz personu (piekļuve pakalpojumam, nauda, tiesības, laiks)? | |
| Aizliegta prakse (5. p.)? | ☐ Nē ☐ Jā: … |
| III pielikuma joma? Kura? | ☐ Nē ☐ Jā: … |
| 6. p. 3. d. izņēmums? Kurš punkts? Profilēšana? | |
| Caurspīdīgums (50. p.)? | |
| **Riska klase** | ☐ Aizliegts ☐ Augsts ☐ Ierobežots (caurspīdīgums) ☐ Minimāls |
| Piemērojamie pienākumi | |
| Termiņš, no kura pienākumi jāpilda | |
| Pasākumi mūsu dizainā (cilvēka uzraudzība, marķējums, žurnāls, datu kvalitāte, FRIA, reģistrācija) | |
| Atlikušie jautājumi / kas jāpārbauda ar juristu | |

## 4. Aizpildīts piemērs: US-7 «MI ieteikums darbiniekam» (tēma + atbildes projekts)

| Lauks | Atbilde |
|-------|---------|
| Mērķis | Iesaka iesnieguma tēmu un sagatavo atbildes projektu darbiniekam |
| Ievade → izvade | Iesnieguma teksts → tēma (viena no 6) + atbildes teksts |
| MI sistēma? | Ar LLM — jā. Atslēgvārdu imitācija — nē (bet projektējam, it kā būtu LLM) |
| Loma | Izstrādājam paši uz GPAI modeļa bāzes → nodrošinātājs un uzturētājs |
| Gala lēmums | Darbinieks: rediģē un apstiprina; sistēma nekad nenosūta |
| Ietekme uz personu | Netieša: ātrāka/vienveidīgāka atbilde; risks — kļūdains projekts nokopēts bez lasīšanas |
| Aizliegta prakse | Nē |
| III pielikums | Tēmu šķirošana un teksta projekts nav 5.a (nevērtē atbilstību pabalstam). **Uzmanību:** ja tēma «Sociālā palīdzība» ietekmētu, *vai* iesniegums tiek izskatīts — jāpārvērtē |
| 6. p. 3. d. | Pat ja uzskatītu par III pielikuma jomu — a) šaurs procedūras uzdevums, d) sagatavošanās; nav profilēšanas |
| 50. p. | Ģenerē tekstu iekšējai lietošanai; publicēto atbildi apstiprina cilvēks → redakcionāla atbildība. Marķējam UI tāpat |
| **Riska klase** | **Minimāls / ierobežots** |
| Pienākumi | Laba prakse; ja izmanto GPAI API — nodrošinātāja noteikumi; VDAR (iesnieguma teksts ar personas datiem uz API — datu apstrādes līgums, minimizācija) |
| Pasākumi | Marķējums «Ģenerēts ar MI»; obligāta rediģēšana; žurnāls `notikumi`; kvalitātes izlases pārbaude reizi mēnesī; iespēja izslēgt |

## 5. Aizpildiet paši

- **US-10 Čata palīgs iedzīvotājam** — padoms: 50. p. 1. d.; kas notiek, ja čats dod nepareizu juridisku informāciju?
- **US-15 «Prioritātes vērtējums» sociālās palīdzības iesniegumiem** — padoms: III pielikums 5.a; profilēšana; 27. p.
  (pamattiesību ietekmes novērtējums publiskām iestādēm), 26. p. (uzturētāja pienākumi: cilvēka uzraudzība, žurnāli ≥ 6 mēn.,
  skarto personu informēšana), 49. p. (reģistrācija ES datubāzē), 86. p. (tiesības uz paskaidrojumu). Termiņš 02.12.2027.
  Jautājums grupai: vai to vispār vērts būvēt mācību prototipā — un ko tā vietā?

## 6. Prompti Claude Code

- «Izlasi docs/MI-RISKA-KLASIFIKACIJA.md un aizpildi veidni komponentam US-10, balstoties uz to, kā tas aprakstīts BACKLOG.md. Atzīmē, kur tu neesi drošs, un ko jāpārbauda juristam.»
- «Pārbaudi ai.py un detaļu šablonu: vai MI ieteikums ir marķēts tekstā, vai darbinieks to var rediģēt, vai lietošana ierakstās notikumos.»
- «Uzraksti 5 testa iesniegumus, ar kuriem MI ieteikums varētu kļūdīties (divdomīga tēma, vairākas problēmas vienā tekstā, sarkasms), un pārbaudi, ko dod ieteikums.»
