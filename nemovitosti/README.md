# Nemovitosti – katalog nabídek (PDF)

Standardní formát pro nabídky nemovitostí z e-mailů (např. Jodi Henley „Palm Beach County to St Lucie County Properties“), které se posílají kamarádovi.

## Požadavky na výstup
- **Žádné jméno, telefon, e-mail, fax ani firma prodávajícího / makléře** – ani v textu, ani na fotkách.
- Vždy **dvě verze se stejným vzhledem**: česká (`Nemovitosti_katalog_Florida_<datum>.pdf`) a anglická (`Property_catalog_Florida_<datum>.pdf`).
- Vzhled: A4 na výšku, strana 1 = přehledová tabulka (#, adresa, město, typ, cena), pak každá nemovitost na vlastní stránce: adresa + cena, velká hlavní fotka, až 2 menší fotky, rámečky ložnice/koupelny · plocha · pozemek, „Stav a poznámky“ v odrážkách. Snížená cena = přeškrtnutá stará cena. Bez fotky = „Fotografie není k dispozici“.

## Postup
1. Najít e-mail v Gmailu, vzít `htmlBody`.
2. Fotky: v HTML jsou za každým „Asking“ obrázky `ci3.googleusercontent.com/...#<původní URL>` – googleusercontent je blokovaný proxy, stahovat **původní URL za `#`** (constantcontact, zillowstatic, redfin...). Opakující se oddělovací obrázek přeskočit. Pojmenovat `p01_0.jpg`, `p01_1.jpg`, … (číslo nemovitosti, `_0` = hlavní), zmenšit na max 1400 px, JPEG q82. Zkontrolovat, že na fotkách nejsou kontakty.
3. Vytvořit `data/<datum>_cs.py` a `data/<datum>_en.py` (TITLE, DATE, seznam P – viz existující soubory).
4. Vygenerovat:
   ```
   python3 nemovitosti/katalog.py nemovitosti/data/<datum>_cs.py cs <img_dir> Nemovitosti_katalog_Florida_<datum>.pdf
   python3 nemovitosti/katalog.py nemovitosti/data/<datum>_en.py en <img_dir> Property_catalog_Florida_<datum>.pdf
   ```
5. Kontrola: `pdftotext <pdf> - | grep -iE "jodi|954|@|ibuy"` nesmí nic najít.
