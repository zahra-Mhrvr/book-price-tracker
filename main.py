"""
Entry point for the project.

Usage:
    python main.py scrape          # scrape all categories and store to sqlite
    python main.py scrape --test   # scrape just 2 categories, for a quick check
    python main.py dashboard       # start the flask dashboard on :5050
"""

import argparse

from scraper.scraper import scrape_all
from scraper.db import insert_books, clear_books


def run_scrape(test_mode):
    limit = 2 if test_mode else None
    books = scrape_all(limit_categories=limit)

    clear_books()
    insert_books(books)
    print(f"stored {len(books)} books in data/books.db")


def run_dashboard():
    from dashboard.app import app
    app.run(debug=True, port=5050)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    scrape_cmd = sub.add_parser("scrape")
    scrape_cmd.add_argument("--test", action="store_true")

    sub.add_parser("dashboard")

    args = parser.parse_args()

    if args.command == "scrape":
        run_scrape(test_mode=args.test)
    elif args.command == "dashboard":
        run_dashboard()
