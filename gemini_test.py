import requests
import os
from dotenv import load_dotenv

# API key'i .env dosyasından al
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# API key'i kullanarak yapılandırma
print("API key'i kullanarak yapılandırma...")

# Mevcut modelleri listele
print("\nMevcut modelleri listeleme...")
models_url = "https://generativelanguage.googleapis.com/v1beta/models"
response = requests.get(models_url, params={'key': GOOGLE_API_KEY})

if response.status_code == 200:
    models = response.json().get('models', [])
    print("\nMevcut modeller:")
    for model in models:
        print(f"Model: {model.get('name', 'Unknown')}")
        print(f"Description: {model.get('description', 'No description')}")
        print("-" * 50)
else:
    print(f"\nHata: {response.status_code}")
    print(response.text)

# Gemini Pro modeliyle içerik üret
print("\nGemini Pro modeli ile içerik üretme...")
content_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"

prompt = {
    "contents": [
        {
            "parts": [
                {
                    "text": "Einstein uzayda fizik dersi anlatıyor gibi bir hikaye yaz."
                }
            ]
        }
    ]
}

headers = {
    'Content-Type': 'application/json',
    'X-Goog-Api-Key': GOOGLE_API_KEY
}

print("\nİçerik oluşturma isteği gönderiliyor...")
response = requests.post(content_url, json=prompt, headers=headers)

if response.status_code == 200:
    print("\nAI'den gelen içerik:")
    if response.json().get('candidates'):
        print(response.json()['candidates'][0]['content']['parts'][0]['text'])
    else:
        print("Hata: Yanıt alınamadı")
else:
    print(f"\nHata: {response.status_code}")
    print(response.text)
