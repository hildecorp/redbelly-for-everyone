# Redbelly for Everyone

An entry for the challenge **"Explain Redbelly Without Saying [the B-word]"**: a 10-post X
thread that explains what Redbelly does and why it matters, in everyday language, for a
friend, a parent or a business owner with no background in digital finance.

> **Format chosen:** X thread (10 posts, 5 original images), submitted as text in a document.

## What to read first

| File | What it is |
|------|------------|
| [`entry/THREAD.md`](entry/THREAD.md) | **The entry.** All 10 posts, ready to copy into X, with image placement and alt text |
| [`entry/Redbelly_Thread.docx`](entry/Redbelly_Thread.docx) / [`.pdf`](entry/Redbelly_Thread.pdf) | The same entry as a document, images inline |
| [`entry/images/`](entry/images) | The 5 images, 1600x900 PNG (16:9, X's in-feed ratio) |
| [`SOURCES.md`](SOURCES.md) | **Deliverable 2:** the list of sources used for the facts |
| [`FACT_CHECK.md`](FACT_CHECK.md) | Every factual sentence in the thread, mapped to the exact source wording |

## The thread at a glance

| # | Idea | Everyday hook |
|---|------|---------------|
| 1 | Money moves in seconds, ownership still moves in days | "allow 3-5 business days" |
| 2 | What Redbelly is: one shared, public record of who owns what | everyone reads the same copy |
| 3 | Where it came from: University of Sydney research with CSIRO, live since Nov 2024 | "not dreamt up in a garage" |
| 4 | Tokenisation | cutting a pizza into slices |
| 5 | Eligibility checked at the moment of trade | a bouncer built into the door |
| 6 | Reusable digital ID with zero-knowledge proofs | not handing over your passport 100 times |
| 7 | Final once confirmed | cash, not a cheque |
| 8 | The RBA's Project Acacia: Redbelly was one of three networks for the trial digital money | a company bond bought with it |
| 9 | Loan repayment, closure and collateral release in one step | 3 steps become 1 |
| 10 | Why it matters, in one line | the plumbing behind money and ownership |

## How the brief's rules are met

| Rule | How it is met | How it is checked |
|------|---------------|-------------------|
| No B-word or any stand-in for it | Never used anywhere: posts, alt text, images, documents, file names, or this repo's own code | `tools/check_entry.py` scans **every file in the repo** plus all text drawn on the images; the banned list is stored ROT13-encoded so even the checker doesn't contain the words |
| Every fact correct | 11 facts, each traced to public Redbelly, Tokeniser or RBA material; Project Acacia claims come from the RBA's own final report | `FACT_CHECK.md`; the checker fails if a post cites a fact ID that isn't documented |
| No price talk or investment advice | No token, price, returns or "buy" language | Checker scans posts, alt text and image text for price/advice words |
| No unlicensed media | All images drawn from scratch in code (no stock, no logos, no AI images). Font: Readex Pro (Redbelly's brand font), SIL Open Font License, licence in `fonts/OFL.txt`. No music or video | `tools/build_images.py` rebuilds every image from nothing |
| No personal credit | No names, handles, signatures or "made by" lines in the entry, the images or the document metadata | Checker scans for handles and "made by"-style lines |
| Fits X | Every post at or under 280 characters, weighted as X counts them (emoji = 2, links = 23) | Checker prints each post's length |
| Not posted before judging | Nothing has been posted | Keep this repository **private** until the DAO announces the winner |

## Rebuild and verify

```bash
pip install -r requirements.txt     # Pillow, python-docx
python3 tools/build_images.py       # draws entry/images/*.png
python3 tools/build_docs.py         # writes THREAD.md, .docx, and .pdf (PDF needs LibreOffice)
python3 tools/check_entry.py        # runs every check; exits non-zero on any problem
```

Expected checker output:

```
PASS self-test: detectors catch planted banned words, price talk and handles
PASS banned-term scan: ... files + all on-image text
PASS price-talk and personal-credit scan of posts, alt text and image text
PASS post lengths: 1:264, 2:279, 3:219, 4:266, 5:274, 6:279, 7:196, 8:279, 9:277, 10:276
PASS every fact ID cited by a post is documented in FACT_CHECK.md

ALL CHECKS PASSED
```

`tools/thread_content.py` is the single source of truth for the text. Edit a post there,
then rerun the three commands, and every output stays in sync.

## Repository layout

```
entry/
  THREAD.md                 the entry (copy-paste ready)
  Redbelly_Thread.docx      the entry as a document
  Redbelly_Thread.pdf       the entry as a PDF
  images/01..05-*.png       thread images
SOURCES.md                  sources (deliverable 2)
FACT_CHECK.md               sentence-to-source mapping
tools/
  thread_content.py         post text, alt text, fact IDs
  build_images.py           draws the images
  build_docs.py             builds THREAD.md, .docx and .pdf
  check_entry.py            automated compliance checks
fonts/                      Readex Pro + OFL licence
```
