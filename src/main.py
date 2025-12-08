#!/usr/bin/env python
import time
import feedparser
from datetime import datetime, timedelta
from rich.console import Console
from rich.theme import Theme
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeRemainingColumn

# Try to import plyer, but don't fail if notifications aren't available
try:
    from plyer import notification
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False

# Check if notifications actually work on this system
if NOTIFICATIONS_AVAILABLE:
    try:
        notification.notify(title="Test", message="Test", timeout=1)
    except NotImplementedError:
        NOTIFICATIONS_AVAILABLE = False
    except Exception:
        # Other errors (like missing dependencies) also mean notifications won't work
        NOTIFICATIONS_AVAILABLE = False

# --- Configuration ---
RSS_URL = "https://news.ycombinator.com/rss"
MAX_POSTS_PER_HOUR = 5   # EXPLICITLY set to 5 per user request
CHECK_INTERVAL = 300     # 5 minutes

# --- Setup Rich Console ---
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "hacker": "bold green"
})
console = Console(theme=custom_theme)

# --- State Tracking ---
seen_links = set()
hourly_post_count = 0
hour_start_time = datetime.now()

def play_sound():
    """
    Plays a system sound.
    \a is the cross-platform 'bell' character.
    On modern terminals (macOS/Linux/Windows), this triggers the default system alert sound.
    """
    print("\a") 

def get_smart_emoji(title):
    title_lower = title.lower()
    keywords = {
        "🐍": ['python', 'django', 'flask', 'pandas'],
        "🤖": ['ai', 'llm', 'gpt', 'robot', 'machine learning'],
        "💰": ['crypto', 'bitcoin', 'finance', 'money', 'vc'],
        "🔓": ['security', 'hack', 'breach', 'bug', 'cve'],
        "🍎": ['apple', 'iphone', 'mac', 'ios'],
        "🐧": ['linux', 'ubuntu', 'bash', 'kernel'],
        "🚀": ['launch', 'space', 'nasa', 'mars'],
        "⚛️": ['react', 'javascript', 'node', 'css']
    }
    
    for emoji, words in keywords.items():
        if any(w in title_lower for w in words):
            return emoji
    return "📰"

def check_rss_feed():
    global seen_links, hourly_post_count, hour_start_time

    # Reset count if the hour has passed
    if datetime.now() - hour_start_time >= timedelta(hours=1):
        hourly_post_count = 0
        hour_start_time = datetime.now()
        console.log("[info]Hourly quota reset.[/info]")

    # Check limit
    if hourly_post_count >= MAX_POSTS_PER_HOUR:
        # We return True to indicate we are "full" so the main loop knows
        return "LIMIT_REACHED"

    try:
        feed = feedparser.parse(RSS_URL)
    except Exception as e:
        console.log(f"[error]Failed to fetch RSS feed: {e}[/error]")
        return

    new_items = []
    for entry in feed.entries:
        if entry.link not in seen_links:
            new_items.append(entry)
            seen_links.add(entry.link)

    # Slice to remaining quota
    remaining_quota = MAX_POSTS_PER_HOUR - hourly_post_count
    items_to_show = new_items[:remaining_quota]

    if items_to_show:
        # Play sound ONLY if we actually found something
        play_sound()
        
    for item in items_to_show:
        title = item.title
        link = item.link
        emoji = get_smart_emoji(title)
        
                # 1. Desktop Notification (if available)
        if NOTIFICATIONS_AVAILABLE:
            try:
                notification.notify(
                    title=f"{emoji} HN: {title[:40]}...",
                    message=f"{title}\n{link}",
                    timeout=10
                )
            except Exception:
                # Silently fail if notification doesn't work
                console.print("[warning]Desktop notifications not supported on this system.[/warning]")
                pass
        
        # 2. Terminal Log
        console.print(f"  {emoji} [bold]{title}[/bold]")
        console.print(f"     [link={link}]{link}[/link]")
        
        hourly_post_count += 1
    
    return "OK"

def main():
    console.clear()
    console.rule("[bold orange1]HackerNews Watcher[/bold orange1]")
    
    # Inform user about notification status
    if not NOTIFICATIONS_AVAILABLE:
        console.print("[yellow]⚠️  Desktop notifications are disabled (system dependencies missing)[/yellow]")
        console.print("[yellow]   Install with: sudo apt install python3-dbus libnotify-bin (Ubuntu/Debian)[/yellow]")
        console.print()
    
    while True:
        try:
            # --- 1. Check Feed ---
            status = check_rss_feed()
            
            msg = "Scanning feed..."
            if status == "LIMIT_REACHED":
                msg = f"Hourly limit ({MAX_POSTS_PER_HOUR}) reached. Waiting..."
            
            # --- 2. Smooth Animation (Progress Bar) ---
            # We define a high-resolution sleep (0.1s) for smooth updates
            total_ticks = CHECK_INTERVAL * 10 
            
            with Progress(
                SpinnerColumn("dots"),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=None), # Fills available space
                TimeRemainingColumn(),
                transient=True, # Disappear when done
                console=console
            ) as progress:
                
                task = progress.add_task(f"[cyan]{msg}", total=total_ticks)
                
                for _ in range(total_ticks):
                    time.sleep(0.1) # Updates 10 times per second
                    progress.advance(task)
                    
        except KeyboardInterrupt:
            console.print("\n[bold red]🛑 Watcher stopped by user.[/bold red]")
            break
        except Exception as e:
            console.print_exception()
            time.sleep(60)

if __name__ == "__main__":
    main()
