import os
import json
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Design Tokens (VÉLOCE Style)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_TAN = (193, 154, 107) # #C19A6B

# Paths
DATA_FILE = "../../data/exports/data.json"
MARKETING_DIR = "../../marketing/v2"
BRAND_DIR = "../../frontend/assets"
FONT_PATH = "/System/Library/Fonts/Supplemental/Impact.ttf" # Fallback for Bebas Neue

# Ensure directories exist
os.makedirs(f"{MARKETING_DIR}/hype", exist_ok=True)
os.makedirs(f"{MARKETING_DIR}/intel", exist_ok=True)
os.makedirs(f"{MARKETING_DIR}/explainers", exist_ok=True)

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return ImageFont.load_default()

def draw_sticker(draw, text, position, font, bg_color=COLOR_WHITE, fg_color=COLOR_BLACK, shadow=True):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    padding = 30
    rect = [position[0], position[1], position[0] + tw + padding*2, position[1] + th + padding*2]
    
    if shadow:
        offset = 8
        shadow_rect = [r + offset for r in rect]
        draw.rounded_rectangle(shadow_rect, radius=15, fill=COLOR_BLACK)
        
    draw.rounded_rectangle(rect, radius=15, fill=bg_color, outline=COLOR_BLACK, width=5)
    draw.text((position[0] + padding, position[1] + padding - 10), text, font=font, fill=fg_color)

def generate_hype_story(event):
    """Tier 1: High-impact brand awareness."""
    post_id = event.get('post_id')
    # Pick a random brand image (pizza, boba, cookies)
    brand_images = [f for f in os.listdir(BRAND_DIR) if f.endswith(('.png', '.jpg'))]
    bg_choice = random.choice(brand_images) if brand_images else None
    
    canvas = Image.new("RGB", (1080, 1920), COLOR_TAN)
    if bg_choice:
        bg = Image.open(os.path.join(BRAND_DIR, bg_choice)).convert("RGBA")
        # Resize/Crop to fit
        ratio = 1080 / bg.width
        bg = bg.resize((1080, int(bg.height * ratio)), Image.Resampling.LANCZOS)
        canvas.paste(bg.convert("RGB"), (0, (1920 - bg.height)//2))
    
    draw = ImageDraw.Draw(canvas)
    
    # Massive Typography
    font_xl = get_font(250)
    font_l = get_font(120)
    
    # Black bars top/bottom
    draw.rectangle([0, 0, 1080, 400], fill=COLOR_BLACK)
    draw.rectangle([0, 1520, 1080, 1920], fill=COLOR_BLACK)
    
    draw.text((50, 50), "HAUL", font=font_xl, fill=COLOR_WHITE)
    draw.text((50, 300), "DETECTED", font=font_l, fill=COLOR_TAN)
    
    # Event Badge
    draw_sticker(draw, f"@{event.get('source_handle', 'USD')}", (100, 1600), font_l, bg_color=COLOR_TAN)
    draw.text((100, 1800), "LINK IN BIO FOR INTEL", font=get_font(60), fill=COLOR_WHITE)
    
    canvas.save(f"{MARKETING_DIR}/hype/hype_{post_id}.png")

def generate_intel_post(event):
    """Tier 2: Data-heavy brutalist detail card."""
    post_id = event.get('post_id')
    canvas = Image.new("RGB", (1080, 1080), COLOR_WHITE)
    draw = ImageDraw.Draw(canvas)
    
    # Checkerboard Strip at top
    strip_h = 40
    for i in range(0, 1080, strip_h):
        fill = COLOR_BLACK if (i // strip_h) % 2 == 0 else COLOR_WHITE
        draw.rectangle([i, 0, i+strip_h, strip_h], fill=fill)
    
    # Background Grid Lines
    for i in range(100, 1080, 100):
        draw.line([i, 0, i, 1080], fill=(240, 240, 240), width=1)
        draw.line([0, i, 1080, i], fill=(240, 240, 240), width=1)

    # Main Data
    draw.text((50, 100), "THE INTEL", font=get_font(100), fill=COLOR_BLACK)
    
    # Location/Time Headers
    draw.text((50, 250), "TARGET:", font=get_font(50), fill=COLOR_BLACK)
    draw_sticker(draw, event.get('location', 'USD campus'), (50, 310), get_font(70))
    
    draw.text((50, 480), "WINDOW:", font=get_font(50), fill=COLOR_BLACK)
    draw_sticker(draw, f"{event.get('date', 'TODAY')} | {event.get('time', 'TBD')}", (50, 540), get_font(70), bg_color=COLOR_TAN)

    draw.text((50, 710), "PAYLOAD:", font=get_font(50), fill=COLOR_BLACK)
    draw_sticker(draw, event.get('food_provided', 'FREE FOOD'), (50, 770), get_font(90), bg_color=COLOR_BLACK, fg_color=COLOR_WHITE)

    # Mini Flyer Sticker
    flyer_path = event.get('image_path')
    if flyer_path and os.path.exists(flyer_path):
        flyer = Image.open(flyer_path).convert("RGBA")
        flyer.thumbnail((400, 400))
        # Add border
        f_w, f_h = flyer.size
        draw.rectangle([600-5, 100-5, 600+f_w+5, 100+f_h+5], fill=COLOR_BLACK)
        canvas.paste(flyer, (600, 100), flyer)

    # Branding
    draw.text((50, 1000), "VÉLOCE PREMIER AGGREGATION", font=get_font(30), fill=COLOR_BLACK)
    
    canvas.save(f"{MARKETING_DIR}/intel/intel_{post_id}.png")

def generate_explainers():
    """Tier 3: The brand foundational series."""
    posts = [
        {
            "id": "1_hook",
            "title": "STOP PAYING",
            "subtitle": "FOR LUNCH.",
            "body": "Student clubs have a massive surplus of food every single day. We bridge the gap. No more $15 salads.",
            "bg": COLOR_BLACK,
            "text": COLOR_WHITE
        },
        {
            "id": "2_tech",
            "title": "REAL-TIME",
            "subtitle": "INTELLIGENCE.",
            "body": "Our AI engine scans 100+ Instagram accounts 24/7. We find the food so you never have to scroll. Pure signal.",
            "bg": COLOR_WHITE,
            "text": COLOR_BLACK
        },
        {
            "id": "3_edge",
            "title": "THE INNER",
            "subtitle": "CIRCLE.",
            "body": "Free food is gone in 15 minutes. Members get alerts 1 hour before the public. Don't be late to the drop.",
            "bg": COLOR_TAN,
            "text": COLOR_BLACK
        }
    ]

    for p in posts:
        canvas = Image.new("RGB", (1080, 1080), p['bg'])
        draw = ImageDraw.Draw(canvas)
        
        # Brutalist Border
        draw.rectangle([20, 20, 1060, 1060], outline=p['text'], width=10)
        
        # Typography
        font_xl = get_font(180)
        font_m = get_font(60)
        
        # Title
        draw.text((60, 100), p['title'], font=font_xl, fill=p['text'])
        draw.text((60, 280), p['subtitle'], font=font_xl, fill=p['text'])
        
        # Horizontal Divider
        draw.line([60, 500, 1020, 500], fill=p['text'], width=8)
        
        # Body Text (Simple wrapping)
        words = p['body'].split()
        lines = []
        current_line = []
        for word in words:
            if len(" ".join(current_line + [word])) < 25:
                current_line.append(word)
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
        lines.append(" ".join(current_line))
        
        y_text = 550
        for line in lines:
            draw.text((60, y_text), line, font=font_m, fill=p['text'])
            y_text += 80

        # Branding Sticker
        draw_sticker(draw, "VÉLOCE PREMIER AGGREGATION", (60, 920), get_font(40), bg_color=p['text'], fg_color=p['bg'], shadow=False)
        
        canvas.save(f"{MARKETING_DIR}/explainers/explainer_{p['id']}.png")
        print(f"Generated Explainer: {p['id']}")

def main():
    if not os.path.exists(DATA_FILE):
        print("No data.json found.")
        return

    with open(DATA_FILE, "r") as f:
        events = json.load(f)

    confirmed = [e for e in events if e.get('has_free_food')]
    for event in confirmed:
        print(f"Generating assets for {event['club_name']}...")
        generate_hype_story(event)
        generate_intel_post(event)
    
    # Generate static explainers
    generate_explainers()
    
    print(f"✅ Marketing assets generated in {MARKETING_DIR}")

if __name__ == "__main__":
    main()
