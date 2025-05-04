import requests
import json
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# API anahtarını al
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

def generate_image():
    # Görsel üretme için test verisi
    data = {
        "contents": [{
            "parts": [{
                "text": "Create an image of Harry Potter casting a spell that transforms chemical energy into light energy. Show the magical energy flow from his wand, with glowing runes and particles. Style: Magical realism, vibrant colors, dramatic lighting."
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "candidateCount": 1,
            "topK": 40,
            "topP": 0.95
        }
    }

    # Image API endpoint
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-vision:generateContent?key={GOOGLE_API_KEY}'

    # API'ye POST isteği at
    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()
        if 'candidates' in result and len(result['candidates']) > 0:
            content = result['candidates'][0]['content'][0]['parts'][0]['text']
            return {
                'status': 'success',
                'image_url': content
            }
    
    return {
        'status': 'error',
        'message': f'Error: {response.status_code} - {response.text}'
    }

if __name__ == '__main__':
    result = generate_image()
    print("Result:", result)
