"""
Scraper for books.toscrape.com (a sandbox site built for scraping practice).

Walks every category page, pulls out title/price/rating/availability,
and hands the results back as a list of dicts ready to insert into sqlite.
"""

import time
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"

RATING_WORDS = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5,
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (personal project - book price tracker)"
}


def get_category_links():
    """Return {category_name: url} for every category in the sidebar."""
    resp = requests.get(BASE_URL, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(resp.text, "html.parser")

    links = {}
    for a in soup.select(".side_categories ul li ul li a"):
        name = a.get_text(strip=True)
        links[name] = BASE_URL + a["href"]
    return links


def parse_book_card(card, category):
    title = card.h3.a["title"]

    price_text = card.select_one(".price_color").get_text(strip=True)
    price = float(price_text.replace("£", "").replace("Â", ""))

    rating_class = card.select_one(".star-rating")["class"]
    rating_word = [c for c in rating_class if c != "star-rating"][0]
    rating = RATING_WORDS.get(rating_word, None)

    availability = card.select_one(".availability").get_text(strip=True)

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability,
        "category": category,
    }


def scrape_category(name, url):
    books = []
    page_url = url

    while page_url:
        resp = requests.get(page_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        for card in soup.select("article.product_pod"):
            books.append(parse_book_card(card, name))

        next_link = soup.select_one("li.next a")
        if next_link:
            page_url = url.rsplit("/", 1)[0] + "/" + next_link["href"]
        else:
            page_url = None

        time.sleep(0.3)  # be polite, this is someone's free practice site

    return books


def scrape_all(limit_categories=None):
    """Scrape every category. Pass limit_categories (int) to only do the
    first N categories, handy while testing so you're not hammering the site."""
    categories = get_category_links()
    if limit_categories:
        categories = dict(list(categories.items())[:limit_categories])

    all_books = []
    for name, url in categories.items():
        print(f"scraping {name}...")
        all_books.extend(scrape_category(name, url))

    return all_books


if __name__ == "__main__":
    books = scrape_all()
    print(f"done, got {len(books)} books")
