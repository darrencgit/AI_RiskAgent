import feedparser
import sqlite3
from datetime import datetime

# List of RSS feeds
FEED_URLS = [
    "https://www.alignmentforum.org/rss",
    "https://openai.com/blog/rss/",
    "https://www.wired.com/feed/category/ai/latest/rss",
    "https://www.partnershiponai.org/blog/rss/",
    "https://www.technologyreview.com/topic/artificial-intelligence/rss/",
    # Add more from the list above
]

# Keywords to filter relevant articles
KEYWORDS = ["ai", "artificial intelligence", "risk", "policy", "governance", "safety", "ethics"]

def scrape_feeds():
    conn = sqlite3.connect("articles.db")
    c = conn.cursor()

    for url in FEED_URLS:
        feed = feedparser.parse(url)
        source = feed.feed.get("title", url)
        
        for entry in feed.entries:
            title = entry.get("title", "")
            link = entry.get("link", "")
            summary = entry.get("summary", "")
            pub_date_str = entry.get("published", "")
            
            # Parse publication date
            try:
                pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %z")
            except ValueError:
                pub_date = datetime.now()

            # Filter for relevance
            text = (title + " " + summary).lower()
            if any(keyword in text for keyword in KEYWORDS):
                # Check for duplicates
                c.execute("SELECT link FROM articles WHERE link = ?", (link,))
                if not c.fetchone():
                    c.execute(
                        "INSERT INTO articles (title, link, summary, pub_date, source) VALUES (?, ?, ?, ?, ?)",
                        (title, link, summary, pub_date, source)
                    )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    scrape_feeds()
