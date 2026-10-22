"""Builds the submission documents from tools/thread_content.py.

Run: python3 tools/build_docs.py
Output:
  entry/THREAD.md                     plain-text thread, ready to copy into X
  entry/Redbelly_Thread.docx          the same thread as a document, images inline
  entry/Redbelly_Thread.pdf           PDF of the .docx (needs LibreOffice; skipped if absent)
  index.html                          the thread as a web page: copy buttons, image downloads
"""

import html
import json
import shutil
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from check_entry import x_length  # noqa: E402
from thread_content import POSTS, TITLE  # noqa: E402

ENTRY = ROOT / "entry"
IMAGES = ENTRY / "images"
RED = RGBColor(0xFF, 0x50, 0x50)
SLATE = RGBColor(0x28, 0x3A, 0x46)
GREY = RGBColor(0x84, 0x8B, 0x91)

INTRO = (
    "Format: X thread, {n} posts, {k} original images. Each post is under X's "
    "280-character limit. Post them in order as one thread, attach each image to the post "
    "marked below, and paste the alt text into the image description."
)

SOURCES_SHORT = [
    ("Redbelly Network home page", "https://redbelly.network"),
    ("Redbelly About us and timeline", "https://redbelly.network/about-us"),
    ("Redbelly asset tokenisation page", "https://redbelly.network/asset-tokenisation"),
    ("Redbelly article: What sets Redbelly Network apart",
     "https://redbelly.network/blog/what-sets-redbelly-network-apart"),
    ("Redbelly Project Acacia page", "https://redbelly.network/projectacacia"),
    ("RBA and DFCRC, Project Acacia final report, May 2026",
     "https://www.rba.gov.au/payments-and-infrastructure/central-bank-digital-currency/pdf/project-acacia-final-report.pdf"),
    ("RBA media release, 18 May 2026", "https://www.rba.gov.au/media-releases/2026/mr-26-13.html"),
    ("Tokeniser home page", "https://tokeniser.com"),
]


def build_markdown():
    n_img = sum(1 for p in POSTS if p.get("image"))
    out = [f"# {TITLE}", "", INTRO.format(n=len(POSTS), k=n_img), ""]
    for i, p in enumerate(POSTS, 1):
        out += [f"## {i}/{len(POSTS)}", "", "```text", p["text"], "```", ""]
        meta = f"*{x_length(p['text'])} / 280 characters*"
        if p.get("image"):
            out += [f"![Image for post {i}](images/{p['image']})", "",
                    f"**Attach:** `images/{p['image']}`  ", f"**Alt text:** {p['alt']}  "]
        out += [meta, ""]
    out += ["---", "", "## Sources", ""]
    out += [f"- {name}: {url}" for name, url in SOURCES_SHORT]
    out += ["", "Sentence-by-sentence source mapping: `FACT_CHECK.md`. Full source notes: `SOURCES.md`.", ""]
    (ENTRY / "THREAD.md").write_text("\n".join(out), encoding="utf8")
    print("wrote entry/THREAD.md")


def build_docx():
    doc = Document()
    doc.core_properties.author = ""
    doc.core_properties.last_modified_by = ""
    doc.core_properties.title = TITLE
    for s in doc.sections:
        s.left_margin = s.right_margin = Cm(2.2)
        s.top_margin = s.bottom_margin = Cm(2)
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(11)

    h = doc.add_paragraph()
    r = h.add_run(TITLE)
    r.bold, r.font.size, r.font.color.rgb = True, Pt(22), SLATE
    n_img = sum(1 for p in POSTS if p.get("image"))
    intro = doc.add_paragraph(INTRO.format(n=len(POSTS), k=n_img))
    intro.runs[0].font.color.rgb = GREY

    for i, p in enumerate(POSTS, 1):
        hp = doc.add_paragraph()
        hp.paragraph_format.space_before = Pt(14)
        hr = hp.add_run(f"{i}/{len(POSTS)}")
        hr.bold, hr.font.size, hr.font.color.rgb = True, Pt(14), RED
        for para in p["text"].split("\n\n"):
            bp = doc.add_paragraph(para)
            bp.paragraph_format.space_after = Pt(4)
        if p.get("image"):
            doc.add_picture(str(IMAGES / p["image"]), width=Cm(15.5))
            doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            ap = doc.add_paragraph()
            a1 = ap.add_run("Attach: ")
            a1.bold = True
            ap.add_run(f"images/{p['image']}")
            ap2 = doc.add_paragraph()
            a2 = ap2.add_run("Alt text: ")
            a2.bold = True
            ap2.add_run(p["alt"])
        cp = doc.add_paragraph(f"{x_length(p['text'])} / 280 characters")
        cp.runs[0].font.size, cp.runs[0].font.color.rgb = Pt(9), GREY

    doc.add_page_break()
    sh = doc.add_paragraph()
    sr = sh.add_run("Sources")
    sr.bold, sr.font.size, sr.font.color.rgb = True, Pt(16), SLATE
    for name, url in SOURCES_SHORT:
        doc.add_paragraph(f"{name}: {url}", style="List Bullet")
    doc.add_paragraph(
        "Sentence-by-sentence source mapping is in FACT_CHECK.md; full notes in SOURCES.md. "
        "All images were drawn from scratch for this entry (no stock art, logos or AI images). "
        "Font: Readex Pro, SIL Open Font License.")
    path = ENTRY / "Redbelly_Thread.docx"
    doc.save(path)
    print("wrote", path.relative_to(ROOT))
    return path


def build_pdf(docx_path):
    office = shutil.which("soffice") or shutil.which("libreoffice")
    if not office:
        print("LibreOffice not found; skipped PDF")
        return
    subprocess.run([office, "--headless", "--convert-to", "pdf", "--outdir", str(ENTRY),
                    str(docx_path)], check=True, capture_output=True)
    print("wrote entry/Redbelly_Thread.pdf")


KIT_CSS = """
:root{--bg:#0f1c25;--card:#1b2b36;--line:#2c3e4b;--text:#ecebec;--muted:#9aa3a9;
--red:#ff5050;--green:#3dd68c;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);
font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:720px;margin:0 auto;padding:32px 16px 64px}
h1{font-size:28px;line-height:1.2;margin:0 0 8px}
.lead{color:var(--muted);margin:0 0 28px}
ol.steps{color:var(--muted);margin:0 0 28px;padding-left:20px}
article{background:var(--card);border:1px solid var(--line);border-radius:16px;
padding:20px;margin:0 0 18px}
header{display:flex;justify-content:space-between;align-items:center;gap:12px;
margin-bottom:12px}
.num{color:var(--red);font-weight:700;font-size:18px}
.count{color:var(--muted);font-size:13px;font-variant-numeric:tabular-nums}
.text{white-space:pre-wrap;margin:0 0 14px;font-size:17px}
img{width:100%;height:auto;border-radius:12px;display:block;margin:0 0 10px}
.alt{color:var(--muted);font-size:14px;margin:0 0 14px}
.btns{display:flex;flex-wrap:wrap;gap:10px}
button,a.btn{font:inherit;font-size:15px;font-weight:600;cursor:pointer;
border-radius:999px;padding:9px 16px;border:1px solid var(--line);
background:#24384a;color:var(--text);text-decoration:none}
button.primary{background:var(--red);border-color:var(--red);color:#fff}
button.done{background:var(--green);border-color:var(--green);color:#0f1c25}
.how{background:var(--card);border:1px solid var(--line);border-radius:16px;
padding:14px 20px;margin:0 0 22px;color:var(--muted)}
.how summary{cursor:pointer;color:var(--text);font-weight:600}
.sources{margin-top:36px;color:var(--muted)}
.sources h2{color:var(--text);font-size:20px}
.sources a{color:var(--text)}
.sources li{margin:4px 0;overflow-wrap:anywhere}
"""

KIT_JS = """
function copyText(btn, text){
  const done = () => { const o = btn.textContent; btn.textContent = 'Copied';
    btn.classList.add('done'); setTimeout(() => { btn.textContent = o;
    btn.classList.remove('done'); }, 1500); };
  if (navigator.clipboard && window.isSecureContext !== false) {
    navigator.clipboard.writeText(text).then(done, () => fallback(text, done));
  } else { fallback(text, done); }
}
function fallback(text, done){
  const t = document.createElement('textarea'); t.value = text;
  t.style.position = 'fixed'; t.style.opacity = '0'; document.body.appendChild(t);
  t.select(); try { document.execCommand('copy'); done(); } catch (e) {}
  t.remove();
}
document.querySelectorAll('[data-copy]').forEach(b =>
  b.addEventListener('click', () => copyText(b, POSTS[+b.dataset.copy][b.dataset.field])));
"""


def build_site():
    """index.html at the repo root: works opened from disk or as a static site."""
    n = len(POSTS)
    cards = []
    for i, p in enumerate(POSTS):
        parts = [
            f'<article id="post-{i + 1}"><header><span class="num">{i + 1}/{n}</span>'
            f'<span class="count">{x_length(p["text"])} / 280</span></header>',
            f'<p class="text">{html.escape(p["text"])}</p>',
        ]
        btns = [f'<button class="primary" data-copy="{i}" data-field="text">Copy text</button>']
        if p.get("image"):
            src = f"entry/images/{p['image']}"
            alt = html.escape(p["alt"])
            parts.append(f'<img src="{src}" alt="{alt}" width="1600" height="900" loading="lazy">')
            parts.append(f'<p class="alt"><strong>Alt text:</strong> {alt}</p>')
            btns.append(f'<a class="btn" href="{src}" download>Download image</a>')
            btns.append(f'<button data-copy="{i}" data-field="alt">Copy alt text</button>')
        parts.append(f'<div class="btns">{"".join(btns)}</div></article>')
        cards.append("".join(parts))
    sources = "".join(f'<li><a href="{html.escape(u)}" target="_blank" rel="noopener">'
                      f'{html.escape(name)}</a></li>' for name, u in SOURCES_SHORT)
    data = json.dumps([{"text": p["text"], "alt": p.get("alt", "")} for p in POSTS])
    n_img = sum(1 for p in POSTS if p.get("image"))
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>Redbelly in Plain English</title>
<meta name="description" content="A {n}-post X thread explaining Redbelly in everyday language.">
<style>{KIT_CSS}</style></head>
<body><main>
<h1>{html.escape(TITLE)}</h1>
<p class="lead">{n} posts, {n_img} images. Every fact is sourced below.</p>
<details class="how"><summary>How to post this thread on X</summary>
<ol>
<li>Press <strong>Copy text</strong> and paste it into a new post (post 1) or a reply to the previous post (posts 2-{n}).</li>
<li>Where a post has an image, press <strong>Download image</strong> and attach it to that post.</li>
<li>On the image in X, choose <strong>Add description</strong> and paste the alt text.</li>
</ol></details>
{"".join(cards)}
<section class="sources"><h2>Sources</h2><ol>{sources}</ol>
<p>Sentence-by-sentence mapping: <a href="FACT_CHECK.md">FACT_CHECK.md</a>.
Document versions: <a href="entry/Redbelly_Thread.pdf">PDF</a>,
<a href="entry/Redbelly_Thread.docx">Word</a>, <a href="entry/THREAD.md">Markdown</a>.</p></section>
</main><script>const POSTS={data};{KIT_JS}</script></body></html>
"""
    (ROOT / "index.html").write_text(page, encoding="utf8")
    print("wrote index.html")


if __name__ == "__main__":
    build_markdown()
    build_site()
    build_pdf(build_docx())
