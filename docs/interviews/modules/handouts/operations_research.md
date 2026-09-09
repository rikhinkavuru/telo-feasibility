# Questions: operations research and drug-supply economics

*This is a research feasibility study of sterile-injectable shortage response. Nothing in this conversation is
a partnership, an endorsement, a pilot, a customer relationship or a regulatory opinion, and it will not be
described as any of those. You will be cited by role and organisation type only unless you tell me in writing
that I may use more, you will see the record before anything is published, and I will follow up once at most.*

**Ranges are better answers than single numbers.** A range with a reason is the best answer of all. "I do not
know, and here is the role that does" is a useful answer. Say the units and the entity level you are answering
in; most apparent disagreement between two experts turns out to be that and nothing else.

---

| # | Question | Units and entity level | Answer form |
|---|---|---|---|
| 1 | At what annual rate do events occur that remove more than one nominally independent site or supplier at once? | events per year, per group of things that fail together | a rate per year, with the event definition and the dataset or elicitation behind it |
| 2 | When such an event happens, how long does it last and how much capacity does it remove at the sites it touches? | days, per event; fraction of capacity, per site | ranges, or a distribution family with parameters |
| 3 | For a single sterile site, what is the annual rate of a failure that stops or degrades production, how long does it last, and does any capacity survive it? | events per site-year; days; fraction | three ranges |
| 4 | For a single API or component supplier, what is the annual disruption rate and the typical duration? | events per supplier-year; days | two ranges |
| 5 | Which dependencies actually make nominally separate sites or suppliers fail together, and are named common-cause groups the right representation, or does this need a copula or an explicit shared-resource model? | structural | a structural answer, and if groups survive, a rate per group |
| 6 | Is a daily discrete-time engine with common random numbers the right harness for this comparison, and what would you change? What would you run to check that the pairing actually holds across architectures with different site counts? | structural | yes or no on the harness, with named changes, and a test you would run for the pairing |
| 7 | What belongs in the objective and what must not be monetized: purchaser cost, provider harm, patient harm? | structural | a boundary statement, plus what must stay unpriced |
