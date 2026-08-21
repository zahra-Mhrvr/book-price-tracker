from pathlib import Path
from bs4 import BeautifulSoup

from scraper.scraper import parse_book_card

FIXTURE = Path(__file__).parent / "fixture_card.html"


def load_card():
    html = FIXTURE.read_text()
    soup = BeautifulSoup(html, "html.parser")
    return soup.select_one("article.product_pod")


def test_parse_book_card_basic_fields():
    card = load_card()
    book = parse_book_card(card, category="Poetry")

    assert book["title"] == "A Light in the Attic"
    assert book["category"] == "Poetry"
    assert book["availability"] == "In stock"


def test_parse_book_card_price_strips_encoding_junk():
    card = load_card()
    book = parse_book_card(card, category="Poetry")

    assert book["price"] == 51.77


def test_parse_book_card_rating():
    card = load_card()
    book = parse_book_card(card, category="Poetry")

    assert book["rating"] == 3
