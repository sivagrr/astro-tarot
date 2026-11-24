from django.http import Http404
from django.shortcuts import render
from .data import CARDS, CARD_BY_SLUG, SPREADS, READING_CARDS


def home(request):
    return render(request, "tarot/home.html")


def cards(request):
    group = request.GET.get("group", "All")
    query = request.GET.get("q", "").strip()[:80]
    valid_groups = ["All", "Major Arcana", "Wands", "Cups", "Swords", "Pentacles"]
    if group not in valid_groups:
        group = "All"
    filtered = [
        card
        for card in CARDS
        if (group == "All" or card["group"] == group)
        and (
            not query
            or query.lower()
            in (card["name"] + " " + card["keyword"] + " " + card["meaning"]).lower()
        )
    ]
    return render(
        request,
        "tarot/cards.html",
        {"cards": filtered, "groups": valid_groups, "group": group, "query": query},
    )


def card_detail(request, slug):
    card = CARD_BY_SLUG.get(slug)
    if card is None:
        raise Http404("Card not found")
    return render(request, "tarot/card_detail.html", {"card": card})


def spreads(request):
    return render(request, "tarot/spreads.html", {"spreads": SPREADS})


def reading(request):
    return render(
        request, "tarot/reading.html", {"cards": READING_CARDS, "spreads": SPREADS}
    )


def about(request):
    return render(request, "tarot/about.html")


def astrology(request):
    from .data import SIGNS

    return render(request, "tarot/astrology.html", {"signs": SIGNS})
