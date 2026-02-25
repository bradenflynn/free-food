import os
import requests
import time
import instaloader
import asyncio

def scrape_instagram_handle(handle):
    """Scrapes a single handle for posts using Instaloader (blocks less than Playwright)."""
    results = []
    print(f"\n--- Checking @{handle} ---")
    
    L = instaloader.Instaloader(
        download_pictures=False,
        download_video_thumbnails=False,
        download_videos=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False
    )
    
    # Removed login logic to keep the scraper running anonymously and quickly.
    # Instaloader can fetch public posts perfectly fine without an account!


    try:
        profile = instaloader.Profile.from_username(L.context, handle)
        
        # We only want the first 2 posts
        count = 0
        posts = profile.get_posts()
        
        for post in posts:
            if count >= 2:
                break
                
            img_url = post.url
            if img_url:
                os.makedirs("downloads", exist_ok=True)
                img_data = requests.get(img_url).content
                filename = f"downloads/{handle}_post_{count}_{int(time.time())}.jpg"
                with open(filename, 'wb') as handler:
                    handler.write(img_data)
                
                print(f"Saved post {count} to {filename}")
                results.append(filename)
                count += 1
                
    except Exception as e:
        print(f"Could not capture posts for @{handle}: {e}")

    return results

async def run_multi_scraper(handles):
    """Orchestrates scraping multiple handles, keeping the exact same async signature for main.py."""
    all_files = []
    
    for handle in handles:
        # We can run the synchronous Instaloader in the async loop
        # For simplicity in this script, we just run it directly.
        files = scrape_instagram_handle(handle.strip())
        all_files.extend([(handle.strip(), f) for f in files])
        await asyncio.sleep(2) # Give it a small pause between accounts
        
    return all_files

if __name__ == "__main__":
    with open("handles.txt", "r") as f:
        handles = [line.strip() for line in f if line.strip()][:5]
    
    asyncio.run(run_multi_scraper(handles))
