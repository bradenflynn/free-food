import instaloader
import os
import time

def test_instaloader(handle):
    # Initialize Instaloader
    L = instaloader.Instaloader()
    
    print(f"Testing instaloader for @{handle}...")
    try:
        # Obtain profile
        profile = instaloader.Profile.from_username(L.context, handle)
        
        # Get posts
        count = 0
        os.makedirs("downloads", exist_ok=True)
        for post in profile.get_posts():
            if count >= 3:
                break
            
            # Download the main image
            img_url = post.url
            print(f"Found post: {img_url}")
            count += 1
            
        print("Success! Instaloader worked.")
    except Exception as e:
        print(f"Instaloader failed: {e}")

if __name__ == "__main__":
    test_instaloader("usdbas")
