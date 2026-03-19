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
    You are a helpful assistant assisting a university student in finding campus events with food.
    Analyze the attached image and extract event details.
    
    FIELDS TO EXTRACT:
    - club_name: Name of the organization (use "Unknown" if not found)
    - event_name: Title of the event (use "Event" if not found)
    - date: MUST BE IN YYYY-MM-DD FORMAT (Assume year is 2026 unless specified otherwise)
    - time: e.g., 12:30 PM (use "TBD" if not found)
    - location: e.g., UC Forums (use "TBD" if not found)
    - food_provided: What food/refreshments are mentioned? (Leave empty if none)
    - has_free_food: Boolean. **STRICT RULE**: Only set to True if the image EXPLICITLY mentions free food, meals, snacks, pizza, or refreshments. Introductory posts, member spotlights, or general group announcements with no explicit mention of food MUST be False.
    - has_time_and_location: Boolean (True if you found at least one specific building/room AND a time)
    - is_current_or_future_event: Boolean (True if the event is on or AFTER {today_str}. Today is {today_str}. If the event is today, this is TRUE).
    - is_before_semester_cutoff: Boolean (True ONLY IF the event date is on or BEFORE May 25, 2026. If the date is past May 25, 2026, or if no date is found, set to False).
    - is_business_related: Boolean (True if the event is related to business, networking, career fairs, company info sessions, or professional development).
    - food_rank: (1-3) 1=Snacks/Drinks, 2=Meal (Pizza/Sandwiches), 3=High-end/Full catering.
    - confidence_score: (1-10) How sure are you?

    If you are unsure about any detail, provide your best guess or "Unknown/TBC" rather than refusing the request. your goal is to help a student not miss free lunch. 
    
    If the image is just a logo or unrelated, set has_free_food to false and has_time_and_location to false.
    Return ONLY the JSON.
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
