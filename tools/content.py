"""Single source of truth for the entry.

Posts, sources and the fact check all live here. tools/build.py turns this file
into the website, the five images, the PDF, the Word file and the Markdown files,
so the text that gets checked is exactly the text that gets submitted.
"""

TITLE = "Redbelly in plain English"
SUBTITLE = "A 10-post X thread that explains what Redbelly does and why it matters, without the jargon."
TASK = "TASK-33"
LAST_VERIFIED = "22 Oct 2026"
LAST_VERIFIED_LONG = "22 October 2026"

# ---------------------------------------------------------------- posts

POSTS = [
    {
        "title": "Money moves fast, ownership doesn't",
        "text": (
            "You can send money to a friend in seconds.\n\n"
            "But changing who owns a bond, a business loan or a slice of a building? "
            "That still runs on paperwork, middlemen and \"allow 3-5 business days\".\n\n"
            "Redbelly is an Australian network built to fix that. Here it is in plain English."
        ),
        "image": "01-money-fast-ownership-slow.png",
        "alt": (
            "Two panels side by side. Left: 'Sending money to a friend', marked 'Seconds'. "
            "Right: 'Changing who owns a bond, a loan or a building', marked 'Paperwork, "
            "middlemen, days'. Heading: 'Money moves fast. Ownership doesn't.'"
        ),
        "facts": ["F1"],
    },
    {
        "title": "What Redbelly is",
        "text": (
            "So what is Redbelly?\n\n"
            "A public digital network for keeping track of who owns what, built for "
            "real-world things like bonds, loans, property and carbon credits.\n\n"
            "Businesses, fund managers and investors all look at the same up-to-date record, "
            "instead of each keeping their own copy."
        ),
        "facts": ["F1", "F2"],
    },
    {
        "title": "Where it came from",
        "text": (
            "It wasn't dreamt up in a garage.\n\n"
            "Redbelly grew out of research at the University of Sydney, working with CSIRO, "
            "Australia's national science agency.\n\n"
            "Work started in 2016. The public network went live in November 2024."
        ),
        "facts": ["F3"],
    },
    {
        "title": "Tokenisation, as a pizza",
        "text": (
            "The big idea has a clunky name: \"tokenisation\".\n\n"
            "Plain version: picture a big asset (a building, a fund, a bundle of loans) "
            "as a pizza.\n\n"
            "Redbelly lets the owner cut it into digital slices that can be issued, held "
            "and traded, each one with a clear owner on record."
        ),
        "image": "02-pizza-slices.png",
        "alt": (
            "Left: one building labelled 'One big asset'. Right: the same asset as a pizza "
            "cut into eight slices, each tagged with a different made-up owner name. "
            "Heading: 'Tokenisation means cutting a big asset into digital slices'."
        ),
        "facts": ["F2", "F4"],
    },
    {
        "title": "The rules travel with the slice",
        "text": (
            "Here's what makes Redbelly different: the rules travel with the slice.\n\n"
            "Many investments are only legally open to certain buyers. On Redbelly, "
            "identity and eligibility are checked at the exact moment of the trade.\n\n"
            "Like a bouncer built into the door, not standing beside it."
        ),
        "image": "03-bouncer-in-the-door.png",
        "alt": (
            "Two rows. Top: a buyer passes 'Identity verified' and 'Allowed to buy this', "
            "and the trade goes through. Bottom: a buyer fails 'Allowed to buy this' and "
            "the trade is blocked. Heading: 'The rules travel with the slice'."
        ),
        "facts": ["F5"],
    },
    {
        "title": "One private, reusable ID",
        "text": (
            "And you don't hand over your passport a hundred times.\n\n"
            "Users are verified with a reusable digital ID, so they skip repeating the "
            "same checks on every platform.\n\n"
            "Clever maths (\"zero-knowledge proofs\") lets you prove you passed the check "
            "without sharing all your personal details."
        ),
        "facts": ["F6"],
    },
    {
        "title": "Done means done",
        "text": (
            "When a trade is done, it's done.\n\n"
            "No \"pending\" for days. Once a transaction is confirmed on Redbelly, it's "
            "final and can't be reversed.\n\n"
            "Think handing over cash, not waiting for a cheque to clear."
        ),
        "facts": ["F7"],
    },
    {
        "title": "Tested by Australia's central bank",
        "text": (
            "Has anyone serious tested it?\n\n"
            "In Project Acacia, Australia's central bank (the RBA) tested digital money in "
            "these markets. Redbelly was one of only three networks used for the RBA's "
            "trial digital money.\n\n"
            "In one pilot, a company bond was bought with that money, both on Redbelly."
        ),
        "facts": ["F8", "F9"],
    },
    {
        "title": "Three steps become one",
        "text": (
            "Another pilot on Redbelly shows why it matters.\n\n"
            "Paying off a loan usually takes 3 steps in separate systems: payment, loan "
            "closed, then the collateral (what backs the loan) handed back.\n\n"
            "On Redbelly, all 3 happened in a single step, so the collateral was free "
            "again instantly."
        ),
        "image": "04-loan-three-steps-to-one.png",
        "alt": (
            "Top, 'The usual way': three separate boxes, 'Payment made', 'Loan closed' and "
            "'Collateral handed back', each in a different system, with a wait between "
            "them. Bottom, 'Pilot on Redbelly, RBA Project Acacia': one box that does all "
            "three at once. Heading: 'Paying off a loan: 3 steps become 1'."
        ),
        "facts": ["F10"],
    },
    {
        "title": "Why it matters",
        "text": (
            "Why should you care? This is the plumbing behind money and ownership.\n\n"
            "Redbelly in one line: real-world things split, owned and traded quickly, "
            "with ID checks and the rules built in.\n\n"
            "Tokeniser, a platform built on Redbelly, reports A$1.2B issued for 160+ "
            "companies and funds."
        ),
        "image": "05-one-line-summary.png",
        "alt": (
            "Summary card. 'Redbelly in one line: real-world things split, owned and traded "
            "quickly, with ID checks and the rules built in.' Four tiles: 'Digital slices "
            "of real assets', 'Rules checked at the moment of trade', 'One reusable, "
            "private ID', 'Final once confirmed'."
        ),
        "facts": ["F11", "F1", "F5", "F6", "F7"],
    },
]

# ---------------------------------------------------------------- sources

SOURCES = [
    {
        "id": "S1", "name": "Redbelly Network home page", "publisher": "Redbelly Network",
        "url": "https://redbelly.network",
        "used_for": "What Redbelly does, the asset types it supports, the shared record, its Sydney base.",
    },
    {
        "id": "S2", "name": "Redbelly About us page and timeline", "publisher": "Redbelly Network",
        "url": "https://redbelly.network/about-us",
        "used_for": "Research start (Dec 2016), the Block8, CSIRO and University of Sydney joint venture (Jun 2021), public network launch (Nov 2024), digital ID credentials (Nov 2024).",
    },
    {
        "id": "S3", "name": "Redbelly asset tokenisation page", "publisher": "Redbelly Network",
        "url": "https://redbelly.network/asset-tokenisation",
        "used_for": "Eligibility enforced at the point of trade, reusable identity credentials, transactions final once confirmed.",
    },
    {
        "id": "S4", "name": "What sets Redbelly Network apart (article)", "publisher": "Redbelly Network",
        "url": "https://redbelly.network/blog/what-sets-redbelly-network-apart",
        "used_for": "Users verified with digital identities and zero-knowledge proofs, no repeated identity checks, no pending states.",
    },
    {
        "id": "S5", "name": "Redbelly Project Acacia page", "publisher": "Redbelly Network",
        "url": "https://redbelly.network/projectacacia",
        "used_for": "Background on Redbelly's part in the RBA's Project Acacia. Claims in the thread rely on S6 instead.",
    },
    {
        "id": "S6", "name": "Project Acacia final report, May 2026",
        "publisher": "Reserve Bank of Australia and Digital Finance Cooperative Research Centre",
        "url": "https://www.rba.gov.au/payments-and-infrastructure/central-bank-digital-currency/pdf/project-acacia-final-report.pdf",
        "used_for": "Redbelly as one of three networks for the pilot wholesale central bank money (p. 13), the bond pilot (p. 57), the loan pilot (pp. 27-28 and 61).",
    },
    {
        "id": "S7", "name": "RBA and DFCRC release findings from Project Acacia (media release, 18 May 2026)",
        "publisher": "Reserve Bank of Australia",
        "url": "https://www.rba.gov.au/media-releases/2026/mr-26-13.html",
        "used_for": "Who ran Project Acacia, what it tested, and how many use cases.",
    },
    {
        "id": "S8", "name": "Tokeniser home page", "publisher": "Tokeniser Pty Ltd",
        "url": "https://tokeniser.com",
        "used_for": "Tokeniser runs on Redbelly, its research origins, its reported A$1.2B and 160+ figures, investor eligibility tests.",
    },
]

# ---------------------------------------------------------------- fact check
# Each fact: the claim as the thread makes it, and the source wording behind it.
# "[...]" marks a cut where the original sentence goes on to other points.

FACTS = [
    {
        "id": "F1", "label": "An Australian network for real-world assets",
        "claim": "Redbelly is an Australian network built for real-world things like bonds, loans, property and carbon credits.",
        "evidence": [
            ("S8", "Tokeniser operates on Redbelly Network, Australia's public digital token infrastructure"),
            ("S1", "Asset types listed: Treasuries & Bonds, Private Credit, Carbon Credits, Derivatives & Commodities, Insurance, Real Estate"),
            ("S1", "Redbelly Network Pty Ltd Australia 304/74 Pitt St. Sydney NSW 2000"),
        ],
        "note": "\"Allow 3-5 business days\" in post 1 is the everyday phrase people know from bank transfers, used as a hook. It is not presented as a measured fact about any market.",
    },
    {
        "id": "F2", "label": "One shared, up-to-date record",
        "claim": "A public network where businesses, fund managers and investors all look at the same up-to-date record.",
        "evidence": [
            ("S1", "Establish digital registries as a shared source of truth across issuers, managers, and investors."),
            ("S6", "p. 12 lists \"Redbelly Network (public)\" among the platforms used in the pilots."),
            ("S8", "Australia's public digital token infrastructure"),
        ],
    },
    {
        "id": "F3", "label": "Origins and launch date",
        "claim": "Grew out of research at the University of Sydney, working with CSIRO. Work started in 2016. The public network went live in November 2024.",
        "evidence": [
            ("S8", "Tokeniser is a Redbelly Network project: born from research at the University of Sydney and Australian Government Science Agency: CSIRO"),
            ("S2", "2016 December Work Started On The Redbelly [...]"),
            ("S2", "2021 June Block8, CSIRO and University of Sydney create Redbelly Network as a joint venture"),
            ("S2", "2024 November Mainnet Launch"),
        ],
        "note": "\"Mainnet\" is the live public network, as opposed to its test networks.",
    },
    {
        "id": "F4", "label": "Tokenisation means digital slices with clear owners",
        "claim": "The owner can cut a big asset into digital slices that can be issued, held and traded, each with a clear owner on record.",
        "evidence": [
            ("S8", "[...] financial products and services as digital tokens, and lets you program the rules of the asset. Holders gain fractional ownership, direct custody, atomic settlement, and 24/7 secondary trading"),
            ("S1", "Redbelly provides the infrastructure to issue, manage, and distribute regulated digital financial assets to a global investor base."),
        ],
        "note": "The pizza is an analogy, not a claim.",
    },
    {
        "id": "F5", "label": "Eligibility checked at the moment of trade",
        "claim": "Many investments are only legally open to certain buyers. On Redbelly, identity and eligibility are checked at the moment of the trade.",
        "evidence": [
            ("S3", "[...] verifiable credentials enable tokenised investment products with defined investor eligibility, enforced at the point of trade."),
            ("S3", "[...] programmatically at the point of issuance and trade"),
            ("S8", "Tokeniser programs eligibility into every asset at the protocol level: identity, KYC, AML, CTF, wholesale and sophisticated investor tests, and TMD."),
        ],
        "note": "The bouncer is an analogy, not a claim.",
    },
    {
        "id": "F6", "label": "Reusable digital ID with zero-knowledge proofs",
        "claim": "Users are verified with a reusable digital ID, so they skip repeating the same checks on every platform. Zero-knowledge proofs let you prove you passed without sharing all your details.",
        "evidence": [
            ("S4", "All users are verified using digital identities and zero-knowledge [proofs] (ZKP), ensuring compliance without compromising personal privacy."),
            ("S4", "With Redbelly, users avoid repetitive KYC checks across multiple platforms."),
            ("S3", "Reusable client identity and KYC credentials streamline onboarding and reduce duplication"),
            ("S2", "2024 November W3C ZKP Verifiable Credentials inc National IDs released"),
        ],
        "note": "\"Without sharing all your personal details\" is the plain-English meaning of \"without compromising personal privacy\" (S4).",
    },
    {
        "id": "F7", "label": "Final once confirmed",
        "claim": "No \"pending\" for days. Once a transaction is confirmed on Redbelly, it's final and can't be reversed.",
        "evidence": [
            ("S3", "Deterministic finality ensures transactions are confirmed once and cannot be reversed, providing certainty for financial markets"),
            ("S4", "Redbelly Network processes transactions with instant finality, meaning no delays, no pending states [...]"),
        ],
        "note": "Cash versus a cheque is an analogy, not a claim.",
    },
    {
        "id": "F8", "label": "One of three networks for the RBA's trial digital money",
        "claim": "In Project Acacia, the RBA tested digital money in these markets. Redbelly was one of only three networks used for the RBA's trial digital money.",
        "evidence": [
            ("S7", "The RBA and the DFCRC released the Project Acacia findings on 18 May 2026. 20 wholesale tokenised asset market use cases were tested."),
            ("S6", "Use cases used three of the short-listed [...] platforms for their experimentation with pilot wCBDC: Australian Payments Plus's (AP+) HashSphere instance [...], Canvas Connect [...], and Redbelly Network [...]. (p. 13)"),
        ],
        "note": "wCBDC is wholesale central bank digital currency: digital money issued by the RBA for banks and institutions, not the public. The thread calls it \"the RBA's trial digital money\".",
    },
    {
        "id": "F9", "label": "A company bond bought with that money",
        "claim": "In one pilot, a company bond was bought with that money, both on Redbelly.",
        "evidence": [
            ("S6", "Australian Bond Exchange piloted secondary market transactions involving the purchase of a tokenised corporate bond digital twin using wCBDC as the settlement asset. Both the tokenised bond and the wCBDC were issued on to the same network. Network listed: Redbelly Network. (p. 57)"),
        ],
    },
    {
        "id": "F10", "label": "Paying off a loan: 3 steps become 1",
        "claim": "Paying off a loan usually takes 3 steps in separate systems. In the pilot on Redbelly, all 3 happened in a single step, so the collateral was free again instantly.",
        "evidence": [
            ("S6", "In traditional finance, the lender records the loan in its loan system, and the collateral in its collateral management system. When the customer repays the loan (in full) the following steps occur sequentially [...] (pp. 27-28)"),
            ("S6", "[...] the loan repayment, loan discharge and collateral release functions were composed into a single atomic transaction. As a result, collateral could be released instantly and made immediately available for reuse [...] (p. 28)"),
            ("S6", "NotCentralised Collateralised Loans (pilot). Network listed: Redbelly Network. (p. 61)"),
        ],
    },
    {
        "id": "F11", "label": "Tokeniser and its reported figures",
        "claim": "Tokeniser, a platform built on Redbelly, reports A$1.2B issued for 160+ companies and funds.",
        "evidence": [
            ("S8", "Tokeniser operates on Redbelly Network [...]"),
            ("S8", "A$1.2B issued equity & funds; 160+ companies and funds"),
            ("S6", "The Macropod fund pilot on Redbelly handled registration and distribution through the Tokeniser platform. (pp. 59-60)"),
        ],
        "note": "These are Tokeniser's own figures, so the thread says \"reports\".",
    },
]

LEFT_OUT = [
    "Throughput figures (transactions per second), because different Redbelly pages quote different numbers.",
    "Roadmap items and partnerships that are announced but not finished.",
    "Anything about prices, tokens or investing.",
]


def post_sources(post):
    """Source IDs behind a post, in S-number order."""
    ids = {sid for f in FACTS if f["id"] in post["facts"] for sid, _ in f["evidence"]}
    return sorted(ids, key=lambda s: int(s[1:]))


def fact(fid):
    return next(f for f in FACTS if f["id"] == fid)


def source(sid):
    return next(s for s in SOURCES if s["id"] == sid)
