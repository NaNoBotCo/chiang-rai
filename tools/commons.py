# -*- coding: utf-8 -*-
"""commons.py — search Wikimedia Commons per topic, keep free-licence landscape files.

    python3 tools/commons.py search   -> data/commons/_triage.json (nothing downloaded)
    python3 tools/commons.py fetch    -> downloads picks in data/commons/picks.json at 1600px
"""
import json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "commons"
UA = "laila-chiang-rai-build/0.1 (https://hongdam.net; nan@motdang.net) python-urllib"
API = "https://commons.wikimedia.org/w/api.php"
FREE = re.compile(r"^(cc0|pd|public.domain|cc.by(.sa)?(.[1-4]\.[0-9])?|fal)", re.I)

TOPICS = {
 "white-temple": "Wat Rong Khun",
 "blue-temple": "Wat Rong Suea Ten",
 "black-house": "Baan Dam Chiang Rai",
 "clock-tower": "Chiang Rai clock tower",
 "golden-triangle": "Golden Triangle Sop Ruak Mekong",
 "golden-buddha": "Golden Triangle Buddha Chiang Saen",
 "mekong": "Mekong river Chiang Saen",
 "slow-boat": "Mekong slow boat Pakbeng",
 "luang-prabang": "Luang Prabang Mekong",
 "chiang-khong": "Chiang Khong Mekong",
 "hall-of-opium": "Hall of Opium Golden Triangle",
 "chiang-saen": "Wat Pa Sak Chiang Saen",
 "doi-tung": "Mae Fah Luang Garden Doi Tung",
 "tham-luang": "Tham Luang Nang Non",
 "mae-salong": "Doi Mae Salong tea",
 "singha-park": "Singha Park Chiang Rai",
 "huay-pla-kang": "Wat Huay Pla Kang",
 "phra-kaew": "Wat Phra Kaew Chiang Rai",
 "night-bazaar": "Chiang Rai night bazaar",
 "phu-chi-fa": "Phu Chi Fa",
 "kok-river": "Kok River Chiang Rai",
 "mae-sai": "Mae Sai",
 "khun-korn": "Khun Korn waterfall",
 "choui-fong": "Choui Fong tea plantation",
 "khao-soi": "Khao soi",
 "lanna-food": "Northern Thai food",
 "wat-rong-khun-night": "White Temple Chiang Rai",
 "phu-sang": "Phu Sang waterfall",
 "mae-kachan": "Mae Kachan hot spring",
 "chiang-rai-city": "Chiang Rai city",
}

def api(params):
    params = dict(params, format="json")
    req = urllib.request.Request(API, data=urllib.parse.urlencode(params).encode(), headers={"User-Agent": UA})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            err = e; time.sleep(2 + 3 * i)
    raise RuntimeError(err)

def strip(s): return re.sub(r"<[^>]+>", "", s or "").strip()

def info(titles, width=1600):
    out = []
    for i in range(0, len(titles), 20):
        d = api({"action": "query", "prop": "imageinfo", "iiprop": "url|size|extmetadata|mime",
                 "iiurlwidth": width, "titles": "|".join(titles[i:i+20])})
        for p in d.get("query", {}).get("pages", {}).values():
            ii = (p.get("imageinfo") or [{}])[0]; m = ii.get("extmetadata", {})
            lic = (m.get("LicenseShortName", {}).get("value") or "")
            out.append({"title": p.get("title"), "w": ii.get("width"), "h": ii.get("height"),
                        "mime": ii.get("mime"), "thumb": ii.get("thumburl"), "page": ii.get("descriptionurl"),
                        "licence": lic, "licence_url": m.get("LicenseUrl", {}).get("value", ""),
                        "author": strip(m.get("Artist", {}).get("value"))[:120],
                        "desc": strip(m.get("ImageDescription", {}).get("value"))[:200]})
    return out

def search():
    tri = {}
    for k, q in TOPICS.items():
        d = api({"action": "query", "list": "search", "srnamespace": 6, "srsearch": q, "srlimit": 30})
        titles = [x["title"] for x in d.get("query", {}).get("search", [])]
        rows = [r for r in info(titles) if r["mime"] == "image/jpeg" and FREE.match(r["licence"].replace(" ", "-"))
                and (r["w"] or 0) >= 1400 and (r["w"] or 0) > (r["h"] or 1) * 1.2]
        tri[k] = rows; print(k, len(titles), len(rows), file=sys.stderr)
        time.sleep(0.5)
    (OUT / "_triage.json").write_text(json.dumps(tri, ensure_ascii=False, indent=1))

def fetch():
    picks = json.loads((OUT / "picks.json").read_text())
    tri = json.loads((OUT / "_triage.json").read_text())
    byt = {r["title"]: r for rows in tri.values() for r in rows}
    meta = {}
    for slug, title in picks.items():
        r = byt[title]; f = OUT / f"{slug}.jpg"
        if not f.exists():
            req = urllib.request.Request(r["thumb"], headers={"User-Agent": UA})
            f.write_bytes(urllib.request.urlopen(req, timeout=120).read()); time.sleep(0.5)
        meta[slug] = {k: r[k] for k in ("title", "page", "licence", "licence_url", "author")}
    (OUT / "credits.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    {"search": search, "fetch": fetch}[sys.argv[1]]()
