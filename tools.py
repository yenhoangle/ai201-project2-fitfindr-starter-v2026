"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re
from difflib import SequenceMatcher

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings


def _size_tokens(value: str | None) -> set[str]:
    """Normalize a size string into key tokens that can be compared safely."""
    if value is None:
        return set()
    text = str(value).strip().lower()
    if not text:
        return set()

    tokens: set[str] = set()
    for chunk in re.split(r"[\s/\-]+", text):
        cleaned = re.sub(r"[^a-z0-9]", "", chunk.lower())
        if cleaned:
            tokens.add(cleaned)
    return tokens


def _description_terms(text: str) -> list[str]:
    """Return meaningful keyword terms from a description, stripping filler words."""
    if not text:
        return []
    stop_words = {
        "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from",
        "have", "i", "im", "in", "is", "it", "its", "of", "on", "or", "our",
        "that", "the", "their", "this", "to", "under", "up", "with", "you",
        "your", "looking", "find", "me", "want", "wanting", "size",
    }
    terms = re.findall(r"[a-z0-9]+", text.lower())
    return [term for term in terms if len(term) > 1 and term not in stop_words]


def _item_search_text(item: dict) -> str:
    """Build a searchable text blob for a listing."""
    pieces = [
        item.get("title", ""),
        item.get("description", ""),
        item.get("category", ""),
        " ".join(item.get("style_tags", []) or []),
        " ".join(item.get("colors", []) or []),
        item.get("brand", "") or "",
    ]
    return " ".join(str(part) for part in pieces)


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    Tasks:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`. (fuzzy match python library)
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    listings = load_listings()

    if max_price is not None:
        listings = [item for item in listings if float(item.get("price", float("inf"))) <= max_price]

    if size is not None:
        requested = _size_tokens(size)
        if requested:
            listings = [
                item
                for item in listings
                if requested.intersection(_size_tokens(str(item.get("size", ""))))
            ]

    query_terms = _description_terms(description or "")
    scored: list[tuple[float, dict]] = []

    for item in listings:
        text = _item_search_text(item)
        text_terms = _description_terms(text)

        if not query_terms:
            score = 1.0
        else:
            overlap = sum(1 for term in query_terms if term in text_terms)
            fuzzy_bonus = 0.0
            for term in query_terms:
                best = 0.0
                for candidate in text_terms:
                    best = max(best, SequenceMatcher(None, term, candidate).ratio())
                if best >= 0.8:
                    fuzzy_bonus += best
            score = (overlap * 8.0) + (fuzzy_bonus * 1.2)

        if score > 0:
            scored.append((score, item))

    ranked = [item for _, item in sorted(scored, key=lambda pair: pair[0], reverse=True)]
    return ranked[: config.SEARCH_RESULT_LIMIT]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    Tasks:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    wardrobe_items = wardrobe.get("items", []) if isinstance(wardrobe, dict) else []

    if not wardrobe_items:
        colors = ", ".join(new_item.get("colors", []) or ["a neutral palette"])
        prompt = (
            f"Suggest styling ideas for this thrifted item: {new_item.get('title', 'item')} "
            f"({new_item.get('category', 'unknown category')}) in {colors}. "
            f"The piece is priced at ${new_item.get('price', 0)} on {new_item.get('platform', 'the platform')}. "
            "Give 2 or 3 versatile outfit ideas with a clear vibe and practical layering notes."
        )
        system = "You are a helpful fashion stylist. Give concise, wearable outfit ideas."
        return generate(prompt, system=system, temperature=0.8)

    wardrobe_lines = []
    for entry in wardrobe_items:
        name = entry.get("name", "wardrobe item")
        category = entry.get("category", "")
        color = entry.get("color", "")
        style = entry.get("style", "")
        details = ", ".join(part for part in [category, color, style] if part)
        wardrobe_lines.append(f"- {name} ({details})" if details else f"- {name}")

    colors = ", ".join(new_item.get("colors", []) or ["a neutral palette"])
    prompt = (
        "I have a thrifted item and a wardrobe. Suggest one or two outfit combinations using "
        "pieces the user already owns.\n\n"
        f"New item: {new_item.get('title', 'item')} ({new_item.get('category', 'unknown category')}) "
        f"in {colors}, price ${new_item.get('price', 0)} on {new_item.get('platform', 'the platform')}.\n"
        f"Wardrobe:\n" + "\n".join(wardrobe_lines) + "\n\n"
        "Name the key pieces from the wardrobe and explain the vibe in a short, natural style note."
    )
    system = "You are a fashion stylist helping someone build outfits from thrift finds and what they already own."
    return generate(prompt, system=system, temperature=0.8)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    Tasks:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    if not outfit or not outfit.strip():
        title = new_item.get("title", "this thrifted piece")
        price = new_item.get("price", 0)
        platform = new_item.get("platform", "the platform")
        return (
            f"This find is {title} for ${price} on {platform}, and the vibe is exactly the kind "
            "of piece that makes an outfit feel instantly more personal."
        )

    prompt = (
        "Write a short, casual social caption for a thrift find. It should sound like a real person "
        "posting online, not a product listing. Mention the item, the price, and the platform once each. "
        "Use a specific vibe, and keep it to 2-4 sentences.\n\n"
        f"Item details:\n- title: {new_item.get('title', 'item')}\n"
        f"- category: {new_item.get('category', 'unknown')}\n"
        f"- price: ${new_item.get('price', 0)}\n"
        f"- platform: {new_item.get('platform', 'the platform')}\n"
        f"- vibe/fit idea: {outfit}\n\n"
        "Write the caption only, with no bullet points or markdown."
    )
    system = "You are a witty but grounded fashion caption writer. Keep the voice natural, casual, and social-media friendly."
    return generate(prompt, system=system, temperature=0.9)
