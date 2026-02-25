import sqlite3
import asyncio
import os
import json
from ig_scraper import run_multi_scraper
from vision_processor import process_image_for_food

# Database Setup
def init_db():
    conn = sqlite3.connect('free_food.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS food_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            source_handle TEXT,
            post_id TEXT UNIQUE,
            club_name TEXT,
            event_name TEXT,
            date TEXT,
            time TEXT,
            location TEXT,
            food_provided TEXT,
            has_free_food BOOLEAN,
            food_rank INTEGER,
            confidence_score INTEGER,
            image_path TEXT,
            status TEXT DEFAULT 'PENDING',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_event(data, handle, image_path, post_id):
    conn = sqlite3.connect('free_food.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO food_events 
            (source, source_handle, post_id, club_name, event_name, date, time, location, food_provided, has_free_food, food_rank, confidence_score, image_path, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'INSTAGRAM', 
            handle, 
            post_id,
            data.get('club_name'), 
            data.get('event_name'), 
            data.get('date'), 
            data.get('time'), 
            data.get('location'), 
            data.get('food_provided'), 
            data.get('has_free_food'),
            data.get('food_rank'), 
            data.get('confidence_score'),
            image_path, 
            'PENDING'
        ))
        conn.commit()
        if data.get('has_free_food'):
            print(f"✅ Found CONFIRMED food at @{handle}! Saved to dashboard.")
        else:
            print(f"📝 Saved general event from @{handle} to dashboard.")
    except sqlite3.IntegrityError:
        # Already processed this exact post
        pass
    conn.close()

async def run_discovery():
    print("🚀 Starting Free Food Discovery...")
    
    # 1. Load handles
    with open("handles.txt", "r") as f:
        handles = [line.strip() for line in f if line.strip()]
    
    # Optional: Rotate or limit handles per run to avoid bans
    subset = handles[:15] # Scan 15 handles per run for safety
    print(f"Scanning {len(subset)} handles...")

    # 2. Scrape (Posts + Stories)
    discovered_posts = await run_multi_scraper(subset)
    
    print(f"Captured {len(discovered_posts)} images total. Analyzing for food...")

    # 3. Analyze each with Vision AI
    for handle, image_path, post_id in discovered_posts:
        # Quick filter: skip if already in DB by post_id
        conn = sqlite3.connect('free_food.db')
        exists = conn.execute('SELECT 1 FROM food_events WHERE post_id=?', (post_id,)).fetchone()
        conn.close()
        
        if exists:
            print(f"Skipping @{handle} post {post_id}: Already processed.")
            continue

        event_data = process_image_for_food(image_path)
        
        if "error" in event_data:
            print(f"Skipping {image_path} due to error.")
            continue

        # Strict Filtering:
        # 1. Must have time AND location
        if event_data.get('has_time_and_location') is False:
            print(f"Skipping {handle} post {post_id}: Missing time or location.")
            continue
            
        # 2. Must be a future event (tomorrow or later)
        if event_data.get('is_future_event') is False:
            print(f"Skipping {handle} post {post_id}: Already passed or happening today.")
            continue

        # Save event if it passes filters
        save_event(event_data, handle, image_path, post_id)

if __name__ == "__main__":
    init_db()
    asyncio.run(run_discovery())
