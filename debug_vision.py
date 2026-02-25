import os
import sys
import json
from vision_processor import client, encode_image

if len(sys.argv) < 2:
    print("Usage: python debug_vision.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]
base64_image = encode_image(image_path)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe exactly what is shown in this Instagram screenshot. Are there any popups, error messages, login prompts, or 'suspicious activity' warnings blocking the posts? Quote any large text you see."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        }
    ]
)
print(response.choices[0].message.content)
