from django.test import TestCase
from django.urls import reverse
from .data import CARDS, READING_CARDS, SPREADS
from pathlib import Path
from django.conf import settings


class SiteTests(TestCase):
    def test_complete_unique_deck(self):
        self.assertEqual(len(CARDS), 78)
        self.assertEqual(len({card["slug"] for card in CARDS}), 78)
        self.assertEqual(len(READING_CARDS), 78)
        self.assertEqual(len({card["name"] for card in READING_CARDS}), 78)
        for card in READING_CARDS:
            for field in (
                "upright_meaning",
                "reversed_meaning",
                "love_note",
                "career_note",
                "yes_no_upright",
                "daily_keywords",
            ):
                self.assertTrue(card[field], (card["name"], field))
            self.assertTrue(
                (
                    Path(settings.BASE_DIR) / "tarot" / "static" / card["image"]
                ).is_file(),
                card["name"],
            )
        self.assertEqual(
            [spread["positions"] for spread in SPREADS],
            [
                ["Present focus"],
                ["Situation", "Challenge", "Next step"],
                [
                    "Present situation",
                    "Underlying influence",
                    "Challenge",
                    "Support",
                    "Next step",
                ],
            ],
        )

    def test_main_pages(self):
        for name in ("home", "cards", "spreads", "reading", "about"):
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)
        response = self.client.get(reverse("reading"))
        self.assertContains(response, "Shuffle &amp; draw")
        self.assertContains(response, "Yes / No")
        for name in ("home", "cards", "spreads", "astrology", "about"):
            self.assertContains(self.client.get(reverse(name)), "tarot/theme.css")
        self.assertContains(
            self.client.get(reverse("cards")), "tarot/deck/the-star.webp"
        )

    def test_home_uses_the_illustrated_orb(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, 'class="hero-orb"')
        self.assertNotContains(response, "tarot/deck/the-star.webp")

    def test_card_search_and_detail(self):
        response = self.client.get(reverse("cards"), {"q": "the star"})
        self.assertContains(response, "The Star")
        self.assertNotContains(response, "The Emperor")
        self.assertEqual(
            self.client.get(reverse("card_detail", args=["the-star"])).status_code, 200
        )
        self.assertEqual(
            self.client.get(reverse("card_detail", args=["unknown"])).status_code, 404
        )
