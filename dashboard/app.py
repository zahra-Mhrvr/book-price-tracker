from collections import defaultdict
from flask import Flask, render_template

from scraper.db import get_connection

app = Flask(__name__)


def fetch_summary():
    conn = get_connection()
    rows = conn.execute(
        "SELECT title, price, rating, availability, category FROM books"
    ).fetchall()
    conn.close()

    total = len(rows)
    by_category = defaultdict(lambda: {"count": 0, "total_price": 0.0})

    for title, price, rating, availability, category in rows:
        cat = category or "Uncategorized"
        by_category[cat]["count"] += 1
        by_category[cat]["total_price"] += price

    category_stats = []
    for cat, data in sorted(by_category.items()):
        avg = data["total_price"] / data["count"] if data["count"] else 0
        category_stats.append({
            "name": cat,
            "count": data["count"],
            "avg_price": round(avg, 2),
        })

    return {
        "total_books": total,
        "categories": category_stats,
        "books": [
            {"title": r[0], "price": r[1], "rating": r[2],
             "availability": r[3], "category": r[4]}
            for r in rows
        ],
    }


@app.route("/")
def index():
    data = fetch_summary()
    return render_template("index.html", **data)


if __name__ == "__main__":
    app.run(debug=True, port=5050)
