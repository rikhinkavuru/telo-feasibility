# Filing record: FDA docket comment

## What was filed

| field | value |
|---|---|
| Docket | FDA-2025-N-6075 |
| RIN | 0910-AI94 |
| Rule | Drug Establishment Registration and Drug Listing Requirements for Establishments Engaged in Distributed Manufacturing and Certain Foreign Establishments |
| Proposed rule published | 13 July 2026 |
| Comment period closed | 11 September 2026, 23:59 Eastern |
| **Comment ID** | **FDA-2025-N-6075-0046** |
| Tracking number | mtu-n6n0-d30h |
| Received by FDA | 9 September 2026 |
| Posted by FDA | 11 September 2026 |
| Document subtype | Electronic Regulation from Form |
| Permanent URL | https://www.regulations.gov/comment/FDA-2025-N-6075-0046 |
| Submitter category | Individual |
| Attachment | `comment.pdf`, 3 pages |
| Comment-box text | `comment_box.txt`, 4,999 characters |

Verified 2026-09-23 against the rendered comment page, which shows the title "Comment from Rikhin Kavuru",
the posting by the Food and Drug Administration, the comment ID, the tracking number, and the full text with
the disclosure of interest and all three requests intact. The page could not be fetched programmatically
from this machine: regulations.gov returns 403 to automated requests and the shared API demo key is rate
limited, so verification was visual.

**Unconfirmed:** whether the three-page PDF attachment uploaded successfully. The comment text says "A
fuller version is attached." Check the posted page for an attachment link. If none is listed, the sentence
points at nothing and the repository URL in the same paragraph is doing all the work instead.

## What the comment argues

Three points, two of them answering questions the Agency expressly raised in the preamble.

1. **Define "unified pharmaceutical quality system."** FDA notes the term and "equivalent" are undefined and
   seeks comment on whether they should be defined. The comment argues they should, and that the ambiguity
   worth resolving is which quality-unit functions may be exercised centrally across distributed manufacturing
   units and which must remain resident at each. A pathway that lets an establishment register as one
   establishment, while leaving unresolved whether its quality system may dispose of batches as one quality
   unit, grants the administrative benefit without the operational one.
2. **The registration timelines are not the interval governing supply.** FDA specifically requested comment on
   the 30-day and 120-day mobile-unit relocation timelines. The comment declines to propose different numbers
   and instead asks that the final rule state explicitly that the registration interval is not the
   qualification-to-release interval, and that it not characterize registration flexibility as shortage
   responsiveness.
3. **The preliminary economic analysis may overstate uptake.** The comment asks that the final regulatory
   impact analysis separate sponsors already operating registered lines from new regional entrants, and state
   which population its uptake estimate assumes.

The comment discloses the author's commercial interest in the subject, states that every input is an
illustrative placeholder, and asks the Agency for nothing.

## Known defect in the filed text

`docs/design_space/post_R012_correction.md` R-4. The filed comment states that where the incumbent plant is
capacity-short, the configurations meeting the service requirement "buy campaigns on lines already registered
and inspected, with positioned finished-goods inventory." After the 2026-09-10 battery, that set also contains
**S4, additional centralized capacity**, at 24.1 million USD per year with P(meet) = 0.95. Building centrally
is not buying campaigns, so the sentence is incomplete as filed.

A submitted docket comment is a fixed public record and cannot be amended. The correction stands here. Any
future filing, reviewer packet, or public description must state it correctly.

The comment's three requests do not depend on that sentence, and the finding that owned distributed nodes fail
on the capacity-short product is unchanged and better supported after the battery than before it.

## How this may and may not be described

**Accurate:**
- "Filed a public comment in FDA rulemaking docket FDA-2025-N-6075 (Comment ID FDA-2025-N-6075-0046)."
- "Submitted a technical analysis to FDA's rulemaking on distributed pharmaceutical manufacturing."

**Never:**
- "The FDA reviewed, accepted, approved, recognized, or endorsed" any part of this. None of those happened.
  Anyone may file. Posting is not evaluation.
- "Worked with," "advised," "consulted for," or "engaged with" FDA.
- Any claim that the Agency responded. FDA does not respond to individual comments. It responds to significant
  comments in the preamble of the final rule, which for this rulemaking is likely one to three years out and
  may never issue.

`CLAIMS_REGISTER.csv` row C010 governs this: "FDA-ready" and "regulator validated" are do-not-say, and filing
a comment does not change that.
