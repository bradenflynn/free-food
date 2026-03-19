import sys
import json
from vision_processor import process_image_for_food

if len(sys.argv) < 2:
    print("Usage: python test_food_vision.py <image_path>")
    sys.exit(1)

result = process_image_for_food(sys.argv[1])
print(json.dumps(result, indent=2))
