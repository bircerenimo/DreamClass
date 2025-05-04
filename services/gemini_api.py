import google.generativeai as genai
import logging
import os
import json
import re
from dotenv import load_dotenv

# Loglama ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

def extract_json_from_response(text):
    """
    Cümleler içinden sadece JSON kısmını çıkarır
    """
    try:
        # Metin içindeki ilk { ile son } arasını bul
        match = re.search(r'{.*}', text, re.DOTALL)
        if match:
            json_text = match.group(0)
            return json.loads(json_text)
        else:
            raise ValueError("JSON formatı bulunamadı")
    except Exception as e:
        raise ValueError(f"JSON çıkarma hatası: {str(e)}")

class GeminiAPI:
    def __init__(self):
        try:
            # API anahtarının varlığını kontrol et
            if not GOOGLE_API_KEY:
                raise ValueError("GOOGLE_API_KEY is not set in .env file")
                
            # API anahtarının formatını kontrol et
            if not GOOGLE_API_KEY.startswith('AIza'):
                raise ValueError("Invalid API key format. It should start with 'AIza'")
                
            genai.configure(api_key=GOOGLE_API_KEY)
            logger.info(f"Configured API with key: {GOOGLE_API_KEY[:5]}...{GOOGLE_API_KEY[-5:]}")
            
            # Modeli oluştur
            try:
                self.model = genai.GenerativeModel("gemini-1.5-pro")
                logger.info("Created Gemini model instance")
                
                # Modelin çalışıp çalışmadığını test et
                test_prompt = "Test prompt"
                test_response = self.model.generate_content(test_prompt)
                logger.info("Test model response successful")
            except Exception as e:
                logger.error(f"Error creating or testing model: {str(e)}")
                raise ValueError(f"Failed to create or test model: {str(e)}")
            
        except Exception as e:
            logger.error(f"Initialization error: {str(e)}")
            raise ValueError(f"Failed to initialize Gemini API: {str(e)}")

    def generate_content(self, data):
        try:
            # Gerekli verilerin varlığını kontrol et
            required_fields = ['level', 'universe', 'topic']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Prompt oluşturma
            prompt = f"""
            Sen bir eğitim asistanısın. Türkçe olarak cevap ver.
            
            Evren: {data['universe']}
            Konu: {data['topic']}
            Sınıf Seviyesi: {data['level']}. Sınıf
            
            Sınıf seviyesine göre zorluk seviyesi:
            - 5-6. Sınıf: Temel kavramlar, basit örnekler ve uygulamalar
            - 7-8. Sınıf: Orta seviye kavramlar, daha detaylı örnekler
            - 9-10. Sınıf: İleri seviye kavramlar, karmaşık örnekler
            - 11-12. Sınıf: Derinlemesine analiz, teorik açıklamalar ve pratik uygulamalar
            
            Lütfen şu formatı kullanarak eğitim içeriği oluştur:
            
            1. Hikaye:
            - {data['universe']} evrenindeki {data['topic']} konusunu {data['level']}. sınıf seviyesine uygun detaylı bir şekilde anlat
            - Evrenin özelliklerini ve konuyu birleştiren örnekler kullan
            - Sınıf seviyesine göre uygun terimler ve kavramlar kullan
            - {data['level']} sınıf seviyesine göre uygun zorlukta detaylar
            
            2. Sorular:
            - 5 tane kısa cevap sorusu oluştur
            - Her sorunun detaylı açıklamasını ve çözüm adımlarını ekleyin
            - Sınıf seviyesine göre uygun zorlukta sorular oluştur:
            - 5-6. Sınıf: Temel bilgileri test eden sorular
            - 7-8. Sınıf: Uygulama ve analiz gerektiren sorular
            - 9-10. Sınıf: Karmaşık durumları çözen sorular
            - 11-12. Sınıf: Derinlemesine analiz ve kritik düşünme gerektiren sorular
            - Evren ve konu arasındaki bağlantıları vurgulayan sorular
            
            3. Görsel Fikir:
            - Konuyu ve evreni görsel olarak temsil eden bir fikir
            - Sınıf seviyesine uygun detay seviyesi
            - Öğrencilerin anlayabilecekleri görsel öğeler
            
            Sadece JSON formatında cevap ver. JSON yapısı:
            {{
                "story": "Konu hakkında detaylı bir hikaye",
                "quiz": [
                    {{
                        "question": "Soru metni",
                        "answer": "Doğru cevap",
                        "explanation": "Sorunun çözümü ve açıklama"
                    }}
                ],
                "visualIdea": "Konuyu görsel olarak temsil etme fikri"
            }}
            
            JSON yapısının dışında herhangi bir açıklama veya metin eklemeyin.
            Sadece JSON nesnesini döndürün.
            """
            
            logger.info(f"Generating content with prompt: {prompt[:50]}...")
            
            # İçerik üret
            try:
                response = self.model.generate_content(prompt)
                logger.info("Successfully generated content")
            except Exception as e:
                logger.error(f"Error generating content: {str(e)}")
                raise ValueError(f"Failed to generate content: {str(e)}")
            
            # Cevabı döndür
            try:
                # Response'u JSON formatında al
                if hasattr(response, 'text'):
                    raw_text = response.text
                    logger.info(f"Raw response: {raw_text}")
                    
                    # JSON formatına dönüştür
                    parsed_json = extract_json_from_response(raw_text)
                    logger.info(f"Successfully parsed JSON content")
                    logger.info(f"Parsed output: {json.dumps(parsed_json, indent=2)}")
                    return parsed_json
                else:
                    raise Exception("AI cevabı geçersiz")
            
            except Exception as e:
                logger.error(f"Error processing response: {str(e)}")
                logger.error(f"Response object: {str(response)}")
                raise ValueError(f"Invalid response format: {str(e)}")

        except Exception as e:
            logger.error(f"Error in generate_content: {str(e)}")
            raise ValueError(f"Failed to generate content: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            raise


if __name__ == '__main__':
    api = GeminiAPI()
    test_data = {
        'universe': 'Science',
        'topic': 'Photosynthesis',
        'level': '5'
    }
    
    try:
        result = api.generate_content(test_data)
        print("Result:", result)
    except Exception as e:
        print("Error:", str(e))
