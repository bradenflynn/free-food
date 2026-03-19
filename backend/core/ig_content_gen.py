import os
import json
from PIL import Image, ImageDraw, ImageFont

# Design Tokens (VÉLOCE Style)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_TAN = (193, 154, 107) # #C19A6B

# Paths
DATA_FILE = "../../data/exports/data.json"
OUTPUT_DIR = "../../marketing/posts"
STORY_DIR = "../../marketing/stories"
FONT_PATH = "/System/Library/Fonts/Supplemental/Impact.ttf" # Fallback for Bebas Neue

# Ensure directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(STORY_DIR, exist_ok=True)

def create_sticker(draw, text, position, font, bg_color=COLOR_WHITE):
    """Draws a VÉLOCE-style sticker with a shadow/offset."""
    # Get text size
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    
    padding = 20
    rect = [position[0], position[1], position[0] + tw + padding*2, position[1] + th + padding*2]
    
    # Draw Shadow
    shadow_offset = 6
    shadow_rect = [r + shadow_offset for r in rect]
    draw.rounded_rectangle(shadow_rect, radius=20, fill=COLOR_BLACK)
    
    # Draw Sticker Background
    draw.rounded_rectangle(rect, radius=20, fill=bg_color, outline=COLOR_BLACK, width=4)
    
    # Draw Text
    draw.text((position[0] + padding, position[1] + padding - 5), text, font=font, fill=COLOR_BLACK)

def generate_marketing_assets():
    if not os.path.exists(DATA_FILE):
        print("No data.json found.")
        return

    with open(DATA_FILE, "r") as f:
        events = json.load(f)

    # Only process confirmed food events for today/future
    confirmed = [e for e in events if e.get('has_free_food')]
    
    if not confirmed:
        print("No confirmed food events to generate content for.")
        return

    # Load Font
    try:
        font_main = ImageFont.truetype(FONT_PATH, 60)
        font_small = ImageFont.truetype(FONT_PATH, 40)
        font_hero = ImageFont.truetype(FONT_PATH, 120)
    except:
        font_main = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_hero = ImageFont.load_default()

    for event in confirmed:
        img_path = event.get('image_path')
        if not img_path or not os.path.exists(img_path):
            continue

        base_img = Image.open(img_path).convert("RGBA")
        post_id = event.get('post_id')

        # 1. SQUARE POST (1080x1080)
        canvas_post = Image.new("RGBA", (1080, 1080), COLOR_WHITE)
        
        # Fit image to square
        img_ratio = base_img.width / base_img.height
        if img_ratio > 1:
            new_w = 1000
            new_h = int(1000 / img_ratio)
        else:
            new_h = 1000
            new_w = int(1000 * img_ratio)
            
        resized_img = base_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
        canvas_post.paste(resized_img, ((1080-new_w)//2, (1080-new_h)//2), resized_img)
        
        draw_post = ImageDraw.Draw(canvas_post)
        
        # Add Stickers
        create_sticker(draw_post, "THE HAUL", (50, 50), font_hero, bg_color=COLOR_TAN)
        create_sticker(draw_post, f"@{event['source_handle']}", (50, 950), font_main)
        create_sticker(draw_post, "PRIORITY", (800, 950), font_main, bg_color=COLOR_WHITE)
        
        # Save Post
        post_filename = f"{OUTPUT_DIR}/haul_{post_id}.png"
        canvas_post.convert("RGB").save(post_filename)
        print(f"Generated Post: {post_filename}")

        # 2. STORY POST (1080x1920)
        canvas_story = Image.new("RGBA", (1080, 1920), COLOR_TAN)
        
        # Top Header Area
        draw_story = ImageDraw.Draw(canvas_story)
        draw_story.rectangle([0, 0, 1080, 300], fill=COLOR_BLACK)
        draw_story.text((100, 100), "THE FREE LUNCH", font=font_hero, fill=COLOR_WHITE)
        
        # Image in center
        story_img_w = 900
        story_img_h = int(900 / img_ratio)
        resized_story_img = base_img.resize((story_img_w, story_img_h), Image.Resampling.LANCZOS)
        
        # Add white border/frame
        frame_rect = [90 - 10, 500 - 10, 90 + story_img_w + 10, 500 + story_img_h + 10]
        draw_story.rectangle(frame_rect, fill=COLOR_BLACK)
        canvas_story.paste(resized_story_img, (90, 500), resized_story_img)
        
        # Details at bottom
        create_sticker(draw_story, f"LOCATION: {event.get('location', 'USD')}", (100, 1500), font_main)
        create_sticker(draw_story, f"FOOD: {event.get('food_provided', 'FREE')}", (100, 1650), font_main)
        create_sticker(draw_story, "LINK IN BIO", (650, 1800), font_small, bg_color=COLOR_BLACK)
        # Note: link in bio text should be white
        draw_story.text((670, 1815), "LINK IN BIO", font=font_small, fill=COLOR_WHITE)

        # Save Story
        story_filename = f"{STORY_DIR}/story_{post_id}.png"
        canvas_story.convert("RGB").save(story_filename)
        print(f"Generated Story: {story_filename}")

if __name__ == "__main__":
    generate_marketing_assets()
