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

INSERT INTO iesniegumi (numurs, temas_id, vards, epasts, adrese, apraksts, statuss, izveidots) VALUES
 ('2026-0001', 1, 'Anna Bērziņa',  'anna@example.lv',  'Liepu iela 3',   'Liela bedre pretī mājai, bīstami velosipēdistiem.', 'Jauns', '2026-10-06 09:12'),
 ('2026-0002', 2, 'Jānis Ozols',   'janis@example.lv', 'Skolas iela 12', 'Nedeg trīs laternas pēc kārtas.', 'Apstrādē', '2026-10-07 14:30'),
 ('2026-0003', 3, 'Līga Kalniņa',  'liga@example.lv',  'Parka iela',     'Pārpildīts konteiners jau nedēļu.', 'Atbildēts', '2026-10-01 08:05');

INSERT INTO notikumi (iesnieguma_id, veids, loma, teksts) VALUES
 (1, 'statuss', 'sistema',    'Iesniegums reģistrēts ar statusu «Jauns».'),
 (2, 'statuss', 'darbinieks', 'Statuss mainīts uz «Apstrādē».'),
 (3, 'atbilde', 'darbinieks', 'Konteiners iztukšots 03.10. Paldies par ziņojumu.');
