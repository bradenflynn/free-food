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
            club_name TEXT,
            event_name TEXT,
            date TEXT,
            time TEXT,
            location TEXT,
            food_provided TEXT,
            has_free_food BOOLEAN,
            food_rank INTEGER,
            confidence_score INTEGER,
            image_path TEXT UNIQUE,
            status TEXT DEFAULT 'PENDING',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_event(data, handle, image_path):
    conn = sqlite3.connect('free_food.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO food_events 
            (source, source_handle, club_name, event_name, date, time, location, food_provided, has_free_food, food_rank, confidence_score, image_path, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'INSTAGRAM', 
            handle, 
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
        # Already processed this exact image
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
    discovered_files = await run_multi_scraper(subset)
    
    print(f"Captured {len(discovered_files)} images total. Analyzing for food...")

    # 3. Analyze each with Vision AI
    for handle, image_path in discovered_files:
        # Quick filter: skip if already in DB
        conn = sqlite3.connect('free_food.db')
        exists = conn.execute('SELECT 1 FROM food_events WHERE image_path=?', (image_path,)).fetchone()
        conn.close()
        
        if exists:
            continue

        event_data = process_image_for_food(image_path)
        
        if "error" in event_data:
            print(f"Skipping {image_path} due to error.")
            continue

        # Save EVERY event now
        save_event(event_data, handle, image_path)

if __name__ == "__main__":
    init_db()
    asyncio.run(run_discovery())
