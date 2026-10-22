"""Builds every output from tools/content.py and tools/templates/images.html.

Run from the repo root:
    python3 tools/build.py

Writes:
    entry/images/*.png              the five thread images (1600x900)
    entry/redbelly-thread-images.zip the images plus their alt text
    index.html                      the website
    entry/THREAD.md                 the thread as plain text
    SOURCES.md, FACT_CHECK.md       sources and the sentence-by-sentence fact check
    entry/Redbelly_Thread.pdf       A4 document (Chromium print)
    entry/Redbelly_Thread.docx      Word document with the brand fonts embedded
"""

import base64
import html
import io
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from content import (  # noqa: E402
    FACTS, LAST_VERIFIED, LAST_VERIFIED_LONG, LEFT_OUT, POSTS, SOURCES, SUBTITLE,
    TASK, TITLE, fact, post_sources, source,
)
from xlength import x_length  # noqa: E402

ENTRY = ROOT / "entry"
IMAGES = ENTRY / "images"
ASSETS = ROOT / "assets"
TEMPLATES = ROOT / "tools" / "templates"
N = len(POSTS)
N_IMG = sum(1 for p in POSTS if p.get("image"))

CHECKLIST = [
    ("No banned word or stand-in", "Not used anywhere: posts, alt text, images, documents, file names or code.",
     "tools/check_entry.py scans every file in the repo, the PDF and Word text, and all text drawn on the images."),
    ("Every fact correct", f"{len(FACTS)} facts, each traced to public Redbelly, Tokeniser or RBA material.",
     "Fact check below. Project Acacia claims rely on the RBA's own final report."),
    ("No price talk or advice", "No tokens, prices, returns or buying language.",
     "The checker scans posts, alt text and image text for price and advice words."),
    ("Licensed assets only", "Images drawn from scratch. Fonts are open licence. Logo from the DAO brand kit.",
     "Image source: tools/templates/images.html. Font licences in assets/fonts."),
    ("No personal credit", "No names, handles, signatures or made-by lines anywhere in the entry.",
     "The checker scans for handles and credit lines."),
    ("Fits X", f"All {N} posts are 280 characters or fewer, counted the way X counts them.",
     "Each post shows its count."),
    ("Not posted before judging", "Nothing has been posted to X.", "The DAO posts the winning entry."),
]


def esc(s):
    return html.escape(s, quote=True)


def fmt_count(p):
    return f"{x_length(p['text'])} / 280"


# ---------------------------------------------------------------- images

def build_images():
    from render import browser, wait_for_fonts
    IMAGES.mkdir(parents=True, exist_ok=True)
    with browser() as b:
        page = b.new_page(viewport={"width": 1700, "height": 1000})
        page.goto((TEMPLATES / "images.html").as_uri())
        wait_for_fonts(page)
        for el in page.query_selector_all(".frame"):
            name = el.get_attribute("data-file")
            el.screenshot(path=str(IMAGES / name))
            print("wrote", (IMAGES / name).relative_to(ROOT))


def build_web_logos():
    from PIL import Image
    for variant in ("on-dark", "on-light"):
        src = ASSETS / "brand" / f"dao-logo-{variant}.png"
        im = Image.open(src).convert("RGBA")
        h = 112
        im.resize((round(im.width * h / im.height), h), Image.LANCZOS).save(
            ASSETS / "brand" / f"dao-logo-{variant}-112.png", optimize=True)


def build_zip():
    out = ENTRY / "redbelly-thread-images.zip"
    alt = []
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for i, p in enumerate(POSTS, 1):
            if p.get("image"):
                z.write(IMAGES / p["image"], p["image"])
                alt.append(f"{p['image']}  (post {i}/{N})\n{p['alt']}\n")
        z.writestr("ALT_TEXT.txt", f"{TITLE}: image alt text\nLast verified {LAST_VERIFIED_LONG}\n\n" + "\n".join(alt))
    print("wrote", out.relative_to(ROOT))


# ---------------------------------------------------------------- markdown

def build_markdown():
    lines = [f"# {TITLE}", "", f"{SUBTITLE} Last verified {LAST_VERIFIED_LONG}.", "",
             f"Format: X thread, {N} posts, {N_IMG} images. Post them in order as one thread, attach each "
             "image to the post marked below, and paste the alt text into the image description.", ""]
    for i, p in enumerate(POSTS, 1):
        lines += [f"## {i}/{N}: {p['title']}", "", "```text", p["text"], "```", ""]
        if p.get("image"):
            lines += [f"![Image for post {i}](images/{p['image']})", "",
                      f"**Attach:** `images/{p['image']}`  ", f"**Alt text:** {p['alt']}  "]
        lines += [f"*{fmt_count(p)} characters. Sources: {', '.join(post_sources(p))}*", ""]
    lines += ["---", "", "Sources: [`SOURCES.md`](../SOURCES.md). Fact check: [`FACT_CHECK.md`](../FACT_CHECK.md).", ""]
    (ENTRY / "THREAD.md").write_text("\n".join(lines), encoding="utf8")

    src = ["# Sources", "", f"Every fact about Redbelly in the thread comes from one of these public sources, "
           f"all checked on {LAST_VERIFIED_LONG}. [`FACT_CHECK.md`](FACT_CHECK.md) maps each claim to the "
           "exact wording it relies on.", "",
           "| ID | Source | Publisher | Used for |", "|----|--------|-----------|----------|"]
    for s in SOURCES:
        src.append(f"| {s['id']} | [{s['name']}]({s['url']}) | {s['publisher']} | {s['used_for']} |")
    src += ["", "## How the sources were used", "",
            "- **The independent source wins.** Project Acacia claims use only the RBA's own final report (S6), not Redbelly's description of it.",
            "- **Company figures are labelled.** Tokeniser's A$1.2B and 160+ figures are its own, so the thread says \"reports\".",
            "- **Illustrations are labelled.** The pizza, the bouncer, cash versus a cheque, and the names on image 2 are illustrations, not facts.",
            "", "## Left out on purpose", ""] + [f"- {x}" for x in LEFT_OUT] + [""]
    (ROOT / "SOURCES.md").write_text("\n".join(src), encoding="utf8")

    fc = ["# Fact check", "",
          f"Each claim the thread makes, the posts that make it, and the source wording behind it. Quotes were "
          f"copied from the sources in [`SOURCES.md`](SOURCES.md) on {LAST_VERIFIED_LONG}. \"[...]\" marks a "
          "cut where the original sentence goes on to other points. Page numbers for S6 are the printed page "
          "numbers of the report.", ""]
    for f in FACTS:
        used = [str(i) for i, p in enumerate(POSTS, 1) if f["id"] in p["facts"]]
        fc += [f"## {f['id']}: {f['label']}", "", f"**Thread says** (post{'s' if len(used) > 1 else ''} {', '.join(used)}): {f['claim']}", ""]
        for sid, q in f["evidence"]:
            fc.append(f"- **{sid}**, {source(sid)['name']}: \"{q}\"")
        if f.get("note"):
            fc += ["", f"*Note: {f['note']}*"]
        fc.append("")
    (ROOT / "FACT_CHECK.md").write_text("\n".join(fc), encoding="utf8")
    print("wrote entry/THREAD.md, SOURCES.md, FACT_CHECK.md")


# ---------------------------------------------------------------- website

ICON_COPY = '<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="5" y="5" width="9" height="9" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M3 11V3a1 1 0 0 1 1-1h7" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>'
ICON_DL = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2v8M4.5 7 8 10.5 11.5 7M3 13.5h10" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def site_post(i, p):
    num = f"{i + 1:02d}"
    refs = "".join(f'<a href="#{s.lower()}">{s}</a>' for s in post_sources(p))
    parts = [f'<article class="post" id="post-{i + 1}">',
             f'<div class="post-head"><div class="left"><span class="post-num">{num} / {N}</span>'
             f'<h3>{esc(p["title"])}</h3></div>'
             f'<span class="count"><span class="dot"></span>{fmt_count(p)}</span></div>',
             f'<div class="post-body"><p class="post-text">{esc(p["text"])}</p>']
    if p.get("image"):
        src = f"entry/images/{p['image']}"
        parts.append(f'<figure><img src="{src}" alt="{esc(p["alt"])}" width="1600" height="900" loading="lazy">'
                     f'<figcaption><span class="caps">Alt text</span>{esc(p["alt"])}</figcaption></figure>')
    parts.append('</div><div class="post-foot"><div class="btns">'
                 f'<button class="btn primary" data-copy="text" data-index="{i}">{ICON_COPY}<span class="label">Copy text</span></button>')
    if p.get("image"):
        parts.append(f'<button class="btn" data-copy="alt" data-index="{i}">{ICON_COPY}<span class="label">Copy alt text</span></button>'
                     f'<a class="btn" href="entry/images/{p["image"]}" download>{ICON_DL}<span class="label">Download PNG</span></a>')
    parts.append(f'</div><div class="refs">Sources {refs}</div></div></article>')
    return "".join(parts)


def build_site():
    toc_posts = "".join(f'<li><a href="#post-{i}"><span class="mono">{i:02d}</span>{esc(p["title"])}</a></li>'
                        for i, p in enumerate(POSTS, 1))
    posts = "\n".join(site_post(i, p) for i, p in enumerate(POSTS))
    gallery = "".join(
        f'<div class="tile"><a href="entry/images/{p["image"]}"><img src="entry/images/{p["image"]}" alt="{esc(p["alt"])}" width="1600" height="900" loading="lazy"></a>'
        f'<div class="row"><span>Post {i}: {esc(p["title"])}</span><a class="btn" href="entry/images/{p["image"]}" download>{ICON_DL}<span class="label">PNG</span></a></div></div>'
        for i, p in enumerate(POSTS, 1) if p.get("image"))
    checklist = "".join(f'<tr><td>{esc(r)}</td><td><span class="status"><span class="dot"></span>PASS</span></td>'
                        f'<td>{esc(h)}<br><span style="color:var(--muted);font-size:14px">{esc(v)}</span></td></tr>'
                        for r, h, v in CHECKLIST)
    sources = "".join(
        f'<li id="{s["id"].lower()}"><span class="sid">{s["id"]}</span><div><div class="name">{esc(s["name"])}</div>'
        f'<div class="pub">{esc(s["publisher"])}</div><a class="url" href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["url"])}</a>'
        f'<p class="use">{esc(s["used_for"])}</p></div></li>' for s in SOURCES)
    facts = []
    for f in FACTS:
        used = [i for i, p in enumerate(POSTS, 1) if f["id"] in p["facts"]]
        quotes = "".join(f'<blockquote><a href="#{sid.lower()}">{sid}</a>{esc(q)}</blockquote>' for sid, q in f["evidence"])
        note = f'<p class="note">{esc(f["note"])}</p>' if f.get("note") else ""
        posts_label = "Post" + ("s " if len(used) > 1 else " ") + ", ".join(str(u) for u in used)
        facts.append(f'<details id="{f["id"].lower()}"><summary><span class="fid">{f["id"]}</span>'
                     f'<span class="label">{esc(f["label"])}</span><span class="used">{posts_label}</span></summary>'
                     f'<div class="body"><p class="claim"><span class="caps">Thread says</span>{esc(f["claim"])}</p>{quotes}{note}</div></details>')
    data = json.dumps([{"text": p["text"], "alt": p.get("alt", "")} for p in POSTS], ensure_ascii=False)
    data = data.replace("</", "<\\/")
    left_out = "".join(f"<li>{esc(x)}</li>" for x in LEFT_OUT)

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(TITLE)}</title>
<meta name="description" content="{esc(SUBTITLE)}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#1d3140">
<link rel="icon" href="assets/brand/icon.png">
<link rel="preload" href="assets/fonts/BeVietnamPro-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/BeVietnamPro-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css">
<script>try{{var t=localStorage.getItem("rb-theme");if(t==="light"||t==="dark")document.documentElement.setAttribute("data-theme",t)}}catch(e){{}}</script>
</head>
<body>
<a class="skip" href="#thread">Skip to the thread</a>
<header class="hero">
  <div class="hero-inner">
    <div class="topbar">
      <a class="logo" href="#top" aria-label="Redbelly DAO"><img src="assets/brand/dao-logo-on-dark-112.png" alt="Redbelly DAO" width="78" height="56"></a>
      <nav aria-label="Sections">
        <a class="navlink" href="#thread">Thread</a>
        <a class="navlink" href="#images">Images</a>
        <a class="navlink" href="#sources">Sources</a>
        <a class="navlink" href="#facts">Fact check</a>
        <button class="theme-btn" id="theme-btn" type="button" aria-label="Switch to light theme" title="Switch to light theme"><svg class="i-sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8"/></svg><svg class="i-moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5z"/></svg></button>
      </nav>
    </div>
    <p class="kicker caps" id="top">Redbelly DAO Task Board, {TASK}</p>
    <h1>{esc(TITLE)}</h1>
    <p class="lead">{esc(SUBTITLE)} Every fact links to a public source.</p>
    <ul class="meta">
      <li>Last verified {LAST_VERIFIED}</li>
      <li>{N} posts</li>
      <li>{N_IMG} images</li>
      <li><span class="dot"></span>All posts within 280 characters</li>
    </ul>
    <div class="actions">
      <a class="btn primary" href="#thread">Read the thread</a>
      <a class="btn" href="entry/Redbelly_Thread.pdf">{ICON_DL}Download PDF</a>
      <a class="btn" href="entry/Redbelly_Thread.docx">{ICON_DL}Word file</a>
      <a class="btn" href="entry/redbelly-thread-images.zip">{ICON_DL}All images</a>
    </div>
  </div>
</header>

<div class="page">
  <aside class="toc" aria-label="On this page">
    <p class="caps">On this page</p>
    <ol class="toc-posts">
      <li><a href="#how"><span class="mono">00</span>How to post it</a></li>
      {toc_posts}
    </ol>
    <ol>
      <li><a href="#images"><span class="mono">IM</span>Images</a></li>
      <li><a href="#brief"><span class="mono">BR</span>Brief checklist</a></li>
      <li><a href="#sources"><span class="mono">SR</span>Sources</a></li>
      <li><a href="#facts"><span class="mono">FC</span>Fact check</a></li>
    </ol>
  </aside>

  <main class="content">
    <section id="how">
      <p class="section-kicker caps">Before you start</p>
      <h2>How to post it</h2>
      <p class="intro">Ten posts, in order, as one thread. Every post below has its own copy button, so nothing has to be retyped.</p>
      <ol class="steps">
        <li><span>Press <strong>Copy text</strong> on post 1 and paste it into a new post on X. Paste each later post as a reply to the one before it.</span></li>
        <li><span>Where a post has an image, press <strong>Download PNG</strong> and attach it to that post.</span></li>
        <li><span>On each image in X, choose <strong>Add description</strong> and paste the alt text from <strong>Copy alt text</strong>.</span></li>
      </ol>
      <button class="btn" data-copy="all">{ICON_COPY}<span class="label">Copy whole thread</span></button>
      <p class="callout"><span class="caps">Judging rule</span>Do not post this before judging ends. The DAO posts the winning entry on its own X account.</p>
    </section>

    <section id="thread">
      <p class="section-kicker caps">The entry</p>
      <h2>The thread</h2>
      <p class="intro">Written for a friend, a parent or a business owner. No jargon, no price talk, and the source behind every fact is one click away.</p>
      <div class="thread">
{posts}
      </div>
    </section>

    <section id="images">
      <p class="section-kicker caps">{N_IMG} images, 1600 x 900</p>
      <h2>Images</h2>
      <p class="intro">Drawn from scratch for this thread, in the DAO brand. Each one carries its sources and a last verified date.</p>
      <div class="gallery">{gallery}</div>
    </section>

    <section id="brief">
      <p class="section-kicker caps">For the reviewer</p>
      <h2>Brief checklist</h2>
      <p class="intro">Each failure condition in the brief, and how this entry avoids it.</p>
      <div class="table-wrap"><table>
        <thead><tr><th>Rule</th><th>Status</th><th>How</th></tr></thead>
        <tbody>{checklist}</tbody>
      </table></div>
    </section>

    <section id="sources">
      <p class="section-kicker caps">Deliverable 2</p>
      <h2>Sources</h2>
      <p class="intro">Every fact in the thread comes from one of these public sources, checked on {LAST_VERIFIED_LONG}.</p>
      <ol class="sources">{sources}</ol>
    </section>

    <section id="facts">
      <p class="section-kicker caps">Verification</p>
      <h2>Fact check</h2>
      <p class="intro">Each claim the thread makes, with the exact source wording behind it. Open any row to see the quotes.</p>
      <div class="facts">{"".join(facts)}</div>
      <p class="intro" style="margin:28px 0 0">Left out on purpose:</p>
      <ul class="left-out">{left_out}</ul>
    </section>
  </main>
</div>

<footer class="foot">
  <div class="foot-inner">
    <img class="logo-dark" src="assets/brand/dao-logo-on-dark-112.png" alt="Redbelly DAO" width="56" height="40">
    <img class="logo-light" src="assets/brand/dao-logo-on-light-112.png" alt="Redbelly DAO" width="56" height="40">
    <span>Redbelly DAO Task Board, {TASK}. Facts last verified {LAST_VERIFIED_LONG}.</span>
  </div>
</footer>
<a class="to-top" id="to-top" href="#top" aria-label="Back to top" title="Back to top"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M5.5 11.5 12 5l6.5 6.5"/></svg></a>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script type="application/json" id="thread-data">{data}</script>
<script src="assets/site.js"></script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(page, encoding="utf8")
    print("wrote index.html")


# ---------------------------------------------------------------- PDF

def build_pdf():
    from render import browser, wait_for_fonts
    print_html = TEMPLATES / "print.html"
    posts = []
    for i, p in enumerate(POSTS, 1):
        img = ""
        if p.get("image"):
            img = (f'<img src="../../entry/images/{p["image"]}" alt="">'
                   f'<p class="alt"><span class="caps">Alt text</span>{esc(p["alt"])}</p>')
        posts.append(
            f'<article class="post"><div class="ph"><span class="num">{i:02d} / {N}</span><h3>{esc(p["title"])}</h3>'
            f'<span class="cnt">{fmt_count(p)}</span></div><p class="text">{esc(p["text"])}</p>{img}'
            f'<p class="refs">Sources: {", ".join(post_sources(p))}</p></article>')
    checklist = "".join(f'<tr><td>{esc(r)}</td><td><span class="ok">PASS</span></td><td>{esc(h)}</td></tr>' for r, h, _ in CHECKLIST)
    glance = "".join(f'<tr><td class="n">{i:02d}</td><td>{esc(p["title"])}</td><td class="i">{"Image " + p["image"][:2] if p.get("image") else ""}</td>'
                     f'<td class="c">{fmt_count(p)}</td></tr>' for i, p in enumerate(POSTS, 1))
    sources = "".join(f'<tr><td class="sid">{s["id"]}</td><td><b>{esc(s["name"])}</b><br>{esc(s["publisher"])}<br>'
                      f'<span class="url">{esc(s["url"])}</span><br><span class="use">{esc(s["used_for"])}</span></td></tr>'
                      for s in SOURCES)
    facts = []
    for f in FACTS:
        used = ", ".join(str(i) for i, p in enumerate(POSTS, 1) if f["id"] in p["facts"])
        q = "".join(f'<blockquote><span class="sid">{sid}</span> {esc(t)}</blockquote>' for sid, t in f["evidence"])
        note = f'<p class="note">{esc(f["note"])}</p>' if f.get("note") else ""
        facts.append(f'<div class="fact"><h4><span class="sid">{f["id"]}</span> {esc(f["label"])} <span class="used">Post {used}</span></h4>'
                     f'<p class="claim">{esc(f["claim"])}</p>{q}{note}</div>')
    doc = f"""<!doctype html>
<!-- Generated by tools/build.py for the PDF. Edit tools/content.py, not this file. -->
<html lang="en"><head><meta charset="utf-8"><title>{esc(TITLE)}</title>
<style>
@font-face {{ font-family: "Be Vietnam Pro"; font-weight: 400; src: url("../../assets/fonts/BeVietnamPro-400.woff2"); }}
@font-face {{ font-family: "Be Vietnam Pro"; font-weight: 600; src: url("../../assets/fonts/BeVietnamPro-600.woff2"); }}
@font-face {{ font-family: "Be Vietnam Pro"; font-weight: 700; src: url("../../assets/fonts/BeVietnamPro-700.woff2"); }}
@font-face {{ font-family: "JetBrains Mono"; font-weight: 100 800; src: url("../../assets/fonts/JetBrainsMono-var.woff2"); }}
@page {{ size: A4; margin: 16mm 16mm 18mm; }}
@page :first {{ margin: 0; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font: 400 10pt/1.5 "Be Vietnam Pro", sans-serif; color: #0F1A22; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.mono, .num, .cnt, .refs, .sid, .used, .url, .meta, .ok {{ font-family: "JetBrains Mono", monospace; font-variant-ligatures: none; }}
.caps {{ font-size: 7.5pt; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; }}
.cover-page {{ height: 296mm; break-after: page; display: flex; flex-direction: column; }}
.cover {{ background: #1d3140; color: #f1f5f8; padding: 18mm 18mm 14mm; }}
.cover-body {{ padding: 10mm 18mm 0; flex: 1; display: flex; flex-direction: column; }}
.glance {{ margin: 0 0 7mm; }}
.glance td {{ padding: 1.8mm 3mm; font-size: 9.5pt; }}
.glance td.n {{ font-family: "JetBrains Mono", monospace; color: #B3272A; font-weight: 600; width: 12mm; }}
.glance td.c {{ font-family: "JetBrains Mono", monospace; color: #596975; font-size: 8pt; text-align: right; white-space: nowrap; font-weight: 400; }}
.glance td.i {{ font-family: "JetBrains Mono", monospace; color: #596975; font-size: 8pt; white-space: nowrap; font-weight: 400; width: 22mm; }}
.cover-foot {{ margin-top: auto; padding: 0 0 10mm; font-family: "JetBrains Mono", monospace; font-size: 7pt; letter-spacing: 0.08em; text-transform: uppercase; color: #596975; display: flex; justify-content: space-between; border-top: 1px solid #DAE1E7; padding-top: 3mm; }}
.cover img {{ height: 18mm; display: block; margin-bottom: 12mm; }}
.cover .k {{ color: #8fa1ad; margin: 0 0 3mm; }}
.cover h1 {{ font-size: 34pt; line-height: 1.1; letter-spacing: -0.02em; margin: 0 0 3mm; }}
.cover p.lead {{ font-size: 12pt; color: #c2ced6; margin: 0 0 5mm; max-width: 150mm; }}
.cover .meta {{ font-size: 8pt; color: #c2ced6; letter-spacing: 0.05em; text-transform: uppercase; }}
.cover .meta span {{ margin-right: 6mm; }}
.cover .meta .d {{ display: inline-block; width: 6px; height: 6px; border-radius: 9999px; background: #86EFAC; margin-right: 2mm; vertical-align: 1px; }}
h2 {{ font-size: 17pt; font-weight: 600; letter-spacing: -0.01em; margin: 0 0 2mm; }}
.kick {{ color: #B3272A; margin: 0 0 1.5mm; }}
.intro {{ color: #394853; margin: 0 0 5mm; }}
.how {{ border-left: 3px solid #EF5350; background: #F4F6F8; padding: 3mm 4mm; margin: 0 0 8mm; color: #394853; }}
.how b {{ color: #0F1A22; }}
.post {{ border: 1px solid #D3DBE1; border-radius: 6px; padding: 4mm 5mm; margin: 0 0 5mm; break-inside: avoid; background: #fff; }}
.ph {{ display: flex; align-items: baseline; gap: 4mm; border-bottom: 1px solid #DAE1E7; padding-bottom: 2.5mm; margin-bottom: 3mm; }}
.ph .num {{ color: #B3272A; font-weight: 600; font-size: 9pt; }}
.ph h3 {{ font-size: 11pt; margin: 0; flex: 1; }}
.ph .cnt {{ color: #596975; font-size: 8pt; }}
.text {{ white-space: pre-wrap; font-size: 10.5pt; line-height: 1.5; margin: 0 0 2.5mm; }}
.post img {{ width: 150mm; border-radius: 4px; display: block; margin: 1mm auto 2mm; }}
.alt {{ color: #596975; font-size: 8.5pt; margin: 0 0 2mm; }}
.alt .caps {{ color: #394853; margin-right: 2mm; }}
.refs {{ color: #596975; font-size: 7.5pt; margin: 0; }}
section {{ margin-top: 9mm; }}
.br {{ break-before: page; }}
table {{ width: 100%; border-collapse: collapse; font-size: 9pt; }}
th {{ text-align: left; font-size: 7pt; letter-spacing: 0.1em; text-transform: uppercase; color: #596975; background: #F4F6F8; padding: 2mm 3mm; border-bottom: 1px solid #D3DBE1; }}
td {{ padding: 2.5mm 3mm; border-bottom: 1px solid #DAE1E7; vertical-align: top; color: #394853; }}
td:first-child {{ color: #0F1A22; font-weight: 600; }}
tr {{ break-inside: avoid; }}
.ok {{ color: #15803D; font-weight: 600; font-size: 8pt; }}
.ok::before {{ content: ""; display: inline-block; width: 6px; height: 6px; border-radius: 9999px; background: #15803D; margin-right: 2mm; vertical-align: 1px; }}
.sid {{ color: #B3272A; font-weight: 600; }}
td.sid {{ width: 12mm; }}
.url {{ font-size: 7.5pt; color: #B3272A; word-break: break-all; }}
.use {{ color: #394853; }}
.fact {{ border-top: 1px solid #DAE1E7; padding: 3mm 0; break-inside: avoid; }}
.fact h4 {{ font-size: 10.5pt; margin: 0 0 1.5mm; display: flex; gap: 3mm; align-items: baseline; }}
.fact .used {{ margin-left: auto; color: #596975; font-size: 7.5pt; font-weight: 500; }}
.claim {{ margin: 0 0 2mm; }}
blockquote {{ margin: 0 0 1.5mm; padding: 1.5mm 3mm; border-left: 2px solid #C3CDD4; background: #F4F6F8; color: #394853; font-size: 9pt; }}
blockquote .sid {{ font-size: 7.5pt; margin-right: 1mm; }}
.note {{ color: #596975; font-size: 8.5pt; margin: 1.5mm 0 0; }}
</style></head><body>
<div class="cover-page">
<div class="cover">
  <img src="../../assets/brand/dao-logo-on-dark.png" alt="Redbelly DAO">
  <p class="k caps">Redbelly DAO Task Board, {TASK}</p>
  <h1>{esc(TITLE)}</h1>
  <p class="lead">{esc(SUBTITLE)}</p>
  <div class="meta"><span>Last verified {LAST_VERIFIED}</span><span>{N} posts</span><span>{N_IMG} images</span><span><i class="d"></i>All within 280 characters</span></div>
</div>
<div class="cover-body">
  <p class="kick caps">At a glance</p>
  <h2>The thread in {N} posts</h2>
  <table class="glance"><tbody>{glance}</tbody></table>
  <div class="how"><b>How to post it.</b> Post the {N} posts in order as one thread on X. Attach each image to the post it sits under, and paste its alt text into the image description. Do not post before judging ends: the DAO posts the winning entry.</div>
  <p class="intro"><b>In this document:</b> the thread (page 2), the brief checklist, the sources (deliverable 2) and a sentence-by-sentence fact check.</p>
  <div class="cover-foot"><span>{esc(TITLE)}</span><span>{TASK}</span><span>Last verified {LAST_VERIFIED}</span></div>
</div>
</div>
<p class="kick caps">The entry</p>
<h2>The thread</h2>
<p class="intro">Written for a friend, a parent or a business owner. Source IDs under each post point to the source list at the end.</p>
{"".join(posts)}
<section class="br">
<p class="kick caps">For the reviewer</p>
<h2>Brief checklist</h2>
<p class="intro">Each failure condition in the brief, and how this entry avoids it.</p>
<table><thead><tr><th>Rule</th><th>Status</th><th>How</th></tr></thead><tbody>{checklist}</tbody></table>
</section>
<section>
<p class="kick caps">Deliverable 2</p>
<h2>Sources</h2>
<p class="intro">Every fact in the thread comes from one of these public sources, checked on {LAST_VERIFIED_LONG}.</p>
<table><tbody>{sources}</tbody></table>
</section>
<section class="br">
<p class="kick caps">Verification</p>
<h2>Fact check</h2>
<p class="intro">Each claim the thread makes, with the exact source wording behind it. "[...]" marks a cut. S6 page numbers are the report's printed pages.</p>
{"".join(facts)}
<p class="intro" style="margin-top:4mm"><b>Left out on purpose:</b> {" ".join(esc(x) for x in LEFT_OUT)}</p>
</section>
</body></html>
"""
    print_html.write_text(doc, encoding="utf8")

    mono = base64.b64encode((ASSETS / "fonts" / "JetBrainsMono-var.woff2").read_bytes()).decode()
    footer = (
        f'<div style="width:100%;padding:0 16mm;font-size:7px;letter-spacing:0.08em;text-transform:uppercase;'
        f'color:#596975;display:flex;justify-content:space-between;font-family:\'JBM\',monospace">'
        f'<style>@font-face{{font-family:"JBM";src:url(data:font/woff2;base64,{mono})}}</style>'
        f'<span>{esc(TITLE)}</span><span>{TASK}</span><span>Last verified {LAST_VERIFIED}</span>'
        f'<span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>')
    out = ENTRY / "Redbelly_Thread.pdf"
    with browser() as b:
        page = b.new_page()
        page.goto(print_html.as_uri())
        wait_for_fonts(page)
        page.wait_for_load_state("networkidle")
        page.pdf(path=str(out), format="A4", print_background=True, prefer_css_page_size=True,
                 display_header_footer=True, header_template="<span></span>", footer_template=footer)
    print("wrote", out.relative_to(ROOT))


if __name__ == "__main__":
    build_web_logos()
    build_images()
    build_zip()
    build_markdown()
    build_site()
    build_pdf()
    import build_docx
    build_docx.build()
