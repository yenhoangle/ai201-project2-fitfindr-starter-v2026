# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->
This program allows the user to type in clothing items with descriptions about type, size, and price and get a listing of 
outfit items from its inventory which match those descriptions. The user can also ask for outfit suggestions by listing an clothing item and importing a list of their own clothing items. The program will return a listing the clothing articles and a cheery outfit description of 2 to 4 sentences long. 


---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the listings.json file for clothing items with optional size and price ceiling which match the descriptions within
- **Inputs:** `description` (string), `max_price` (float), `size` (string)
- **Returns:** A list of best matched first items
- **When it has nothing:** Returns empty list

### `suggest_outfit`

- **What it does:** Suggests one or two outfits based on the user’s input of their thrifted item
- **Inputs:** `new_item` (dictionary), `wardrobe` (dictionary)
- **Returns:** A non empty string with outfit suggestions
- **When it has nothing:** Returns a general styling advice

### `create_fit_card`

- **What it does:** Creates a short caption about the outfit
- **Inputs:** `outfit` (string), `new_item` (dictionary) 
- **Returns:** Two to four sentences of description of the outfit
- **When it has nothing:** Returns an explanation of why no outfit was returned and a suggestion of how to expand search results

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->


**Branch rule:** In the case of search_listings returns an empty list, put a message in session["error"] telling the user to broaden price, size, or description and stop. Otherwise, take the first result as session["selected_item"] and go to suggest_outfit.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex extracts an optional size and maximum price; the remaining text is used as the listing description.

**What moves through the session:** <!-- which fields, in what order -->
In function order of first to last:
`query` - user input
`wardrobe` - user input
`parsed` - from the query
`search_results` - populated as the non-empty output of `search_listings` on the query
`error` - a branch result that gets populated when the results is empty
`selected_item` - first listing dictionary item of `search_results`
`outfit_suggestion` - the agent's description of the suggested outfit
`fit_card` - description combined from `outfit_suggestion` and `wardrobe`

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'big dinosaur costume under $10'     

  No listings matched those filters. Try broadening the description, removing the size, or increasing the maximum price.

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_012', 'title': 'Oversized Crewneck Sweatshirt — Vintage Navy', 'description': 'Perfectly faded navy crewneck. Genuinely vintage — not manufactured distressed. Ribbed cuffs and hem. No graphics, clean.', 'category': 'tops', 'style_tags': ['vintage', 'basics', 'oversized', 'classic'], 'size': 'XL (fits oversized)', 'condition': 'good', 'price': 20.0, 'colors': ['navy'], 'brand': None, 'platform': 'thredUp'}, {'id': 'lst_020', 'title': 'Henley Long Sleeve — Washed Burgundy', 'description': 'Soft washed henley in a rich burgundy. Three-button placket. Slightly shrunken/cropped fit. 100% cotton.', 'category': 'tops', 'style_tags': ['vintage', 'basics', 'earth tones', 'classic'], 'size': 'M', 'condition': 'excellent', 'price': 16.0, 'colors': ['burgundy', 'wine'], 'brand': None, 'platform': 'thredUp'}, {'id': 'lst_024', 'title': 'Vintage Polo Shirt — Forest Green', 'description': 'Classic polo in forest green. Short sleeve, ribbed collar. Slightly boxy. The kind of piece that goes with everything.', 'category': 'tops', 'style_tags': ['vintage', 'preppy', 'classic', 'earth tones'], 'size': 'M', 'condition': 'good', 'price': 18.0, 'colors': ['green', 'forest green'], 'brand': 'Ralph Lauren', 'platform': 'thredUp'}, {'id': 'lst_026', 'title': 'Biker Shorts — Black, Shiny', 'description': 'Shiny black biker shorts in a slightly glossy material. High-waisted. Y2K-coded. Can be styled athletic or fashion.', 'category': 'bottoms', 'style_tags': ['y2k', 'athletic', 'streetwear', '2000s'], 'size': 'S', 'condition': 'excellent', 'price': 14.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}]

```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Here are two ways to style those vintage Levi's 501s using pieces you already own:

**Look 1: Off-Duty Cool**
*   **Top:** White ribbed tank top
*   **Outerwear:** Vintage black denim jacket 
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Style Note:** A classic double-denim moment that feels effortlessly cool. The crisp white tank keeps it fresh for daytime, while the chunky sneakers and black crossbody add that relaxed, 90s off-dutymodel energy.

***

**Look 2: Edgy & Laid-Back**
*   **Top:** Oversized grey crewneck sweatshirt
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt

**Style Note:** High-low styling at its best. Tucking the heavy grey crewneck into the 501s with a brown belt grounds the look, and the black combat boots add a tough, utilitarian edge to the classic medium-wash denim.

```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and black boots', load_listings()[0]))"   
Found these vintage Levi's 501s on Depop for $38 and they are officially my new personality. Honestly nothing beats this medium wash paired with beat-up black boots

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I used Claude to help implement fuzzy logic in the `search_listing`.   
- *What came back:* Claude was able to implement fuzzy logic but the result was formatted differently than what I expected
- *What I changed:* I made an additional ask to Claude to double check the size and the price formatting

**Moment 2**

- *What I asked for:* I asked Claude to make the `create_fit_card` function to generate 2 - 4 sentences of outfit suggestions.
- *What came back:* It generated the correction responses that was a bit too formal.
- *What I changed:* I asked it to use a casual tone instead.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. impossible query stops early | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. item id being passed from one tool function to another matches | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. The fit card description is the right size | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. The ceiling price of an item is respected | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

Output copied from `results/run_2026-10-13_2209_before.md` produced by `run_eval.py::main`, function `agent.py::run_agent` using scenario "example wardrobe."

```
### impossible query stops early

- Query: `designer ballgown size XXS under $5`
- Wardrobe: example

**Try 1**

- stopped early: yes — No listings matched those filters. Try broadening the description, removing the size, or increasing the maximum price.
- selected_item: (none)
- search_results: 0

Trace:

```
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
[2] search_listings (via MCP)
      in:  {'description': 'designer ballgown', 'size': 'XXS', 'max_price': 5.0}
      out: [] (empty)
      →    branch: empty, stopping before suggest_outfit
```
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | matching query completes | 4 of 5 | MET | trace log printed full run results with branch decisions for 5 of 5 runs |
| 2 | impossible query stops early | 5 of 5 | MET | trace log printed truncated run results with early stop branch for 5 of 5 runs |
| 3 | item id being passed from one tool function to another matches | 5 of 5 | MET | trace log printed `lst_004` which matches the id of the suggested track jacket for 5 out of 5 runs |
| 4 | The fit card description is the right size | 5 of 5 | MET | the fit card description is no more than four sentences for 5 out 5 runs |
| 5 | The ceiling price of an item is respected | 5 of 5 | MET | the system recommended the correct item priced under the given ceiling price for 5 out of 5 runs |

**Diagnoses**

The system has no misses. 

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
python app.py ask 'vintage graphic tee under $20' --trace
[1] parse_query
      in:  vintage graphic tee under $20
      out: {'description': 'vintage graphic tee', 'size': None, 'max_price': 20.0}
[2] search_listings (via MCP)
      in:  {'description': 'vintage graphic tee', 'size': None, 'max_price': 20.0}
      out: 8 items: Y2K Baby Tee — Butterfly Print, Vintage Band Tee — Faded Grey, Mesh Long-Sleeve Top — Black … +5 more
      →    branch: results, selected lst_002
[3] suggest_outfit
      in:  {'new_item': 'Y2K Baby Tee — Butterfly Print', 'wardrobe_items': 10}
      out: Here is an effortless, throwback-inspired look using your new Depop find:  **The Outfit:** *   **New Item:** Y…
[4] create_fit_card
      in:  {'outfit': 'Here is an effortless, throwback-inspired look using your new Depop find:\n\n**The Outfit:**\n*   …
      out: Channeling my inner 2000s off-duty model with this butterfly print baby tee I just scored. Honestly, nothing b…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Here is an effortless, throwback-inspired look using your new Depop find:

**The Outfit:**
*   **New Item:** Y2K Butterfly Baby Tee
*   **Bottoms:** Baggy straight-leg jeans (dark wash)
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Style Note:**
This is peak 2000s off-duty model. Pairing the fitted, pastel baby tee with heavy dark-wash denim creates that classic tight-top-baggy-bottom proportion, while the black denim jacket and chunky sneakers keep it grounded, effortless, and wearable for everyday.

  Fit card: Channeling my inner 2000s off-duty model with this butterfly print baby tee I just scored. Honestly, nothing beats finding a fitted little top like this for only $18 on Depop. Paired it with baggy denim and chunky sneakersso I didn't have to overthink it today.

0 model calls this session, 2 served from cache
```

**Empty search**

```
 python app.py ask '...' --trace         
[1] parse_query
      in:  ...
      out: {'description': '', 'size': None, 'max_price': None}
[2] search_listings (via MCP)
      in:  {'description': '', 'size': None, 'max_price': None}
      out: 10 items: Vintage Levi's 501 Jeans — Medium Wash, Y2K Baby Tee — Butterfly Print, Oversized Flannel Shirt — Plaid Red/Black … +7 more
      →    branch: results, selected lst_001
[3] suggest_outfit
      in:  {'new_item': "Vintage Levi's 501 Jeans — Medium Wash", 'wardrobe_items': 10}
      out: Here are two ways to style those vintage Levi's 501s using pieces you already own:  **Look 1: Off-Duty Cool** …
[4] create_fit_card
      in:  {'outfit': "Here are two ways to style those vintage Levi's 501s using pieces you already own:\n\n**Look 1: Of…
      out: Finally hunted down the ultimate off-duty model jeans and honestly, I might never take these vintage Levi's 50…

  Found:    Vintage Levi's 501 Jeans — Medium Wash — $38.0 on depop

  Outfit:   Here are two ways to style those vintage Levi's 501s using pieces you already own:

**Look 1: Off-Duty Cool**
*   **Top:** White ribbed tank top
*   **Outerwear:** Vintage black denim jacket 
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

**Style Note:** A classic double-denim moment that feels effortlessly cool. The crisp white tank keeps it fresh for daytime, while the chunky sneakers and black crossbody add that relaxed, 90s off-duty model energy.

***

**Look 2: Edgy & Laid-Back**
*   **Top:** Oversized grey crewneck sweatshirt
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt

**Style Note:** High-low styling at its best. Tucking the heavy grey crewneck into the 501s with a brown belt grounds the look, and the black combat boots add a tough, utilitarian edge to the classic medium-wash denim.

  Fit card: Finally hunted down the ultimate off-duty model jeans and honestly, I might never take these vintage Levi's 501s off. Snagged them on Depop for just $38, and they’ve got that exact 90s broken-in feel right out of the box. Going to live in these with chunky sneakers and oversized crewnecks all season long.

0 model calls this session, 2 served from cache
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->

I moved `search_listing()` to an mcp by uncommenting the @mcp logic in `mcp_server.py`and implementing `search_listing()` there. I then imported the function and call it in the `agent.py` file. The move worked and the project works the same as before moving the method over to mcp.

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**
I decided to change the prompt and the system suggestion for the `create_fit_card` function in `tools.py` to sound less preppy and slightly more professional. 
My new instructions for the system are `You are a grounded fashion caption writer. Keep the voice natural and social-media friendly.` and `use a cheerful tone`
I made this change because I feel a more professional tone would lend the suggestion more credibility but I still want the description to be cheerful.

**Which failure it was meant to fix:**
I am not hoping it fix any failures since all my criterias were met, but rather I hope it does not start failing my criteria 4 - `The fit card description is the right size`.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. matching query completes | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET |
| 2. impossible query stops early | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET |
| 3. item id being passed from one tool function to another matches | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET |
| 4. The fit card description is the right size | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET |
| 5. The ceiling price of an item is respected | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET |
**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->
The change in the prompt seems to affect how prices are written. The system used more instances of "$" and "dollars" compared to before, where it sometimes uses "bucks." I feel this change makes the description seems more professional and less casual. The fit card description is still under 4 sentences for all 5 of 5 runs so criteria 4 is still met.

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->

I have no miss criterion but I do still want to play around with how the system generate the fit card some more. I stopped where I did because I did not want to use more tokens just on testing tones.


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
