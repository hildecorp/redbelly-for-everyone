# Redbelly in plain English

An entry for Redbelly DAO Task Board **TASK-33: Explain Redbelly without saying the B-word.**

A 10-post X thread that explains what Redbelly does and why it matters, for a friend, a
parent or a business owner. No jargon, no price talk, and every fact traced to a public
source. Facts last verified 22 October 2026.

**Format chosen:** X thread, 10 posts, 5 original images, submitted as a document.

## Start here

| File | What it is |
|------|------------|
| [`index.html`](index.html) | The entry as a web page. Every post with a copy button, every image with a download button and its alt text, the brief checklist, the sources and the fact check. Opens straight from disk. |
| [`entry/Redbelly_Thread.pdf`](entry/Redbelly_Thread.pdf) | The entry as an A4 document: cover, the thread, brief checklist, sources, fact check. |
| [`entry/Redbelly_Thread.docx`](entry/Redbelly_Thread.docx) | The same document as a Word file, with the brand fonts embedded. |
| [`entry/images/`](entry/images) | The 5 thread images, 1600 x 900 PNG. Also as one zip: [`entry/redbelly-thread-images.zip`](entry/redbelly-thread-images.zip), with an alt text file. |
| [`entry/THREAD.md`](entry/THREAD.md) | The thread as plain text. |
| [`SOURCES.md`](SOURCES.md) | **Deliverable 2:** the sources used for the facts. |
| [`FACT_CHECK.md`](FACT_CHECK.md) | Every claim in the thread, mapped to the exact wording in its source. |

## The thread at a glance

| # | Post | Everyday picture |
|---|------|------------------|
| 1 | Money moves fast, ownership doesn't | "allow 3-5 business days" |
| 2 | What Redbelly is | one shared, up-to-date record |
| 3 | Where it came from | not dreamt up in a garage |
| 4 | Tokenisation | cutting a pizza into slices |
| 5 | The rules travel with the slice | a bouncer built into the door |
| 6 | One private, reusable ID | not handing over your passport 100 times |
| 7 | Done means done | cash, not a cheque |
| 8 | Tested by Australia's central bank | a company bond bought with trial digital money |
| 9 | Three steps become one | paying off a loan |
| 10 | Why it matters | the plumbing behind money and ownership |

## How the brief is met

| Failure condition | How this entry avoids it | How it is checked |
|-------------------|--------------------------|-------------------|
| The B-word or a stand-in | Not used in any post, alt text, image, document, file name or line of code. | `tools/check_entry.py` scans every file, the PDF and Word text, and the image text. The banned list is stored ROT13-encoded, so the checker itself is clean. |
| A factual error | 11 facts, each traced to Redbelly, Tokeniser or RBA material. Project Acacia claims rely on the RBA's own final report, not on Redbelly's description of it. | `FACT_CHECK.md`. The checker fails if a post cites a fact that has no source behind it. |
| Posted before judging | Nothing has been posted. | Keep this repository private and do not deploy the site until judging ends. |
| Price talk or advice | No tokens, prices, returns or buying language. | The checker scans posts, alt text and image text. |
| Unlicensed media | Images drawn from scratch as HTML and rendered to PNG. Fonts are Be Vietnam Pro and JetBrains Mono (SIL Open Font License, in `assets/fonts`). Logo from the DAO Task Board brand kit. No music, stock art or AI images. | The image source is `tools/templates/images.html`. |
| Unchecked AI text | Every sentence was checked against its source. Company figures are labelled as the company's own. | `FACT_CHECK.md` |
| Personal credit | No names, handles, signatures or made-by lines anywhere in the entry or document metadata. | The checker scans for handles and credit lines. |

## Brand

Built on the [Redbelly DAO Task Board brand kit](https://taskboard.redbellydao.network/brand):
the tokens from its `tokens.css`, Be Vietnam Pro for all text and JetBrains Mono for
numbers and labels only, `#EF5350` as the one accent, 4px and 8px radii, tonal depth with
1px borders, a dark default with a light theme, and a steel hero band in both themes. The
copy follows its voice rules: plain hyphens only, no em dashes or en dashes, no emoji.
Every image carries a dated "last verified" line and keeps its text inside a 5% safe margin.

## Rebuild and verify

All outputs are already built and committed. To change a post, edit
`tools/content.py` and rebuild:

```bash
pip install -r tools/requirements.txt
python3 -m playwright install chromium       # or set CHROMIUM_PATH to an existing Chrome
python3 tools/build.py                       # images, website, PDF, Word file, Markdown
python3 tools/check_entry.py                 # every check; exits non-zero on any problem
```

Expected checker output:

```
PASS self-test: detectors catch planted banned words, dashes, emoji, price talk and handles
PASS banned-term and dash scan: ... files, including the PDF, the Word file and file names
PASS posts, alt text and image text: no emoji, jargon, price talk, advice or credit
PASS post lengths: 1:269, 2:279, 3:219, 4:263, 5:274, 6:279, 7:196, 8:279, 9:277, 10:276
PASS 5 images present, 1600x900 PNG, each with alt text
PASS 11 facts, 8 sources, every link between them resolves
PASS website: ... local links and every in-page anchor resolve, posts match the content
PASS all 5 images carry 'Last verified 22 Oct 2026'

ALL CHECKS PASSED
```

The PDF check needs `pdftotext` (package `poppler-utils`).

## Deploying the website

The site is static: `index.html` plus `assets/` and `entry/`. `vercel.json` sets no
framework and no build step, and `.vercelignore` keeps `tools/` out of the deployment.
Any deployment is a public link, so wait until judging ends.

## Layout

```
index.html                    the website
assets/
  site.css, site.js           styles (DAO brand tokens) and copy buttons
  fonts/                      Be Vietnam Pro, JetBrains Mono, licences
  brand/                      DAO logo files from the brand kit
entry/
  Redbelly_Thread.pdf/.docx   the entry as a document
  THREAD.md                   the thread as text
  images/                     the 5 PNGs
  redbelly-thread-images.zip  the PNGs plus alt text
SOURCES.md                    sources (deliverable 2)
FACT_CHECK.md                 claim-by-claim source mapping
tools/
  content.py                  posts, sources and facts: the single source of truth
  templates/images.html       editable source for the images
  templates/print.html        generated source for the PDF
  build.py, build_docx.py     build everything
  check_entry.py              automated checks
```
