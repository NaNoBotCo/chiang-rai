# -*- coding: utf-8 -*-
"""build.py — writes docs/ from content.py, data/own/own.json and data/commons/credits.json.

    python3 tools/build.py            # SITE_URL defaults to the GitHub Pages address
"""
import html, json, os, shutil, sys, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import content as C  # noqa: E402
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


def img(ref: str, thumb=False) -> str:
    kind, slug = ref.split(":", 1)
    base = "img/own/" if kind == "own" else "img/c/"
    return base + slug + ("-t.jpg" if thumb else ".jpg")


def credit(ref: str) -> str:
    kind, slug = ref.split(":", 1)
    if kind == "own":
        return 'Photo: NaN · <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>'
    c = CRED[slug]
    return (f'{e(c["author"][:48])} · <a href="{e(c["page"])}">Commons</a> · '
            f'<a href="{e(c["licence_url"])}">{e(c["licence"])}</a>')


def osm(q: str) -> str:
    return "https://www.openstreetmap.org/search?query=" + urllib.parse.quote(q + ", Chiang Rai")


def band(ref, kicker="", head="", line="", href="", cta="", cls="", th="", pre="{PRE}"):
    inner = [f'<span class="kicker">{e(kicker)}</span>' if kicker else "",
             f"<h2>{e(head)}</h2>" if head else "",
             f'<p class="th" lang="th">{e(th)}</p>' if th else "",
             f"<p>{e(line)}</p>" if line else "",
             f'<a class="btn" href="{"" if href.startswith("http") else pre}{e(href)}">{e(cta)}</a>' if href and cta else ""]
    return (f'<section class="band {cls}" style="background-image:url({pre}{img(ref)})">'
            f'<div class="in">{"".join(inner)}</div><span class="cred">{credit(ref)}</span></section>')


def shot(ref, name, href, sub="", ratio=125, pre="", ext=False):
    """The linked-image formula: background · scrim · spacer · text, the whole box a link."""
    tgt = ' rel="noopener"' if ext else ""
    return (f'<a class="shot" href="{e(href)}"{tgt}><span class="bg" style="background-image:url({pre}{img(ref, True)})"></span>'
            f'<span class="scrim"></span><span class="sp" style="padding-top:{ratio}%"></span>'
            f'<span class="tx"><b>{e(name)}</b>{f"<i>{e(sub)}</i>" if sub else ""}</span></a>')


def note(key, pre=""):
    n = C.NOTES[key]
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

/* Nan's roll */
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
.count small{display:block;font-family:var(--sans);font-size:.62rem;letter-spacing:.24em;text-transform:uppercase;color:#e9dcc4}
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
"""

NAV = [("", "Chiang Rai"), ("golden-triangle/", "Golden Triangle"), ("see/", "The sights"),
       ("sidequests/", "Sidequests"), ("slow-boat/", "Slow boat"), ("with-laila/", "Laila Group"),
       ("lanterns/", "Lanterns"), ("roll/", "Nan's roll")]


def page(path: str, title: str, desc: str, body: str, card="card.jpg", ld=None):
    depth = path.count("/")
    pre = "../" * depth
    nav = "".join(f'<a href="{pre}{h}"{" aria-current=page" if h == path else ""}>{e(t)}</a>' for h, t in NAV)
    url = CANON + "/" + path
    alt = PAGES + "/" + path
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    full = title if title == TITLE else f"{title} · {TITLE}"
    body = body.replace("{PRE}", pre)
    doc = f"""<!doctype html><html lang="en" translate="no" class="notranslate"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="google" content="notranslate">
<title>{e(full)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}"><link rel="alternate" href="{alt}"><meta name="theme-color" content="#0e6b62">
<meta property="og:type" content="website"><meta property="og:title" content="{e(full)}">
<meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/{card}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE_URL}/{card}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cpath d='M16 3 29 27H3z' fill='%23a8791f'/%3E%3C/svg%3E">
<style>{CSS}</style>{lds}</head><body>
<div class="presented">Presented with <a href="{pre}with-laila/">Laila Group</a>, Chiang Rai · <span lang="th" class="th">ไลลากรุ๊ป เชียงราย</span></div>
<header class="mast"><div class="in"><a class="brand" href="{pre}">Chiang Rai, <i>Slowly</i></a><nav aria-label="Sections">{nav}</nav></div></header>
<main>{body}</main>
<footer><div class="in">
<p><b>Chiang Rai, Slowly</b> · <span lang="th" class="th">{TITLE_TH}</span> · presented with Laila Group, {e(C.ADDRESS)} ·
<a href="{C.WA}" rel="noopener">WhatsApp {e(C.PHONE)}</a> · <a href="mailto:{C.MAIL}">{e(C.MAIL)}</a></p>
<p>Prices are Laila Group's own, as listed on <a href="{C.SHOP}/" rel="noopener">slowboatthailandlaos.com</a> on {C.READ}.
Photographs by NaN are CC BY 4.0; every other photograph carries its author and licence beside it. Text CC BY 4.0, code MIT.
<a href="{pre}credits/">Credits</a>.</p>
{fleet.maker_html()}
{fleet.row_html("chiang-rai")}
</div></footer>
<script>{LANTERN_JS}</script><script>try{{document.querySelectorAll('video[data-tap]').forEach(v=>v.addEventListener('click',()=>v.paused?v.play():v.pause()))}}catch(e){{}}</script>
</body></html>"""
    out = DOCS / path / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")


ORG = {"@context": "https://schema.org", "@type": "TravelAgency", "name": "Laila Group Chiangrai Tour",
       "alternateName": "ไลลากรุ๊ป เชียงราย ทัวร์", "url": C.SHOP + "/", "telephone": C.PHONE, "email": C.MAIL,
       "address": {"@type": "PostalAddress", "streetAddress": "869/51 Thai Viwat Alley", "addressLocality": "Chiang Rai",
                   "postalCode": "57000", "addressCountry": "TH"},
       "geo": {"@type": "GeoCoordinates", "latitude": C.OFFICE[0], "longitude": C.OFFICE[1]},
       "sameAs": [C.FB, C.IG, C.VISA]}



LANTERN_JS = r"""
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
  el.querySelector('b').textContent=d>0?d:'Tonight';
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

# ---------------------------------------------------------------- pages
def home():
    sights = "".join(
        f'<figure class="card">{shot(s["img"], s["name"], s.get("href") or "see/#" + s["id"], s["th"])}'
        f'<figcaption>{e(s["kicker"])}</figcaption></figure>' for s in C.SIGHTS[:8])
    side = "".join(
        f'<figure class="card">{shot(s["img"], s["name"], "sidequests/#" + slug(s["name"]), s["th"], 100)}</figure>'
        for s in C.SIDE[:6])
    body = f"""
<div class="col open"><div class="rubric">A Journey · <span lang="th" class="th">แอ่ว</span></div>
<h1>Chiang Rai, Slowly</h1>
<p class="dek">Three temples in three colours, a golden clock, the bend in the Mekong where three countries meet, and a slow boat to Laos.</p>
<p class="dek-th th" lang="th">{TITLE_TH} — วัดขาว วัดฟ้า บ้านดำ หอนาฬิกาทอง สามเหลี่ยมทองคำ แล้วก็ล่องเรือช้าไปลาวเจ้า</p>
<p class="by">By <a href="https://hongdam.net/" rel="noopener">NaN</a> · Photographs from her camera roll</p></div>
{band("c:golden-triangle-3", "Sop Ruak", "The most beautiful afternoon in the north", th="สามเหลี่ยมทองคำ ยามแลง งามขนาดเจ้า", href="golden-triangle/", cta="The Golden Triangle", cls="tall")}
<div class="col">
{note("day")}
<p class="lede">Chiang Rai is the northernmost city in Thailand and among its gentlest: a {e("sleepy little town full of lovely people")}, as Nan puts it, with a golden clock tower at the centre and the hills rising on every side. It is small enough to cross by scooter in ten minutes and generous enough to fill a week.</p>
<p>Within half an hour of the clock tower stand three of the most extraordinary buildings in Asia, each the life's work of a Chiang Rai artist: a temple in white, a temple in blue, and a house in black. An hour north, the Kok and the Ruak and the Mekong carry you to the Golden Triangle, where Thailand, Laos and Myanmar meet on one bend of the river. That was the highlight of our visit, and we went back several times.</p>
<p class="th" lang="th">เชียงรายเป็นเมืองเล็ก ๆ ผู้คนใจดี แอ่วได้สบาย ๆ ทั้งวัน ม่วนใจ๋แต๊เจ้า</p>
</div>
<div class="wide"><h2 class="sec"><small>The sights · <span lang="th" class="th">ที่เที่ยว</span></small>Headliners</h2>
<div class="shots">{sights}</div><p><a href="see/">All the sights →</a></p></div>
<div class="col">{note("boat", "")}
<blockquote class="pull"><p>“{e(C.QUOTE_GT)}”</p><cite>Nan, on the Golden Triangle</cite></blockquote>
<figure class="polaroid"><img src="img/own/nan-golden-triangle-t.jpg" alt="Nan smiling at the Golden Triangle viewpoint" loading="lazy" width="405" height="720"><figcaption>Nan, at the Golden Triangle</figcaption></figure>
</div>
{band("c:luang-prabang-1", "Laila Group · the slow boat", "Two days down the Mekong to Luang Prabang", line="Picked up at your door before dawn, across the border by eight, on the river by ten. From ฿1,690.", th="ล่องเรือช้าไปหลวงพระบาง สองวันหนึ่งคืนเจ้า", href="slow-boat/", cta="The slow boat", cls="right")}
{skyband("c:lantern-dark", "Yi Peng · 24 November 2026", "Lantern Night", "ยี่เป็ง เชียงราย", count=True, href="lanterns/", cta="Lantern Night")}
<div class="wide"><h2 class="sec"><small>Sidequests · <span lang="th" class="th">แอ่วนอกเส้นทาง</span></small>The small wonders</h2>
<div class="shots">{side}</div><p><a href="sidequests/">Every sidequest →</a></p></div>
<div class="col">{note("desk")}
<h2 class="sec"><small>Laila Group · <span lang="th" class="th">ไลลากรุ๊ป</span></small>Everything, from one alley</h2>
<p>Laila Group keeps its office on Thai Viwat Alley, a few minutes' walk from the clock tower. From there it runs the slow boats and trains to Laos, day trips to every mountain on this page, cars with drivers and scooters by the day, a visa office, and a designer consignment shop next door.</p>
<p class="th" lang="th">ไลลากรุ๊ป อยู่ซอยไทยวิวัฒน์ กลางเมืองเชียงราย มีทั้งทัวร์ เรือช้าไปลาว รถเช่า มอเตอร์ไซค์ งานวีซ่า แล้วก็ร้านแบรนด์เนมฝากขาย ทักมาได้เน้อเจ้า</p>
<div class="ctas"><a class="btn" href="with-laila/">Laila Group</a><a class="btn ghost" href="{e(C.wa("Hello Laila Group! I found you on Chiang Rai, Slowly."))}" rel="noopener">WhatsApp</a></div>
{note("shop")}
</div>
{band("c:clock-tower-2", "Ho Nalika · evenings", "Red, green, gold, and then the night bazaar", th="หอนาฬิกาเปลี่ยนสีทุกค่ำเจ้า", href="see/#clock-tower", cta="The clock tower", cls="short")}
"""
    page("", TITLE, "A journey through Chiang Rai and the Golden Triangle — temples, the Mekong, sidequests and the slow boat to Laos, with Laila Group.",
         body, ld=[ORG, {"@context": "https://schema.org", "@type": "WebSite", "name": TITLE, "url": SITE_URL + "/"}])


def slug(s):
    import re
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def go_line(s, pre):
    parts = []
    if s.get("osm"):
        parts.append(f'<a href="{osm(s["osm"])}" rel="noopener">Map</a>')
    if s.get("laila"):
        parts.append(f'<a href="{trip(s["laila"])}" rel="noopener">Go with Laila Group</a>')
    if s.get("href"):
        parts.append(f'<a href="{pre}{s["href"]}">More</a>')
    return f'<p class="go">{"".join(parts)}</p>' if parts else ""


def sight_block(s, pre):
    ratio = 125
    vid = ""
    if s.get("video"):
        vid = (f'<video src="{pre}{s["video"]}" poster="{pre}{img(s["img"], True)}" preload="none" muted loop playsinline '
               f'data-tap controls width="270" height="480"></video><span class="cred">Video: NaN · CC BY 4.0</span>')
    kick = f'<span class="kick">{e(s["kicker"])}</span>' if s.get("kicker") else ""
    tht = f'<p class="th" lang="th">{e(s["th_text"])}</p>' if s.get("th_text") else ""
    href = osm(s["osm"]) if s.get("osm") else "#" + s.get("id", slug(s["name"]))
    return (f'<section class="sight" id="{s.get("id", slug(s["name"]))}"><figure class="card">'
            f'{shot(s["img"], s["th"], href, "", ratio, pre, True)}'
            f'<span class="cred">{credit(s["img"])}</span>{vid}</figure>'
            f'<div>{kick}<h3>{e(s["name"])}<span class="thn" lang="th">{e(s["th"])}</span></h3>'
            f'<p>{e(s["text"])}</p>{tht}{go_line(s, pre)}</div></section>')


def see():
    blocks = []
    for i, s in enumerate(C.SIGHTS):
        blocks.append(sight_block(s, "../"))
        if i == 2:
            blocks.append(note("day", "../"))
        if i == 6:
            blocks.append(note("car", "../"))
        if i == 9:
            blocks.append(note("wa", "../"))
    body = f"""
<div class="col open"><div class="rubric">The sights · <span lang="th" class="th">ที่เที่ยว</span></div>
<h1>The Headliners</h1><p class="dek">White, blue, black and gold, and the mountains beyond.</p></div>
{band("c:white-temple-2", "Wat Rong Khun", "A temple built of light", th="วัดร่องขุ่น งามจับใจ๋เจ้า", cls="short")}
<div class="col">{"".join(blocks)}</div>
{band("c:phu-chi-fa-3", "Phu Chi Fa", "First light over the mist", th="ทะเลหมอกภูชี้ฟ้า", href=trip("phu-chi-fa-chiang-rai-mountains"), cta="Go before dawn", cls="right")}
"""
    page("see/", "The Headliners", "The White Temple, the Blue Temple, the Black House, the golden clock tower and the mountains of Chiang Rai.", body)


def golden():
    blocks = []
    for i, s in enumerate(C.GT):
        blocks.append(sight_block(s, "../"))
        if i == 1:
            blocks.append(note("day", "../"))
        if i == 3:
            blocks.append(note("car", "../"))
    body = f"""
<div class="col open"><div class="rubric">The highlight · <span lang="th" class="th">สามเหลี่ยมทองคำ</span></div>
<h1>The Golden Triangle</h1>
<p class="dek">Three countries, two rivers, one long golden afternoon.</p>
<p class="dek-th th" lang="th">น้ำรวกบรรจบน้ำโขง ไทย ลาว เมียนมา มาพบกันตรงนี้เจ้า</p></div>
{band("c:golden-triangle-2", "Sop Ruak", "Where the Ruak meets the Mekong", th="ยามแลงแดดสีทองส่องน้ำโขง งามขนาดเน้อ", cls="tall")}
<div class="col">
<blockquote class="pull"><p>“{e(C.QUOTE_GT)}”</p><cite>Nan</cite></blockquote>
<p class="lede">An hour and a little north of Chiang Rai, past Mae Chan and the turn for Chiang Saen, the road comes down to the water and stops. Across the Mekong is Laos. Up the smaller river, the Ruak, is Myanmar. The bend between them is the Golden Triangle, and in the late afternoon the name explains itself: the light goes gold, the river goes gold, and so does the great seated Buddha on the bank.</p>
<p>Plan on the whole afternoon. Start at the Hall of Opium, walk the river road to the viewpoint, take a longtail out onto the Mekong, and finish on the glass walkway south of Chiang Saen with the sun going down behind the hills.</p>
<figure class="polaroid"><img src="../img/own/nan-golden-triangle-t.jpg" alt="Nan at the Golden Triangle" loading="lazy" width="405" height="720"><figcaption>Late afternoon, the first of several visits</figcaption></figure>
{"".join(blocks)}
<h2 class="sec"><small>Getting there · <span lang="th" class="th">ไปจะไดเจ้า</span></small>Three ways north</h2>
<table class="list">
<tr><td><b><a href="{trip("one-day-sightseeing-tour-in-chiang-rai")}" rel="noopener">Laila Group's one-day tour</a></b><small>Golden Triangle and the Hall of Opium, with the White Temple, Blue Temple and Black House on the same day. Guide and lunch included.</small></td><td class="p">฿1,200</td></tr>
<tr><td><b><a href="../with-laila/#wheels">A car with a driver</a></b><small>Go at your own pace, stay for the sunset, come back several times.</small></td><td class="p">from ฿1,200 a day</td></tr>
<tr><td><b><a href="../with-laila/#wheels">A scooter</a></b><small>About seventy kilometres each way on the main road.</small></td><td class="p">from ฿250 a day</td></tr>
</table><p class="asof">Prices as listed by Laila Group, {C.READ}.</p>
</div>
<div class="wide"><div class="shots three">
{"".join(f'<figure class="card">{shot(r, c, "../roll/", "", 150, "../")}</figure>' for r, c in [("own:skywalk-blossom", "Blossom over the glass"), ("own:skywalk-arch", "Toward the river"), ("own:across-mekong", "Across the Mekong"), ("own:opium-mural-2", "The farming year")])}
</div></div>
{band("c:mekong-2", "Chiang Saen", "Keep going: the river runs all the way to Luang Prabang", href="slow-boat/", cta="The slow boat", cls="right")}
"""
    page("golden-triangle/", "The Golden Triangle", "Sop Ruak, the golden Buddha, the Hall of Opium, the glass walkway and Chiang Saen — the highlight of Chiang Rai.", body,
         ld=[{"@context": "https://schema.org", "@type": "TouristAttraction", "name": "Golden Triangle (Sop Ruak)",
              "geo": {"@type": "GeoCoordinates", "latitude": 20.3526, "longitude": 100.0818}}])


def sidequests():
    blocks = []
    for i, s in enumerate(C.SIDE):
        blocks.append(sight_block(dict(s, id=slug(s["name"])), "../"))
        if i in (2, 7):
            blocks.append(note(["shop", "visa"][i == 7], "../"))
    body = f"""
<div class="col open"><div class="rubric">Sidequests · <span lang="th" class="th">แอ่วนอกเส้นทาง</span></div>
<h1>The Small Wonders</h1><p class="dek">Vanilla, painted pillars, a warm waterfall, eggs boiled in a spring, and khao soi twice a day.</p></div>
<div class="col">{"".join(blocks)}</div>
{band("c:kok-river-2", "Mae Nam Kok", "The river through town", th="แม่น้ำกก ไหลผ่านกลางเมืองเจ้า", cls="short")}
"""
    page("sidequests/", "Sidequests", "Chiang Rai's small wonders — vanilla farm, bus-station murals, hot-spring eggs, a warm waterfall, khao soi.", body)


def slowboat():
    rows = "".join(
        f'<tr><td><b><a href="{trip(b["slug"])}" rel="noopener">{e(b["name"])}</a></b> <span class="th" lang="th">{e(b["th"])}</span>'
        f'<small>{e(b["days"])} · {e(b["text"])}</small></td><td class="p">{thb(b["price"])}</td></tr>' for b in C.BOATS)
    trains = "".join(f'<tr><td><a href="{trip(s)}" rel="noopener">{e(n)}</a></td><td class="p">{thb(p)}</td></tr>' for n, s, p in C.TRAINS)
    body = f"""
<div class="col open"><div class="rubric">Laila Group · <span lang="th" class="th">เรือช้า</span></div>
<h1>The Slow Boat</h1><p class="dek">Two days down the Mekong from Chiang Rai to Luang Prabang, with a night in Pak Beng between.</p>
<p class="dek-th th" lang="th">ล่องเรือช้าน้ำโขงไปหลวงพระบาง นอนปากแบ่งหนึ่งคืน ไลลากรุ๊ปมารับถึงที่พักตั้งแต่เช้ามืด พาข้ามด่าน ส่งถึงท่าเรือเจ้า</p></div>
{band("c:luang-prabang-2", "The Mekong", "The long way is the lovely way", th="ทางไกลที่งามที่สุดเจ้า", cls="tall")}
<div class="col">
{note("wa", "../")}
<p class="lede">It begins in the dark. Laila Group's van collects you from your hotel at five, and by the time the sun is up you are at the river at Chiang Khong with your passport stamped. Across the bridge is Huay Xai; below it the long wooden boats wait at the pier. At ten you cast off.</p>
<p>For two days the Mekong carries you between green hills, past sand bars and fishing boats and villages that come down to the water. The first night is at Pak Beng, a river town that exists to welcome the boats. On the second afternoon, Luang Prabang.</p>
<h2 class="sec"><small>The boats · <span lang="th" class="th">เรือ</span></small>Choose your river</h2>
<table class="list">{rows}</table>
<p class="asof">Prices as listed by Laila Group, {C.READ}. Pack US dollars for the Lao visa on arrival (USD 40 on her listing) and your passport photo.</p>
<div class="ctas"><a class="btn" href="{trip("slow-boat-chiang-rai-to-luang-prabang")}" rel="noopener">Book the slow boat</a><a class="btn ghost" href="{e(C.wa("Hello Laila Group! I would like the slow boat to Luang Prabang."))}" rel="noopener">Ask on WhatsApp</a></div>
</div>
<div class="wide"><div class="shots three">
{shot("c:chiang-khong-1", "Chiang Khong", "../with-laila/", "เชียงของ", 66, "../")}{shot("c:slow-boat-1", "Pak Beng", "../with-laila/", "ปากแบ่ง", 66, "../")}{shot("c:luang-prabang-3", "Luang Prabang", "../with-laila/", "หลวงพระบาง", 66, "../")}
</div></div>
<div class="col">
<h2 class="sec"><small>Or by rail · <span lang="th" class="th">รถไฟลาว-จีน</span></small>The train through Laos</h2>
<p>Laila Group also runs the fast way: across the border and onto the Laos–China Railway, Luang Prabang the same day, Vang Vieng and Vientiane beyond.</p>
<table class="list">{trains}</table>
{note("desk", "../")}
</div>
"""
    page("slow-boat/", "The Slow Boat", "Laila Group's slow boat from Chiang Rai to Luang Prabang, from ฿1,690 — plus the train and bus to Laos.", body,
         ld=[ORG, {"@context": "https://schema.org", "@type": "TouristTrip", "name": "Slow boat Chiang Rai to Luang Prabang",
                   "provider": {"@type": "TravelAgency", "name": "Laila Group Chiangrai Tour"},
                   "offers": {"@type": "Offer", "price": "1690", "priceCurrency": "THB",
                              "url": trip("slow-boat-chiang-rai-to-luang-prabang")}}])


def laila():
    days = "".join(f'<tr><td><b><a href="{trip(s)}" rel="noopener">{e(n)}</a></b><small>{e(t)}</small></td><td class="p">{e(p)}</td></tr>' for n, s, p, t in C.DAYS)
    wheels = "".join(f'<tr><td><a href="{trip(s)}" rel="noopener">{e(n)}</a></td><td class="p">{thb(p)} a day</td></tr>' for n, s, p in C.WHEELS)
    visas = "".join(f'<tr><td><b>{e(n)}</b><small>{e(t)}</small></td></tr>' for n, t in C.VISAS)
    boats = "".join(f'<tr><td><a href="{trip(b["slug"])}" rel="noopener">{e(b["name"])}</a></td><td class="p">{thb(b["price"])}</td></tr>' for b in C.BOATS)
    body = f"""
<div class="col open"><div class="rubric">Presented with · <span lang="th" class="th">ไลลากรุ๊ป</span></div>
<h1>Laila Group</h1><p class="dek">Tours, boats, trains, cars, visas and a designer consignment shop, from one alley in the middle of Chiang Rai.</p>
<p class="dek-th th" lang="th">ไลลากรุ๊ป ซอยไทยวิวัฒน์ เชียงราย — ทัวร์ เรือช้า รถไฟไปลาว รถเช่า วีซ่า แล้วก็ร้านแบรนด์เนมฝากขายเจ้า</p></div>
<div class="col">
<div class="ctas"><a class="btn" href="{e(C.wa("Hello Laila Group! I found you on Chiang Rai, Slowly."))}" rel="noopener">WhatsApp {e(C.PHONE)}</a>
<a class="btn ghost" href="{C.SHOP}/" rel="noopener">slowboatthailandlaos.com</a><a class="btn ghost" href="mailto:{C.MAIL}">Email</a></div>
<p><b>Where:</b> {e(C.ADDRESS)}, at Sofia Hostel. <span lang="th" class="th">{e(C.ADDRESS_TH)}</span> · <a href="https://www.openstreetmap.org/?mlat={C.OFFICE[0]}&amp;mlon={C.OFFICE[1]}#map=18/{C.OFFICE[0]}/{C.OFFICE[1]}" rel="noopener">Map</a> ·
<a href="https://www.openstreetmap.org/directions?to={C.OFFICE[0]}%2C{C.OFFICE[1]}" rel="noopener">Directions</a></p>
<p>Also on <a href="{C.FB}" rel="noopener">Facebook</a> and <a href="{C.IG}" rel="noopener">Instagram</a>.</p>
<h2 class="sec" id="boats"><small>To Laos · <span lang="th" class="th">ไปลาว</span></small>Slow boats</h2>
<table class="list">{boats}</table><p><a href="../slow-boat/">The slow boat, day by day →</a></p>
<h2 class="sec" id="days"><small>Day trips · <span lang="th" class="th">เที่ยวรายวัน</span></small>Every mountain</h2>
<table class="list">{days}</table>
{note("desk", "../")}
<h2 class="sec" id="wheels"><small>By the day · <span lang="th" class="th">รถเช่า</span></small>Wheels</h2>
<table class="list">{wheels}</table>
<p class="asof">Prices as listed by Laila Group, {C.READ}. Cars come with a driver.</p>
<h2 class="sec" id="visas"><small>Visa Services Thailand · <span lang="th" class="th">วีซ่า</span></small>The visa office</h2>
<p>For a longer stay, Laila Group's visa office handles the paperwork from consultation to approval, and the bank account and tax number after.</p>
<table class="list">{visas}</table>
<div class="ctas"><a class="btn ghost" href="{C.VISA}" rel="noopener">visaservicesthailand.com</a></div>
<aside class="note"><span class="nk">In Chiang Mai <span lang="th" class="th">· เชียงใหม่</span></span><p>Chiang Mai Visa Desk, for Thai visas in Chiang Mai, and for Thai families bound for America.</p><a href="{C.DESK}" rel="noopener">chiangmaivisadesk.com →</a></aside>
<h2 class="sec" id="shop"><small>Laila's Designer Consignment · <span lang="th" class="th">ร้านแบรนด์เนมฝากขาย</span></small>The shop</h2>
<p>Designer pieces, consigned, next door to the visa office on Thai Viwat Alley. Come in and see what has arrived; or bring something beautiful of your own to leave with Laila.</p>
<p class="th" lang="th">ของแบรนด์เนมสภาพงาม ฝากขายได้ ซื้อได้ อยู่ติดกับสำนักงานวีซ่าเจ้า แวะมาแอ่วเน้อ</p>
</div>
{band("c:mekong-3", "Laila Group", "The river is waiting", th="ทักมาได้เน้อเจ้า", href=C.wa("Hello Laila Group! I found you on Chiang Rai, Slowly."), cta="Say hello", cls="short")}
"""
    page("with-laila/", "Laila Group", "Laila Group, Chiang Rai: slow boats and trains to Laos, day trips, cars and scooters, visas, and designer consignment.", body, ld=[ORG])



def skyband(ref, kicker, head, th, pre="{PRE}", count=False, href="", cta=""):
    cnt = ""
    if count:
        cnt = ('<div class="count" data-count><svg viewBox="-50 -50 100 100" data-moon aria-hidden="true">'
               '<circle r="46" fill="#2a2433"/><path fill="#fff4d6" d=""/></svg>'
               '<div><b>–</b><small>nights to the Yi Peng moon · 24 Nov 2026</small></div></div>')
    btn = f'<p><a class="btn" href="{"" if href.startswith("http") else pre}{e(href)}">{e(cta)}</a></p>' if href else ""
    return (f'<section class="skyband" style="background-image:url({pre}{img(ref)})"><canvas class="sky" aria-hidden="true"></canvas>'
            f'<div class="in"><span class="kicker">{e(kicker)}</span><h2>{e(head)}</h2><div class="thbig" lang="th">{e(th)}</div>'
            f'{cnt}{btn}<p class="tap">Tap the sky</p></div><span class="cred" style="position:absolute;right:0;bottom:0;'
            f'background:rgba(0,0,0,.6);padding:.2rem .5rem">{credit(ref)}</span></section>')


def lanterns():
    cards = "".join(
        f'<figure class="card"><a class="shot" href="{e(osm(l["osm"]) if l.get("osm") else "#float")}" rel="noopener">'
        f'<span class="bg" style="background-image:url(../{img(l["img"])})"></span><span class="scrim"></span>'
        f'<span class="sp" style="padding-top:120%"></span><span class="tx"><b>{e(l["name"])}</b><i>{e(l["th"])}</i>'
        f'<p>{e(l["line"])}</p></span></a></figure>' for l in C.LANTERNS)
    body = f"""
{skyband("c:lantern-sky", "Yi Peng · Loy Krathong", "Lantern Night", "ยี่เป็ง ลอยกระทง", count=True)}
<div class="col" style="text-align:center">
<p class="dek">One full moon. Lanterns up, krathongs down the river, and every wish with them.</p>
<p class="dek-th th" lang="th">คืนเพ็ญเดือนยี่ โคมลอยขึ้นฟ้า กระทงลอยตามน้ำ ขอให้โชคดีมีสุขเจ้า</p>
</div>
<div class="bigshots">{cards}</div>
<div class="col" id="float">
{note("lantern", "../")}
<h2 class="sec"><small>Three nights · <span lang="th" class="th">สามคืน</span></small>Around the full moon</h2>
<p>Chiang Rai lights the Kok and Chiang Saen lights the Mekong over the nights around the full moon. The city posts its programme in the weeks before.</p>
<p class="th" lang="th">งานในเมืองเข้าฟรีเจ้า กระทงใบตองราว 30–100 บาท</p>
</div>
{band("c:lantern-many", "The wish goes up", "A sky of lanterns", th="โคมลอยพาความทุกข์ลอยไปเจ้า", href="with-laila/", cta="Plan it with Laila", cls="tall")}
<div class="wide"><div class="shots three">{shot("c:lantern-field", "Lanterns", "../golden-triangle/", "โคมลอย", 66, "../")}{shot("c:lantern-candles", "Candles", "../golden-triangle/", "ประทีป", 66, "../")}{shot("c:krathong-float", "Krathong", "../golden-triangle/", "กระทง", 66, "../")}</div></div>
"""
    page("lanterns/", "Lantern Night", "Yi Peng and Loy Krathong in Chiang Rai and Chiang Saen — the Kok River, four nations on the Mekong, and your own krathong. 24 November 2026.", body,
         ld=[{"@context": "https://schema.org", "@type": "Event", "name": "Yi Peng & Loy Krathong, Chiang Rai", "startDate": C.LANTERN_NIGHT,
              "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
              "location": {"@type": "Place", "name": "Kok River, Chiang Rai", "address": "Chiang Rai, Thailand"}}])


def roll():
    figs = "".join(f'<figure><img src="../img/own/{k}-t.jpg" alt="{e(v["caption"])}" loading="lazy" width="{v["w"]}" height="{v["h"]}">'
                   f'<figcaption>{e(v["caption"])}</figcaption></figure>' for k, v in OWN.items())
    body = f"""
<div class="col open"><div class="rubric">From the camera roll · <span lang="th" class="th">ภาพถ่าย</span></div>
<h1>Nan's Roll</h1><p class="dek">February to June, Chiang Rai and the Golden Triangle, as they came off the phone.</p></div>
<div class="wide"><div class="roll">{figs}</div>
<p class="cred">Photographs by NaN, CC BY 4.0.</p></div>
<div class="col">{note("day", "../")}</div>
"""
    page("roll/", "Nan's Roll", "Chiang Rai and the Golden Triangle from NaN's camera roll.", body)


def credits():
    rows = "".join(f'<tr><td><a href="{e(c["page"])}" rel="noopener">{e(c["title"][5:])}</a><small>{e(c["author"])}</small></td>'
                   f'<td class="p"><a href="{e(c["licence_url"])}" rel="noopener">{e(c["licence"])}</a></td></tr>' for c in CRED.values())
    body = f"""<div class="col open"><h1>Credits</h1></div><div class="col">
<p>Photographs marked NaN are hers, CC BY 4.0. These are from Wikimedia Commons, each under its own licence:</p>
<table class="list">{rows}</table>
<p>Tour, boat, rental and visa details are Laila Group's own, from slowboatthailandlaos.com and visaservicesthailand.com, read {C.READ}.</p></div>"""
    page("credits/", "Credits", "Photo credits and sources.", body)


def machine():
    urls = ["", "lanterns/", "golden-triangle/", "see/", "sidequests/", "slow-boat/", "with-laila/", "roll/", "credits/"]
    (DOCS / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                                      + "".join(f"<url><loc>{SITE_URL}/{u}</loc></url>" for u in urls) + "</urlset>\n")
    (DOCS / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    (DOCS / "llms.txt").write_text(
        f"# {TITLE}\n\n> Chiang Rai and the Golden Triangle — the headline sights, the sidequests, and the slow boat to "
        f"Luang Prabang — presented with Laila Group, Thai Viwat Alley, Chiang Rai.\n\n"
        + "".join(f"- [{t}]({SITE_URL}/{u})\n" for u, t in NAV) +
        f"\nLaila Group: {C.SHOP}/ · WhatsApp {C.PHONE} · {C.MAIL}\nVisa Services Thailand: {C.VISA}\n")
    (DOCS / ".nojekyll").write_text("")
    fleet.decorate(DOCS, "chiang-rai")


def main():
    for p in ["lanterns", "golden-triangle", "see", "sidequests", "slow-boat", "with-laila", "roll", "credits"]:
        shutil.rmtree(DOCS / p, ignore_errors=True)
    home(); lanterns(); see(); golden(); sidequests(); slowboat(); laila(); roll(); credits(); machine()
    print("built", sum(1 for _ in DOCS.rglob("index.html")), "pages →", DOCS)


if __name__ == "__main__":
    main()
