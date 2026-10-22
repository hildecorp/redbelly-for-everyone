"""Single source of truth for the thread.

Every other file (THREAD.md, the .docx, the .pdf) is generated from this one,
so the text that gets checked is exactly the text that gets submitted.
Each post lists the fact IDs it relies on; see FACT_CHECK.md.
"""

TITLE = "Redbelly in plain English: an X thread"

POSTS = [
    {
        "text": (
            "You can send money to a friend in seconds.\n\n"
            "But changing who owns a bond, a business loan or a slice of a building? "
            "That still runs on paperwork, middlemen and \"allow 3-5 business days\".\n\n"
            "Redbelly is an Australian network built to fix that. Plain-English thread \U0001F447"
        ),
        "image": "01-money-fast-ownership-slow.png",
        "alt": (
            "Two cards side by side. Left card: 'Sending money to a friend' with the word "
            "'Seconds'. Right card: 'Changing who owns a bond, a loan or a building' with "
            "the words 'Paperwork, middlemen, days'. Heading: 'Money moves fast. Ownership doesn't.'"
        ),
        "facts": ["F1"],
    },
    {
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
        "text": (
            "It wasn't dreamt up in a garage.\n\n"
            "Redbelly grew out of research at the University of Sydney, working with CSIRO, "
            "Australia's national science agency.\n\n"
            "Work started in 2016. The public network went live in November 2024."
        ),
        "facts": ["F3"],
    },
    {
        "text": (
            "The big idea has a clunky name: \"tokenisation\".\n\n"
            "Plain version: picture a big asset (a building, a fund, a bundle of loans) "
            "as a pizza. \U0001F355\n\n"
            "Redbelly lets the owner cut it into digital slices that can be issued, held "
            "and traded, each one with a clear owner on record."
        ),
        "image": "02-pizza-slices.png",
        "alt": (
            "A building on the left, an arrow, then a pizza cut into eight slices on the "
            "right, each slice tagged with a different owner. Heading: 'Tokenisation = "
            "cutting a big asset into digital slices'."
        ),
        "facts": ["F2", "F4"],
    },
    {
        "text": (
            "Here's what makes Redbelly different: the rules travel with the slice.\n\n"
            "Many investments are only legally open to certain buyers. On Redbelly, "
            "identity and eligibility are checked at the exact moment of the trade.\n\n"
            "Like a bouncer built into the door, not standing beside it."
        ),
        "image": "03-bouncer-in-the-door.png",
        "alt": (
            "Two rows. Top row: a buyer passes two checks, 'Identity verified' and "
            "'Allowed to buy this', and the trade goes through. Bottom row: a buyer fails "
            "the 'Allowed to buy this' check and the trade is blocked. Heading: 'The rules "
            "travel with the slice'."
        ),
        "facts": ["F5"],
    },
    {
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
        "text": (
            "When a trade is done, it's done.\n\n"
            "No \"pending\" for days. Once a transaction is confirmed on Redbelly, it's "
            "final and can't be reversed.\n\n"
            "Think handing over cash, not waiting for a cheque to clear."
        ),
        "facts": ["F7"],
    },
    {
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
        "text": (
            "Another pilot on Redbelly shows why it matters.\n\n"
            "Paying off a loan usually takes 3 steps in separate systems: payment, loan "
            "closed, then the collateral (what backs the loan) handed back.\n\n"
            "On Redbelly, all 3 happened in a single step, so the collateral was free "
            "again instantly."
        ),
        "image": "04-loan-three-steps-to-one.png",
        "alt": (
            "Top half, 'The usual way': three separate boxes, 'Payment made', 'Loan "
            "closed', 'Collateral handed back', each in a different system with waiting in "
            "between. Bottom half, 'Redbelly pilot in the RBA's Project Acacia': one box "
            "doing all three at once. Heading: 'Paying off a loan: 3 steps become 1'."
        ),
        "facts": ["F10"],
    },
    {
        "text": (
            "Why should you care? This is the plumbing behind money and ownership.\n\n"
            "Redbelly in one line: real-world things split, owned and traded quickly, "
            "with ID checks and the rules built in.\n\n"
            "Tokeniser, a platform built on Redbelly, reports A$1.2B issued for 160+ "
            "companies and funds."
        ),
        "image": "05-one-line-summary.png",
        "alt": (
            "Summary card. 'Redbelly in one line: a public network where real-world things "
            "can be split, owned and traded quickly, with ID checks and the rules built "
            "in.' Four tiles: 'Digital slices of real assets', 'Rules checked at the "
            "moment of trade', 'Reusable, private digital ID', 'Final once confirmed'."
        ),
        "facts": ["F11", "F1", "F5", "F6", "F7"],
    },
]
