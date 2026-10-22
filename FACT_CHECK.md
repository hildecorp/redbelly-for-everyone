# Fact check

Each fact ID below is cited by one or more posts (see `facts` in
`tools/thread_content.py`), and `tools/check_entry.py` fails if a post cites an ID
that is missing here. Quotes are copied from the sources in `SOURCES.md`, as they read
on 22 October 2026. "[...]" marks a cut, used where the original sentence goes on to
other points.

---

## F1: Redbelly is an Australian network for real-world assets
**Thread:** posts 1, 2, 10. "Redbelly is an Australian network built to fix that." "built
for real-world things like bonds, loans, property and carbon credits."

- S8 (Tokeniser): "Tokeniser operates on Redbelly Network, Australia's public digital token infrastructure"
- S1 (home page) lists the asset types it supports: "Treasuries & Bonds", "Private Credit", "Carbon Credits", "Derivatives & Commodities", "Insurance", "Real Estate".
- S1 footer: "Redbelly Network Pty Ltd Australia 304/74 Pitt St. Sydney NSW 2000"
- Post 1's "allow 3-5 business days" is the everyday phrase people know from bank
  transfers, used as a hook. It is not presented as a measured fact about any market.

## F2: One shared, up-to-date record of who owns what
**Thread:** posts 2, 4. "Businesses, fund managers and investors all look at the same
up-to-date record, instead of each keeping their own copy." "a public digital network"

- S1: "Establish digital registries as a shared source of truth across issuers, managers, and investors."
- S6, printed p. 12: lists "Redbelly Network (public)" among the platforms used in the pilots.
- S8: "Australia's public digital token infrastructure"

## F3: Where it came from, and when it went live
**Thread:** post 3. "grew out of research at the University of Sydney, working with CSIRO,
Australia's national science agency. Work started in 2016. The public network went live
in November 2024."

- S8: "Tokeniser is a Redbelly Network project: born from research at the University of Sydney and Australian Government Science Agency: CSIRO"
- S2 timeline: "2016 December Work Started On The Redbelly [...]"
- S2 timeline: "2021 June Block8, CSIRO and University of Sydney create Redbelly Network as a joint venture"
- S2 timeline: "2024 November Mainnet Launch" (the live public network, as opposed to its test networks)

## F4: "Tokenisation" means cutting an asset into digital slices with clear owners
**Thread:** post 4. "lets the owner cut it into digital slices that can be issued, held and
traded, each one with a clear owner on record."

- S8: "[...] financial products and services as digital tokens, and lets you program the rules of the asset. Holders gain fractional ownership, direct custody, atomic settlement, and 24/7 secondary trading"
- S3: Redbelly describes its offering as infrastructure for "issuing, managing, and distributing digital financial assets".
- The pizza is an analogy, not a claim.

## F5: Eligibility is checked at the moment of the trade
**Thread:** posts 5, 10. "Many investments are only legally open to certain buyers. On
Redbelly, identity and eligibility are checked at the exact moment of the trade."

- S3: "[...] verifiable credentials enable tokenised investment products with defined investor eligibility, enforced at the point of trade."
- S3: "[...] programmatically at the point of issuance and trade"
- S8 (why some buyers are excluded): "Tokeniser programs eligibility into every asset at the protocol level: identity, KYC, AML, CTF, wholesale and sophisticated investor tests, and TMD."
- The bouncer is an analogy, not a claim.

## F6: Reusable digital ID, with zero-knowledge proofs for privacy
**Thread:** posts 6, 10. "Users are verified with a reusable digital ID, so they skip
repeating the same checks on every platform. Clever maths ("zero-knowledge proofs") lets
you prove you passed the check without sharing all your personal details."

- S4: "All users are verified using digital identities and zero-knowledge [proofs] (ZKP), ensuring compliance without compromising personal privacy."
- S4: "With Redbelly, users avoid repetitive KYC checks across multiple platforms."
- S3: "Reusable client identity and KYC credentials streamline onboarding and reduce duplication"
- S2 timeline: "2024 November W3C ZKP Verifiable Credentials inc National IDs released"
- "Without sharing all your personal details" is the plain-English meaning of
  "without compromising personal privacy" (S4).

## F7: Final once confirmed, with no "pending"
**Thread:** posts 7, 10. "No "pending" for days. Once a transaction is confirmed on
Redbelly, it's final and can't be reversed."

- S3: "Finality - Deterministic finality ensures transactions are confirmed once and cannot be reversed, providing certainty for financial markets"
- S4: "Redbelly Network processes transactions with instant finality, meaning no delays, no pending states [...]"
- Cash versus cheque is an analogy, not a claim.

## F8: Project Acacia, and Redbelly as one of three networks for the RBA's trial digital money
**Thread:** post 8. "In Project Acacia, Australia's central bank (the RBA) tested digital
money in these markets. Redbelly was one of only three networks used for the RBA's trial
digital money."

- S7: the RBA and the Digital Finance Cooperative Research Centre released the Project Acacia
  findings on 18 May 2026. 20 wholesale tokenised asset market use cases were tested.
- S6, title: "Project Acacia: Exploring the Role of Digital Money in Wholesale Tokenised Asset Markets"
- S6, printed p. 13: "Use cases used three of the short-listed [...] platforms for their experimentation with pilot wCBDC: Australian Payments Plus's (AP+) HashSphere instance [...], Canvas Connect [...], and Redbelly Network [...]."
- "wCBDC" is wholesale central bank digital currency: digital money issued by the RBA
  for banks and institutions, not for the public. The thread calls it "the RBA's trial
  digital money", which is accurate and readable.

## F9: A company bond bought with that money, both on Redbelly
**Thread:** post 8. "In one pilot, a company bond was bought with that money, both on
Redbelly."

- S6, Appendix 1, printed p. 57: "Australian Bond Exchange piloted secondary market transactions involving the purchase of a tokenised corporate bond digital twin using wCBDC as the settlement asset. Both the tokenised bond and the wCBDC were issued on to the same network." Network listed for this use case: "Redbelly Network".

## F10: Paying off a loan, 3 steps done as 1
**Thread:** post 9 and image 4. "Paying off a loan usually takes 3 steps in separate
systems: payment, loan closed, then the collateral (what backs the loan) handed back. On
Redbelly, all 3 happened in a single step, so the collateral was free again instantly."

- S6, Box C, printed pp. 27-28: "In traditional finance, the lender records the loan in its loan system, and the collateral in its collateral management system. When the customer repays the loan (in full) the following steps occur sequentially" (payment posted, loan closed, collateral returned).
- S6, same box: "[...] the loan repayment, loan discharge and collateral release functions were composed into a single atomic transaction. As a result, collateral could be released instantly and made immediately available for reuse [...]"
- S6, Appendix 1, printed p. 61: "NotCentralised Collateralised Loans (pilot)". Network listed for this use case: "Redbelly Network".

## F11: Tokeniser, built on Redbelly, and its reported figures
**Thread:** post 10. "Tokeniser, a platform built on Redbelly, reports A$1.2B issued for
160+ companies and funds."

- S8: "Tokeniser operates on Redbelly Network [...]"
- S8: "A$1.2B issued equity & funds", "160+ companies and funds"
- These are Tokeniser's own figures, so the thread says "reports". Tokeniser also shows
  up in the RBA report (S6, printed pp. 59-60): the Macropod fund pilot on Redbelly
  handled "registration and distribution [...] through the Tokeniser platform".
