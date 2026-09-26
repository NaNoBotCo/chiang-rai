# Chiang Rai, Slowly · แอ่วเชียงราย ค่อย ๆ ไปเน้อ

A journey through Chiang Rai and the Golden Triangle — the headline sights, the sidequests,
and the slow boat to Luang Prabang — presented with Laila Group, Thai Viwat Alley, Chiang Rai.
Made by Hongdam, Chiang Rai.

Pages: home · golden-triangle · see · sidequests · slow-boat · with-laila · roll · credits.
The same pages in Thai under `th/`, each linked to its English partner.

    python3 tools/build.py     # docs/ from tools/content.py
    python3 tools/card.py      # docs/card.jpg, 1200×630
    python3 tools/serve.py     # http://127.0.0.1:8871

- Words: `tools/content.py`, English plus Thai in the rao/jao register.
- The Thai edition's words: `tools/content_th.py`, keyed to content.py; the build stops on a missing partner.
- Laila Group's tours, prices and contacts: slowboatthailandlaos.com and
  visaservicesthailand.com, read 2026-09-26.
- Photographs: NaN's camera roll (CC BY 4.0) in `docs/img/own/`; Wikimedia Commons in
  `docs/img/c/`, each credited on the page and in `data/commons/credits.json`.
- `tools/commons.py search|fetch` re-runs the Commons harvest.

Licence: text CC BY 4.0, code MIT. Commons photographs keep their own licences.
