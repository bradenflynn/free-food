import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(dotenv_path="backend/core/../../.env")

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def test_sync():
    print("🧪 Running Test Sync to Supabase...")
    test_event = {
        'source': 'SYSTEM_TEST',
        'source_handle': 'antigravity',
        'post_id': 'test-sync-01',
        'club_name': 'Test Club',
        'event_name': 'Full-Stack Kickoff',
        'date': '2026-03-10',
        'time': '12:00 PM',
        'location': 'The Cloud',
        'food_provided': 'Virtual Pizza',
        'has_free_food': True,
        'food_rank': 1,
        'confidence_score': 100.0,
        'status': 'APPROVED'
    }
    try:
        res = supabase.table("food_events").upsert(test_event, on_conflict="post_id").execute()
        print("✅ Success! Test event synced to Supabase.")
        print(f"Response: {res.data}")
    except Exception as e:
        print(f"❌ Sync Failed: {e}")

if __name__ == "__main__":
    test_sync()
