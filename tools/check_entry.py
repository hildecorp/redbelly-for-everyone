"""Automated checks for the entry. Run from the repo root: python3 tools/check_entry.py

 1. Self-test: the detectors catch planted bad text before a clean result is trusted.
 2. Banned word and stand-ins: every file in the repo, the PDF and Word text, file names.
 3. DAO brand voice: no em dashes or en dashes in any file, no emoji in the entry.
 4. Price talk, investment advice and personal credit: posts, alt text, image text.
 5. Thread shape: 5 to 10 posts, each within 280 characters as X counts them.
 6. Images: every referenced image exists, is a 1600x900 PNG and has alt text.
 7. Facts: every fact a post cites exists, every quote names a real source, and
    every source except background reading backs at least one fact.
 8. Website: every local link and image in index.html points to a real file.
 9. Dates: every image carries the same "last verified" date as the content.

The banned terms are stored ROT13-encoded so that this file does not contain them
and the repo-wide scan can stay strict with no exceptions.
"""

import codecs
import html as htmllib
import re
import struct
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from content import FACTS, LAST_VERIFIED, POSTS, SOURCES  # noqa: E402
from xlength import x_length  # noqa: E402

# ROT13-encoded terms (letters only; a space matches any run of spaces or hyphens).
# Decoded, they cover the forbidden word in every spelling (and any word built on
# its second half), the record-book family and its three-letter acronym, and the
# words that usually stand in for them. True = match whole words only.
# Checked in every file of the repo.
BANNED_ROT13 = [
    ("punva", False), ("yrqtre", False), ("qyg", True), ("pelcgb", False),
    ("jro 3", False), ("qrpragenyvfrq", False), ("qrpragenyvmrq", False),
    ("ynlre 1", True), ("ynlre bar", True), ("y1", True),
]
# Technical jargon kept out of the posts, alt text and images (not stand-ins, just
# words an everyday reader would trip on). The fact check may quote them.
JARGON = [r"\bsmart contracts?\b", r"\bmainnet\b", r"\bdapps?\b", r"\bnodes?\b", r"\bconsensus\b",
          r"\bwallets?\b", r"\bgas\b"]


def _rx(encoded, word):
    body = r"[\s-]*".join(re.escape(w) for w in codecs.decode(encoded, "rot13").split(" "))
    return re.compile(rf"\b{body}\b" if word else body, re.I)


BANNED = [(codecs.decode(t, "rot13"), _rx(t, w)) for t, w in BANNED_ROT13]

PRICE_TALK = [
    r"\bprice", r"\breturns?\b", r"\bprofit", r"\bmoon", r"\bpump", r"\byield",
    r"\bapy\b", r"\bapr\b", r"\bgains?\b", r"\bbuy now\b", r"\binvestment advice\b",
    r"\bguarantee", r"\brbnt\b", r"\bairdrop", r"\b10x\b", r"\bnot financial advice\b", r"\bcoin\b",
]
CREDIT = [r"@\w", r"made by", r"created by", r"designed by", r"written by", r"\bby me\b", "©"]
DASHES = re.compile("[\u2013\u2014]")
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️]")

TEXT_SUFFIXES = {".md", ".py", ".txt", ".sh", ".json", ".yml", ".yaml", ".csv", ".html", ".css", ".js"}
SKIP_PARTS = {".git", "__pycache__", "node_modules"}
LICENCE_FILES = {"OFL-BeVietnamPro.txt", "OFL-JetBrainsMono.txt"}


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        parts = [z.read(n).decode("utf8") for n in z.namelist()
                 if n.endswith(".xml") and (n.startswith("word/") or n.startswith("docProps/"))]
    return re.sub(r"<[^>]+>", " ", " ".join(parts))


def pdf_text(path):
    try:
        out = subprocess.run(["pdftotext", str(path), "-"], capture_output=True, text=True, check=True).stdout
        info = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True).stdout
        return out + "\n" + info
    except (OSError, subprocess.CalledProcessError):
        return None


def repo_files():
    for p in sorted(ROOT.rglob("*")):
        if p.is_file() and not any(part in SKIP_PARTS for part in p.relative_to(ROOT).parts):
            yield p


def image_text():
    """Visible text of the image template, tags and styles removed."""
    t = (ROOT / "tools" / "templates" / "images.html").read_text(encoding="utf8")
    t = re.sub(r"(?s)<(style|script)[^>]*>.*?</\1>|<!--.*?-->", " ", t)
    return htmllib.unescape(re.sub(r"<[^>]+>", " ", t))


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", head[16:24])


def self_test():
    bad = [codecs.decode(w, "rot13") for w in
           ("oybpxpunva", "Oybpx Punva", "oybpx-punva", "qvfgevohgrq yrqtre", "QYG",
            "ba-punva", "bapunva", "pelcgb", "Jro3", "ynlre-1")]
    for w in bad:
        assert any(rx.search(f"text with {w} inside") for _, rx in BANNED), w
    for ok in ("Redbelly", "tokenisation", "collateral", "a public digital network", "Australia's"):
        assert not any(rx.search(ok) for _, rx in BANNED), ok
    assert any(re.search(p, "the price will go up", re.I) for p in PRICE_TALK)
    assert any(re.search(p, "thread by @someone", re.I) for p in CREDIT)
    assert any(re.search(p, "connect your wallet", re.I) for p in JARGON)
    assert DASHES.search("a \u2014 b") and DASHES.search("3\u20135") and not DASHES.search("3-5")
    assert EMOJI.search("thread \U0001F447") and not EMOJI.search("plain text")
    assert x_length("a" * 280) == 280 and x_length("\U0001F355") == 2
    assert x_length("see https://example.com/a/very/long/path/indeed") == 4 + 23


def main():
    errors, passes = [], []
    self_test()
    passes.append("self-test: detectors catch planted banned words, dashes, emoji, price talk and handles")

    # 2 + 3. Whole repo.
    scanned = 0
    for p in repo_files():
        rel = p.relative_to(ROOT)
        if p.name in LICENCE_FILES:
            continue
        if p.suffix in TEXT_SUFFIXES:
            text = p.read_text(encoding="utf8")
        elif p.suffix == ".docx":
            text = docx_text(p)
        elif p.suffix == ".pdf":
            text = pdf_text(p)
            if text is None:
                errors.append(f"could not read {rel} (install poppler-utils)")
                continue
        else:
            text = ""
        scanned += 1
        for label, rx in BANNED:
            for m in rx.finditer(f"{text}\n{rel}"):
                errors.append(f"banned term in {rel}: {m.group(0)!r}")
        for m in DASHES.finditer(text):
            errors.append(f"em or en dash in {rel}: ...{text[max(0, m.start() - 20): m.end() + 20]!r}...")
    passes.append(f"banned-term and dash scan: {scanned} files, including the PDF, the Word file and file names")

    # 3 + 4. The entry itself.
    entry = [p["text"] for p in POSTS] + [p.get("alt", "") for p in POSTS] + [image_text()]
    for t in entry:
        if EMOJI.search(t):
            errors.append(f"emoji in entry text: {t[:60]!r}")
        for pat in PRICE_TALK:
            if re.search(pat, t, re.I):
                errors.append(f"price or advice wording {pat!r} in: {t[:60]!r}")
        for pat in CREDIT:
            if re.search(pat, t, re.I):
                errors.append(f"personal credit {pat!r} in: {t[:60]!r}")
        for pat in JARGON:
            if re.search(pat, t, re.I):
                errors.append(f"jargon {pat!r} in entry text: {t[:60]!r}")
    passes.append("posts, alt text and image text: no emoji, jargon, price talk, advice or credit")

    # 5. Thread shape.
    if not 5 <= len(POSTS) <= 10:
        errors.append(f"thread has {len(POSTS)} posts; the brief asks for 5 to 10")
    for i, p in enumerate(POSTS, 1):
        if x_length(p["text"]) > 280:
            errors.append(f"post {i} is {x_length(p['text'])} characters (limit 280)")
    passes.append("post lengths: " + ", ".join(f"{i}:{x_length(p['text'])}" for i, p in enumerate(POSTS, 1)))

    # 6. Images.
    for i, p in enumerate(POSTS, 1):
        if not p.get("image"):
            continue
        path = ROOT / "entry" / "images" / p["image"]
        if not path.exists():
            errors.append(f"post {i}: image missing: {p['image']}")
        elif png_size(path) != (1600, 900):
            errors.append(f"post {i}: {p['image']} is {png_size(path)}, expected 1600x900 PNG")
        if not p.get("alt"):
            errors.append(f"post {i}: image has no alt text")
    passes.append(f"{sum(1 for p in POSTS if p.get('image'))} images present, 1600x900 PNG, each with alt text")

    # 7. Facts and sources.
    fact_ids = {f["id"] for f in FACTS}
    source_ids = {s["id"] for s in SOURCES}
    used_sources = set()
    for i, p in enumerate(POSTS, 1):
        for fid in p["facts"]:
            if fid not in fact_ids:
                errors.append(f"post {i} cites {fid}, which is not in the fact check")
    for f in FACTS:
        if not any(f["id"] in p["facts"] for p in POSTS):
            errors.append(f"{f['id']} is not used by any post")
        for sid, _ in f["evidence"]:
            if sid not in source_ids:
                errors.append(f"{f['id']} quotes {sid}, which is not in the source list")
            used_sources.add(sid)
    for s in SOURCES:
        if s["id"] not in used_sources and not s["used_for"].startswith("Background"):
            errors.append(f"{s['id']} backs no fact")
    fc = (ROOT / "FACT_CHECK.md").read_text(encoding="utf8")
    for f in FACTS:
        if f"## {f['id']}:" not in fc:
            errors.append(f"FACT_CHECK.md is out of date: no section for {f['id']} (run tools/build.py)")
    passes.append(f"{len(FACTS)} facts, {len(SOURCES)} sources, every link between them resolves")

    # 8. Website links.
    site = (ROOT / "index.html").read_text(encoding="utf8")
    links = set(re.findall(r'(?:href|src)="([^"#][^"]*)"', site))
    local = [u for u in links if not re.match(r"[a-z]+:", u)]
    for u in local:
        if not (ROOT / u.split("?")[0]).exists():
            errors.append(f"index.html links to a missing file: {u}")
    for anchor in set(re.findall(r'href="#([^"]+)"', site)):
        if f'id="{anchor}"' not in site:
            errors.append(f"index.html links to a missing section: #{anchor}")
    for i, p in enumerate(POSTS):
        if htmllib.escape(p["text"], quote=True) not in site:
            errors.append(f"index.html is out of date for post {i + 1} (run tools/build.py)")
    passes.append(f"website: {len(local)} local links and every in-page anchor resolve, posts match the content")

    # 9. Dates on images.
    tpl = (ROOT / "tools" / "templates" / "images.html").read_text(encoding="utf8")
    frames = tpl.count('class="frame ')
    if tpl.count(f"Last verified {LAST_VERIFIED}") != frames:
        errors.append(f"not every image says 'Last verified {LAST_VERIFIED}'")
    passes.append(f"all {frames} images carry 'Last verified {LAST_VERIFIED}'")

    for p in passes:
        print("PASS", p)
    for e in errors:
        print("FAIL", e)
    print(f"\n{'ALL CHECKS PASSED' if not errors else f'{len(errors)} PROBLEM(S)'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
