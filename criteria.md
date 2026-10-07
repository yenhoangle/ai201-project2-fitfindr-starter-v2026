# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->
The search logic is a keyword match with keyword overlap scoring. 4 out of 5 target allows for the occasional miss from the users typing in keywords that are not exact match, for example "shades" vs "sunglasses" will not be a match even though they mean the same thing.
---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->
The branch logic in `agent.py` is set up so that if there are no results in `search_listings()` then there will never be the case where the agent will call `suggest_outfit` so it will stop in 5 out of 5 tries in normal condition.

---

## 3. The item id being passed from one tool function to another matches

<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->

The `id` returned by `selected_item` matches the `id` of `suggested_outfit` in 5 out of 5 tries.



**Why this target:**
The static code logic passes the `id` from `selected_item` to `suggested_outfit` without changing the id, so we expect the id will match 5 out of 5 times.


---

## 4. The fit card description is the right size

<!-- YOU WRITE THIS ONE. -->

The fit card is no more than 4 sentences long in 5 out of 5 tries when the same outfit request is asked.



**Why this target:**
In `tools.py` the `create_fit_card` function has a logic to limit the response to only 2-4 sentences so we should not expect anything longer than 4 sentences.


---

## 5. The ceiling price of an item is respected
<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->

The ceiling price of an item is respected

**Why this target:**
When the user search for an item with a `maximum_price`, the user will get a listing containing no items that cost more than that price in 5 out of 5 tries. 


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
