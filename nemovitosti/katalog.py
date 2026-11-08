"""Generate a property catalog PDF (summary table + one page per property with photos).
Usage: python3 katalog.py data/<date>_<lang>.py <cs|en> <image_dir> <out.pdf>
Images in image_dir are named p01_0.jpg, p01_1.jpg ... (property number, photo index; _0 = main photo).
"""
import html, glob, os, re, sys, subprocess
data, lang, imgdir, out = sys.argv[1:5]
ns = {}; exec(open(data).read(), ns); P, TITLE, DATE = ns['P'], ns['TITLE'], ns['DATE']
L = {
 'cs': dict(cols=['#','Adresa','Město','Typ','Cena'], bb='Ložnice / koupelny', area='Obytná plocha', lot='Pozemek',
            notes='Stav a poznámky', nophoto='Fotografie není k dispozici', cut='snížená cena', acre='akr',
            sub='Nabídka k {d} · {n} nemovitostí · ceny v USD · pouze hotovost nebo hard money · detail a fotografie na dalších stranách',
            foot='Všechny nemovitosti se prodávají ve stavu „as-is“. Údaje o stavu a stáří vybavení jsou orientační – doporučeno ověřit vlastní prověrkou. 1 sq ft ≈ 0,093 m² · 1 akr ≈ 4 047 m² · CBS = zděná konstrukce z betonových tvárnic · HOA/POA = poplatek společenství vlastníků.'),
 'en': dict(cols=['#','Address','City','Type','Price'], bb='Beds / baths', area='Living area', lot='Lot',
            notes='Condition & notes', nophoto='Photo not available', cut='price reduced', acre='acre',
            sub='Listings as of {d} · {n} properties · prices in USD · cash or hard money only · details and photos on the following pages',
            foot='All properties are sold as-is. Condition and system ages are approximate – buyers should do their own due diligence. 1 sq ft ≈ 0.093 m² · 1 acre ≈ 4,047 m² · CBS = concrete block & stucco construction · HOA/POA = homeowners / property owners association fee.'),
}[lang]
e = html.escape
def money(s): return '$' + s.replace(' ', ',')
def unit(lot): return lot if L['acre'] in lot or lot == '–' else lot + ' sq ft'
summary = ""
for i, (a, c, t, bb, sq, lot, n, price, old) in enumerate(P, 1):
    city = re.sub(r'\s*\d{5}$', '', c)
    summary += f"<tr><td class='n'>{i}</td><td><b>{e(a)}</b></td><td class='city'>{e(city)}</td><td>{e(t)}</td><td class='p'>{money(price)}</td></tr>"
pages = ""
for i, (a, c, t, bb, sq, lot, n, price, old) in enumerate(P, 1):
    imgs = sorted(glob.glob(os.path.join(os.path.abspath(imgdir), f'p{i:02d}_*.jpg')))
    zipc = re.search(r'\d{5}$', c).group(0); city = c[:-6]
    if imgs:
        main = f"<div class='main' style=\"background-image:url('file://{imgs[0]}')\"></div>"
        thumbs = "".join(f"<div class='th' style=\"background-image:url('file://{x}')\"></div>" for x in imgs[1:])
        thumbs = f"<div class='thumbs'>{thumbs}</div>" if thumbs else ""
    else:
        main = f"<div class='main none'>{L['nophoto']}</div>"; thumbs = ""
    pr = f"<div class='old'>{money(old)}</div>{money(price)}<div class='cut'>{L['cut']}</div>" if old else money(price)
    bullets = "".join(f"<li>{e(x.strip()[0].upper() + x.strip()[1:])}</li>" for x in n.split(';'))
    pages += f"""<section class='prop'>
<div class='num'>{i:02d} / {len(P)}</div>
<div class='head'><div><h2>{e(a)}</h2><div class='loc'>{e(city)}, FL {zipc} · {e(t)}</div></div><div class='price'>{pr}</div></div>
{main}{thumbs}
<div class='facts'><div><span>{L['bb']}</span><b>{e(bb)}</b></div><div><span>{L['area']}</span><b>{sq} sq ft</b></div><div><span>{L['lot']}</span><b>{e(unit(lot))}</b></div></div>
<h3>{L['notes']}</h3><ul>{bullets}</ul></section>"""
head = "".join(f"<th>{x}</th>" for x in L['cols'])
CSS = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'katalog.css')).read()
doc = f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<h1>{e(TITLE)}</h1>
<div class="sub">{L['sub'].format(d=DATE, n=len(P))}</div>
<table><thead><tr>{head}</tr></thead><tbody>{summary}</tbody></table>
<div class="note">{L['foot']}</div>
{pages}</body></html>"""
tmp = os.path.abspath(out) + '.html'
open(tmp, 'w').write(doc)
js = ("const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();"
      f"await p.goto('file://{tmp}',{{waitUntil:'load'}});await p.pdf({{path:'{os.path.abspath(out)}',preferCSSPageSize:true,printBackground:true}});await b.close()}})()")
subprocess.run(['node', '-e', js], check=True)
os.remove(tmp)
print('written', out)
