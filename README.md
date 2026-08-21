# Book Price Tracker

A small scraper + dashboard project I built to practice web scraping and get
more comfortable with Flask. It pulls book data (title, price, rating,
category, stock status) from [books.toscrape.com](https://books.toscrape.com) —
a sandbox site that's specifically made for people to practice scraping on,
so nothing here is against anyone's ToS.

Data gets saved into a local SQLite database, and there's a tiny dashboard
where you can see average prices per category and browse what's there.

## Why I built this

I wanted a project that touches a few different things at once instead of
just another notebook: making HTTP requests, parsing HTML, dealing with
pagination, storing stuff in a real database, and then actually showing it
somewhere instead of just printing to console.

## What it does

- Walks every book category on the site (there are 50) and paginates through
  each one
- Parses out title, price, star rating, and stock availability
- Stores everything in `data/books.db` (sqlite)
- Serves a dashboard at `/` showing:
  - total books tracked
  - average price per category (bar chart)
  - a full table of everything scraped

## Setup

```bash
git clone <your-repo-url>
cd book-price-tracker
python3 -m venv venv
source venv/bin/activate   # venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Usage

Scrape everything and store it:

```bash
python main.py scrape
```

If you just want to try it out without scraping all 50 categories:

```bash
python main.py scrape --test
```

Then start the dashboard:

```bash
python main.py dashboard
```

and open `http://localhost:5050`.

## Running tests

```bash
pytest tests/
```

The tests use a saved HTML fixture instead of hitting the live site, so they
run offline and won't get anyone rate-limited.

## Project structure

```
book-price-tracker/
├── scraper/
│   ├── scraper.py      # the actual scraping + parsing logic
│   └── db.py           # sqlite storage
├── dashboard/
│   ├── app.py          # flask app
│   └── templates/
│       └── index.html
├── tests/
│   └── test_scraper.py
└── main.py             # CLI: scrape / dashboard
```

## Notes / things I'd improve

- Right now a full scrape takes a couple minutes since it's single-threaded
  and sleeps between requests on purpose (didn't want to hammer the site).
  Could speed this up with `concurrent.futures` if it ever needs to be fast.
- No price-history tracking yet — right now every scrape wipes the table and
  starts fresh. Adding a timestamp column and keeping history would make the
  "tracker" part of the name actually mean something over time.
- The dashboard is read-only, no auth, not meant to be deployed anywhere
  public — it's just for local use.

## License

MIT
