# -*- coding: utf-8 -*-
"""build.py — writes docs/ from content.py, data/own/own.json and data/commons/credits.json.

    python3 tools/build.py            # SITE_URL defaults to the GitHub Pages address
"""
import html, json, os, shutil, sys, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import content as C  # noqa: E402
import content_th as TH  # noqa: E402
import fleet  # noqa: E402

DOCS = Path(os.environ["OUT"]) if os.environ.get("OUT") else ROOT / "docs"
SITE_URL = os.environ.get("SITE_URL", "https://nanobotco.github.io/chiang-rai").rstrip("/")
CANON = "https://motdang.net/chiang-rai"
PAGES = "https://nanobotco.github.io/chiang-rai"
TITLE = "Chiang Rai, Slowly"
TITLE_TH = "แอ่วเชียงราย ค่อย ๆ ไปเน้อ"
OWN = json.loads((ROOT / "data/own/own.json").read_text())
CRED = json.loads((ROOT / "data/commons/credits.json").read_text())
BANDS_CSS = (ROOT / "tools/bands.css").read_text()
e = lambda s: html.escape("" if s is None else str(s), quote=True)  # noqa: E731
LANG = "en"
A = "{A}"  # the site root, for img/ and v/; {PRE} is the root of the page's own language


def t(en, th):
    return th if LANG == "th" else en


def bi(en, th, tp=None):
    """A label and its other-language partner: English first on English pages, Thai first on Thai."""
    if LANG == "th":
        return f'{tp or th} · <span lang="en">{en}</span>'
    return f'{en} · <span lang="th" class="th">{th}</span>'


def sub_lang():
    return "en" if LANG == "th" else "th"


def loc(s, table=None, key="name"):
    """An item from content.py in the page's language. The `th` field carries the other language's name."""
    s = dict(s)
    s.setdefault("id", slug(s["name"]))
    if LANG != "th":
        return s
    th = table.get(s[key]) if table is not None else None
    if isinstance(th, dict):
        s.update({k: v for k, v in th.items() if k in ("kicker", "text", "days")})
    elif isinstance(th, str):
        s["text"] = th
    s["name"], s["th"] = s["th"], s["name"]
    s["th_text"] = None
    return s


def img(ref: str, thumb=False) -> str:
    kind, slug = ref.split(":", 1)
    base = A + ("img/own/" if kind == "own" else "img/c/")
    return base + slug + ("-t.jpg" if thumb else ".jpg")


def credit(ref: str) -> str:
    kind, slug = ref.split(":", 1)
    if kind == "own":
        return t('Photo', 'ภาพ') + ': NaN · <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>'
    c = CRED[slug]
    return (f'{e(c["author"][:48])} · <a href="{e(c["page"])}">Commons</a> · '
            f'<a href="{e(c["licence_url"])}">{e(c["licence"])}</a>')


def osm(q: str) -> str:
    return "https://www.openstreetmap.org/search?query=" + urllib.parse.quote(q + ", Chiang Rai")


def band(ref, kicker="", head="", line="", href="", cta="", cls="", th="", pre="{PRE}"):
    inner = [f'<span class="kicker">{e(kicker)}</span>' if kicker else "",
             f"<h2>{e(head)}</h2>" if head else "",
             f'<p class="th" lang="th">{e(th)}</p>' if th and LANG == "en" else "",
             f"<p>{e(line)}</p>" if line else "",
             f'<a class="btn" href="{"" if href.startswith("http") else pre}{e(href)}">{e(cta)}</a>' if href and cta else ""]
    return (f'<section class="band {cls}" style="background-image:url({img(ref)})">'
            f'<div class="in">{"".join(inner)}</div><span class="cred">{credit(ref)}</span></section>')


def shot(ref, name, href, sub="", ratio=125, pre="", ext=False):
    """The linked-image formula: background · scrim · spacer · text, the whole box a link."""
    tgt = ' rel="noopener"' if ext else ""
    return (f'<a class="shot" href="{e(href)}"{tgt}><span class="bg" style="background-image:url({img(ref, True)})"></span>'
            f'<span class="scrim"></span><span class="sp" style="padding-top:{ratio}%"></span>'
            f'<span class="tx"><b>{e(name)}</b>{f"<i>{e(sub)}</i>" if sub else ""}</span></a>')


def note(key, pre=""):
    n = C.NOTES[key]
    if LANG == "th":
        n = dict(n, **TH.NOTES[key])
        n["kicker"] = n["kicker"] + " · " + C.NOTES[key]["th"]
        ext = n["href"].startswith("http")
        rel = ' rel="noopener"' if ext else ""
        return (f'<aside class="note"><span class="nk">{e(n["kicker"])}</span><p>{e(n["line"])}</p>'
                f'<a href="{e(n["href"] if ext else pre + n["href"])}"{rel}>{e(n["cta"])} →</a></aside>')
    href = n["href"] if n.get("ext") or n["href"].startswith("http") else pre + n["href"]
    rel = ' rel="noopener"' if n.get("ext") or href.startswith("http") else ""
    return (f'<aside class="note"><span class="nk">{e(n["kicker"])} <span lang="th" class="th">· {e(n["th"])}</span></span>'
            f'<p>{e(n["line"])}</p><a href="{e(href)}"{rel}>{e(n["cta"])} →</a></aside>')


def trip(slug):
    return C.TRIP + slug + "/"


def thb(n):
    return f"฿{n:,}"


# ---------------------------------------------------------------- the stylesheet
CSS = r"""
:root{--bg:#fbf8f1;--paper:#fffdf8;--ink:#161412;--mute:#6b6259;--line:#e3dccd;--accent:#0e6b62;
 --gold:#a8791f;--rose:#b3413b;--focus:#0a4fd1;
 --display:"Didot","Bodoni 72","Bodoni MT","Iowan Old Style",Georgia,serif;
 --body:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
 --sans:"Avenir Next",Avenir,"Helvetica Neue",Arial,sans-serif;
 --thai:"Noto Serif Thai","Thonburi","Sukhumvit Set","Leelawadee UI",Tahoma,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#121110;--paper:#1a1816;--ink:#f3ede2;
 --mute:#b3a898;--line:#34302a;--accent:#4fc1b1;--gold:#e0b458;--rose:#f08a7f;--focus:#8ab4f8}}
:root[data-theme="dark"]{--bg:#121110;--paper:#1a1816;--ink:#f3ede2;--mute:#b3a898;--line:#34302a;
 --accent:#4fc1b1;--gold:#e0b458;--rose:#f08a7f;--focus:#8ab4f8}
*{box-sizing:border-box}
html{font-size:19px;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);line-height:1.62;
 font-feature-settings:"onum","liga","kern"}
.th,:lang(th){font-family:var(--thai);line-height:1.9}
a{color:var(--accent);text-decoration-thickness:.06em;text-underline-offset:.2em}
a:hover{color:var(--rose)}
a:focus-visible{outline:3px solid var(--focus);outline-offset:3px;border-radius:3px}
img,video{max-width:100%;height:auto;display:block}
.col{max-width:40rem;margin:0 auto;padding:0 16px}
.wide{max-width:66rem;margin:0 auto;padding:0 16px}

/* masthead */
header.mast{border-bottom:1px solid var(--ink);background:var(--bg)}
header.mast .in{max-width:66rem;margin:0 auto;padding:.9rem 16px .6rem;display:flex;flex-wrap:wrap;
 align-items:baseline;justify-content:space-between;gap:.4rem 1.2rem}
.brand{font-family:var(--display);font-size:1.7rem;font-weight:400;letter-spacing:.01em;color:var(--ink);
 text-decoration:none;line-height:1}
.brand i{color:var(--accent)}
header.mast nav{display:flex;flex-wrap:wrap;gap:.2rem 1rem;font-family:var(--sans);font-size:.66rem;
 letter-spacing:.16em;text-transform:uppercase}
header.mast nav a{color:var(--mute);text-decoration:none;padding:.2rem 0}
header.mast nav a:hover,header.mast nav a[aria-current]{color:var(--ink);box-shadow:inset 0 -1px 0 var(--ink)}
.presented{font-family:var(--sans);font-size:.6rem;letter-spacing:.2em;text-transform:uppercase;color:var(--mute);
 text-align:center;padding:.45rem 16px;border-bottom:1px solid var(--line)}
.presented a{color:var(--gold);text-decoration:none}

/* the feature opening */
.open{text-align:center;padding:3.2rem 0 1.6rem}
.rubric{font-family:var(--sans);font-size:.66rem;letter-spacing:.3em;text-transform:uppercase;color:var(--rose)}
h1{font-family:var(--display);font-weight:400;font-size:clamp(2.6rem,9vw,5rem);line-height:.98;margin:.6rem 0 .5rem;
 letter-spacing:-.01em}
.dek{font-style:italic;font-size:1.2rem;color:var(--mute);max-width:32rem;margin:0 auto}
.dek-th{font-size:1rem;color:var(--mute);margin:.4rem auto 0}
.by{font-family:var(--sans);font-size:.62rem;letter-spacing:.2em;text-transform:uppercase;margin-top:1.2rem}
.by a{color:var(--ink)}
h2.sec{font-family:var(--display);font-weight:400;font-size:clamp(1.7rem,5vw,2.4rem);line-height:1.08;
 margin:2.6rem 0 .3rem}
h2.sec small{display:block;font-family:var(--sans);font-size:.6rem;letter-spacing:.3em;text-transform:uppercase;
 color:var(--rose);margin-bottom:.5rem}
h3{font-family:var(--display);font-weight:400;font-size:1.45rem;margin:1.8rem 0 .2rem;line-height:1.15}
h3 .thn{font-family:var(--thai);font-size:.8rem;color:var(--mute);margin-left:.4rem}
p.lede::first-letter{font-family:var(--display);float:left;font-size:4.6rem;line-height:.82;
 padding:.34rem .5rem 0 0;color:var(--accent)}
p.th{color:var(--mute);font-size:.95rem}
.fleuron{text-align:center;color:var(--gold);letter-spacing:1em;margin:2.2rem 0;font-size:.9rem}

/* pull quote */
blockquote.pull{margin:2.4rem 0;padding:1.2rem 0;border-top:1px solid var(--ink);border-bottom:1px solid var(--ink);
 text-align:center}
blockquote.pull p{font-family:var(--display);font-size:clamp(1.4rem,4vw,1.9rem);line-height:1.22;margin:0}
blockquote.pull cite{display:block;margin-top:.7rem;font-family:var(--sans);font-style:normal;font-size:.62rem;
 letter-spacing:.24em;text-transform:uppercase;color:var(--mute)}

/* the margin notes, New Yorker style: small, ruled, easy to pass by */
aside.note{font-family:var(--sans);font-size:.72rem;line-height:1.45;color:var(--mute);border-top:2px solid var(--gold);
 padding:.55rem 0 .2rem;margin:1.4rem 0;
 background:linear-gradient(180deg,color-mix(in srgb,var(--gold) 9%,transparent),transparent 70%);
 background-attachment:fixed}
aside.note .nk{display:block;font-size:.56rem;letter-spacing:.22em;text-transform:uppercase;color:var(--gold);
 margin-bottom:.25rem}
aside.note .nk .th{letter-spacing:0;text-transform:none;font-size:.7rem}
aside.note p{margin:0 0 .3rem}
aside.note a{font-weight:600;text-decoration:none;color:var(--accent)}
aside.note a:hover{text-decoration:underline}
@media (min-width:70rem){
 .col aside.note{float:right;clear:right;width:12.5rem;margin:.3rem -15rem 1rem 1.5rem}
 .col aside.note.l{float:left;clear:left;margin:.3rem 1.5rem 1rem -15rem}
}
@media (pointer:coarse),(prefers-reduced-motion:reduce){aside.note{background-attachment:scroll}}

/* the linked-image formula */
.shots{display:grid;grid-template-columns:repeat(auto-fill,minmax(14rem,1fr));gap:1.1rem;margin:1.4rem 0}
.shots.three{grid-template-columns:repeat(auto-fill,minmax(18rem,1fr))}
figure.card{margin:0}
a.shot{position:relative;display:block;overflow:hidden;text-decoration:none;color:#fff;isolation:isolate;
 background:#0b0906}
a.shot .bg{position:absolute;inset:0;z-index:-3;background-size:cover;background-position:center}
a.shot .scrim{position:absolute;inset:0;z-index:-2;background:linear-gradient(180deg,rgba(0,0,0,0) 38%,
 rgba(8,6,4,.84) 100%)}
a.shot .sp{display:block}
a.shot .tx{position:absolute;left:0;right:0;bottom:0;padding:.9rem 1rem}
a.shot .tx b{display:block;font-family:var(--display);font-weight:400;font-size:1.35rem;line-height:1.08}
a.shot .tx i{display:block;font-family:var(--thai);font-style:normal;font-size:.78rem;opacity:.86;margin-top:.2rem}
@media (prefers-reduced-motion:no-preference){
 a.shot .bg{transition:transform .9s cubic-bezier(.2,.7,.2,1)}
 a.shot:hover .bg,a.shot:focus-visible .bg{transform:scale(1.06)}
}
figure.card figcaption{font-size:.84rem;line-height:1.5;padding:.55rem 0 0}
figure.card .cred,.cred{font-family:var(--sans);font-size:.56rem;color:var(--mute)}
figure.card .cred a,.cred a{color:var(--mute)}

/* a sight, long form */
.sight{display:grid;grid-template-columns:1fr;gap:1rem;margin:2.2rem 0;padding-top:1.4rem;border-top:1px solid var(--line)}
@media (min-width:46rem){.sight{grid-template-columns:15rem 1fr;gap:1.6rem}}
.sight .go{font-family:var(--sans);font-size:.66rem;letter-spacing:.12em;text-transform:uppercase;margin-top:.4rem}
.sight .go a{margin-right:1rem}
.sight video{margin-top:.8rem;border-radius:2px}
.kick{font-family:var(--sans);font-size:.6rem;letter-spacing:.26em;text-transform:uppercase;color:var(--rose)}

/* Laila's list, typeset like a listings column */
table.list{width:100%;border-collapse:collapse;margin:1rem 0 1.6rem;font-size:.92rem}
table.list td{padding:.62rem .3rem;border-bottom:1px solid var(--line);vertical-align:top}
table.list td.p{text-align:right;width:9.5rem;font-variant-numeric:lining-nums tabular-nums;color:var(--ink)}
table.list td b{font-weight:600}
table.list td a{text-decoration:none}
table.list td small{display:block;color:var(--mute);font-size:.82rem}
@media (max-width:34rem){table.list tr{display:block;border-bottom:1px solid var(--line);padding:.5rem 0}table.list td{display:block;border:0;padding:.1rem 0;width:auto}table.list td.p{text-align:left;font-weight:600;color:var(--gold)}}
.asof{font-family:var(--sans);font-size:.62rem;color:var(--mute);letter-spacing:.06em}
.btn{display:inline-block;font-family:var(--sans);font-size:.66rem;font-weight:600;letter-spacing:.2em;
 text-transform:uppercase;text-decoration:none;color:#fff;background:var(--accent);padding:.8rem 1.2rem;border-radius:2px}
.btn:hover{color:#fff;background:var(--rose)}
.btn.ghost{background:transparent;color:var(--accent);box-shadow:inset 0 0 0 1px var(--accent)}
@media (prefers-reduced-motion:no-preference){.btn{transition:transform .25s cubic-bezier(.3,1.6,.5,1),background .2s}
 .btn:hover{transform:translateY(-2px) scale(1.03)}}
.ctas{display:flex;flex-wrap:wrap;gap:.6rem;margin:1.2rem 0}

/* NaN's roll */
.roll{columns:3 12rem;column-gap:1rem;margin:1.4rem 0}
.roll figure{break-inside:avoid;margin:0 0 1rem}
.roll figcaption{font-size:.78rem;color:var(--mute);padding-top:.3rem}
.polaroid{background:var(--paper);padding:.6rem .6rem 1.4rem;box-shadow:0 10px 30px rgba(20,14,6,.14);
 transform:rotate(-1.6deg);max-width:17rem;margin:1.4rem auto}
.polaroid figcaption{font-style:italic;text-align:center;font-size:.85rem;padding-top:.5rem}

footer{margin-top:4rem;border-top:1px solid var(--ink);padding:1.6rem 16px 3rem;font-family:var(--sans);
 font-size:.7rem;color:var(--mute);line-height:1.7}
footer .in{max-width:66rem;margin:0 auto}
footer a{color:var(--mute)}
footer .support,footer .fleet{margin-top:.6rem}

/* lantern sky: photo · scrim · canvas of rising lanterns (math) · type */
.skyband{position:relative;isolation:isolate;margin-left:calc(50% - 50vw);margin-right:calc(50% - 50vw);width:100vw;
 min-height:clamp(420px,92vh,900px);display:grid;place-items:center;text-align:center;color:#fff;overflow:hidden;
 background:#07060a center/cover no-repeat;background-attachment:fixed;margin-block:2.6rem}
.skyband::before{content:"";position:absolute;inset:0;z-index:-2;background:radial-gradient(90% 70% at 50% 35%,
 rgba(20,10,30,.25),rgba(6,4,10,.86) 80%),linear-gradient(180deg,rgba(6,4,12,.7),rgba(6,4,12,.2) 40%,rgba(6,4,12,.9))}
.skyband canvas{position:absolute;inset:0;width:100%;height:100%;z-index:-1;cursor:pointer}
.skyband .in{padding:3rem 16px;pointer-events:none}
.skyband .in a{pointer-events:auto}
.skyband .kicker{font-family:var(--sans);font-size:.66rem;letter-spacing:.34em;text-transform:uppercase;color:#ffcf7a}
.skyband h2{font-family:var(--display);font-weight:400;font-size:clamp(3rem,13vw,9rem);line-height:.9;margin:.4rem 0;
 text-shadow:0 0 40px rgba(255,170,60,.45)}
.skyband .thbig{font-family:var(--thai);font-size:clamp(1.3rem,4vw,2.2rem);color:#ffe3b0}
.skyband .tap{font-family:var(--sans);font-size:.62rem;letter-spacing:.2em;text-transform:uppercase;color:#d9c7a6;margin-top:1rem}
@media (pointer:coarse),(prefers-reduced-motion:reduce){.skyband{background-attachment:scroll}}
.count{display:flex;justify-content:center;align-items:center;gap:1.4rem;margin:1.6rem 0 0;flex-wrap:wrap}
.count b{display:block;font-family:var(--display);font-weight:400;font-size:clamp(4rem,16vw,8rem);line-height:.85;color:#ffcf7a}
.count small{display:block;max-width:17rem;margin:.4rem auto 0;line-height:1.7;font-family:var(--sans);font-size:.62rem;letter-spacing:.2em;text-transform:uppercase;color:#e9dcc4}
.count svg{width:92px;height:92px;filter:drop-shadow(0 0 22px rgba(255,220,150,.5))}
.bigshots{display:grid;grid-template-columns:repeat(auto-fit,minmax(18rem,1fr));gap:0;margin:0 calc(50% - 50vw);width:100vw}
.bigshots a.shot .tx b{font-size:clamp(1.8rem,4vw,2.6rem)}
.bigshots a.shot .tx i{font-size:.95rem}
.bigshots a.shot .tx p{margin:.4rem 0 0;font-size:.95rem;max-width:26ch;color:#f3e7d2}
""" + BANDS_CSS + r"""
.band{--display:"Didot","Bodoni 72",Georgia,serif;--accent:#0e6b62;border-top:1px solid var(--ink);border-bottom:1px solid var(--ink)}
.band h2{text-transform:none;font-weight:400;letter-spacing:0;line-height:1.02}
.band .kicker{font-family:var(--sans);font-weight:600}
.band p.th{color:#efe6d6;font-size:1rem}
@media print{aside.note,header.mast nav{display:none}}
.skip{position:absolute;left:-9999px;top:0;z-index:9;background:var(--ink);color:var(--bg);padding:.5rem .9rem;font-family:var(--sans)}
.skip:focus{left:8px;top:8px}
:lang(th){letter-spacing:0!important;text-transform:none!important}
html:lang(th) :is(h1,h2,h3,.brand,a.shot .tx b,blockquote.pull p,.band h2){line-height:1.32}
html:lang(th) .skyband h2{line-height:1.15}
html:lang(th) :is(h1,h2,.dek){text-wrap:balance}
html:lang(th) table.list td.p{width:13rem}
html:lang(th) .count b{line-height:.85}
html:lang(th) p.lede::first-letter{float:none;font:inherit;padding:0;color:inherit}
"""

NAV_TH = ["เชียงราย", "สามเหลี่ยมทองคำ", "ที่เที่ยว", "แอ่วนอกเส้นทาง", "เรือช้า", "ไลลากรุ๊ป", "โคมลอย", "ภาพของ NaN"]
NAV = [("", "Chiang Rai"), ("golden-triangle/", "Golden Triangle"), ("see/", "The sights"),
       ("sidequests/", "Sidequests"), ("slow-boat/", "Slow boat"), ("with-laila/", "Laila Group"),
       ("lanterns/", "Lanterns"), ("roll/", "NaN's roll")]


def page(path: str, title: str, desc: str, body: str, card="card.jpg", ld=None):
    th = LANG == "th"
    pre = "../" * path.count("/")
    ap = pre + ("../" if th else "")
    labels = NAV_TH if th else [x for _, x in NAV]
    nav = "".join(f'<a href="{pre}{h}"{" aria-current=page" if h == path else ""}>{e(t)}</a>' for (h, _), t in zip(NAV, labels))
    nav += (f'<a href="{ap}{path}" lang="en" hreflang="en">English</a>' if th
            else f'<a href="{pre}th/{path}" lang="th" hreflang="th">ไทย</a>')
    tp = "th/" if th else ""
    url = CANON + "/" + tp + path
    alt = PAGES + "/" + tp + path
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    site_title = TITLE_TH if th else TITLE
    full = title if title == site_title else f"{title} · {site_title}"
    body = body.replace("{PRE}", pre).replace(A, ap)
    brand = f"แอ่วเชียงราย <i>ค่อย ๆ ไปเน้อ</i>" if th else "Chiang Rai, <i>Slowly</i>"
    presented = (f'ร่วมนำเสนอโดย <a href="{pre}with-laila/">ไลลากรุ๊ป</a> เชียงราย · <span lang="en">Laila Group, Chiang Rai</span>' if th
                 else f'Presented with <a href="{pre}with-laila/">Laila Group</a>, Chiang Rai · <span lang="th" class="th">ไลลากรุ๊ป เชียงราย</span>')
    if th:
        foot = f"""<p><b>{TITLE_TH}</b> · <span lang="en">Chiang Rai, Slowly</span> · ร่วมนำเสนอโดยไลลากรุ๊ป {e(C.ADDRESS_TH)} ·
<a href="{e(C.wa(TH.HELLO))}" rel="noopener">WhatsApp {e(C.PHONE)}</a> · <a href="mailto:{C.MAIL}">{e(C.MAIL)}</a></p>
<p>ราคาเป็นของไลลากรุ๊ปเอง ตามที่ลงไว้บน <a href="{C.SHOP}/" rel="noopener">slowboatthailandlaos.com</a> เมื่อ {TH.READ}
ภาพถ่ายของ NaN ใช้สัญญาอนุญาต CC BY 4.0 ภาพอื่นมีชื่อผู้ถ่ายและสัญญาอนุญาตกำกับไว้ข้างภาพ ข้อความ CC BY 4.0 โค้ด MIT
<a href="{pre}credits/">เครดิต</a></p>
{fleet.maker_html(lang="th")}
{fleet.row_html("chiang-rai", label="เว็บอื่นจาก NaNoBotCo")}"""
    else:
        foot = f"""<p><b>Chiang Rai, Slowly</b> · <span lang="th" class="th">{TITLE_TH}</span> · presented with Laila Group, {e(C.ADDRESS)} ·
<a href="{C.WA}" rel="noopener">WhatsApp {e(C.PHONE)}</a> · <a href="mailto:{C.MAIL}">{e(C.MAIL)}</a></p>
<p>Prices are Laila Group's own, as listed on <a href="{C.SHOP}/" rel="noopener">slowboatthailandlaos.com</a> on {C.READ}.
Photographs by NaN are CC BY 4.0; every other photograph carries its author and licence beside it. Text CC BY 4.0, code MIT.
<a href="{pre}credits/">Credits</a>.</p>
{fleet.maker_html()}
{fleet.row_html("chiang-rai")}"""
    doc = f"""<!doctype html><html lang="{LANG}" translate="no" class="notranslate"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="google" content="notranslate">
<title>{e(full)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}"><link rel="alternate" href="{alt}"><meta name="theme-color" content="#0e6b62">
<link rel="alternate" hreflang="en" href="{CANON}/{path}"><link rel="alternate" hreflang="th" href="{CANON}/th/{path}"><link rel="alternate" hreflang="x-default" href="{CANON}/{path}">
<meta property="og:type" content="website"><meta property="og:title" content="{e(full)}"><meta property="og:locale" content="{"th_TH" if th else "en_US"}">
<meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/{card}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE_URL}/{card}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cpath d='M16 3 29 27H3z' fill='%23a8791f'/%3E%3C/svg%3E">
<style>{CSS}</style>{lds}</head><body>
<a class="skip" href="#main">{t("Skip to the story", "ข้ามไปที่เนื้อหา")}</a>
<div class="presented">{presented}</div>
<header class="mast"><div class="in"><a class="brand" href="{pre}">{brand}</a><nav aria-label="{t("Sections", "หมวด")}">{nav}</nav></div></header>
<main id="main">{body}</main>
<footer><div class="in">
{foot}
</div></footer>
<script>{lantern_js()}</script><script>try{{document.querySelectorAll('video[data-tap]').forEach(v=>v.addEventListener('click',()=>v.paused?v.play():v.pause()))}}catch(e){{}}</script>
</body></html>"""
    doc = doc.replace(" ๆ", " \u2060ๆ")  # a word joiner keeps ไม้ยมก with the word it repeats
    out = DOCS / tp / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")


ORG = {"@context": "https://schema.org", "@type": "TravelAgency", "name": "Laila Group Chiangrai Tour",
       "alternateName": "ไลลากรุ๊ป เชียงราย ทัวร์", "url": C.SHOP + "/", "telephone": C.PHONE, "email": C.MAIL,
       "address": {"@type": "PostalAddress", "streetAddress": "869/51 Thai Viwat Alley", "addressLocality": "Chiang Rai",
                   "postalCode": "57000", "addressCountry": "TH"},
       "geo": {"@type": "GeoCoordinates", "latitude": C.OFFICE[0], "longitude": C.OFFICE[1]},
       "sameAs": [C.FB, C.IG, C.VISA]}



LANTERN_JS_SRC = r"""
(function(){
 var night=new Date('%NIGHT%T19:00:00+07:00');
 // mean full moon: 2000-01-21 04:40 UTC, synodic month 29.530588853 days
 function phase(t){var d=(t-Date.UTC(2000,0,21,4,40))/864e5, s=29.530588853; return ((d/s)%1+1)%1}
 function moonPath(f,r){ // f: 0 new → .5 full; returns the lit shape
  var a=Math.cos(2*Math.PI*f)*r, sw=f<.5?1:0;
  return 'M0,'+(-r)+' A'+r+','+r+' 0 0,'+sw+' 0,'+r+' A'+Math.abs(a)+','+r+' 0 0,'+((f<.25||f>.75)?sw:1-sw)+' 0,'+(-r);
 }
 document.querySelectorAll('[data-moon]').forEach(function(el){
  var f=phase(Date.now()); el.querySelector('path').setAttribute('d',moonPath(f,46));
 });
 document.querySelectorAll('[data-count]').forEach(function(el){
  var d=Math.ceil((night-Date.now())/864e5);
  if(d<-2){el.hidden=true;return}
  el.querySelector('b').textContent=d>0?d:'%TONIGHT%';
  if(d<=0) el.querySelector('small').textContent='';
 });
 var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
 document.querySelectorAll('canvas.sky').forEach(function(cv){
  var cx=cv.getContext('2d'),W,H,dpr=Math.min(2,devicePixelRatio||1),L=[],N=+cv.dataset.n||90;
  function size(){W=cv.clientWidth;H=cv.clientHeight;cv.width=W*dpr;cv.height=H*dpr;cx.setTransform(dpr,0,0,dpr,0,0)}
  function mk(y,x){var z=Math.random();return{x:x==null?Math.random()*W:x,y:y==null?H+20+Math.random()*H:y,z:z,
   s:4+z*16,v:.15+z*.55,ph:Math.random()*6.28,w:.3+Math.random()*.7,f:Math.random()*6.28}}
  size();for(var i=0;i<N;i++)L.push(mk(Math.random()*H));
  addEventListener('resize',size);
  cv.addEventListener('pointerdown',function(e){var r=cv.getBoundingClientRect();
   for(var i=0;i<3;i++){var l=mk(e.clientY-r.top,e.clientX-r.left+(i-1)*14);l.z=.9;l.s=18;l.v=.7;L.push(l)}});
  function draw(t){
   cx.clearRect(0,0,W,H);
   L.sort(function(a,b){return a.z-b.z});
   for(var i=0;i<L.length;i++){var l=L[i];
    if(!reduce){l.y-=l.v;l.x+=Math.sin(t/1800*l.w+l.ph)*.25*l.z}
    if(l.y<-40){if(L.length>N){L.splice(i,1);i--;continue}Object.assign(l,mk())}
    var fl=.82+.18*Math.sin(t/140*l.w+l.f)*Math.sin(t/67+l.ph), s=l.s, a=(.35+.65*l.z)*Math.min(1,l.y/(H*.25));
    var g=cx.createRadialGradient(l.x,l.y,0,l.x,l.y,s*2.6);
    g.addColorStop(0,'rgba(255,196,92,'+(.55*a*fl)+')');g.addColorStop(1,'rgba(255,140,40,0)');
    cx.fillStyle=g;cx.beginPath();cx.arc(l.x,l.y,s*2.6,0,6.283);cx.fill();
    cx.fillStyle='rgba(255,'+(200+40*fl|0)+',140,'+a+')';
    cx.beginPath();cx.moveTo(l.x-s*.45,l.y-s*.7);cx.lineTo(l.x+s*.45,l.y-s*.7);
    cx.quadraticCurveTo(l.x+s*.55,l.y+s*.4,l.x+s*.3,l.y+s*.62);cx.lineTo(l.x-s*.3,l.y+s*.62);
    cx.quadraticCurveTo(l.x-s*.55,l.y+s*.4,l.x-s*.45,l.y-s*.7);cx.fill();
   }
   if(!reduce&&cv._on)requestAnimationFrame(draw);
  }
  if('IntersectionObserver' in window&&!reduce){new IntersectionObserver(function(es){
   var v=es[0].isIntersecting;if(v&&!cv._on){cv._on=true;requestAnimationFrame(draw)}else if(!v)cv._on=false}).observe(cv)}else draw(0);
 });
})();
""".replace("%NIGHT%", C.LANTERN_NIGHT)


def lantern_js():
    return LANTERN_JS_SRC.replace("%TONIGHT%", t("Tonight", "คืนนี้"))


def stay_block(pre="{PRE}"):
    b = C.STAY
    name, other = (b["th"], b["name"]) if LANG == "th" else (b["name"], b["th"])
    line = TH.STAY_LINE if LANG == "th" else b["line"]
    tl = f'<p class="th" lang="th">{e(b["th_line"])}</p>' if LANG == "en" else ""
    return (f'<section class="sight" id="stay"><figure class="card">'
            f'{shot(b["img"], other, b["book"], "", 125, pre, True)}<span class="cred">{credit(b["img"])}</span></figure>'
            f'<div><span class="kick">{bi("Where to stay", "ที่พัก")}</span><h3>{e(name)}<span class="thn" lang="{sub_lang()}">{e(other)}</span></h3>'
            f'<p>{e(line)}</p>{tl}'
            f'<p class="go"><a href="{e(b["book"])}" rel="noopener">{t("Book direct", "จองตรง")}</a>'
            f'<a href="https://www.openstreetmap.org/?mlat={b["lat"]}&amp;mlon={b["lng"]}#map=18/{b["lat"]}/{b["lng"]}" rel="noopener">{t("Map", "แผนที่")}</a>'
            f'<a href="tel:{b["phone"].replace(" ", "")}">{e(b["phone"])}</a></p></div></section>')


def hello():
    return C.wa(TH.HELLO) if LANG == "th" else C.wa("Hello Laila Group! I found you on Chiang Rai, Slowly.")


def quote(key):
    return getattr(TH, key) if LANG == "th" else getattr(C, key)

# ---------------------------------------------------------------- pages
def home():
    S = [loc(s, TH.SIGHTS, "id") for s in C.SIGHTS[:8]]
    Q = [loc(s, TH.SIDE) for s in C.SIDE[:6]]
    sights = "".join(
        f'<figure class="card">{shot(s["img"], s["name"], s.get("href") or "see/#" + s["id"], s["th"])}'
        f'<figcaption>{e(s["kicker"])}</figcaption></figure>' for s in S)
    side = "".join(
        f'<figure class="card">{shot(s["img"], s["name"], "sidequests/#" + s["id"], s["th"], 100)}</figure>'
        for s in Q)
    en = LANG == "en"
    body = f"""
<div class="col open"><div class="rubric">{bi("A Journey", "แอ่ว")}</div>
<h1>{t("Chiang Rai, Slowly", TITLE_TH)}</h1>
<p class="dek">{t("Three temples in three colours, a golden clock, the bend in the Mekong where three countries meet, and a slow boat to Laos.",
                  "วัดสามวัดสามสี หอนาฬิกาสีทอง โค้งแม่น้ำโขงที่สามประเทศมาพบกัน และเรือช้าไปลาว")}</p>
{f'<p class="dek-th th" lang="th">{TITLE_TH} — วัดขาว วัดฟ้า บ้านดำ หอนาฬิกาทอง สามเหลี่ยมทองคำ แล้วก็ล่องเรือช้าไปลาวเจ้า</p>' if en else ""}
<p class="by">{t('By <a href="https://hongdam.net/" rel="noopener">NaN</a> · Photographs from her camera roll',
                 'โดย <a href="https://hongdam.net/" rel="noopener">NaN</a> · ภาพถ่ายจากมือถือของเธอ')}</p></div>
{band("c:golden-triangle-3", t("Sop Ruak", "สบรวก"), t("The most beautiful afternoon in the north", "ยามบ่ายที่งามที่สุดของภาคเหนือ"), th="สามเหลี่ยมทองคำ ยามแลง งามขนาดเจ้า", href="golden-triangle/", cta=t("The Golden Triangle", "สามเหลี่ยมทองคำ"), cls="tall")}
<div class="col">
{note("day")}
{t(f'<p class="lede">Chiang Rai is the northernmost city in Thailand and among its gentlest: a {e("sleepy little town full of lovely people")}, as NaN puts it, with a golden clock tower at the centre and the hills rising on every side. It is small enough to cross by scooter in ten minutes and generous enough to fill a week.</p>',
   f'<p class="lede">เชียงรายเป็นเมืองเหนือสุดของประเทศไทย และเป็นเมืองที่อ่อนโยนที่สุดเมืองหนึ่ง “{TH.QUOTE_TOWN}” อย่างที่ NaN ว่าไว้ มีหอนาฬิกาสีทองอยู่ใจกลางเมือง และภูเขาล้อมรอบทุกด้าน เมืองเล็กพอจะขี่สกู๊ตเตอร์ข้ามได้ในสิบนาที แต่มีเรื่องให้แอ่วได้เต็มหนึ่งสัปดาห์</p>')}
<p>{t("Within half an hour of the clock tower stand three of the most extraordinary buildings in Asia, each the life's work of a Chiang Rai artist: a temple in white, a temple in blue, and a house in black. An hour north, the Kok and the Ruak and the Mekong carry you to the Golden Triangle, where Thailand, Laos and Myanmar meet on one bend of the river. That was the highlight of our visit, and we went back several times.",
      "ห่างจากหอนาฬิกาไม่เกินครึ่งชั่วโมง มีสิ่งก่อสร้างที่น่าทึ่งที่สุดในเอเชียถึงสามแห่ง แต่ละแห่งคืองานทั้งชีวิตของศิลปินเชียงราย วัดสีขาว วัดสีน้ำเงิน และบ้านสีดำ ขึ้นเหนือไปอีกหนึ่งชั่วโมง แม่น้ำกก แม่น้ำรวก และแม่น้ำโขงจะพาคุณไปถึงสามเหลี่ยมทองคำ ที่ไทย ลาว และเมียนมามาพบกันบนโค้งน้ำเดียว ที่นั่นคือไฮไลต์ของทริปเรา และเรากลับไปอีกหลายครั้ง")}</p>
{'<p class="th" lang="th">เชียงรายเป็นเมืองเล็ก ๆ ผู้คนใจดี แอ่วได้สบาย ๆ ทั้งวัน ม่วนใจ๋แต๊เจ้า</p>' if en else ""}
</div>
<div class="wide"><h2 class="sec"><small>{bi("The sights", "ที่เที่ยว")}</small>{t("Headliners", "ไฮไลต์ของเชียงราย")}</h2>
<div class="shots">{sights}</div><p><a href="see/">{t("All the sights", "ที่เที่ยวทั้งหมด")} →</a></p></div>
<div class="col">{note("boat", "")}
<blockquote class="pull"><p>“{e(quote("QUOTE_GT"))}”</p><cite>{t("NaN, on the Golden Triangle", "NaN พูดถึงสามเหลี่ยมทองคำ")}</cite></blockquote>
<figure class="polaroid"><img src="{A}img/own/nan-golden-triangle-t.jpg" alt="{t("NaN smiling at the Golden Triangle viewpoint", "NaN ยิ้มที่จุดชมวิวสามเหลี่ยมทองคำ")}" loading="lazy" width="405" height="720"><figcaption>{t("NaN, at the Golden Triangle", "NaN ที่สามเหลี่ยมทองคำ")}</figcaption></figure>
</div>
{band("c:luang-prabang-1", t("Laila Group · the slow boat", "ไลลากรุ๊ป · เรือช้า"), t("Two days down the Mekong to Luang Prabang", "ล่องแม่น้ำโขงสองวันไปหลวงพระบาง"), line=t("Picked up at your door before dawn, across the border by eight, on the river by ten. From ฿1,690.", "รับถึงหน้าที่พักก่อนรุ่งสาง ข้ามด่านราวแปดโมง ลงเรือสิบโมง เริ่มต้น ฿1,690"), th="ล่องเรือช้าไปหลวงพระบาง สองวันหนึ่งคืนเจ้า", href="slow-boat/", cta=t("The slow boat", "เรือช้า"), cls="right")}
{skyband("c:lantern-dark", t("Yi Peng · 24 November 2026", "ยี่เป็ง · 24 พฤศจิกายน 2569"), "Lantern Night", "ยี่เป็ง เชียงราย", count=True, href="lanterns/", cta=t("Lantern Night", "คืนโคมลอย"))}
<div class="wide"><h2 class="sec"><small>{bi("Sidequests", "แอ่วนอกเส้นทาง")}</small>{t("The small wonders", "สิ่งเล็ก ๆ ที่น่าทึ่ง")}</h2>
<div class="shots">{side}</div><p><a href="sidequests/">{t("Every sidequest", "แอ่วนอกเส้นทางทั้งหมด")} →</a></p></div>
<div class="col">{note("desk")}
<h2 class="sec"><small>{bi("Laila Group", "ไลลากรุ๊ป")}</small>{t("Everything, from one alley", "ครบทุกอย่าง จากซอยเดียว")}</h2>
<p>{t("Laila Group keeps its office on Thai Viwat Alley, a few minutes' walk from the clock tower. From there it runs the slow boats and trains to Laos, day trips to every mountain on this page, cars with drivers and scooters by the day, a visa office, and a designer consignment shop next door.",
      "ไลลากรุ๊ปมีสำนักงานอยู่ในซอยไทยวิวัฒน์ เดินจากหอนาฬิกาไม่กี่นาที จากที่นั่นดูแลทั้งเรือช้าและรถไฟไปลาว ทริปหนึ่งวันไปทุกดอยในหน้านี้ รถพร้อมคนขับและสกู๊ตเตอร์รายวัน สำนักงานวีซ่า และร้านแบรนด์เนมฝากขายที่อยู่ติดกัน")}</p>
{'<p class="th" lang="th">ไลลากรุ๊ป อยู่ซอยไทยวิวัฒน์ กลางเมืองเชียงราย มีทั้งทัวร์ เรือช้าไปลาว รถเช่า มอเตอร์ไซค์ งานวีซ่า แล้วก็ร้านแบรนด์เนมฝากขาย ทักมาได้เน้อเจ้า</p>' if en else ""}
<div class="ctas"><a class="btn" href="with-laila/">{t("Laila Group", "ไลลากรุ๊ป")}</a><a class="btn ghost" href="{e(hello())}" rel="noopener">WhatsApp</a></div>
{note("shop")}
<h2 class="sec"><small>{bi("Stay", "ที่พัก")}</small>{t("Where NaN stays", "ที่ที่ NaN พัก")}</h2>
{stay_block("")}
</div>
{band("c:clock-tower-2", t("Ho Nalika · evenings", "หอนาฬิกา · ยามค่ำ"), t("Red, green, gold, and then the night bazaar", "แดง เขียว ทอง แล้วก็ไปไนท์บาซาร์"), th="หอนาฬิกาเปลี่ยนสีทุกค่ำเจ้า", href="see/#clock-tower", cta=t("The clock tower", "หอนาฬิกา"), cls="short")}
"""
    page("", t(TITLE, TITLE_TH), t("A journey through Chiang Rai and the Golden Triangle — temples, the Mekong, sidequests and the slow boat to Laos, with Laila Group.",
                                  "แอ่วเชียงรายและสามเหลี่ยมทองคำ วัด แม่น้ำโขง ที่เที่ยวนอกเส้นทาง และเรือช้าไปลาว กับไลลากรุ๊ป"),
         body, ld=[ORG, {"@context": "https://schema.org", "@type": "WebSite", "name": TITLE, "url": SITE_URL + "/"}])


def slug(s):
    import re
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def go_line(s, pre):
    parts = []
    if s.get("osm"):
        parts.append(f'<a href="{osm(s["osm"])}" rel="noopener">{t("Map", "แผนที่")}</a>')
    if s.get("laila"):
        parts.append(f'<a href="{trip(s["laila"])}" rel="noopener">{t("Go with Laila Group", "ไปกับไลลากรุ๊ป")}</a>')
    if s.get("href"):
        parts.append(f'<a href="{pre}{s["href"]}">{t("More", "อ่านต่อ")}</a>')
    return f'<p class="go">{"".join(parts)}</p>' if parts else ""


def sight_block(s, pre):
    ratio = 125
    vid = ""
    if s.get("video"):
        vid = (f'<video src="{A}{s["video"]}" poster="{img(s["img"], True)}" preload="none" muted loop playsinline '
               f'data-tap controls width="270" height="480"></video><span class="cred">{t("Video", "วิดีโอ")}: NaN · CC BY 4.0</span>')
    kick = f'<span class="kick">{e(s["kicker"])}</span>' if s.get("kicker") else ""
    tht = f'<p class="th" lang="th">{e(s["th_text"])}</p>' if s.get("th_text") else ""
    href = osm(s["osm"]) if s.get("osm") else "#" + s["id"]
    return (f'<section class="sight" id="{s["id"]}"><figure class="card">'
            f'{shot(s["img"], s["th"], href, "", ratio, pre, True)}'
            f'<span class="cred">{credit(s["img"])}</span>{vid}</figure>'
            f'<div>{kick}<h3>{e(s["name"])}<span class="thn" lang="{sub_lang()}">{e(s["th"])}</span></h3>'
            f'<p>{e(s["text"])}</p>{tht}{go_line(s, pre)}</div></section>')


def see():
    blocks = []
    for i, s in enumerate(C.SIGHTS):
        blocks.append(sight_block(loc(s, TH.SIGHTS, "id"), "../"))
        if i == 2:
            blocks.append(note("day", "../"))
        if i == 6:
            blocks.append(note("car", "../"))
        if i == 9:
            blocks.append(note("wa", "../"))
    body = f"""
<div class="col open"><div class="rubric">{bi("The sights", "ที่เที่ยว")}</div>
<h1>{t("The Headliners", "ที่เที่ยวหลัก")}</h1><p class="dek">{t("White, blue, black and gold, and the mountains beyond.", "ขาว น้ำเงิน ดำ และทอง แล้วก็ภูเขาไกลออกไป")}</p></div>
{band("c:white-temple-2", t("Wat Rong Khun", "วัดร่องขุ่น"), t("A temple built of light", "วัดที่สร้างจากแสง"), th="วัดร่องขุ่น งามจับใจ๋เจ้า", cls="short")}
<div class="col">{"".join(blocks)}</div>
{band("c:phu-chi-fa-3", t("Phu Chi Fa", "ภูชี้ฟ้า"), t("First light over the mist", "แสงแรกเหนือทะเลหมอก"), th="ทะเลหมอกภูชี้ฟ้า", href=trip("phu-chi-fa-chiang-rai-mountains"), cta=t("Go before dawn", "ไปก่อนรุ่งสาง"), cls="right")}
"""
    page("see/", t("The Headliners", "ที่เที่ยวหลัก"), t("The White Temple, the Blue Temple, the Black House, the golden clock tower and the mountains of Chiang Rai.",
                                                      "วัดร่องขุ่น วัดร่องเสือเต้น บ้านดำ หอนาฬิกาสีทอง และภูเขาของเชียงราย"), body)


def golden():
    blocks = []
    for i, s in enumerate(C.GT):
        blocks.append(sight_block(loc(s, TH.GT), "../"))
        if i == 1:
            blocks.append(note("day", "../"))
        if i == 3:
            blocks.append(note("car", "../"))
    en = LANG == "en"
    shots = [("own:skywalk-blossom", "Blossom over the glass", "ดอกไม้เหนือพื้นกระจก"), ("own:skywalk-arch", "Toward the river", "มุ่งสู่แม่น้ำ"),
             ("own:across-mekong", "Across the Mekong", "ข้ามแม่น้ำโขง"), ("own:opium-mural-2", "The farming year", "ปีแห่งการเพาะปลูก")]
    body = f"""
<div class="col open"><div class="rubric">{bi("The highlight", "สามเหลี่ยมทองคำ", "ไฮไลต์")}</div>
<h1>{t("The Golden Triangle", "สามเหลี่ยมทองคำ")}</h1>
<p class="dek">{t("Three countries, two rivers, one long golden afternoon.", "สามประเทศ สองสายน้ำ หนึ่งบ่ายยาวสีทอง")}</p>
{'<p class="dek-th th" lang="th">น้ำรวกบรรจบน้ำโขง ไทย ลาว เมียนมา มาพบกันตรงนี้เจ้า</p>' if en else ""}</div>
{band("c:golden-triangle-2", t("Sop Ruak", "สบรวก"), t("Where the Ruak meets the Mekong", "ที่แม่น้ำรวกบรรจบแม่น้ำโขง"), th="ยามแลงแดดสีทองส่องน้ำโขง งามขนาดเน้อ", cls="tall")}
<div class="col">
<blockquote class="pull"><p>“{e(quote("QUOTE_GT"))}”</p><cite>NaN</cite></blockquote>
<p class="lede">{t("An hour and a little north of Chiang Rai, past Mae Chan and the turn for Chiang Saen, the road comes down to the water and stops. Across the Mekong is Laos. Up the smaller river, the Ruak, is Myanmar. The bend between them is the Golden Triangle, and in the late afternoon the name explains itself: the light goes gold, the river goes gold, and so does the great seated Buddha on the bank.",
                   "ขึ้นเหนือจากเชียงรายไปชั่วโมงกว่า ผ่านแม่จันและทางแยกไปเชียงแสน ถนนจะลงไปถึงริมน้ำแล้วก็สุดทาง ฝั่งโน้นของแม่น้ำโขงคือลาว ขึ้นไปตามแม่น้ำสายเล็กกว่า คือแม่น้ำรวก คือเมียนมา โค้งน้ำระหว่างนั้นคือสามเหลี่ยมทองคำ และยามบ่ายแก่ ชื่อนี้ก็อธิบายตัวเอง แสงกลายเป็นสีทอง แม่น้ำกลายเป็นสีทอง พระพุทธรูปองค์ใหญ่ริมฝั่งก็เป็นสีทองเช่นกัน")}</p>
<p>{t("Plan on the whole afternoon. Start at the Hall of Opium, walk the river road to the viewpoint, take a longtail out onto the Mekong, and finish on the glass walkway south of Chiang Saen with the sun going down behind the hills.",
      "เผื่อเวลาไว้ทั้งบ่าย เริ่มที่หอฝิ่น เดินตามถนนริมน้ำไปจุดชมวิว นั่งเรือหางยาวออกไปกลางแม่น้ำโขง แล้วปิดท้ายบนทางเดินกระจกทางใต้ของเชียงแสน ตอนตะวันลับหลังภูเขา")}</p>
<figure class="polaroid"><img src="{A}img/own/nan-golden-triangle-t.jpg" alt="{t("NaN at the Golden Triangle", "NaN ที่สามเหลี่ยมทองคำ")}" loading="lazy" width="405" height="720"><figcaption>{t("Late afternoon, the first of several visits", "ยามบ่ายแก่ ครั้งแรกจากหลายครั้ง")}</figcaption></figure>
{"".join(blocks)}
<blockquote class="pull"><p>“{e(quote("QUOTE_OPIUM"))}”</p><cite>NaN</cite></blockquote>
<h2 class="sec"><small>{bi("Getting there", "ไปจะไดเจ้า", "การเดินทาง")}</small>{t("Three ways north", "สามทางขึ้นเหนือ")}</h2>
<table class="list">
<tr><td><b><a href="{trip("one-day-sightseeing-tour-in-chiang-rai")}" rel="noopener">{t("Laila Group's one-day tour", "ทริปหนึ่งวันของไลลากรุ๊ป")}</a></b><small>{t("Golden Triangle and the Hall of Opium, with the White Temple, Blue Temple and Black House on the same day. Guide and lunch included.", "สามเหลี่ยมทองคำและหอฝิ่น พร้อมวัดร่องขุ่น วัดร่องเสือเต้น และบ้านดำในวันเดียวกัน รวมไกด์และอาหารกลางวัน")}</small></td><td class="p">฿1,200</td></tr>
<tr><td><b><a href="../with-laila/#wheels">{t("A car with a driver", "รถพร้อมคนขับ")}</a></b><small>{t("Go at your own pace, stay for the sunset, come back several times.", "ไปตามจังหวะของคุณเอง อยู่ดูตะวันตกดิน แล้วกลับไปอีกหลายครั้ง")}</small></td><td class="p">{t("from ฿1,200 a day", "เริ่มต้นวันละ ฿1,200")}</td></tr>
<tr><td><b><a href="../with-laila/#wheels">{t("A scooter", "สกู๊ตเตอร์")}</a></b><small>{t("About seventy kilometres each way on the main road.", "ถนนสายหลักราวเจ็ดสิบกิโลเมตรต่อเที่ยว")}</small></td><td class="p">{t("from ฿250 a day", "เริ่มต้นวันละ ฿250")}</td></tr>
</table><p class="asof">{t(f"Prices as listed by Laila Group, {C.READ}.", f"ราคาตามที่ไลลากรุ๊ปลงไว้ {TH.READ}")}</p>
<h2 class="sec"><small>{bi("Stay", "ที่พัก")}</small>{t("A bed for the night", "ที่นอนสำหรับคืนนี้")}</h2>
<p>{t("The triangle has grand riverside resorts. NaN goes back to town.", "ที่สามเหลี่ยมมีรีสอร์ตหรูริมน้ำ แต่ NaN กลับไปนอนในเมือง")}</p>
{stay_block("../")}
</div>
<div class="wide"><div class="shots three">
{"".join(f'<figure class="card">{shot(r, t(c, ct), "../roll/", "", 150, "../")}</figure>' for r, c, ct in shots)}
</div></div>
{band("c:mekong-2", t("Chiang Saen", "เชียงแสน"), t("Keep going: the river runs all the way to Luang Prabang", "ไปต่อเถอะ แม่น้ำไหลไปถึงหลวงพระบาง"), href="slow-boat/", cta=t("The slow boat", "เรือช้า"), cls="right")}
"""
    page("golden-triangle/", t("The Golden Triangle", "สามเหลี่ยมทองคำ"), t("Sop Ruak, the golden Buddha, the Hall of Opium, the glass walkway and Chiang Saen — the highlight of Chiang Rai.",
                                                                        "สบรวก พระพุทธรูปทองคำ หอฝิ่น ทางเดินกระจก และเชียงแสน ไฮไลต์ของเชียงราย"), body,
         ld=[{"@context": "https://schema.org", "@type": "TouristAttraction", "name": "Golden Triangle (Sop Ruak)",
              "geo": {"@type": "GeoCoordinates", "latitude": 20.3526, "longitude": 100.0818}},
             {"@context": "https://schema.org", "@type": "ImageObject", "contentUrl": CANON + "/img/own/across-mekong.jpg",
              "name": "Across the Mekong from Sop Ruak", "creator": {"@type": "Person", "name": "NaN"},
              "license": "https://creativecommons.org/licenses/by/4.0/", "description": OWN["across-mekong"]["alt"]}])


def sidequests():
    blocks = []
    for i, s in enumerate(C.SIDE):
        blocks.append(sight_block(loc(s, TH.SIDE), "../"))
        if i in (2, 7):
            blocks.append(note(["shop", "visa"][i == 7], "../"))
    body = f"""
<div class="col open"><div class="rubric">{bi("Sidequests", "แอ่วนอกเส้นทาง")}</div>
<h1>{t("The Small Wonders", "สิ่งเล็ก ๆ ที่น่าทึ่ง")}</h1><p class="dek">{t("Vanilla, painted pillars, a warm waterfall, eggs boiled in a spring, and khao soi twice a day.", "วานิลลา เสาภาพวาด น้ำตกน้ำอุ่น ไข่ต้มในบ่อน้ำร้อน และข้าวซอยวันละสองรอบ")}</p></div>
<div class="col">{"".join(blocks)}</div>
{band("c:kok-river-2", t("Mae Nam Kok", "แม่น้ำกก"), t("The river through town", "แม่น้ำกลางเมือง"), th="แม่น้ำกก ไหลผ่านกลางเมืองเจ้า", cls="short")}
"""
    page("sidequests/", t("Sidequests", "แอ่วนอกเส้นทาง"), t("Chiang Rai's small wonders — vanilla farm, bus-station murals, hot-spring eggs, a warm waterfall, khao soi.",
                                                            "สิ่งเล็ก ๆ ที่น่าทึ่งของเชียงราย ฟาร์มวานิลลา ภาพวาดที่สถานีขนส่ง ไข่ต้มน้ำพุร้อน น้ำตกน้ำอุ่น ข้าวซอย"), body)


def slowboat():
    en = LANG == "en"
    B = [loc(dict(b, text=b["text"]), TH.BOATS, "slug") for b in C.BOATS]
    rows = "".join(
        f'<tr><td><b><a href="{trip(b["slug"])}" rel="noopener">{e(b["name"])}</a></b> <span class="th" lang="{sub_lang()}">{e(b["th"])}</span>'
        f'<small>{e(b["days"])} · {e(b["text"])}</small></td><td class="p">{thb(b["price"])}</td></tr>' for b in B)
    trains = "".join(f'<tr><td><a href="{trip(s)}" rel="noopener">{e(t(n, TH.TRAINS[s]))}</a></td><td class="p">{thb(p)}</td></tr>' for n, s, p in C.TRAINS)
    shots = [("c:chiang-khong-1", "Chiang Khong", "เชียงของ"), ("c:slow-boat-1", "Pak Beng", "ปากแบ่ง"), ("c:luang-prabang-3", "Luang Prabang", "หลวงพระบาง")]
    body = f"""
<div class="col open"><div class="rubric">{bi("Laila Group", "เรือช้า")}</div>
<h1>{t("The Slow Boat", "เรือช้า")}</h1><p class="dek">{t("Two days down the Mekong from Chiang Rai to Luang Prabang, with a night in Pak Beng between.", "ล่องแม่น้ำโขงสองวันจากเชียงรายไปหลวงพระบาง แวะนอนปากแบ่งหนึ่งคืน")}</p>
{'<p class="dek-th th" lang="th">ล่องเรือช้าน้ำโขงไปหลวงพระบาง นอนปากแบ่งหนึ่งคืน ไลลากรุ๊ปมารับถึงที่พักตั้งแต่เช้ามืด พาข้ามด่าน ส่งถึงท่าเรือเจ้า</p>' if en else ""}</div>
{band("c:luang-prabang-2", t("The Mekong", "แม่น้ำโขง"), t("The long way is the lovely way", "ทางไกลคือทางที่งดงาม"), th="ทางไกลที่งามที่สุดเจ้า", cls="tall")}
<div class="col">
{note("wa", "../")}
<p class="lede">{t("It begins in the dark. Laila Group's van collects you from your hotel at five, and by the time the sun is up you are at the river at Chiang Khong with your passport stamped. Across the bridge is Huay Xai; below it the long wooden boats wait at the pier. At ten you cast off.",
                   "ทุกอย่างเริ่มตอนฟ้ายังมืด รถตู้ของไลลากรุ๊ปมารับที่โรงแรมตอนตีห้า พอตะวันขึ้น คุณก็อยู่ริมแม่น้ำที่เชียงของ พาสปอร์ตประทับตราเรียบร้อย ข้ามสะพานไปคือห้วยทราย ใต้สะพาน เรือไม้ลำยาวจอดรออยู่ที่ท่า สิบโมงเรือออก")}</p>
<p>{t("For two days the Mekong carries you between green hills, past sand bars and fishing boats and villages that come down to the water. The first night is at Pak Beng, a river town that exists to welcome the boats. On the second afternoon, Luang Prabang.",
      "สองวันเต็ม แม่น้ำโขงพาคุณผ่านขุนเขาเขียวขจี ผ่านสันทราย เรือหาปลา และหมู่บ้านที่ลงมาถึงริมน้ำ คืนแรกพักที่ปากแบ่ง เมืองริมน้ำที่อยู่เพื่อต้อนรับเรือ บ่ายวันที่สอง ถึงหลวงพระบาง")}</p>
<h2 class="sec"><small>{bi("The boats", "เรือ")}</small>{t("Choose your river", "เลือกเส้นทางของคุณ")}</h2>
<table class="list">{rows}</table>
<p class="asof">{t(f"Prices as listed by Laila Group, {C.READ}. Pack US dollars for the Lao visa on arrival (USD 40 on her listing) and your passport photo.",
                  f"ราคาตามที่ไลลากรุ๊ปลงไว้ {TH.READ} ผู้ถือหนังสือเดินทางต่างชาติ เตรียมเงินดอลลาร์สหรัฐสำหรับวีซ่าลาวแบบ visa on arrival (USD 40 ตามที่ลงไว้) และรูปถ่ายติดพาสปอร์ต")}</p>
<div class="ctas"><a class="btn" href="{trip("slow-boat-chiang-rai-to-luang-prabang")}" rel="noopener">{t("Book the slow boat", "จองเรือช้า")}</a><a class="btn ghost" href="{e(C.wa(t("Hello Laila Group! I would like the slow boat to Luang Prabang.", "สวัสดีเจ้า ไลลากรุ๊ป อยากจองเรือช้าไปหลวงพระบางเจ้า")))}" rel="noopener">{t("Ask on WhatsApp", "ถามทาง WhatsApp")}</a></div>
</div>
<div class="wide"><div class="shots three">
{"".join(shot(r, t(n, th), "../with-laila/", t(th, n), 66, "../") for r, n, th in shots)}
</div></div>
<div class="col">
<h2 class="sec"><small>{bi("Or by rail", "รถไฟลาว-จีน")}</small>{t("The train through Laos", "รถไฟผ่านลาว")}</h2>
<p>{t("Laila Group also runs the fast way: across the border and onto the Laos–China Railway, Luang Prabang the same day, Vang Vieng and Vientiane beyond.",
      "ไลลากรุ๊ปมีทางเร็วด้วย ข้ามด่านแล้วขึ้นรถไฟลาว–จีน ถึงหลวงพระบางในวันเดียว และไปต่อวังเวียงกับเวียงจันทน์")}</p>
<table class="list">{trains}</table>
{note("desk", "../")}
</div>
"""
    page("slow-boat/", t("The Slow Boat", "เรือช้า"), t("Laila Group's slow boat from Chiang Rai to Luang Prabang, from ฿1,690 — plus the train and bus to Laos.",
                                                     "เรือช้าของไลลากรุ๊ปจากเชียงรายไปหลวงพระบาง เริ่มต้น ฿1,690 พร้อมรถไฟและรถบัสไปลาว"), body,
         ld=[ORG, {"@context": "https://schema.org", "@type": "TouristTrip", "name": "Slow boat Chiang Rai to Luang Prabang",
                   "provider": {"@type": "TravelAgency", "name": "Laila Group Chiangrai Tour"},
                   "offers": {"@type": "Offer", "price": "1690", "priceCurrency": "THB",
                              "url": trip("slow-boat-chiang-rai-to-luang-prabang")}}])


def laila():
    en = LANG == "en"

    def day(n, s, p, x):
        return (n, p, x) if en else TH.DAYS[s]
    days = "".join(f'<tr><td><b><a href="{trip(s)}" rel="noopener">{e(dn)}</a></b><small>{e(dx)}</small></td><td class="p">{e(dp)}</td></tr>'
                   for n, s, p, x in C.DAYS for dn, dp, dx in [day(n, s, p, x)])
    wheels = "".join(f'<tr><td><a href="{trip(s)}" rel="noopener">{e(t(n, TH.WHEELS.get(s, n)))}</a></td><td class="p">{thb(p)} {t("a day", "ต่อวัน")}</td></tr>' for n, s, p in C.WHEELS)
    visas = "".join(f'<tr><td><b>{e(vn)}</b><small>{e(vx)}</small></td></tr>'
                    for n, x in C.VISAS for vn, vx in [(n, x) if en else TH.VISAS[n]])
    boats = "".join(f'<tr><td><a href="{trip(b["slug"])}" rel="noopener">{e(t(b["name"], b["th"]))}</a></td><td class="p">{thb(b["price"])}</td></tr>' for b in C.BOATS)
    osm_map = f"https://www.openstreetmap.org/?mlat={C.OFFICE[0]}&amp;mlon={C.OFFICE[1]}#map=18/{C.OFFICE[0]}/{C.OFFICE[1]}"
    osm_dir = f"https://www.openstreetmap.org/directions?to={C.OFFICE[0]}%2C{C.OFFICE[1]}"
    where = (f'<p><b>Where:</b> {e(C.ADDRESS)}, at Sofia Hostel. <span lang="th" class="th">{e(C.ADDRESS_TH)}</span> · <a href="{osm_map}" rel="noopener">Map</a> ·\n'
             f'<a href="{osm_dir}" rel="noopener">Directions</a></p>\n'
             f'<p>Also on <a href="{C.FB}" rel="noopener">Facebook</a> and <a href="{C.IG}" rel="noopener">Instagram</a>.</p>') if en else (
             f'<p><b>ที่อยู่:</b> {e(C.ADDRESS_TH)} ที่โซเฟียโฮสเทล <span lang="en">{e(C.ADDRESS)}</span> · <a href="{osm_map}" rel="noopener">แผนที่</a> ·\n'
             f'<a href="{osm_dir}" rel="noopener">เส้นทาง</a></p>\n'
             f'<p>ติดตามได้ทาง <a href="{C.FB}" rel="noopener">Facebook</a> และ <a href="{C.IG}" rel="noopener">Instagram</a></p>')
    body = f"""
<div class="col open"><div class="rubric">{bi("Presented with", "ไลลากรุ๊ป", "ร่วมนำเสนอโดย")}</div>
<h1>{t("Laila Group", "ไลลากรุ๊ป")}</h1><p class="dek">{t("Tours, boats, trains, cars, visas and a designer consignment shop, from one alley in the middle of Chiang Rai.", "ทัวร์ เรือ รถไฟ รถ วีซ่า และร้านแบรนด์เนมฝากขาย จากซอยเดียวกลางเมืองเชียงราย")}</p>
{'<p class="dek-th th" lang="th">ไลลากรุ๊ป ซอยไทยวิวัฒน์ เชียงราย — ทัวร์ เรือช้า รถไฟไปลาว รถเช่า วีซ่า แล้วก็ร้านแบรนด์เนมฝากขายเจ้า</p>' if en else ""}</div>
<div class="col">
<div class="ctas"><a class="btn" href="{e(hello())}" rel="noopener">WhatsApp {e(C.PHONE)}</a>
<a class="btn ghost" href="{C.SHOP}/" rel="noopener">slowboatthailandlaos.com</a><a class="btn ghost" href="mailto:{C.MAIL}">{t("Email", "อีเมล")}</a></div>
{where}
<h2 class="sec" id="boats"><small>{bi("To Laos", "ไปลาว")}</small>{t("Slow boats", "เรือช้า")}</h2>
<table class="list">{boats}</table><p><a href="../slow-boat/">{t("The slow boat, day by day", "เรือช้า วันต่อวัน")} →</a></p>
<h2 class="sec" id="days"><small>{bi("Day trips", "เที่ยวรายวัน")}</small>{t("Every mountain", "ทุกดอย")}</h2>
<table class="list">{days}</table>
{note("desk", "../")}
<h2 class="sec" id="wheels"><small>{bi("By the day", "รถเช่า")}</small>{t("Wheels", "รถเช่ารายวัน")}</h2>
<table class="list">{wheels}</table>
<p class="asof">{t(f"Prices as listed by Laila Group, {C.READ}. Cars come with a driver.", f"ราคาตามที่ไลลากรุ๊ปลงไว้ {TH.READ} รถยนต์มาพร้อมคนขับ")}</p>
<h2 class="sec" id="visas"><small>{bi("Visa Services Thailand", "วีซ่า")}</small>{t("The visa office", "สำนักงานวีซ่า")}</h2>
<p>{t("For a longer stay, Laila Group's visa office handles the paperwork from consultation to approval, and the bank account and tax number after.",
      "สำหรับการพำนักระยะยาว สำนักงานวีซ่าของไลลากรุ๊ปดูแลเอกสารตั้งแต่ให้คำปรึกษาจนได้รับอนุมัติ รวมถึงบัญชีธนาคารและเลขประจำตัวผู้เสียภาษีหลังจากนั้น")}</p>
<table class="list">{visas}</table>
<div class="ctas"><a class="btn ghost" href="{C.VISA}" rel="noopener">visaservicesthailand.com</a></div>
<aside class="note"><span class="nk">{t('In Chiang Mai <span lang="th" class="th">· เชียงใหม่</span>', 'เชียงใหม่ · <span lang="en">In Chiang Mai</span>')}</span><p>{t("Chiang Mai Visa Desk, for Thai visas in Chiang Mai, and for Thai families bound for America.", "Chiang Mai Visa Desk รับทำวีซ่าไทยในเชียงใหม่ และดูแลครอบครัวคนไทยที่จะไปอเมริกา")}</p><a href="{C.DESK}" rel="noopener">chiangmaivisadesk.com →</a></aside>
<h2 class="sec" id="shop"><small>{bi("Laila's Designer Consignment", "ร้านแบรนด์เนมฝากขาย")}</small>{t("The shop", "ร้าน")}</h2>
<p>{t("Designer pieces, consigned, next door to the visa office on Thai Viwat Alley. Come in and see what has arrived; or bring something beautiful of your own to leave with Laila.",
      "ของแบรนด์เนมฝากขาย อยู่ติดกับสำนักงานวีซ่าในซอยไทยวิวัฒน์ แวะมาดูว่ามีอะไรมาใหม่ หรือนำของสวย ๆ ของคุณมาฝากขายกับไลลา")}</p>
{'<p class="th" lang="th">ของแบรนด์เนมสภาพงาม ฝากขายได้ ซื้อได้ อยู่ติดกับสำนักงานวีซ่าเจ้า แวะมาแอ่วเน้อ</p>' if en else ""}
</div>
{band("c:mekong-3", t("Laila Group", "ไลลากรุ๊ป"), t("The river is waiting", "แม่น้ำรออยู่"), th="ทักมาได้เน้อเจ้า", href=hello(), cta=t("Say hello", "ทักทาย"), cls="short")}
"""
    page("with-laila/", t("Laila Group", "ไลลากรุ๊ป"), t("Laila Group, Chiang Rai: slow boats and trains to Laos, day trips, cars and scooters, visas, and designer consignment.",
                                                       "ไลลากรุ๊ป เชียงราย เรือช้าและรถไฟไปลาว ทริปรายวัน รถยนต์และสกู๊ตเตอร์ วีซ่า และร้านแบรนด์เนมฝากขาย"), body, ld=[ORG])


def skyband(ref, kicker, head, th, pre="{PRE}", count=False, href="", cta=""):
    """head is English, th is Thai; the page's own language goes large."""
    big, small = (th, head) if LANG == "th" else (head, th)
    cnt = ""
    if count:
        cnt = ('<div class="count" data-count><svg viewBox="-50 -50 100 100" data-moon aria-hidden="true">'
               '<circle r="46" fill="#2a2433"/><path fill="#fff4d6" d=""/></svg>'
               f'<div><b>–</b><small>{t("nights to the Yi Peng moon · 24 Nov 2026", "คืน ถึงคืนเพ็ญยี่เป็ง · 24 พ.ย. 2569")}</small></div></div>')
    btn = f'<p><a class="btn" href="{"" if href.startswith("http") else pre}{e(href)}">{e(cta)}</a></p>' if href else ""
    return (f'<section class="skyband" style="background-image:url({img(ref)})"><canvas class="sky" aria-hidden="true"></canvas>'
            f'<div class="in"><span class="kicker">{e(kicker)}</span><h2>{e(big)}</h2><div class="thbig" lang="{sub_lang()}">{e(small)}</div>'
            f'{cnt}{btn}<p class="tap">{t("Tap the sky", "แตะท้องฟ้า")}</p></div><span class="cred" style="position:absolute;right:0;bottom:0;'
            f'background:rgba(0,0,0,.6);padding:.2rem .5rem">{credit(ref)}</span></section>')


def lanterns():
    en = LANG == "en"
    L = [dict(l, th=l["name"], name=l["th"], line=TH.LANTERNS[l["name"]]) if not en else l for l in C.LANTERNS]
    cards = "".join(
        f'<figure class="card"><a class="shot" href="{e(osm(l["osm"]) if l.get("osm") else "#float")}" rel="noopener">'
        f'<span class="bg" style="background-image:url({img(l["img"])})"></span><span class="scrim"></span>'
        f'<span class="sp" style="padding-top:120%"></span><span class="tx"><b>{e(l["name"])}</b><i>{e(l["th"])}</i>'
        f'<p>{e(l["line"])}</p></span></a></figure>' for l in L)
    shots = [("c:lantern-field", "Lanterns", "โคมลอย"), ("c:lantern-candles", "Candles", "ประทีป"), ("c:krathong-float", "Krathong", "กระทง")]
    body = f"""
{skyband("c:lantern-sky", t("Yi Peng · Loy Krathong", "ยี่เป็ง · ลอยกระทง"), "Lantern Night", t("ยี่เป็ง ลอยกระทง", "คืนโคมลอย"), count=True)}
<div class="col" style="text-align:center">
<p class="dek">{t("One full moon. Lanterns up, krathongs down the river, and every wish with them.", "คืนเพ็ญหนึ่งคืน โคมลอยขึ้นฟ้า กระทงลอยตามน้ำ และทุกคำอธิษฐานก็ลอยไปด้วยกัน")}</p>
{'<p class="dek-th th" lang="th">คืนเพ็ญเดือนยี่ โคมลอยขึ้นฟ้า กระทงลอยตามน้ำ ขอให้โชคดีมีสุขเจ้า</p>' if en else ""}
</div>
<div class="bigshots">{cards}</div>
<div class="col" id="float">
{note("lantern", "../")}
<h2 class="sec"><small>{bi("Three nights", "สามคืน")}</small>{t("Around the full moon", "รอบคืนเพ็ญ")}</h2>
<p>{t("Chiang Rai lights the Kok and Chiang Saen lights the Mekong over the nights around the full moon. The city posts its programme in the weeks before.",
      "เชียงรายจุดไฟริมแม่น้ำกก และเชียงแสนจุดไฟริมแม่น้ำโขง ตลอดหลายคืนรอบวันเพ็ญ เมืองจะประกาศกำหนดการล่วงหน้าไม่กี่สัปดาห์")}</p>
{'<p class="th" lang="th">งานในเมืองเข้าฟรีเจ้า กระทงใบตองราว 30–100 บาท</p>' if en else "<p>งานในเมืองเข้าฟรีเจ้า กระทงใบตองราว 30–100 บาท</p>"}
</div>
{band("c:lantern-many", t("The wish goes up", "คำอธิษฐานลอยขึ้นฟ้า"), t("A sky of lanterns", "ท้องฟ้าเต็มไปด้วยโคม"), th="โคมลอยพาความทุกข์ลอยไปเจ้า", href="with-laila/", cta=t("Plan it with Laila", "วางแผนกับไลลา"), cls="tall")}
<div class="wide"><div class="shots three">{"".join(shot(r, t(n, th), "../golden-triangle/", t(th, n), 66, "../") for r, n, th in shots)}</div></div>
"""
    page("lanterns/", t("Lantern Night", "คืนโคมลอย"), t("Yi Peng and Loy Krathong in Chiang Rai and Chiang Saen — the Kok River, four nations on the Mekong, and your own krathong. 24 November 2026.",
                                                     "ยี่เป็งและลอยกระทงที่เชียงรายและเชียงแสน แม่น้ำกก สี่ชาติบนแม่น้ำโขง และกระทงของคุณเอง 24 พฤศจิกายน 2569"), body,
         ld=[{"@context": "https://schema.org", "@type": "Event", "name": "Yi Peng & Loy Krathong, Chiang Rai", "startDate": C.LANTERN_NIGHT,
              "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
              "location": {"@type": "Place", "name": "Kok River, Chiang Rai", "address": "Chiang Rai, Thailand"}}])


def roll():
    en = LANG == "en"

    def cap(k, v):
        return (v.get("alt") or v["caption"], v["caption"]) if en else (TH.ALT.get(k) or TH.CAPTIONS[k], TH.CAPTIONS[k])
    figs = "".join(f'<figure><img src="{A}img/own/{k}-t.jpg" alt="{e(alt)}" loading="lazy" width="{v["w"]}" height="{v["h"]}">'
                   f'<figcaption>{e(c)}</figcaption></figure>' for k, v in OWN.items() for alt, c in [cap(k, v)])
    body = f"""
<div class="col open"><div class="rubric">{bi("From the camera roll", "ภาพถ่าย")}</div>
<h1>{t("NaN's Roll", "ภาพของ NaN")}</h1><p class="dek">{t("February to June, Chiang Rai and the Golden Triangle, as they came off the phone.", "กุมภาพันธ์ถึงมิถุนายน เชียงรายและสามเหลี่ยมทองคำ ตามที่ถ่ายไว้ในมือถือ")}</p></div>
<div class="wide"><div class="roll">{figs}</div>
<p class="cred">{t("Photographs by NaN, CC BY 4.0.", "ภาพถ่ายโดย NaN, CC BY 4.0")}</p></div>
<div class="col">{note("day", "../")}</div>
"""
    page("roll/", t("NaN's Roll", "ภาพของ NaN"), t("Chiang Rai and the Golden Triangle from NaN's camera roll.", "เชียงรายและสามเหลี่ยมทองคำ จากภาพในมือถือของ NaN"), body)


def credits():
    rows = "".join(f'<tr><td><a href="{e(c["page"])}" rel="noopener">{e(c["title"][5:])}</a><small>{e(c["author"])}</small></td>'
                   f'<td class="p"><a href="{e(c["licence_url"])}" rel="noopener">{e(c["licence"])}</a></td></tr>' for c in CRED.values())
    body = f"""<div class="col open"><h1>{t("Credits", "เครดิต")}</h1></div><div class="col">
<p>{t("Photographs marked NaN are hers, CC BY 4.0. These are from Wikimedia Commons, each under its own licence:",
      "ภาพที่ระบุว่า NaN เป็นภาพของเธอ ใช้สัญญาอนุญาต CC BY 4.0 ภาพเหล่านี้มาจากวิกิมีเดียคอมมอนส์ แต่ละภาพใช้สัญญาอนุญาตของตัวเอง:")}</p>
<table class="list">{rows}</table>
<p>{t(f"Tour, boat, rental and visa details are Laila Group's own, from slowboatthailandlaos.com and visaservicesthailand.com, read {C.READ}.",
      f"รายละเอียดทัวร์ เรือ รถเช่า และวีซ่า มาจากไลลากรุ๊ปเอง ที่ slowboatthailandlaos.com และ visaservicesthailand.com อ่านเมื่อ {TH.READ}")}</p></div>"""
    page("credits/", t("Credits", "เครดิต"), t("Photo credits and sources.", "เครดิตภาพและแหล่งที่มา"), body)


def machine():
    urls = ["", "lanterns/", "golden-triangle/", "see/", "sidequests/", "slow-boat/", "with-laila/", "roll/", "credits/"]
    urls += ["th/" + u for u in urls]
    (DOCS / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                      + "".join(f"<url><loc>{SITE_URL}/{u}</loc></url>" for u in urls) + "</urlset>\n")
    (DOCS / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    (DOCS / "llms.txt").write_text(
        f"# {TITLE}\n\n> Chiang Rai and the Golden Triangle — the headline sights, the sidequests, and the slow boat to "
        f"Luang Prabang — presented with Laila Group, Thai Viwat Alley, Chiang Rai.\n\n"
        + "".join(f"- [{t}]({SITE_URL}/{u})\n" for u, t in NAV) +
        f"\nThai edition · ฉบับภาษาไทย: {SITE_URL}/th/\n" +
        f"\nOn the picture across the Mekong ({CANON}/img/own/across-mekong.jpg): {OWN['across-mekong']['alt']}\n"
        f"\nLaila Group: {C.SHOP}/ · WhatsApp {C.PHONE} · {C.MAIL}\nVisa Services Thailand: {C.VISA}\n")
    (DOCS / ".nojekyll").write_text("")
    fleet.decorate(DOCS, "chiang-rai")


def main():
    global LANG
    TH.check(OWN)
    for p in ["lanterns", "golden-triangle", "see", "sidequests", "slow-boat", "with-laila", "roll", "credits", "th"]:
        shutil.rmtree(DOCS / p, ignore_errors=True)
    for LANG in ("en", "th"):
        home(); lanterns(); see(); golden(); sidequests(); slowboat(); laila(); roll(); credits()
    LANG = "en"
    machine()
    print("built", sum(1 for _ in DOCS.rglob("index.html")), "pages →", DOCS)


if __name__ == "__main__":
    main()
