import json
from pathlib import Path
from django.utils.text import slugify

MAJOR = [
    ("The Fool", "Beginnings", "A fresh step asks for curiosity and trust."),
    ("The Magician", "Agency", "Use the tools already within reach."),
    ("The High Priestess", "Intuition", "Make room for what you know quietly."),
    ("The Empress", "Nurture", "Give an idea the care it needs to grow."),
    ("The Emperor", "Structure", "A clear boundary can create freedom."),
    ("The Hierophant", "Tradition", "Learn from a tradition, then ask what resonates."),
    ("The Lovers", "Choice", "Let your values guide a meaningful choice."),
    ("The Chariot", "Direction", "Commit your energy to a chosen path."),
    ("Strength", "Courage", "Gentleness can be a steady kind of strength."),
    ("The Hermit", "Reflection", "Step back to hear your own perspective."),
    ("Wheel of Fortune", "Change", "Notice what is shifting and where you can adapt."),
    ("Justice", "Balance", "Consider the facts and the effects of your choices."),
    ("The Hanged Man", "Perspective", "A pause may reveal another way to see things."),
    ("Death", "Transition", "An ending can make space for something new."),
    ("Temperance", "Harmony", "Try a measured blend instead of an extreme."),
    ("The Devil", "Patterns", "Notice a habit that may be limiting your freedom."),
    ("The Tower", "Revelation", "A disruption may uncover what needs rebuilding."),
    ("The Star", "Hope", "Find a small sign of renewal to follow."),
    ("The Moon", "Uncertainty", "Move gently when the full picture is not yet clear."),
    ("The Sun", "Clarity", "Welcome warmth, confidence, and a clear view."),
    ("Judgement", "Awakening", "Reflect on what you are ready to answer for."),
    ("The World", "Completion", "Recognize how far you have come."),
]

SUITS = {
    "Wands": ("Creativity", "energy, ambition, and creative action"),
    "Cups": ("Feeling", "emotion, connection, and intuition"),
    "Swords": ("Thought", "ideas, conflict, and clear communication"),
    "Pentacles": ("Grounding", "resources, work, and the material world"),
}
RANKS = [
    "Ace",
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Page",
    "Knight",
    "Queen",
    "King",
]
RANK_MEANINGS = [
    "a new opening",
    "a choice or partnership",
    "growth and collaboration",
    "stability and foundations",
    "a challenge or adjustment",
    "exchange and support",
    "assessment and patience",
    "movement and practice",
    "ripening and independence",
    "a full cycle",
    "curiosity and learning",
    "purposeful movement",
    "mature care",
    "steady leadership",
]

CARDS = []
for number, (name, keyword, meaning) in enumerate(MAJOR):
    CARDS.append(
        {
            "name": name,
            "slug": slugify(name),
            "number": f"{number:02d}",
            "group": "Major Arcana",
            "keyword": keyword,
            "meaning": meaning,
            "reflection": f"Where might {keyword.lower()} be showing up in your life?",
        }
    )
for suit, (theme, domain) in SUITS.items():
    for index, rank in enumerate(RANKS):
        name = f"{rank} of {suit}"
        CARDS.append(
            {
                "name": name,
                "slug": slugify(name),
                "number": f"{index + 1:02d}",
                "group": suit,
                "keyword": theme,
                "meaning": f"This card invites you to consider {RANK_MEANINGS[index]} in matters of {domain}.",
                "reflection": f"What would {RANK_MEANINGS[index]} look like for you right now?",
            }
        )

for card in CARDS:
    card["image"] = "tarot/deck/" + card["slug"] + ".webp"
CARD_BY_SLUG = {card["slug"]: card for card in CARDS}
# The supplied export holds the full reading text; CARDS above provides short
# introductions for browsing the library.
READING_CARDS = json.loads(
    (Path(__file__).with_name("card_meanings.json")).read_text(encoding="utf-8")
)
if len(READING_CARDS) != 78 or len({card["name"] for card in READING_CARDS}) != 78:
    raise ValueError("The reading deck must contain 78 unique cards")
major_names = {name for name, _, _ in MAJOR}
for card in READING_CARDS:
    card["group"] = (
        "Major Arcana"
        if card["name"] in major_names
        else card["name"].split(" of ")[-1]
    )
    card["slug"] = slugify(card["name"])
    card["image"] = "tarot/deck/" + card["slug"] + ".webp"
SPREADS = [
    {
        "id": "one",
        "name": "One card",
        "subtitle": "Present focus",
        "description": "One card for the question in front of you.",
        "positions": ["Present focus"],
    },
    {
        "id": "three",
        "name": "Three cards",
        "subtitle": "Situation · Challenge · Next step",
        "description": "Explore the situation, a challenge, and a practical next step.",
        "positions": ["Situation", "Challenge", "Next step"],
    },
    {
        "id": "five",
        "name": "Five cards",
        "subtitle": "A deeper look",
        "description": "See the present, an influence beneath it, a challenge, support, and a next step.",
        "positions": [
            "Present situation",
            "Underlying influence",
            "Challenge",
            "Support",
            "Next step",
        ],
    },
]

SIGNS = [
    (
        "Aries",
        "♈",
        "Fire",
        "Cardinal",
        "Mar 21 – Apr 19",
        "Begin boldly, then give your spark a direction.",
    ),
    (
        "Taurus",
        "♉",
        "Earth",
        "Fixed",
        "Apr 20 – May 20",
        "Notice what helps you feel rooted and nourished.",
    ),
    (
        "Gemini",
        "♊",
        "Air",
        "Mutable",
        "May 21 – Jun 20",
        "Let curiosity open a new conversation.",
    ),
    (
        "Cancer",
        "♋",
        "Water",
        "Cardinal",
        "Jun 21 – Jul 22",
        "Care for your inner life as thoughtfully as others.",
    ),
    (
        "Leo",
        "♌",
        "Fire",
        "Fixed",
        "Jul 23 – Aug 22",
        "Share your warmth without dimming anyone else's.",
    ),
    (
        "Virgo",
        "♍",
        "Earth",
        "Mutable",
        "Aug 23 – Sep 22",
        "Small, attentive steps can create meaningful change.",
    ),
    (
        "Libra",
        "♎",
        "Air",
        "Cardinal",
        "Sep 23 – Oct 22",
        "Seek balance while staying honest about your needs.",
    ),
    (
        "Scorpio",
        "♏",
        "Water",
        "Fixed",
        "Oct 23 – Nov 21",
        "Look beneath the surface with compassion.",
    ),
    (
        "Sagittarius",
        "♐",
        "Fire",
        "Mutable",
        "Nov 22 – Dec 21",
        "Let a wider view renew your sense of possibility.",
    ),
    (
        "Capricorn",
        "♑",
        "Earth",
        "Cardinal",
        "Dec 22 – Jan 19",
        "Build patiently toward what matters.",
    ),
    (
        "Aquarius",
        "♒",
        "Air",
        "Fixed",
        "Jan 20 – Feb 18",
        "Imagine a more generous way forward.",
    ),
    (
        "Pisces",
        "♓",
        "Water",
        "Mutable",
        "Feb 19 – Mar 20",
        "Make space for imagination and gentle boundaries.",
    ),
]
