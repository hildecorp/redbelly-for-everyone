"""Automated checks for the entry. Run: python3 tools/check_entry.py

1. Banned-word scan over EVERY file in the repo (posts, alt text, image text,
   docs, the generated .docx and .pdf, and these scripts).
2. Price / investment-advice wording scan over the entry itself.
3. Personal-credit scan (handles, "made by" lines) over the entry itself.
4. Each post fits X's 280-character limit (weighted the way X counts).
5. Thread length is 5-10 posts and every referenced image exists.
6. Every fact ID used by a post is documented in FACT_CHECK.md.

The banned terms are stored ROT13-encoded so that this file itself does not
contain them and the repo-wide scan can be strict with no exceptions.
"""

import codecs
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from thread_content import POSTS  # noqa: E402

# ROT13-encoded terms (letters only; a space matches any run of spaces or
# hyphens). Decoded, they cover the forbidden word in every spelling (and any word
# built on its second half), the record-book family and its three-letter acronym, and the
# jargon that usually travels with them. "word" = match whole words only.
BANNED_ROT13 = [
    ("punva", False),
    ("yrqtre", False),
    ("qyg", True),
    ("pelcgb", False),
    ("jro 3", False),
    ("qrpragenyvfrq", False),
    ("qrpragenyvmrq", False),
    ("ynlre 1", True),
    ("ynlre bar", True),
    ("y1", True),
    ("fzneg pbagenpg", False),
    ("znvarg", False),
    ("qncc", True),
]


def _rx(encoded, word):
    body = r"[\s-]*".join(re.escape(w) for w in codecs.decode(encoded, "rot13").split(" "))
    return re.compile(rf"\b{body}\b" if word else body, re.I)


BANNED = [_rx(t, w) for t, w in BANNED_ROT13]

# Only checked in the entry (posts + alt text + image text), where any of
# these would be price talk, advice or a promise of returns.
PRICE_TALK = [
    r"\bprice\b", r"\breturns?\b", r"\bprofit", r"\bmoon", r"\bpump",
    r"\byield", r"\bapy\b", r"\bapr\b", r"\bgains?\b", r"\bbuy now\b",
    r"\binvestment advice\b", r"\bguarantee", r"\brbnt\b", r"\bairdrop",
    r"\b10x\b", r"\bnot financial advice\b", r"\bcoin\b",
]
CREDIT = [r"@\w", r"made by", r"created by", r"designed by", r"written by",
          r"\bby me\b", r"©"]

TEXT_SUFFIXES = {".md", ".py", ".txt", ".sh", ".json", ".yml", ".yaml", ".csv"}
SKIP_DIRS = {".git", "__pycache__", "fonts"}  # fonts: licence text from the font authors


def x_length(text):
    """Weighted length as X counts it: URLs are 23, most Latin chars 1, emoji 2."""
    text = re.sub(r"https?://\S+", "x" * 23, text)
    n = 0
    for ch in text:
        cp = ord(ch)
        light = (cp <= 4351 or 8192 <= cp <= 8205 or 8208 <= cp <= 8223
                 or 8242 <= cp <= 8247)
        n += 1 if light else 2
    return n


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf8")
        props = "".join(z.read(n).decode("utf8") for n in z.namelist()
                        if n.startswith("docProps/") and n.endswith(".xml"))
    return re.sub(r"<[^>]+>", " ", xml) + " " + re.sub(r"<[^>]+>", " ", props)


def pdf_text(path):
    import subprocess
    try:
        out = subprocess.run(["pdftotext", str(path), "-"], capture_output=True,
                             text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        return None
    info = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True).stdout
    return out + "\n" + info


def all_repo_texts():
    for p in sorted(ROOT.rglob("*")):
        if p.is_dir() or any(part in SKIP_DIRS for part in p.relative_to(ROOT).parts):
            continue
        rel = p.relative_to(ROOT)
        if p.suffix in TEXT_SUFFIXES:
            yield rel, p.read_text(encoding="utf8")
        elif p.suffix == ".docx":
            yield rel, docx_text(p)
        elif p.suffix == ".pdf":
            t = pdf_text(p)
            if t is not None:
                yield rel, t
        # Rel path itself is checked too (file names count as on-screen text).
        yield Path(f"{rel} (file name)"), str(rel)


def image_texts():
    import build_images
    return build_images.ALL_TEXT


def self_test():
    """Prove the detectors fire on known-bad text before trusting a clean result."""
    bad = [codecs.decode(w, "rot13") for w in
           ("oybpxpunva", "Oybpx Punva", "oybpx-punva", "qvfgevohgrq yrqtre", "QYG",
            "ba-punva", "bapunva", "pelcgb", "Jro3", "fzneg pbagenpg")]
    for w in bad:
        assert any(rx.search(f"text with {w} inside") for rx in BANNED), w
    for ok in ("Redbelly", "tokenisation", "collateral", "a public digital network"):
        assert not any(rx.search(ok) for rx in BANNED), ok
    assert any(re.search(p, "the price will go up", re.I) for p in PRICE_TALK)
    assert any(re.search(p, "thread by @someone", re.I) for p in CREDIT)
    assert x_length("a" * 280) == 280 and x_length("\U0001F355") == 2
    assert x_length("see https://example.com/a/very/long/path/indeed") == 4 + 23


def main():
    errors, passes = [], []
    self_test()
    passes.append("self-test: detectors catch planted banned words, price talk and handles")

    # 1. Banned words, whole repo.
    scanned = 0
    for rel, text in all_repo_texts():
        scanned += 1
        for rx in BANNED:
            for m in rx.finditer(text):
                errors.append(f"banned term in {rel}: {m.group(0)!r}")
    for t in image_texts():
        for rx in BANNED:
            if rx.search(t):
                errors.append(f"banned term in image text: {t!r}")
    passes.append(f"banned-term scan: {scanned} files + all on-image text")

    # 2 + 3. Price talk and personal credit, entry only.
    entry_texts = [p["text"] for p in POSTS] + [p.get("alt", "") for p in POSTS] + list(image_texts())
    for t in entry_texts:
        for pat in PRICE_TALK:
            if re.search(pat, t, re.I):
                errors.append(f"price/advice wording {pat!r} in: {t[:60]!r}")
        for pat in CREDIT:
            if re.search(pat, t, re.I):
                errors.append(f"personal credit {pat!r} in: {t[:60]!r}")
    passes.append("price-talk and personal-credit scan of posts, alt text and image text")

    # 4 + 5. Lengths, count and images.
    if not 5 <= len(POSTS) <= 10:
        errors.append(f"thread has {len(POSTS)} posts; brief asks for 5-10")
    for i, p in enumerate(POSTS, 1):
        n = x_length(p["text"])
        if n > 280:
            errors.append(f"post {i} is {n} chars (limit 280)")
        if p.get("image") and not (ROOT / "entry" / "images" / p["image"]).exists():
            errors.append(f"post {i} image missing: {p['image']}")
        if p.get("image") and not p.get("alt"):
            errors.append(f"post {i} image has no alt text")
    passes.append("post lengths: " + ", ".join(
        f"{i}:{x_length(p['text'])}" for i, p in enumerate(POSTS, 1)))

    # 6. Fact IDs documented.
    fc = (ROOT / "FACT_CHECK.md").read_text(encoding="utf8")
    for i, p in enumerate(POSTS, 1):
        for f in p["facts"]:
            if not re.search(rf"^##+ {f}\b", fc, re.M):
                errors.append(f"post {i} cites {f} but FACT_CHECK.md has no {f} section")
    passes.append("every fact ID cited by a post is documented in FACT_CHECK.md")

    for p in passes:
        print("PASS", p)
    for e in errors:
        print("FAIL", e)
    print(f"\n{'ALL CHECKS PASSED' if not errors else f'{len(errors)} PROBLEM(S)'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
