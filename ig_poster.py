import os
import json
import time
from instagrapi import Client
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")
IG_SESSIONID = os.getenv("IG_SESSIONID")

DATA_FILE = "data.json"
POSTS_DIR = "marketing/posts"
STORIES_DIR = "marketing/stories"

def post_to_instagram():
    cl = Client()
    
    # 1. Try to Login via Session ID (Highest Success Rate)
    if IG_SESSIONID:
        print("Attempting login via Session ID...")
        try:
            cl.login_by_sessionid(IG_SESSIONID)
            print("✅ Successfully logged in via Session ID!")
        except Exception as e:
            print(f"⚠️ Session ID login failed: {e}. Falling back to standard login.")
            cl = Client() # Reset client
    
    # 2. Try to Login via Username/Password if Session ID failed or is missing
    if not cl.user_id:
        if not IG_USERNAME or not IG_PASSWORD:
            print("❌ Error: No login credentials found. Add IG_SESSIONID or IG_USERNAME to .env")
            return

        settings_path = "ig_settings.json"
        if os.path.exists(settings_path):
            cl.load_settings(settings_path)
        
        print(f"Logging in as {IG_USERNAME}...")
        try:
            cl.login(IG_USERNAME, IG_PASSWORD)
            cl.dump_settings(settings_path)
            print("✅ Logged in successfully via username/password.")
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return

    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, "r") as f:
        events = json.load(f)

    # Process confirmed free food events
    confirmed = [e for e in events if e.get('has_free_food')]
    
    # For safety, let's track what we've already posted (simple version)
    posted_log = "posted_events.txt"
    if not os.path.exists(posted_log):
        with open(posted_log, "w") as f: f.write("")
    
    with open(posted_log, "r") as f:
        already_posted = f.read().splitlines()

    for event in confirmed:
        post_id = event.get('post_id')
        if post_id in already_posted:
            continue

        print(f"🚀 Processing event: {event.get('club_name')}...")

        # 1. Post to Feed
        post_path = os.path.join(POSTS_DIR, f"haul_{post_id}.png")
        if os.path.exists(post_path):
            caption = f"🍕 FREE FOOD ALERT at {event.get('location', 'USD')}!\n\nClub: {event.get('club_name')}\nTime: {event.get('time')}\nFood: {event.get('food_provided')}\n\nFull daily haul at the link in bio. #USD #FreeFood #TheHaul"
            try:
                cl.photo_upload(post_path, caption)
                print(f"✅ Feed post successful for {post_id}")
            except Exception as e:
                print(f"❌ Feed post failed: {e}")

        # 2. Post to Story
        story_path = os.path.join(STORIES_DIR, f"story_{post_id}.png")
        if os.path.exists(story_path):
            try:
                # Note: story_upload with link requires more complex handling, 
                # but a simple story upload is straightforward.
                cl.photo_upload_to_story(story_path)
                print(f"✅ Story post successful for {post_id}")
            except Exception as e:
                print(f"❌ Story post failed: {e}")

        # Log that we've posted it
        with open(posted_log, "a") as f:
            f.write(f"{post_id}\n")

        # Sleep to avoid rate limits
        print("Waiting 60 seconds before next post...")
        time.sleep(60)

if __name__ == "__main__":
    post_to_instagram()
