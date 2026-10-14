-- Iesniegumi: datu modelis (minimums). Papildiniet, ja vajag.

CREATE TABLE temas (
    id        INTEGER PRIMARY KEY,
    nosaukums TEXT NOT NULL UNIQUE,
    apraksts  TEXT
);

CREATE TABLE iesniegumi (
    id            INTEGER PRIMARY KEY,
    numurs        TEXT NOT NULL UNIQUE,          -- piem., 2026-0001
    temas_id      INTEGER NOT NULL REFERENCES temas(id),
    vards         TEXT NOT NULL,
    epasts        TEXT NOT NULL,
    adrese        TEXT,
    apraksts      TEXT NOT NULL,
    statuss       TEXT NOT NULL DEFAULT 'Jauns'  -- Jauns | Apstrādē | Atbildēts | Noraidīts
                  CHECK (statuss IN ('Jauns', 'Apstrādē', 'Atbildēts', 'Noraidīts')),
    atbilde       TEXT,
    izveidots     TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    atjaunots     TEXT NOT NULL DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE notikumi (
    id            INTEGER PRIMARY KEY,
    iesnieguma_id INTEGER NOT NULL REFERENCES iesniegumi(id) ON DELETE CASCADE,
    laiks         TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
    veids         TEXT NOT NULL,                 -- statuss | komentars | atbilde | mi_ieteikums
    loma          TEXT,                          -- iedzivotajs | darbinieks | vaditajs | sistema
    teksts        TEXT NOT NULL
);

INSERT INTO temas (nosaukums, apraksts) VALUES
 ('Ielas un ceļi',        'Bedres, ceļa zīmes, ietves'),
 ('Apgaismojums',         'Nedeg vai bojāts ielu apgaismojums'),
 ('Atkritumi un vide',    'Nesavākti atkritumi, piesārņojums'),
 ('Bērnudārza rinda',     'Jautājumi par rindu un vietām'),
 ('Sociālā palīdzība',    'Pabalsti un sociālie pakalpojumi'),
 ('Cits',                 'Viss pārējais');

-- Testa dati: izdomātas personas un adreses (nav reālu personu datu)
INSERT INTO iesniegumi (numurs, temas_id, vards, epasts, adrese, apraksts, statuss, atbilde, izveidots, atjaunots) VALUES
 ('2026-0001', 1, 'Anna Bērziņa',   'anna@example.lv',   'Liepu iela 3',      'Liela bedre pretī mājai, bīstami velosipēdistiem.', 'Jauns', NULL, '2026-10-06 09:12', '2026-10-06 09:12'),
 ('2026-0002', 2, 'Jānis Ozols',    'janis@example.lv',  'Skolas iela 12',    'Nedeg trīs laternas pēc kārtas.', 'Apstrādē', NULL, '2026-10-07 14:30', '2026-10-08 10:00'),
 ('2026-0003', 3, 'Līga Kalniņa',   'liga@example.lv',   'Parka iela',        'Pārpildīts konteiners jau nedēļu.', 'Atbildēts', 'Konteiners iztukšots 03.10. Paldies par ziņojumu.', '2026-10-01 08:05', '2026-10-03 11:20'),
 ('2026-0004', 1, 'Pēteris Liepa',  'peteris@example.lv', 'Dārza iela 7',     'Ietve izdrupusi pie autobusa pieturas, grūti pārvietoties ar ratiņiem.', 'Apstrādē', NULL, '2026-10-02 16:40', '2026-10-05 09:15'),
 ('2026-0005', 2, 'Ilze Krūmiņa',   'ilze@example.lv',   'Ezera iela 1',      'Laterna pie skolas mirgo visu nakti.', 'Atbildēts', 'Laternas spuldze nomainīta 06.10.', '2026-10-03 07:55', '2026-10-06 13:00'),
 ('2026-0006', 3, 'Mārtiņš Egle',   'martins@example.lv', 'Meža ceļš',        'Mežmalā izmesti būvgruži un riepas.', 'Jauns', NULL, '2026-10-09 12:10', '2026-10-09 12:10'),
 ('2026-0007', 4, 'Kristīne Vītola','kristine@example.lv', 'Saules iela 15',   'Vēlos uzzināt, kurā vietā rindā uz bērnudārzu ir mans bērns.', 'Atbildēts', 'Jūsu bērns rindā ir 12. vietā. Rindu varat pārbaudīt arī klātienē domē.', '2026-09-28 10:00', '2026-10-01 15:30'),
 ('2026-0008', 4, 'Andris Kļava',   'andris@example.lv', 'Upes iela 4',       'Vai var mainīt izvēlēto bērnudārzu, ja esam pārcēlušies?', 'Noraidīts', 'Bērnudārza maiņai jāiesniedz jauns pieteikums ar deklarēto adresi.', '2026-09-30 09:20', '2026-10-02 14:00'),
 ('2026-0009', 5, 'Dace Rozīte',    'dace@example.lv',   'Lauku iela 9',      'Lūdzu informāciju, kādi dokumenti vajadzīgi, lai pieteiktos sociālajam pakalpojumam.', 'Apstrādē', NULL, '2026-10-08 11:45', '2026-10-09 08:30'),
 ('2026-0010', 6, 'Edgars Priede',  'edgars@example.lv', NULL,                'Pašvaldības mājaslapā nestrādā saite uz pasākumu kalendāru.', 'Jauns', NULL, '2026-10-10 18:05', '2026-10-10 18:05');

INSERT INTO notikumi (iesnieguma_id, laiks, veids, loma, teksts) VALUES
 (1,  '2026-10-06 09:12', 'statuss', 'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (2,  '2026-10-07 14:30', 'statuss', 'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (2,  '2026-10-08 10:00', 'statuss', 'darbinieks', 'Statuss mainīts uz «Apstrādē».'),
 (3,  '2026-10-01 08:05', 'statuss', 'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (3,  '2026-10-02 09:00', 'statuss', 'darbinieks', 'Statuss mainīts uz «Apstrādē».'),
 (3,  '2026-10-03 11:15', 'atbilde', 'darbinieks', 'Konteiners iztukšots 03.10. Paldies par ziņojumu.'),
 (3,  '2026-10-03 11:20', 'statuss', 'darbinieks', 'Statuss mainīts uz «Atbildēts».'),
 (4,  '2026-10-02 16:40', 'statuss', 'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (4,  '2026-10-05 09:15', 'statuss', 'darbinieks', 'Statuss mainīts uz «Apstrādē».'),
 (4,  '2026-10-05 09:20', 'komentars', 'darbinieks', 'Nodots Ceļu nodaļai apsekošanai.'),
 (5,  '2026-10-03 07:55', 'statuss', 'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (5,  '2026-10-04 10:30', 'statuss', 'darbinieks', 'Statuss mainīts uz «Apstrādē».'),
 (5,  '2026-10-06 12:55', 'atbilde', 'darbinieks', 'Laternas spuldze nomainīta 06.10.'),
 (5,  '2026-10-06 13:00', 'statuss', 'darbinieks', 'Statuss mainīts uz «Atbildēts».'),
 (6,  '2026-10-09 12:10', 'statuss', 'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (7,  '2026-09-28 10:00', 'statuss', 'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (7,  '2026-09-29 09:10', 'statuss', 'darbinieks', 'Statuss mainīts uz «Apstrādē».'),
 (7,  '2026-10-01 15:25', 'atbilde', 'darbinieks', 'Jūsu bērns rindā ir 12. vietā. Rindu varat pārbaudīt arī klātienē domē.'),
 (7,  '2026-10-01 15:30', 'statuss', 'darbinieks', 'Statuss mainīts uz «Atbildēts».'),
 (8,  '2026-09-30 09:20', 'statuss', 'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (8,  '2026-10-02 13:55', 'atbilde', 'darbinieks', 'Bērnudārza maiņai jāiesniedz jauns pieteikums ar deklarēto adresi.'),
 (8,  '2026-10-02 14:00', 'statuss', 'darbinieks', 'Statuss mainīts uz «Noraidīts».'),
 (9,  '2026-10-08 11:45', 'statuss', 'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (9,  '2026-10-09 08:30', 'statuss', 'darbinieks', 'Statuss mainīts uz «Apstrādē».'),
 (10, '2026-10-10 18:05', 'statuss', 'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».');
