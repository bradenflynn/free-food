import os
import json
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Setup OpenAI
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

from datetime import datetime

def process_image_for_food(image_path):
    if not api_key:
        return {"error": "OPENAI_API_KEY missing"}

    today_str = datetime.now().strftime("%B %d, %Y")
    print(f"Analyzing {image_path} with GPT-4o (Today is {today_str})...")
    
    base64_image = encode_image(image_path)
    
    prompt = f"""
    CRITICAL MISSION: You are a "Free Food Hunter" for a university. 
    Look at this image (Instagram post or story) and hunt for ANY signs of free food.
    
    Look specifically for phrases like:
    - "Lunch provided"
    - "Free snacks"
    - "Pizza included"
    - "Catered by..."
    - "Dinner is on us"
    - "Light refreshments"
    - "Food & Drinks"
    
    Extract the discovery into a JSON object:
    - club_name: Name of the organization
    - event_name: What is the event title?
    - date: Date (YYYY-MM-DD or descriptive)
    - time: Time (e.g., 6:00 PM)
    - location: Building/Room number or campus spot
    - food_provided: EXACTLY what food is mentioned.
    - has_free_food: Boolean (True ONLY if food is explicitly promised)
    - has_time_and_location: Boolean (True ONLY if BOTH a specific time AND a specific location are mentioned in the post)
    - is_future_event: Boolean (True if the event date is clearly on or after {today_str}. False if it clearly happened before this date).
    - food_rank: 1-5 scale (1=coffee/cookies, 3=Pizza/Sandwiches, 5=Chipotle/Full Buffet/Catering)
    - confidence_score: 1-10 (How sure are you that there is actually free food for attendees?)

    Rules:
    - If there is NO specific time AND NO specific location, set has_time_and_location to FALSE.
    - If the event date is before {today_str}, set is_future_event to FALSE.
    - If it's a "Food Drive" (where you GIVE food), has_free_food should be FALSE.
    - If it's a "Bake Sale" (where you BUY food), has_free_food should be FALSE.
    - Return ONLY the JSON.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            response_format={ "type": "json_object" }
        )
        
        content = response.choices[0].message.content
        if content is None:
            print(f"Vision Error: Model returned empty content for {image_path}. Refusal: {getattr(response.choices[0].message, 'refusal', 'N/A')}")
            return {"error": "Empty response from vision model"}
            
        data = json.loads(content)
        return data
    except Exception as e:
        print(f"Vision Error: {e}")
        return {"error": str(e)}
