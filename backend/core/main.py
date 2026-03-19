import sqlite3
import asyncio
import os
import json
from ig_scraper import run_multi_scraper
from vision_processor import process_image_for_food
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

# Supabase Setup
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("🌐 Connected to Supabase Cloud")
    except Exception as e:
        print(f"⚠️ Supabase connection failed: {e}")

# Database Setup
def init_db():
    db_path = os.path.join(os.path.dirname(__file__), '../../data/database/free_food.db')
    conn = sqlite3.connect(db_path)
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
    # 1. Save to Supabase (Cloud)
    if supabase:
        try:
            event_entry = {
                'source': 'INSTAGRAM',
                'source_handle': handle,
                'post_id': post_id,
                'club_name': data.get('club_name'),
                'event_name': data.get('event_name'),
                'date': data.get('date'),
                'time': data.get('time'),
                'location': data.get('location'),
                'food_provided': data.get('food_provided'),
                'has_free_food': data.get('has_free_food'),
                'food_rank': data.get('food_rank'),
                'confidence_score': data.get('confidence_score'),
                'image_path': image_path,
                'status': 'PENDING'
            }
            supabase.table("food_events").upsert(event_entry, on_conflict="post_id").execute()
            print(f"☁️ Cloud: Event from @{handle} saved/updated in Supabase.")
        except Exception as e:
            print(f"❌ Supabase Sync Error: {e}")

    # 2. Save to SQLite (Local Fallback)
    db_path = os.path.join(os.path.dirname(__file__), '../../data/database/free_food.db')
    conn = sqlite3.connect(db_path)
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
    except sqlite3.IntegrityError:
        pass
    conn.close()

    if data.get('has_free_food'):
        print(f"✅ Found CONFIRMED food at @{handle}! Logic complete.")

async def run_discovery():
    print("🚀 Starting Free Food Discovery...")
    
    # 1. Load handles
    handles_path = os.path.join(os.path.dirname(__file__), "../../data/config/handles.txt")
    with open(handles_path, "r") as f:
        handles = [line.strip() for line in f if line.strip()]
    
    # Optional: Rotate or limit handles per run to avoid bans
    subset = handles[:50] # Scan up to 50 handles per run
    print(f"Scanning {len(subset)} handles...")

    # 2. Scrape (Posts + Stories)
    discovered_posts = await run_multi_scraper(subset)
    
    print(f"Captured {len(discovered_posts)} images total. Analyzing for food...")

    # 3. Analyze each with Vision AI
    for handle, image_path, post_id in discovered_posts:
        # Quick filter: skip if already in DB
        # Cloud Check
        cloud_exists = False
        if supabase:
            try:
                res = supabase.table("food_events").select("post_id").eq("post_id", post_id).execute()
                if res.data: cloud_exists = True
            except Exception as e:
                print(f"⚠️ Supabase check failed for {post_id}: {e}")
                # Continue with local-only check
        
        # Local Check
        db_path = os.path.join(os.path.dirname(__file__), '../../data/database/free_food.db')
        conn = sqlite3.connect(db_path)
        local_exists = conn.execute('SELECT 1 FROM food_events WHERE post_id=?', (post_id,)).fetchone()
        conn.close()
        
        if cloud_exists or local_exists:
            print(f"Skipping @{handle} post {post_id}: Already processed.")
            continue

        event_data = process_image_for_food(image_path)
        
        if "error" in event_data:
            print(f"Skipping {image_path} due to error.")
            continue

        has_food = event_data.get('has_free_food', False)
        is_business = event_data.get('is_business_related', False)
        is_before_cutoff = event_data.get('is_before_semester_cutoff', True)
        has_date = event_data.get('date') not in [None, 'TBD', 'Unknown', 'Unknown/TBC', '']
        has_time = event_data.get('time') not in [None, 'TBD', 'Unknown', 'Unknown/TBC', '']

        # 1. Absolute Date Cutoff (May 26, 2026)
        if not is_before_cutoff:
            print(f"🚫 Removing @{handle} post {post_id}: After semester cutoff (May 26).")
            continue

        # 2. Must be a current or future event
        if event_data.get('is_current_or_future_event') is False:
            print(f"Skipping {handle} post {post_id}: Event has already passed.")
            continue

        # 3. Quality Gate
        if has_food:
            # Any confirmed food event is valuable even if missing time/location
            pass
        else:
            # Non-food events MUST have a real date + time AND be business-related
            if not has_date or not has_time:
                print(f"🚫 Removing @{handle} post {post_id}: Missing valid date or time (not an event).")
                continue
            if not is_business:
                print(f"🚫 Removing @{handle} post {post_id}: Non-business event, no food.")
                continue

        # Save event if it passes all gates
        save_event(event_data, handle, image_path, post_id)
    
    # 4. Export for GitHub Pages
    export_to_json()

def export_to_json():
    print("📦 Exporting data for GitHub Pages...")
    db_path = os.path.join(os.path.dirname(__file__), '../../data/database/free_food.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    # Only export pending and approved events, sorted by date
    events = cursor.execute('''
        SELECT * FROM food_events 
        WHERE status != "REJECTED" 
        ORDER BY date ASC
    ''').fetchall()
    conn.close()
    
    data = [dict(ix) for ix in events]
    export_json_path = os.path.join(os.path.dirname(__file__), '../../data/exports/data.json')
    with open(export_json_path, 'w') as f:
        json.dump(data, f, indent=4)
    
    # Also export as data.js to bypass CORS for local file viewing
    export_js_path = os.path.join(os.path.dirname(__file__), '../../data/exports/data.js')
    with open(export_js_path, 'w') as f:
        f.write(f"window.FREE_FOOD_DATA = {json.dumps(data, indent=4)};")
    
    print("✅ data.json and data.js updated.")

if __name__ == "__main__":
    init_db()
    asyncio.run(run_discovery())
