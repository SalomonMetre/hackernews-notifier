#!/usr/bin/env python
import time
import feedparser
from plyer import notification
from datetime import datetime, timedelta

# URL to the live Hacker News RSS feed
RSS_URL = "https://news.ycombinator.com/rss"

# Customizable max number of notifications per hour
MAX_POSTS_PER_HOUR = 3

# Set to track seen items
seen_links = set()

# Track how many were shown this hour and when the hour started
hourly_post_count = 0
hour_start_time = datetime.now()

def check_rss_feed():
    global seen_links, hourly_post_count, hour_start_time

    # Reset count if the hour has passed
    if datetime.now() - hour_start_time >= timedelta(hours=1):
        hourly_post_count = 0
        hour_start_time = datetime.now()

    if hourly_post_count >= MAX_POSTS_PER_HOUR:
        return  # Don't notify more than the limit this hour

    feed = feedparser.parse(RSS_URL)
    new_items = []

    for entry in feed.entries:
        if entry.link not in seen_links:
            new_items.append(entry)
            seen_links.add(entry.link)

    # Only show up to the remaining limit
    remaining_quota = MAX_POSTS_PER_HOUR - hourly_post_count
    new_items = new_items[:remaining_quota]

    for item in new_items:
        title = item.title
        link = item.link
        notification.notify(
            title="📰 New HackerNews Post",
            message=f"{title}\n{link}",
            timeout=10  # seconds
        )
        hourly_post_count += 1

def main():
    print("🔄 Monitoring Hacker News RSS feed. Press Ctrl+C to stop.")
    while True:
        try:
            check_rss_feed()
            time.sleep(300)  # Check every 5 minutes
        except KeyboardInterrupt:
            print("\n🛑 Stopped.")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
